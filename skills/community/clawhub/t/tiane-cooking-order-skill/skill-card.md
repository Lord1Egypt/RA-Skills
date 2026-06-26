## Description: <br>
This skill helps an agent book Tian'e Daojia home-cooking hourly services by collecting address, time, and service details, checking availability, showing an order preview, and placing the order after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianejypt](https://clawhub.ai/user/tianejypt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to arrange Tian'e Daojia home-cooking hourly worker appointments in supported cities, including address selection, schedule checks, service specification selection, order preview, and confirmed order creation. <br>

### Deployment Geography for Use: <br>
China, limited to supported Tian'e Daojia service cities listed by the skill. <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runtime is obfuscated and the authoritative security verdict is suspicious. <br>
Mitigation: Review the publisher, bundled runtime, and service identifiers before normal use or installation in a trusted agent environment. <br>
Risk: The skill can use account authorization, read saved addresses, send location and order details, store tokens locally, and create a real paid order after confirmation. <br>
Mitigation: Run it only in the intended Tian'e/Daojia ordering environment, verify the order preview carefully, and require explicit user confirmation before order creation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tianejypt/tiane-cooking-order-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/tianejypt) <br>
- [Command Reference](references/commands.md) <br>
- [Parameter Reference](references/params.md) <br>
- [Error Handling Reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown user responses with order preview details and shell command invocations for the agent runtime.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use network-backed service commands; the final paid order is created only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, VERSION.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
