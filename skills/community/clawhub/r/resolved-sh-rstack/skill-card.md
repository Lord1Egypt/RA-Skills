## Description: <br>
The operator skill suite for the agentic web: it helps resolved.sh operators audit page quality, craft A2A agent cards, optimize data products, register paid service endpoints, publish monetized content, and distribute to registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hichana](https://clawhub.ai/user/hichana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and resolved.sh operators use this skill suite to improve and monetize agent-native listings by auditing their presence, generating page and A2A agent-card content, configuring data products and paid services, publishing content, and preparing registry submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live resolved.sh business, publishing, price, paywall, service, and listing changes. <br>
Mitigation: Review every generated curl payload, resource ID, price, publication state, email address, service endpoint, and paywall setting before executing commands. <br>
Risk: The workflow uses sensitive values such as RESOLVED_SH_API_KEY and webhook_secret. <br>
Mitigation: Keep API keys and webhook secrets out of chat logs, source control, screenshots, and generated artifacts. <br>
Risk: Temporary rstack files may contain account, listing, or secret-bearing data. <br>
Mitigation: Clean up temporary rstack files after use when they contain account details or secrets. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hichana/resolved-sh-rstack) <br>
- [rstack documentation](https://github.com/resolved-sh/rstack) <br>
- [resolved.sh](https://resolved.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, code snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scorecards, prioritized action lists, generated curl commands, A2A agent-card JSON, webhook verification snippets, and registry submission text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
