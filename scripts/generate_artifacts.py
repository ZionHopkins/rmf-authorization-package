#!/usr/bin/env python3
"""
generate_artifacts.py
=====================================================================
Generates RMF authorization artifacts from a single source of truth.

Input:   controls/control-baseline.yaml
Outputs: generated/poam.md                 (Plan of Action & Milestones)
         generated/compliance-report.md     (control status summary)
         generated/dashboard.html           (visual compliance snapshot)

Design principle — "artifact as code":
    The control baseline is authoritative. Artifacts are derived, never
    hand-maintained, so they cannot drift out of sync with reality.

Usage:
    python scripts/generate_artifacts.py
=====================================================================
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required. Install it with:  pip install pyyaml")

# --- Paths -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "controls" / "control-baseline.yaml"
OUT_DIR = ROOT / "generated"

# Statuses that represent an open weakness and therefore belong in the POA&M.
OPEN_STATUSES = {"Partially Implemented", "Planned", "Not Implemented"}

# Stable ordering for reports.
STATUS_ORDER = [
    "Implemented",
    "Partially Implemented",
    "Planned",
    "Not Implemented",
]
RISK_ORDER = {"High": 0, "Moderate": 1, "Low": 2, None: 3}


def load_baseline(path: Path) -> dict:
    """Load and lightly validate the control baseline."""
    if not path.exists():
        sys.exit(f"Baseline not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if "controls" not in data or "system" not in data:
        sys.exit("Baseline must contain 'system' and 'controls' keys.")
    return data


def squash(text: str | None) -> str:
    """Collapse YAML folded-block whitespace into a single clean line."""
    if not text:
        return ""
    return " ".join(text.split())


def compliance_stats(controls: list[dict]) -> dict:
    """Compute headline compliance metrics from the control list."""
    counts = Counter(c["status"] for c in controls)
    total = len(controls)
    implemented = counts.get("Implemented", 0)
    pct = round((implemented / total) * 100, 1) if total else 0.0
    return {"counts": counts, "total": total, "implemented": implemented, "pct": pct}


def write_compliance_report(data: dict, stats: dict) -> str:
    sysinfo = data["system"]
    controls = data["controls"]
    today = date.today().isoformat()

    lines: list[str] = []
    lines.append(f"# Compliance Report — {sysinfo['name']} ({sysinfo['acronym']})")
    lines.append("")
    lines.append(f"*Auto-generated {today} from `controls/control-baseline.yaml`. "
                 "Do not edit by hand.*")
    lines.append("")
    lines.append(f"**Framework:** NIST SP 800-53 Rev 5  |  "
                 f"**Baseline:** {sysinfo['categorization']['overall']}  |  "
                 f"**RMF Step:** {sysinfo['rmf_step']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Controls assessed:** {stats['total']}")
    lines.append(f"- **Fully implemented:** {stats['implemented']} "
                 f"({stats['pct']}%)")
    lines.append(f"- **Open items (POA&M):** "
                 f"{stats['total'] - stats['implemented']}")
    lines.append("")
    lines.append("### Status breakdown")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---|")
    for status in STATUS_ORDER:
        lines.append(f"| {status} | {stats['counts'].get(status, 0)} |")
    lines.append("")

    # Per-family rollup.
    by_family: dict[str, Counter] = defaultdict(Counter)
    for c in controls:
        by_family[c["family"]][c["status"]] += 1
    lines.append("### By control family")
    lines.append("")
    lines.append("| Family | Implemented | Open | Total |")
    lines.append("|---|---|---|---|")
    for family in sorted(by_family):
        fam_total = sum(by_family[family].values())
        fam_impl = by_family[family].get("Implemented", 0)
        lines.append(f"| {family} | {fam_impl} | {fam_total - fam_impl} | {fam_total} |")
    lines.append("")

    # Full control register.
    lines.append("## Control register")
    lines.append("")
    lines.append("| Control | Title | Status | Responsible | Last assessed |")
    lines.append("|---|---|---|---|---|")
    for c in sorted(controls, key=lambda x: x["id"]):
        lines.append(
            f"| {c['id']} | {c['title']} | {c['status']} | "
            f"{c.get('responsible_role', '—')} | {c.get('last_assessed', '—')} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_poam(data: dict) -> str:
    sysinfo = data["system"]
    today = date.today().isoformat()
    open_controls = [c for c in data["controls"] if c["status"] in OPEN_STATUSES]
    open_controls.sort(key=lambda c: (RISK_ORDER.get(c.get("risk"), 3), c["id"]))

    lines: list[str] = []
    lines.append(f"# Plan of Action & Milestones (POA&M) — {sysinfo['acronym']}")
    lines.append("")
    lines.append(f"*Auto-generated {today} from `controls/control-baseline.yaml`. "
                 "Do not edit by hand.*")
    lines.append("")
    lines.append(f"**Open items:** {len(open_controls)}")
    lines.append("")
    if not open_controls:
        lines.append("_No open items. All controls are fully implemented._")
        return "\n".join(lines)

    lines.append("| # | Control | Status | Risk | Weakness | Remediation | Milestone | Owner |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(open_controls, start=1):
        lines.append(
            f"| {i} | {c['id']} {c['title']} | {c['status']} | "
            f"{c.get('risk', '—')} | {squash(c.get('weakness'))} | "
            f"{squash(c.get('remediation'))} | "
            f"{c.get('scheduled_completion', 'TBD')} | "
            f"{c.get('responsible_role', '—')} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_dashboard(data: dict, stats: dict) -> str:
    sysinfo = data["system"]
    counts = stats["counts"]
    today = date.today().isoformat()

    palette = {
        "Implemented": "#1f8a4c",
        "Partially Implemented": "#c9911f",
        "Planned": "#2563b0",
        "Not Implemented": "#b3341f",
    }
    bars = []
    for status in STATUS_ORDER:
        n = counts.get(status, 0)
        width = (n / stats["total"] * 100) if stats["total"] else 0
        bars.append(
            f'<div class="row"><span class="lbl">{status}</span>'
            f'<div class="track"><div class="fill" style="width:{width:.1f}%;'
            f'background:{palette[status]}"></div></div>'
            f'<span class="num">{n}</span></div>'
        )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compliance Dashboard — {sysinfo['acronym']}</title>
<style>
  body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
       margin:0;padding:2rem;background:#0f1419;color:#e6e6e6;}}
  .card{{max-width:760px;margin:0 auto;background:#171c24;border-radius:14px;
        padding:2rem;box-shadow:0 8px 30px rgba(0,0,0,.4);}}
  h1{{margin:0 0 .25rem;font-size:1.4rem;}}
  .meta{{color:#8a94a6;font-size:.85rem;margin-bottom:1.5rem;}}
  .score{{font-size:3rem;font-weight:700;color:#1f8a4c;}}
  .score small{{font-size:1rem;color:#8a94a6;font-weight:400;}}
  .row{{display:flex;align-items:center;gap:.75rem;margin:.6rem 0;}}
  .lbl{{width:190px;font-size:.85rem;}}
  .track{{flex:1;background:#0f1419;border-radius:6px;height:18px;overflow:hidden;}}
  .fill{{height:100%;border-radius:6px;}}
  .num{{width:28px;text-align:right;font-variant-numeric:tabular-nums;}}
  .note{{margin-top:1.5rem;font-size:.75rem;color:#5f6b7d;}}
</style></head>
<body><div class="card">
  <h1>{sysinfo['name']} — Compliance Snapshot</h1>
  <div class="meta">NIST SP 800-53 Rev 5 · {sysinfo['categorization']['overall']} baseline · generated {today}</div>
  <div class="score">{stats['pct']}%<small> fully implemented ({stats['implemented']}/{stats['total']} controls)</small></div>
  <div style="margin-top:1.5rem">{''.join(bars)}</div>
  <div class="note">Synthetic portfolio artifact. Fictional system. Generated from control-baseline.yaml.</div>
</div></body></html>"""


def main() -> None:
    data = load_baseline(BASELINE)
    stats = compliance_stats(data["controls"])
    OUT_DIR.mkdir(exist_ok=True)

    (OUT_DIR / "compliance-report.md").write_text(
        write_compliance_report(data, stats), encoding="utf-8")
    (OUT_DIR / "poam.md").write_text(write_poam(data), encoding="utf-8")
    (OUT_DIR / "dashboard.html").write_text(
        write_dashboard(data, stats), encoding="utf-8")

    print("Generated artifacts:")
    print(f"  - generated/compliance-report.md")
    print(f"  - generated/poam.md")
    print(f"  - generated/dashboard.html")
    print(f"\n{stats['implemented']}/{stats['total']} controls implemented "
          f"({stats['pct']}%) · "
          f"{stats['total'] - stats['implemented']} open POA&M items")


if __name__ == "__main__":
    main()
