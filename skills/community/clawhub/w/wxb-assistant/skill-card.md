## Description:

Queries Wangxiaobao recordings, visits, customer profiles, customer journeys, Panke analyses, todos, tenants, and projects through authenticated Wangxiaobao APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Sales consultants and managers use this skill to retrieve Wangxiaobao customer, visit, recording, and Panke analysis data after QR-code authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens are persisted locally and may be printed during authorization or token checks.

Mitigation: Use the skill only on a trusted machine, avoid shared terminals and logged automation, and clear ~/.wxb-auth-token when finished.

Risk: The skill exposes sensitive write or control actions, including editing recordings, switching tenants or projects, starting or stopping visits, submitting tables, adding comments, and ignoring records.

Mitigation: Require explicit user confirmation before executing any write, tenant/project switch, visit control, submission, comment, delete, or ignore action.

Risk: Queries can return sensitive Wangxiaobao customer, recording, visit, and sales-analysis data.

Mitigation: Use least-privileged Wangxiaobao accounts and limit requests and displayed outputs to the business data needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/156554395/skills/wxb-assistant)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summaries with JSON API responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QR-code authorization and network access to Wangxiaobao services.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
