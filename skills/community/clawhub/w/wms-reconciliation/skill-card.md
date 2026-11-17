## Description:

WMS仓库收费对账 helps agents compare third-party warehouse billing Excel files with WMS OpenAPI business records to check whether billed outbound, return, packaging, storage, and disposal activities occurred and were completed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlin1](https://clawhub.ai/user/vinlin1)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, finance, and warehouse-operations teams use this skill to reconcile third-party warehouse fee statements against WMS records and identify missing records, incomplete business events, and amount mismatches. It is especially relevant for monthly or quarterly billing checks involving outbound fees, return handling fees, packaging fees, storage fees, and disposal fees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WMS API credentials and business billing data.

Mitigation: Verify the WMS base URL, prefer HTTPS, avoid exposing real AppSecret values in shared shells or logs, and treat generated reconciliation reports as sensitive business files.

Risk: Reconciliation conclusions may be incomplete because the documented API lacks direct financial-detail and logistics-tracking endpoints.

Mitigation: Review important discrepancies against original WMS records and confirm that use of automated reconciliation is permitted by the relevant WMS or warehouse service agreement.

## Reference(s):

- [WMS OpenAPI adaptation reference](artifact/references/wms_api_reference.md)
- [ClawHub skill page](https://clawhub.ai/vinlin1/skills/wms-reconciliation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, Files]

**Output Format:** [Markdown guidance with bash commands; generated reconciliation artifacts may include HTML, JSON, and marked XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Excel billing file plus user-provided WMS base URL, AppKey, AppSecret, warehouse ID, and billing date range.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
