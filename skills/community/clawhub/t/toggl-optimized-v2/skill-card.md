## Description:

Optimize Toggl Track usage with token-efficient API calls and fast reporting via a shell script for JSON and PDF summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex1389](https://clawhub.ai/user/alex1389)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators who track client work in Toggl use this skill to configure API-token based reporting and generate compact JSON or PDF summaries over client and date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a Toggl API token supplied through the environment, which can expose account data if the token is over-scoped or mishandled.

Mitigation: Use the minimum Toggl account access needed, keep the token out of shared logs and files, and unset or rotate it when reporting is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alex1389/skills/toggl-optimized-v2)
- [Toggl Profile Settings](https://track.toggl.com/profile)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and script usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled shell script accepts client name, start date, end date, and output format arguments for Toggl reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
