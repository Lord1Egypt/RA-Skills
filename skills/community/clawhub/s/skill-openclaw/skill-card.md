## Description: <br>
Give your OpenClaw agent the power to spend. Stablecoin payments, spending policies, and compliance - built-in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fluxaventures](https://clawhub.ai/user/fluxaventures) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect OpenClaw agents to Oris payment infrastructure for stablecoin payments, wallet balance checks, spending review, marketplace orders, fiat on-ramp/off-ramp flows, cross-chain quotes, and KYA attestations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent durable authority to move money through payment, order, approval, and off-ramp tools. <br>
Mitigation: Install only when agent payments are intended, set very low spending limits, keep limited wallet balances, and require host-side human approval for pay, order, off-ramp, and approval workflows. <br>
Risk: Sensitive financial credentials and bank details can be exposed through local configuration or argument logging. <br>
Mitigation: Protect ~/.openclaw/config.json, rotate Oris credentials if exposed, and disable or redact logging for payment and banking arguments. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/fluxaventures/skill-openclaw) <br>
- [Oris OpenClaw documentation](https://useoris.finance/docs/openclaw) <br>
- [Oris documentation](https://useoris.finance/docs) <br>
- [Oris dashboard](https://useoris.finance/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and JSON-compatible MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Oris credentials and an OpenClaw MCP server configuration.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
