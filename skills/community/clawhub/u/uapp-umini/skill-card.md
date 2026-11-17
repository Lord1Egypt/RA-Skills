## Description:

Helps agents answer Umeng mini program, H5, and mini game analytics questions by using `umeng-cli call` to query 12 read-only Umeng OpenAPI endpoints for overview, users, retention, pages, sharing, and custom events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to answer product analytics questions for Umeng mini program, H5, and mini game properties. It covers read-only queries for app overview metrics, total users, retention, page analysis, sharing analysis, and custom event statistics, while directing Android and iOS app questions to adjacent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to send usage telemetry, including each AppKey, through `umeng-cli trace` without a clear consent or privacy boundary.

Mitigation: Review this behavior before installation, especially when AppKeys are sensitive; install only if AppKey telemetry reporting is acceptable for the organization.

Risk: The skill depends on a globally installed `umeng-cli` and cached Umeng credentials.

Mitigation: Use a pinned, trusted CLI installation and confirm credential-cache handling before enabling the skill in shared or managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-umini)
- [Umeng CLI homepage](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include `umeng-cli` installation, login, and read-only API call guidance plus summarized analytics results; the skill itself does not define write operations.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
