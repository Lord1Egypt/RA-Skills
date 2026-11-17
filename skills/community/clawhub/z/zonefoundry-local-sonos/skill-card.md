## Description:

Use this skill when an agent needs to control Sonos through ZoneFoundry `zf` on a same-LAN node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kisssam6886](https://clawhub.ai/user/kisssam6886)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent control local Sonos playback, readiness checks, queue actions, service-linking flows, and recovery through the `zf` CLI on a same-LAN node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local `zf` runtime is granted authority to update itself.

Mitigation: Require confirmation before applying runtime updates and keep skill package updates separate from `zf` runtime updates.

Risk: Runtime hints such as `nextCommand` or `nextAction` can cause the agent to execute follow-up commands automatically.

Mitigation: Only execute reviewed `zf` commands that match the expected Sonos control, readiness, linking, or recovery flows.

Risk: `zf skill show` can replace reviewed skill instructions with runtime-provided content.

Mitigation: Do not let runtime-provided skill text replace the reviewed instructions used for deployment decisions.

Risk: Queue cleanup and recovery commands can remove or alter queued playback items.

Mitigation: Ask before pruning or deleting queue items unless the deployment policy explicitly allows automatic cleanup.

## Reference(s):

- [ZoneFoundry homepage](https://github.com/kisssam6886/zonefoundry)
- [Command Map](references/command-map.md)
- [Onboarding Boundary](references/onboarding-boundary.md)
- [China Service Readiness Notes](references/china-service-linking.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON-formatted `zf` command output when executing local checks.]

## Skill Version(s):

1.5.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
