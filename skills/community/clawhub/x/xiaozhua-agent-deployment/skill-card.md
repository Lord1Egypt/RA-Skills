## Description:

AI Agent deployment and management guidance for installing OpenClaw on WSL2/Linux, configuring GitHub Copilot authentication, starting the gateway, initializing workspace files, handling multi-agent ports, and troubleshooting authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up or restart OpenClaw-based agents on WSL2/Linux, configure GitHub Copilot authentication, select gateway ports and models, and initialize workspace coordination documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run a remote installer and install OpenClaw globally without pinning every dependency.

Mitigation: Download and inspect installers before execution, pin npm package versions where possible, and perform installation in a controlled WSL2/Linux environment.

Risk: The skill involves Copilot authentication tokens and gateway configuration that could expose credentials if copied into logs, screenshots, or repositories.

Mitigation: Do not share Copilot tokens or gateway details, and keep ~/.openclaw/openclaw.json out of screenshots, logs, and source control.

Risk: Port and gateway configuration mistakes can interrupt existing agents or expose unintended local services.

Mitigation: Use a unique gateway port for each agent and review the gateway configuration after startup because the skill notes that configuration can be overwritten.

## Reference(s):

- [NVM install script referenced by the skill](https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh)
- [ClawHub skill page](https://clawhub.ai/mirowangl-ops/skills/xiaozhua-agent-deployment)
- [Publisher profile](https://clawhub.ai/user/mirowangl-ops)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholders for local ports, tokens, model names, and workspace document names.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
