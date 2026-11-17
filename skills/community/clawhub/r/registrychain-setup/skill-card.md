## Description:

Installs the RegistryChain plugin for on-chain entity registration when setup is needed or the register_entity tool is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kutaibah](https://clawhub.ai/user/kutaibah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and enable the RegistryChain OpenClaw plugin so entity registration tooling becomes available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup persistently downloads and enables third-party plugin code.

Mitigation: Review the plugin source and package metadata before installation, prefer a full reviewed commit hash, and use lockfile-based dependency installation where available.

Risk: The setup changes OpenClaw's global tool profile to full, which can broaden available tool access beyond this plugin.

Mitigation: Back up the OpenClaw configuration first and use a narrower tool profile if OpenClaw supports one.

Risk: The setup force-restarts the OpenClaw gateway and provides limited rollback guidance.

Mitigation: Run installation during an acceptable maintenance window and record rollback steps for disabling the plugin and restoring the prior configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kutaibah/skills/registrychain-setup)
- [Publisher profile](https://clawhub.ai/user/kutaibah)
- [RegistryChain plugin repository referenced by setup commands](https://github.com/RegistryChain/registrychain-agents.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sequential setup guidance that stops and reports errors when a setup step fails.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
