## Description: <br>
Set up Rei Qwen3 Coder as a model provider for Clawdbot, including configuration, model switching, and troubleshooting for Rei endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xReisearch](https://clawhub.ai/user/0xReisearch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add Rei Qwen3 Coder as an OpenAI-compatible Clawdbot model provider, switch between Rei and Opus, and troubleshoot Rei configuration errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Rei API key is written into the local Clawdbot configuration. <br>
Mitigation: Use a dedicated revocable Rei API key, avoid sharing it in chats or logs, and review ~/.clawdbot/clawdbot.json after setup. <br>
Risk: The setup script changes the local Clawdbot provider and model allowlist configuration. <br>
Mitigation: Keep the generated backup available and use the revert script if the configuration needs to be restored. <br>


## Reference(s): <br>
- [Rei OpenAI-compatible endpoint](https://coder.reilabs.org/v1) <br>
- [ClawHub skill page](https://clawhub.ai/0xReisearch/rei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Clawdbot configuration when the setup script is run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
