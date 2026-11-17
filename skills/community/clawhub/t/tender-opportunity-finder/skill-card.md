## Description:

Finds and ranks early tender opportunities across proposed projects, procurement intentions, and expiring contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business-development teams use it to discover and prioritize prospective procurement opportunities by industry, product, and region before tenders are issued.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and account requests are sent to the vendor service, and scans consume paid credits.

Mitigation: Review the vendor's data and pricing terms, avoid sensitive search terms, and confirm expected credit use before scanning.

Risk: Automatic registration transmits a hashed MAC-derived device identifier and creates an account.

Mitigation: Preconfigure ZLBX_API_KEY to skip registration, or obtain informed consent before collecting device features.

Risk: An automatically obtained API credential may be stored in the user's home directory.

Mitigation: Use a separately managed credential when possible and review local credential storage and access permissions.

Risk: Requests include package identity, and account checks may trigger update-notice acknowledgment behavior that is not prominent to users.

Mitigation: Review this request and acknowledgment behavior before enabling the skill; acknowledge a notice only after showing it to the user.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/tender-opportunity-finder)
- [Vendor skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Workflow](references/workflow.md)
- [API quick reference](references/api-quick.md)
- [Automatic registration](references/auto-register.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Ranked Markdown opportunity list; shareable HTML report in full-scan mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, priority rationale, and suggested next actions.]

## Skill Version(s):

1.0.8 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
