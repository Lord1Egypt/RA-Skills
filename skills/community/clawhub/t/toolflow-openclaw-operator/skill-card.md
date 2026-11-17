## Description:

Enables running jobs as durable, stepwise ToolFlow workflows with approvals, recovery, and progress tracking via OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcg-tries-to-code](https://clawhub.ai/user/mcg-tries-to-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run multi-step OpenClaw work as durable ToolFlow workflows with explicit approval boundaries, recovery, and progress visibility. It also installs and verifies the bundled local ToolFlow plugin/runtime payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled plugin can read arbitrary local files through workflow read actions and persist workflow outputs in a local ledger.

Mitigation: Install only in trusted workspaces, review workflow files before submitting them, and configure the ledger/plugin storage location to a workspace you trust.

Risk: Elevated workflow actions can run local commands when elevated mode is enabled.

Mitigation: Keep elevated mode disabled unless needed, require exact approval for elevated steps, and restrict elevated commands with the configured allowlist.

Risk: Command-based progress updates can execute a configured local command.

Mitigation: Use the default stderr progress sink unless command progress reporting is explicitly required and the configured command has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcg-tries-to-code/skills/toolflow-openclaw-operator)
- [Canonical ToolFlow repository](https://github.com/mcg-tries-to-code/ToolFlow)
- [Artifact README](artifact/README.md)
- [ToolFlow bundle README](artifact/toolflow-bundle/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON workflow/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow framing, installation and verification commands, approval-aware operating guidance, and ToolFlow run-state inspection guidance.]

## Skill Version(s):

0.3.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
