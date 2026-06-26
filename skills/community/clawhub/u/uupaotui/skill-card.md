## Description: <br>
UU跑腿 helps an agent quote, create, manage, cancel, and track same-city delivery and errand-service orders through the UU跑腿 platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to estimate delivery costs, place same-city delivery or errand orders, query order details, cancel orders, and track riders using configured UU跑腿 credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel real-world delivery orders and initiate payment flows. <br>
Mitigation: Require explicit final confirmation before every create, cancel, or payment action, including the price, address, phone number, and order type. <br>
Risk: The skill handles phone numbers, addresses, payment links, and rider tracking details. <br>
Mitigation: Collect only the minimum required data, limit where outputs are shared, and avoid retaining order or tracking details after the task is complete. <br>
Risk: Bundled application credentials and local config files can expose service secrets or user authorization data. <br>
Mitigation: Replace or remove bundled appSecret values, prefer environment variables or a protected secret store, and avoid committing generated config.json files. <br>
Risk: Third-party IP lookup or QR-code services may receive network or payment metadata. <br>
Mitigation: Disable those services or replace them with approved internal alternatives before production use. <br>


## Reference(s): <br>
- [UU跑腿 Open Platform](https://open.uupt.com) <br>
- [UU跑腿 API Documentation](https://open.uupt.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/uupt-mcp/skills/uupaotui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order identifiers, payment links, QR-code file paths, delivery status, and rider tracking details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.6 and package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
