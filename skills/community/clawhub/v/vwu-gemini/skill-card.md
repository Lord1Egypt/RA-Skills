## Description: <br>
Helps an agent call five vwu.ai Gemini-series models through an OpenAI-compatible chat completions endpoint after a vwu.ai API key is configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send prompts to selected vwu.ai Gemini-compatible models and receive chat responses from the configured endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and responses are sent to vwu.ai or another endpoint if VWU_BASE_URL is changed. <br>
Mitigation: Use only trusted endpoints, keep VWU_BASE_URL unset unless intentionally changed, and avoid submitting secrets or confidential data. <br>
Risk: The skill requires an API key for a third-party service. <br>
Mitigation: Use a dedicated, revocable vwu.ai API key and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [vwu.ai](https://vwu.ai) <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-gemini) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY and sends prompts to vwu.ai or the configured compatible endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
