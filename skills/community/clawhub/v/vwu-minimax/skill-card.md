## Description: <br>
Calls vwu.ai MiniMax chat models through an OpenAI-compatible chat completions helper using a user-provided API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3273283](https://clawhub.ai/user/a3273283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure a vwu.ai API key and call MiniMax-Hailuo chat models from a shell helper. It is useful when an agent needs text responses from vwu.ai models through an OpenAI-compatible chat completions endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and chat content are sent to vwu.ai using the configured API key. <br>
Mitigation: Avoid putting secrets in prompts and install only when that external API use is intended. <br>
Risk: VWU_BASE_URL can redirect requests to a different endpoint if set incorrectly. <br>
Mitigation: Verify VWU_BASE_URL before use, or leave it unset to use the default https://vwu.ai endpoint. <br>
Risk: The shell helper depends on local command-line tools. <br>
Mitigation: Confirm zsh, curl, and jq are installed before relying on the helper. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/a3273283/vwu-minimax) <br>
- [Publisher profile](https://clawhub.ai/user/a3273283) <br>
- [vwu.ai](https://vwu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires zsh, curl, jq, and a VWU_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
