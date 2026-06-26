## Description: <br>
uupaotui helps agents quote, create, inspect, cancel, and track UU Paotui same-city delivery and on-site helper-service orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage UU Paotui same-city delivery and helper-service workflows, including registration, price quotes, order creation, payment handling, order lookup, cancellation, and driver tracking. <br>

### Deployment Geography for Use: <br>
China, where UU Paotui same-city delivery coverage is available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel paid real-world delivery orders using personal addresses, phone numbers, notes, and order data. <br>
Mitigation: Require the agent to show the full order, price, addresses, recipient phone, notes, and action type for explicit user approval before creating or cancelling an order. <br>
Risk: Payment links and IP or credential data may be shared with UU Paotui or with a third-party QR-code service when WeChat QR generation is used. <br>
Mitigation: Use the skill only when the user accepts this data sharing; avoid WeChat QR generation unless the user accepts third-party QR processing, and supply credentials manually only when necessary. <br>


## Reference(s): <br>
- [UU Paotui Open Platform](https://open.uupt.com) <br>
- [UU Paotui API Documentation](https://open.uupt.com/docs) <br>
- [ClawHub skill page](https://clawhub.ai/uupt-mcp/skills/uu-paotui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and status text from delivery scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration state and payment QR-code image files during execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.6 and package.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
