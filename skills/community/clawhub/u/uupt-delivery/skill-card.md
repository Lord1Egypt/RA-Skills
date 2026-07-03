## Description: <br>
UU Paotui delivery service skill helps an agent quote, create, manage, cancel, and track same-city delivery and on-site help orders through UU Paotui APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to arrange same-city courier delivery or on-site help, including price quotes, order creation, payment handoff, order lookup, cancellation, and courier tracking. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-world delivery or help orders and may not enforce a final confirmation before create-order actions. <br>
Mitigation: Require explicit user confirmation after reviewing address, phone number, service details, price, and payment implications before running any create-order command. <br>
Risk: The skill handles delivery addresses, phone numbers, courier tracking data, payment links, and account authorization data. <br>
Mitigation: Minimize data shared with the agent, avoid broad automatic triggers, and store credentials in environment variables or a secret store instead of plaintext config files. <br>
Risk: Payment QR generation and automatic public-IP lookup can contact third-party services outside the delivery API. <br>
Mitigation: Use QR generation and automatic IP lookup only when necessary, disclose the external contact to users, and prefer a manually supplied IP when appropriate. <br>


## Reference(s): <br>
- [UU Paotui Open Platform](https://open.uupt.com) <br>
- [ClawHub skill page](https://clawhub.ai/uupt-mcp/skills/uupt-delivery) <br>
- [Publisher profile](https://clawhub.ai/user/uupt-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON API responses, payment links, and optional QR image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local config.json during registration and payment_qrcode.png when QR-code payment is requested.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
