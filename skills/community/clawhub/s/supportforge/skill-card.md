## Description: <br>
AI customer support via SupportForge API for ticket creation, auto-replies, routing, and knowledge base search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support teams, developers, and agents use this skill to create support tickets, request manual or AI replies, search a support knowledge base, and check SupportForge service health through the SupportForge API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Support data sent through this skill is shared with a third-party SupportForge service. <br>
Mitigation: Use only with customer and account data approved for third-party processing. <br>
Risk: Generated or supplied SupportForge API keys may appear in command output or logs. <br>
Mitigation: Prefer a dedicated SUPPORTFORGE_API_KEY, avoid printing keys in shared logs, and keep logs private. <br>
Risk: Email-based auto-signup can create API access from SUPPORTFORGE_EMAIL without a pre-provisioned key. <br>
Mitigation: Use a controlled email account for signup or provide an explicitly managed API key. <br>


## Reference(s): <br>
- [SupportForge ClawHub release](https://clawhub.ai/Jbennett111/supportforge) <br>
- [SupportForge API health endpoint](https://anton.vosscg.com/v1/health) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the SupportForge API and return API responses for ticket, knowledge base, or health-check requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
