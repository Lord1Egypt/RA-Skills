## Description: <br>
UU跑腿 is a same-city delivery skill for quoting, creating, querying, canceling, and tracking UU跑腿 delivery or on-site help orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage UU跑腿 same-city delivery or on-site help requests, including price quotes, order creation, payment handoff, order lookup, cancellation, and courier tracking. <br>

### Deployment Geography for Use: <br>
Global, subject to UU跑腿 service coverage. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and cancel real-world delivery or help orders, which may create charges or cancellation fees. <br>
Mitigation: Require explicit user confirmation before every order creation or cancellation, including price, addresses, phone number, order type, and cancellation reason. <br>
Risk: The skill handles phone numbers, addresses, SMS codes, payment links, and courier tracking data. <br>
Mitigation: Collect only the minimum necessary data and avoid retaining sensitive values in chat transcripts or plaintext configuration files. <br>
Risk: The skill may contact third-party IP lookup and QR-code services outside UU跑腿. <br>
Mitigation: Disclose these external calls before registration or payment QR generation, or use manual IP and payment-link handling where appropriate. <br>
Risk: The artifact includes default application credentials and can write local configuration. <br>
Mitigation: Review credentials before use and replace or rotate defaults for production deployments. <br>


## Reference(s): <br>
- [UU跑腿开放平台](https://open.uupt.com) <br>
- [ClawHub skill page](https://clawhub.ai/uupt-mcp/skills/uupaotui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-formatted guidance with shell commands and JSON/API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce payment links or QR-code image file paths when payment is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter 1.0.6, _meta.json 1.0.1, package.json 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
