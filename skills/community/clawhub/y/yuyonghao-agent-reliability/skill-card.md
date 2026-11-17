## Description:

Provides error monitoring, automatic fallback, confidence evaluation, and multi-agent voting to help maintain accuracy in multi-step workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add reliability monitoring, fallback execution, confidence scoring, voting consensus, and reliability reports to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted callers or high-impact decisions could supply unreliable votes, confidence values, weights, IDs, or metadata.

Mitigation: Add authentication and validate vote decisions, confidence values, weights, identifiers, and metadata sizes before using results for important actions.

Risk: Dissent reasons and monitoring metadata may contain sensitive information.

Mitigation: Disable or limit dissent recording when sensitive reasons may be present, and configure cleanup or hard retention limits for stored records.

Risk: The library improves workflow resilience but is not a hardened security control.

Mitigation: Use it as a developer reliability layer and pair it with application-level security, authorization, and review controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-reliability)

## Skill Output:

**Output Type(s):** [Code, Configuration, Markdown, JSON, Guidance]

**Output Format:** [JavaScript library APIs with Markdown or JSON reliability reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-memory monitoring, fallback, confidence, voting, and reporting utilities for Node.js agent workflows]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
