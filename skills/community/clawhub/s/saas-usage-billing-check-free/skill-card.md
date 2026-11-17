## Description:

Checks SaaS subscription usage and overage billing tables by recomputing overage usage, overage fees, bill tie-outs, plan fit, duplicate subscription rows, and missing key fields, with findings tied to source line numbers and subscription IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

SaaS billing, finance, business operations, and customer-side finance teams use this skill during monthly billing, reconciliation, and renewal discussions to check tabular subscription usage and overage billing details. It helps identify arithmetic mismatches, duplicate subscription rows, missing required fields, and plan-quota fit issues within the free-version scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node.js script over billing spreadsheets or pasted billing-table text.

Mitigation: Install and run it only in environments where local processing of those billing materials is approved.

Risk: The free version checks only the listed free-version items and does not validate contract terms, true usage-metering policy, invoices, payments, or withheld checks.

Mitigation: Use its findings as table-level reconciliation support and review contracts, source usage systems, invoices, payments, and out-of-scope checks separately.

Risk: The tool is mainly Chinese-language, which may affect review by teams that do not read Chinese.

Mitigation: Have a qualified reviewer confirm input headers, findings, and limitations before relying on the output.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chenqg618/skills/saas-usage-billing-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance and optional JSON results from local Node.js execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and subscription IDs; insufficient input returns missing-field guidance instead of conclusions.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
