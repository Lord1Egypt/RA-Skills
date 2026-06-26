## Description: <br>
Access seven Kling models on vwu.ai through an OpenAI-compatible chat completions endpoint using API key authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send prompts to selected vwu.ai Kling models from a shell workflow or agent session. It is suited for text-style chat completion calls that require a vwu.ai API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to vwu.ai or to the endpoint configured through VWU_BASE_URL. <br>
Mitigation: Use the default endpoint unless a replacement endpoint is explicitly trusted, and avoid sending secrets or sensitive data in prompts. <br>
Risk: The skill requires an API key for authenticated requests. <br>
Mitigation: Use a dedicated, revocable VWU_API_KEY and rotate or revoke it if it is exposed. <br>
Risk: The shell wrapper depends on local command-line tools. <br>
Mitigation: Confirm zsh, curl, and jq are installed before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/a3273283/vwu-kling) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text API responses and Markdown guidance with shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VWU_API_KEY; VWU_BASE_URL may be set to an explicitly trusted replacement endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
