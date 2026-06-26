## Description: <br>
Create and manage test payment links including one-time, recurring, plans, multi-product, custom, pay-what-you-want, and discount options. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yaggit](https://clawhub.ai/user/yaggit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and testers use this skill to create and inspect sandbox payment-link flows, including one-time payments, subscriptions, payment plans, discounts, webhook handling, and validation behavior. It is intended for test environments and does not process real payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sandbox payment workflows could be mistaken for production payment processing. <br>
Mitigation: Use only with a local sandbox payment service and test credentials; do not connect it to a real payment processor without a production security review. <br>
Risk: Credential handling, authentication headers, and logging behavior may be insufficient for real payment environments. <br>
Mitigation: Review and fix credential storage, request authentication, sensitive-data masking, and logging before any use beyond local testing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yaggit/upload-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Raw structured JSON responses with validation errors when requests are incomplete or unsupported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses test API credentials and a local sandbox payment service; output should preserve API response structure without added commentary.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
