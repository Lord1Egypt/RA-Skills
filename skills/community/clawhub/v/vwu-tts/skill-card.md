## Description: <br>
Calls the vwu.ai speech-2.8-hd and speech-2.8-turbo models through an OpenAI-compatible chat completions API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure a vwu.ai API key and call the listed speech models from a shell command. It is suited for workflows that need OpenAI-compatible chat-completions access to those vwu.ai models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and account quota are handled by vwu.ai when the skill calls the API. <br>
Mitigation: Install only if you trust vwu.ai, use a limited or replaceable API key, and avoid sending prompts that should not be shared with that service. <br>
Risk: Changing VWU_BASE_URL can direct prompts and credentials to an untrusted host. <br>
Mitigation: Keep the default endpoint unless a trusted replacement endpoint is explicitly required. <br>
Risk: The artifact uses a chat-completions request path rather than a clearly dedicated audio TTS workflow. <br>
Mitigation: Validate model behavior against the intended speech or text workflow before relying on it in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a3273283/vwu-tts) <br>
- [Publisher profile](https://clawhub.ai/user/a3273283) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text model responses and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY. VWU_BASE_URL defaults to https://vwu.ai and should only be changed to a trusted endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
