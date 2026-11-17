## Description:

Office Hours guides an agent through a YC-style startup diagnostic that tests demand, status quo, target-user specificity, narrowest wedge, observation, future fit, and viability before producing a report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianen6](https://clawhub.ai/user/qianen6)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and product teams use this skill to pressure-test startup or product ideas before implementation. The agent conducts a viability screen, asks forcing questions one at a time, challenges assumptions, and saves a diagnostic report with demand scoring and a concrete assignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web search and read product-related repository files and recent git history while diagnosing a startup idea.

Mitigation: Install only in repositories where that access is acceptable, and limit accessible files before use when unrelated confidential plans, credentials, or sensitive customer data may be present.

Risk: The skill writes a business diagnostic report under docs/business, which may contain sensitive product strategy or founder feedback.

Mitigation: Review the generated report before sharing or committing it, and keep the report out of public repositories when it includes confidential business information.

## Reference(s):

- [Office Hours ClawHub release](https://clawhub.ai/qianen6/skills/yc-office-hours)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report with conversational prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves the diagnostic report to docs/business/office-hours-report.md when used in a repository.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
