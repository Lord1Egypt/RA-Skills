## Description: <br>
UUPT Delivery helps an agent price, create, inspect, cancel, and track same-city courier and on-site assistance orders through the UUPT service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to request local courier delivery or on-site assistance, including price quotes, order placement, payment handoff, order lookup, cancellation, and rider tracking. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real-world paid delivery or assistance orders. <br>
Mitigation: Require explicit final user confirmation before creating or canceling any order. <br>
Risk: The skill handles delivery account credentials, phone numbers, addresses, payment links, and rider tracking data. <br>
Mitigation: Use environment variables or managed secret storage for credentials, minimize personal data in chat, and share tracking details only for authorized orders. <br>
Risk: Registration, IP lookup, and payment QR generation may contact third-party services. <br>
Mitigation: Tell users before making these calls and verify payment links or QR codes before presenting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uupt-mcp/skills/uupt-delivery) <br>
- [UUPT open platform](https://open.uupt.com) <br>
- [UUPT API documentation](https://open.uupt.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration and payment QR-code files during registration and payment flows.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact frontmatter says 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
