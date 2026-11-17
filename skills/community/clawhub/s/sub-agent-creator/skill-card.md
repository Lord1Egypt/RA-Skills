## Description:

Creates OpenClaw agents by collecting setup details, scaffolding workspace and runtime files, updating openclaw.json bindings, copying runtime configuration, and restarting the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidian6864677](https://clawhub.ai/user/lidian6864677)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to create and configure new OpenClaw agents with workspace files, runtime directories, optional chat bindings, and gateway restart steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can write or overwrite sensitive OpenClaw files without adequate validation or confirmation.

Mitigation: Review before installing or running, confirm the exact agent ID and destination paths, and avoid running the helper until it validates agent IDs, refuses existing destinations by default, and asks for confirmation before writes.

Risk: The workflow can restart the OpenClaw gateway and modify agent bindings.

Mitigation: Use only with explicit administrative intent, inspect openclaw.json changes before applying them, and ensure rollback is available for partial failures.

## Reference(s):

- [SOUL.md Templates](artifact/references/soul_templates.md)
- [ClawHub skill page](https://clawhub.ai/lidian6864677/skills/sub-agent-creator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file scaffolding steps and local OpenClaw configuration updates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
