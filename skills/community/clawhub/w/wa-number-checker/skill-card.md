## Description: <br>
Query whether a phone number is registered on WhatsApp using a configured wa-check-api MCP service or the documented REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqling](https://clawhub.ai/user/zhuqling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer whether a supplied phone number is registered on WhatsApp. It is intended for authorized single-number checks with E.164 or digits-only input and clear handling of API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked phone numbers are sent to wa-check-api.whatsabot.com or the configured MCP service. <br>
Mitigation: Use the skill only for numbers the user is authorized to check and avoid bulk or surveillance-style lookups. <br>
Risk: The REST API requires an x-api-key credential. <br>
Mitigation: Keep the API key out of prompts, logs, and shared code, and store it through the agent or environment's secret handling. <br>


## Reference(s): <br>
- [WhatsApp Number Checker API](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhuqling/wa-number-checker) <br>
- [Publisher profile](https://clawhub.ai/user/zhuqling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown or concise text with optional REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a WhatsApp registration status or a brief API error explanation based on the service response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
