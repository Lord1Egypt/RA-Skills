## Description: <br>
Grove CLI guide - philosophy, commands, and quick start. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Olshansk](https://clawhub.ai/user/Olshansk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and operators use this skill to install and operate the Grove CLI for checking destinations, sending USDC micro-tips, monitoring balances, and automating funding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install remote Grove tooling before use. <br>
Mitigation: Review the remote installer and install only when Grove tooling is intended for the environment. <br>
Risk: Grove workflows can move real USDC funds and use wallet credentials or API keys. <br>
Mitigation: Use a dedicated low-balance wallet or constrained API key and protect ~/.grove configuration files. <br>
Risk: Automated funding can run without confirmation when --yes or cron usage is enabled. <br>
Mitigation: Avoid unattended auto-funding unless strict balance and funding limits are configured. <br>
Risk: Balance alerts can send account information to webhook destinations. <br>
Mitigation: Configure webhooks only for trusted destinations. <br>


## Reference(s): <br>
- [Tip with Grove on ClawHub](https://clawhub.ai/Olshansk/tip-with-grove) <br>
- [Grove](https://grove.city) <br>
- [Grove CLI documentation](https://grove.city/docs/cli) <br>
- [Grove skills documentation](https://grove.city/docs/skills) <br>
- [Grove CLI installer](https://grove.city/install-cli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Grove CLI commands that move funds or read wallet/API-key configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
