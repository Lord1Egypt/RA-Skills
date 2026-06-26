## Description: <br>
Travel Customizer is an OpenClaw travel assistant that collects confirmed customer trip requirements through conversation and submits the structured inquiry to a configured Feishu Bitable table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijingxu007](https://clawhub.ai/user/lijingxu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel providers and customer-facing teams use this skill to gather traveler contact details, destination, group size, timing, budget, preferences, and special requirements, then submit the confirmed inquiry to Feishu for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores customer contact and travel inquiry details in Feishu. <br>
Mitigation: Use a dedicated least-privilege Feishu app, restrict destination table access, and tell users before submission how their data will be retained and deleted. <br>
Risk: Incorrect Feishu credentials or table configuration can prevent inquiry submission. <br>
Mitigation: Configure the required Feishu environment variables for the intended table and verify the table columns before using the skill with customers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lijingxu007/tc-travel) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python tool behavior, and structured status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a Base Token, and a Table ID; stores submitted travel inquiry fields only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
