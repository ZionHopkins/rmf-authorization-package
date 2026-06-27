# RMF Authorization Package (as Code)

A complete, version-controlled **NIST SP 800-53 Rev 5** authorization package
for a fictional Moderate-impact system — where the **POA&M, compliance report,
and dashboard are generated from a single structured source of truth** instead
of being maintained by hand.

> ⚠️ **Synthetic / portfolio artifact.** *Sentinel Access Portal* is a
> fictional system. This repository contains **no** real-world configuration,
> system boundary, environment detail, or controlled information. It exists to
> demonstrate RMF / A&A artifact management.

---

## Why this exists

GRC artifacts — System Security Plans, POA&Ms, assessment reports — are
normally kept as separate documents and updated by hand. They drift. A control
gets remediated, the POA&M gets updated, the compliance report doesn't, and the
SSP says something different again.

This repo demonstrates a different approach I think in: **artifact as code.**
One authoritative file describes every control's status. Every downstream
artifact is *generated* from it, so they are consistent by construction.

```
controls/control-baseline.yaml   ──►   generated/poam.md
   (single source of truth)       │     generated/compliance-report.md
                                   └──►  generated/dashboard.html
```

Change a control's status in one place, re-run one script, and every artifact
updates together. That is the same discipline RMF asks for in continuous
monitoring — applied with automation.

## What this demonstrates

| RMF / GRC competency | Where to see it |
|---|---|
| Security categorization (FIPS 199 / 800-60) | `docs/system-security-plan.md` |
| SSP development & maintenance | `docs/system-security-plan.md` |
| NIST 800-53 Rev 5 control implementation | `controls/control-baseline.yaml` |
| POA&M management & remediation tracking | `generated/poam.md` |
| Continuous monitoring posture | CA-7 narrative + regeneration workflow |
| Audit-readiness / evidence packaging | full register in `generated/compliance-report.md` |
| Automation for compliance | `scripts/generate_artifacts.py` |

## Repository structure

```
rmf-authorization-package/
├── README.md                      ← you are here
├── controls/
│   └── control-baseline.yaml      ← single source of truth (20 controls)
├── docs/
│   └── system-security-plan.md    ← abridged SSP
├── scripts/
│   └── generate_artifacts.py      ← generator (Python, PyYAML only)
├── generated/                     ← committed outputs (no install needed to read)
│   ├── compliance-report.md
│   ├── poam.md
│   └── dashboard.html
└── requirements.txt
```

## Run it

```bash
pip install -r requirements.txt
python scripts/generate_artifacts.py
```

Output:

```
12/20 controls implemented (60.0%) · 8 open POA&M items
```

## Snapshot

- **Framework:** NIST SP 800-53 Rev 5
- **Baseline:** Moderate (FIPS 199: M / M / M)
- **Controls:** 20 across 8 families (AC, AU, CA, CM, IA, IR, RA, SC, SI)
- **RMF step:** Authorize / continuous monitoring

## Roadmap

- [ ] Migrate the baseline to **OSCAL** (NIST's machine-readable control format) — the direction the federal space is moving
- [ ] Add a GitHub Action to regenerate artifacts on every commit (continuous-monitoring automation)
- [ ] Expand to a full Moderate baseline control set
- [ ] Add a STIG-checklist ingestion path (`.ckl` → control evidence)

---

*Author: Zion E. Hopkins — cybersecurity compliance / GRC.*
