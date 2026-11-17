## Description:

Connect coding agents and other agent runtimes to withHuman with the withhuman CLI so their tool calls wait for human approval. Covers installing the CLI, guided onboarding, connecting a runtime to an existing agent, checking the connection, refreshing the tool catalogue, upgrading, and removing the adapter. Use for Claude Code, Codex, OpenClaw, Pi, Hermes and DeepSeek on macOS or Linux, hosted or self-hosted. Trigger keywords - withhuman, withHuman CLI, install withhuman, connect agent to withhuman, withhuman onboard, withhuman agent install, agent eject, refresh-tools, approval hook, calls not gated, human approval for tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[withhuman](https://clawhub.ai/user/withhuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and organization administrators use this skill to install and connect a supported agent runtime to a withHuman organization, then check, update, refresh, or remove its approval adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an installer from an untrusted source can put the local machine at risk.

Mitigation: Verify the download source before running the installer.

Risk: Tool-call details are sent to the withHuman approval pipeline, and organization rules may approve some calls automatically.

Mitigation: Confirm the server, organization, runtime, and gateway permissions, and review which rules approve automatically.

Risk: Removing the local adapter does not revoke its withHuman instance.

Mitigation: When disconnecting permanently, remove the adapter and revoke the instance in the app.

## Reference(s):

- [withHuman Quickstart](https://withhuman.ai/docs/getting-started/quickstart.md)
- [withHuman Agents Guide](https://withhuman.ai/docs/web-app/agents.md)
- [withhuman-cli on ClawHub](https://clawhub.ai/withhuman/skills/withhuman-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
