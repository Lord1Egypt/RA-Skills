## Description: <br>
Calls vwu.ai Veo family models through an OpenAI-compatible chat completions API after VWU_API_KEY is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call one of five vwu.ai Veo models from shell workflows by supplying a model name and prompt. It is useful when an agent needs output from a remote vwu.ai model endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and model requests are sent to the remote vwu.ai provider. <br>
Mitigation: Use the skill only with data appropriate for that provider and avoid sending secrets or sensitive private content unless the provider is trusted for that use. <br>
Risk: Changing VWU_BASE_URL can redirect prompts and the API key to another endpoint. <br>
Mitigation: Leave VWU_BASE_URL unset or set it only to a trusted endpoint. <br>
Risk: The skill requires an API key for remote access. <br>
Mitigation: Use a dedicated VWU_API_KEY where possible and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-veo) <br>
- [vwu.ai](https://vwu.ai) <br>
- [Publisher profile](https://clawhub.ai/user/a3273283) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text from the remote API, with Markdown usage guidance and shell commands in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY and optionally accepts VWU_BASE_URL; sends prompts to a remote vwu.ai endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
