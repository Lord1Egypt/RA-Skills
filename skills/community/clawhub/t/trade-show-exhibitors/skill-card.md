## Description:

Builds a trade-show exhibitor list and, when requested, identifies people with public evidence of attendance and booth roles, scoring each against the user's target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to find and qualify exhibitors for a trade show, and optionally to review people whose public posts or company news indicate attendance and identify booth staff by role.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete because one local reference could not be resolved.

Mitigation: Check the unresolved reference and confirm the skill fits your needs before installing.

Risk: Apify Actors can charge per result, and third-party Actors can bill the user's account.

Mitigation: Run the estimate first, review both cost estimates and caps, and confirm before starting a run that exceeds the documented threshold.

Risk: Public posts and company news provide evidence of attendance, not proof that a person attended.

Mitigation: Keep attendance scores and source evidence beside each person, and treat attendance as a probability.

## Reference(s):

- [Declared skill homepage](https://github.com/maxouf/sherwood-skills/tree/main/skills/trade-show-exhibitors)
- [Apify MCP connection](https://mcp.apify.com/?tools=sherwood/trade-show-people-finder)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance, JSON, CSV, Markdown, Shell commands]

**Output Format:** [Structured JSON or CSV records with Markdown summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company and people records can include source evidence and fit or attendance scores; no email addresses or phone numbers are collected.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
