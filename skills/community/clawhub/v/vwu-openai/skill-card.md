## Description: <br>
Provides a shell wrapper for calling vwu.ai's OpenAI-compatible chat completions API with supported GPT-4 and GPT-5 series model names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure a vwu.ai API key and send prompts to vwu.ai-hosted OpenAI-compatible chat models from a shell command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to vwu.ai's OpenAI-compatible chat API. <br>
Mitigation: Use this skill only when you trust vwu.ai with submitted content, and avoid sending secrets or sensitive data unless that use is appropriate. <br>
Risk: VWU_BASE_URL can redirect requests and the API key to a different endpoint. <br>
Mitigation: Keep the default endpoint or set VWU_BASE_URL only to an endpoint you trust. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/a3273283/vwu-openai) <br>
- [Publisher profile](https://clawhub.ai/user/a3273283) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text API responses and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY; optional VWU_BASE_URL changes the API endpoint; the wrapper depends on curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
