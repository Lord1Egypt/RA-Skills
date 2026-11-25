## Description:

Collects public Weibo post text, author and publication details, engagement counts, and batch results for CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts and campaign teams use this skill to collect public Weibo post data for campaign reporting, content audits, activity monitoring, and creator analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags reusable-token exposure and credential migration as unresolved concerns.

Mitigation: Protect the local credential file, use a dedicated account, and clarify these findings before installing.

Risk: The CLI defaults to an HTTP service, and the security review also flags a process-wide TLS verification bypass.

Mitigation: Use a verified HTTPS service endpoint and do not enable the insecure TLS option.

Risk: The security review reports capabilities and settings beyond the stated Weibo collection purpose; its scan was partial.

Mitigation: Review the complete package and clarify out-of-scope behavior before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mystery77777777/skills/wb-collect)

## Skill Output:

**Output Type(s):** [JSON, CSV files]

**Output Format:** [JSON results on stdout; CSV file on export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch collection accepts 1–50 post links; exported CSV includes a UTF-8 BOM for Excel compatibility.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
