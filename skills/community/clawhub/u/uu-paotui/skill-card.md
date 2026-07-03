## Description: <br>
uupaotui helps agents use UU Paotui same-city delivery and on-site help services for quotes, order creation, order lookup, cancellation, and courier tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and delivery operators use this skill through an agent to price, place, manage, cancel, and track real same-city courier or help-service orders. Developers can also use the included Node.js and Python command wrappers to connect agent workflows to the UU Paotui API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel real courier orders using phone numbers, addresses, payment links, and rider tracking data. <br>
Mitigation: Require explicit final user confirmation before order creation or cancellation, and disclose what personal and payment data will be sent to UU Paotui. <br>
Risk: WeChat QR generation can share a payment URL with an external QR-code service. <br>
Mitigation: Avoid QR generation unless the user accepts that sharing, or send the payment URL directly through a trusted channel. <br>
Risk: Registration can automatically query public-IP services. <br>
Mitigation: Prefer manual IP entry when privacy-sensitive users do not want automatic public-IP lookup. <br>


## Reference(s): <br>
- [UU Paotui Open Platform](https://open.uupt.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/uupt-mcp/skills/uu-paotui) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node or python3, UU Paotui credentials, and user-supplied order details such as addresses and phone numbers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.6 and package.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
