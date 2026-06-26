## Description: <br>
Call and manage seven doubao models on vwu.ai with an OpenAI-compatible chat completions API using a vwu.ai API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a vwu.ai API key, inspect supported Doubao model names, and call a selected model through an OpenAI-compatible chat completions endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated responses are sent to vwu.ai or another endpoint configured through VWU_BASE_URL. <br>
Mitigation: Confirm VWU_BASE_URL is unset or points to a trusted endpoint, and avoid sensitive prompts unless the service is approved for that data. <br>
Risk: The shell wrapper uses an API key and may display a partial key prefix in quota-related error messages. <br>
Mitigation: Use a dedicated API key where possible and avoid sharing logs that include API-key prefixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-doubao) <br>
- [vwu.ai](https://vwu.ai) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Supported model list](artifact/models.txt) <br>
- [vwu-chat shell wrapper](artifact/vwu-chat.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text model output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY; sends prompts to the configured VWU_BASE_URL, defaulting to https://vwu.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
