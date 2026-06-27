# Plan of Action & Milestones (POA&M) — SAP

*Auto-generated 2026-06-27 from `controls/control-baseline.yaml`. Do not edit by hand.*

**Open items:** 8

| # | Control | Status | Risk | Weakness | Remediation | Milestone | Owner |
|---|---|---|---|---|---|---|---|
| 1 | AU-6 Audit Record Review, Analysis, and Reporting | Partially Implemented | Moderate | Log review is performed manually on an ad hoc basis. No automated correlation or scheduled review cadence is documented. | Forward audit records to the enterprise SIEM, define correlation rules for privileged-account anomalies, and establish a weekly review SOP. | 2026-09-30 | ISSO |
| 2 | CA-7 Continuous Monitoring | Planned | Moderate | A continuous monitoring strategy exists in draft but metrics, reporting frequency, and responsible parties are not yet finalized or approved. | Finalize the ConMon strategy, define security metrics and reporting frequency, and obtain ISSM/AO approval. | 2026-10-31 | ISSM |
| 3 | CM-7 Least Functionality | Not Implemented | Moderate | No formal review of installed services/ports/protocols has been performed; unnecessary functionality may be enabled. | Inventory services/ports/protocols, disable those not required for operations, and document the approved functionality list. | 2026-08-15 | System Administrator |
| 4 | RA-5 Vulnerability Monitoring and Scanning | Partially Implemented | Moderate | Authenticated scans run monthly, but remediation timelines by severity are not consistently enforced and trending is not reported. | Enforce remediation SLAs by CVSS severity, automate scan scheduling, and report vulnerability trend metrics to the ISSM. | 2026-09-15 | ISSO |
| 5 | SC-28 Protection of Information at Rest | Planned | Moderate | Database-tier encryption at rest is approved but not yet enabled in the target environment. | Enable transparent data encryption on the database tier and validate via configuration evidence. | 2026-10-15 | System Administrator |
| 6 | SC-7 Boundary Protection | Partially Implemented | Moderate | Boundary firewalls are deployed, but the documented inventory of managed interfaces and deny-by-default ruleset review is outdated. | Update the managed-interface inventory, validate deny-by-default posture, and schedule semiannual ruleset reviews. | 2026-09-30 | System Administrator |
| 7 | SI-4 System Monitoring | Partially Implemented | Moderate | Host and network monitoring are deployed, but alerting thresholds and response procedures for indicators of compromise are not fully defined. | Define alerting thresholds, document the monitoring response SOP, and integrate alerts with the incident handling workflow. | 2026-09-30 | ISSO |
| 8 | CM-6 Configuration Settings | Partially Implemented | Low | DISA STIG settings are applied to servers but a documented record of approved deviations (exceptions) is incomplete. | Complete the STIG checklist review, document and obtain approval for all deviations, and store results with the authorization package. | 2026-08-31 | System Administrator |
