## Description: <br>
Guides agents through Trading 212 API authentication, environment selection, account and portfolio queries, instrument lookup, order placement, transaction history, and CSV report export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsvetelin-kulinski](https://clawhub.ai/user/tsvetelin-kulinski) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and developers use this skill to connect agents to Trading 212 demo or live API accounts for account review, portfolio monitoring, instrument lookup, order management, transaction history, and CSV report workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live trading actions and financial-data access without enough action-level safeguards. <br>
Mitigation: Review carefully before installing, use DEMO mode first, and require explicit confirmation before every live order or cancellation. <br>
Risk: Credential exposure could allow unauthorized access to Trading 212 accounts. <br>
Mitigation: Do not paste API secrets into chat; keep credentials in private environment variables and avoid logging authorization headers. <br>
Risk: Downloaded reports can contain sensitive financial information. <br>
Mitigation: Store downloaded reports only in a private location and remove them when no longer needed. <br>
Risk: Trading 212 API behavior may change because the skill states that the API is in beta. <br>
Mitigation: Verify Trading 212 API details with official documentation before relying on generated commands or workflows. <br>


## Reference(s): <br>
- [Trading 212 Demo API Endpoint](https://demo.trading212.com/api/v0) <br>
- [Trading 212 Live API Endpoint](https://live.trading212.com/api/v0) <br>
- [ClawHub Skill Page](https://clawhub.ai/tsvetelin-kulinski/trading212-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands and environment variable names; API calls require a user-selected demo or live environment and configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
