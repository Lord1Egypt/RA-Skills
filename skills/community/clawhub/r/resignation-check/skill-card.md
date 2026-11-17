## Description:

Checks Office 365 and Adobe tenant users against Feishu contact records by email, reports likely departed accounts, and requests explicit confirmation before deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and operations engineers use this skill to compare Office 365 and Adobe accounts with Feishu directory records, produce an offboarding review report, and remove confirmed departed users after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete Office 365 and Adobe accounts after identifying likely departed users.

Mitigation: Require a separate explicit deletion approval that shows the exact account list, keep shared-pool and non-employee accounts out of automatic deletion, and verify each deletion result.

Risk: The workflow depends on multiple enterprise secrets and can use a configurable Feishu API base URL.

Mitigation: Use least-privilege app permissions, isolate credentials by provider and workflow stage, and restrict or remove FEISHU_API_BASE unless a trusted endpoint is required.

Risk: The skill relies on mutable external repository code and dependencies.

Mitigation: Install only from a trusted, pinned revision of the office365-tools repository and review dependency changes before use.

Risk: Generated reports and deletion logs may contain sensitive identity and account-status records.

Mitigation: Treat resignation reports and /tmp deletion logs as sensitive records, limit access, and remove or retain them according to the organization's offboarding policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eggyrooch-blip/skills/resignation-check)
- [office365-tools Repository](https://github.com/eggyrooch-blip/office365-tools)
- [Feishu Open Platform](https://open.feishu.cn)
- [Adobe User Management API](https://usermanagement.adobe.io/v2/usermanagement)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Console report and Markdown report with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write timestamped resignation reports and deletion logs under /tmp.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
