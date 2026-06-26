## Description: <br>
Manage Smartlead campaigns, leads, and webhooks from the command line via the smartlead CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzakirov](https://clawhub.ai/user/jzakirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent workflows use this skill to inspect and manage Smartlead campaigns, leads, message history, and webhook-triggered reply alerts through the smartlead CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup helper can enable local openclaw-smartlead plugin code that may not have been independently reviewed. <br>
Mitigation: Install only after reviewing and trusting the local plugin source, and keep plugin configuration minimal unless a specific operational need requires more. <br>
Risk: Webhook-triggered agent activity can act with Smartlead account access when reply events arrive. <br>
Mitigation: Set a strong webhook secret, ensure the endpoint is not publicly triggerable without authentication, and require explicit approval for lead, campaign, webhook, delete, or raw API actions. <br>
Risk: The smartlead CLI can modify or delete campaigns, leads, and webhooks when supplied with account credentials. <br>
Mitigation: Use SMARTLEAD_API_KEY only in trusted environments, review destructive commands before execution, and avoid passing --yes outside reviewed automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jzakirov/smartlead) <br>
- [Smartlead Skill Guide](artifact/SKILL.md) <br>
- [Smartlead Setup Helper](artifact/setup.sh) <br>
- [Smartlead API Base URL](https://server.smartlead.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, workflow steps, and operational cautions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the smartlead CLI and SMARTLEAD_API_KEY; setup guidance can configure OpenClaw hooks and webhook routing.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
