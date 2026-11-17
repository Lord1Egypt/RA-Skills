## Description:

Set up Rei Qwen3 Coder as a model provider for Clawdbot using the OpenAI-compatible Rei endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xreisearch](https://clawhub.ai/user/0xreisearch)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to configure Rei Qwen3 Coder as an OpenAI-compatible model provider, switch between Rei and Opus, and troubleshoot Rei endpoint access errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow handles a Rei API key and writes it into the Clawdbot configuration.

Mitigation: Avoid pasting API keys into chat or command history; use a safer secret input method and verify that ~/.clawdbot/clawdbot.json and its backup are permission-restricted.

Risk: The setup and revert scripts modify Clawdbot configuration files and restart the gateway.

Mitigation: Review configuration changes before execution, keep the backup available, and use the revert script if the new provider configuration causes issues.

## Reference(s):

- [ClawHub Rei-Clawd Skill Page](https://clawhub.ai/0xreisearch/skills/rei)
- [Rei OpenAI-Compatible Endpoint](https://coder.reilabs.org/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, model-switching, revert, and troubleshooting guidance for Clawdbot Rei provider configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
