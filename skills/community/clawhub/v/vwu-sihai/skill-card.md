## Description: <br>
Call vwu.ai Sihai models through an OpenAI-compatible API using the bundled vwu-chat command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure a vwu.ai API key, inspect available Sihai models, and send prompts to a selected model through the OpenAI-compatible chat completions interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to a remote vwu.ai model service. <br>
Mitigation: Avoid sending secrets, credentials, regulated data, or other sensitive content in prompts. <br>
Risk: The skill uses an API key and allows VWU_BASE_URL to override the default endpoint. <br>
Mitigation: Use a revocable API key and verify VWU_BASE_URL has not been set to an unexpected endpoint before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-sihai) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text model responses, with Markdown and bash examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY; VWU_BASE_URL defaults to https://vwu.ai and may be overridden by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
