# System Security Plan (SSP) — Sentinel Access Portal (SAP)

> **Synthetic portfolio artifact.** Sentinel Access Portal is a fictional
> system created to demonstrate RMF authorization-artifact management. No
> real environment, configuration, or system boundary is represented.

| Field | Value |
|---|---|
| System name | Sentinel Access Portal (SAP) |
| Framework | NIST SP 800-53 Rev 5 |
| Baseline | Moderate |
| RMF step | Step 5 — Authorize (pre-ATO continuous monitoring) |
| Document type | System Security Plan (abridged) |

## 1. System description

The Sentinel Access Portal is an internal web application that brokers access
requests and approvals for enterprise resources. It illustrates how an
information system is described, categorized, and bounded for authorization
under the Risk Management Framework.

## 2. Security categorization (FIPS 199 / NIST SP 800-60)

| Objective | Impact |
|---|---|
| Confidentiality | Moderate |
| Integrity | Moderate |
| Availability | Moderate |
| **Overall** | **Moderate** |

The high-water mark across security objectives sets the overall categorization
at **Moderate**, which drives selection of the Moderate control baseline.

## 3. Authorization boundary

The boundary comprises the application tier, its supporting database, and the
identity-provider integration. The boundary is intentionally abstract for a
public artifact; in a real package it would include a data-flow diagram,
hardware/software inventory, and interconnection table.

## 4. Roles and responsibilities

| Role | Responsibility |
|---|---|
| Authorizing Official (AO) | Accepts residual risk; issues the ATO |
| ISSM | Oversees the security program and POA&M closure |
| ISSO | Day-to-day control operation, monitoring, assessment evidence |
| System Administrator | Implements technical controls and baselines |
| IAM Administrator | Manages identities, access, and authenticators |

## 5. Control implementation

Control implementation status is maintained as structured data in
[`controls/control-baseline.yaml`](../controls/control-baseline.yaml) and
rendered into:

- [`generated/compliance-report.md`](../generated/compliance-report.md) — full control register and status rollup
- [`generated/poam.md`](../generated/poam.md) — open weaknesses and milestones
- [`generated/dashboard.html`](../generated/dashboard.html) — visual snapshot

This keeps the SSP, the POA&M, and the compliance report consistent by
construction — they share one source of truth rather than diverging over time.

## 6. Continuous monitoring

Per CA-7, the system is in ongoing authorization. Control status is reassessed
on a defined cadence and the POA&M is regenerated from the baseline so that
remediation progress is always reflected in the current artifacts.
