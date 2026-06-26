## Description: <br>
Safely rotate the OpenRouter API key across all config files in an OpenClaw installation by finding every location, updating them, restarting the gateway, and verifying the key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to rotate OpenRouter API keys across environment, agent, and global configuration files while preserving backups and verifying that the new key works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live OpenRouter API keys and can expose secrets through shared chats, reusable shell commands, backups, or shell history. <br>
Mitigation: Use find or dry-run mode first, redact discovered key values before reporting them, avoid placing real keys in reusable commands or shared chats, and delete or protect backups and shell history that may contain old keys. <br>
Risk: Updating the wrong host or path can leave stale keys active or modify unintended OpenClaw configurations. <br>
Mitigation: Review the reported paths before making changes and limit SSH-based rotation to hosts the operator explicitly names. <br>


## Reference(s): <br>
- [Key Rotation Guide](references/key-rotation-guide.md) <br>
- [OpenRouter Key Management](https://openrouter.ai/keys) <br>
- [OpenRouter Key Authentication Endpoint](https://openrouter.ai/api/v1/auth/key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can scan OpenClaw configuration files, create timestamped backups, update OpenRouter key values, and verify the replacement key against OpenRouter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.yml, changelog released 2026-02-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
