## Description: <br>
众安车险自助投保 helps an agent guide users through car-insurance login, vehicle quote, underwriting, payment, and policy issuance flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henry4c](https://clawhub.ai/user/henry4c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their assisting agents use this skill to complete a ZhongAn car-insurance flow: authenticate by phone, select or provide vehicle details, obtain a quote, confirm underwriting, open a payment QR code, and query policy issuance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles car-insurance, identity, phone, vehicle, credential, and payment-flow data. <br>
Mitigation: Install only when this data handling is appropriate, obtain user consent before collection or transmission, and keep sensitive values out of chat transcripts and files. <br>
Risk: Server security review flagged privacy and credential-handling gaps around local phone-number authorization storage and browser-visible API keys. <br>
Mitigation: Remove or replace the local phone-number authorization file design, avoid placing car-api-key values in URLs, and pass credentials through scoped environment variables or request headers where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/henry4c/za-car-insurance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user consent and a car-api-key credential before insurance, identity, vehicle, or payment-flow data is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
