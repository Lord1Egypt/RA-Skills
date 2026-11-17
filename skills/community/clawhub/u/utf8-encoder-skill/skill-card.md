## Description:

为AI代理和开发者打造的UTF-8发布基础设施，自动处理跨平台编码问题，集成防卡顿策略和韧性保障，防止API token浪费，遵循'防止勤务干扰'原则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrpulor-gh](https://clawhub.ai/user/mrpulor-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to validate UTF-8 text, calculate byte lengths, build UTF-8 JSON payloads, and publish encoded content to supported platforms such as Discord and GitHub. It is most relevant when multilingual content, especially Chinese text and emoji, must be sent through command-line or API workflows without encoding-related corruption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking fallback credentials in its integration test.

Mitigation: Remove embedded credentials before running integration-test.js and use only credentials created specifically for testing.

Risk: Publishing commands can send credentials or content to external services.

Mitigation: Use least-privilege Discord, GitHub, and Reddit credentials; prefer environment variables over command-line arguments.

Risk: Failed publishing flows may save content as local plaintext backups.

Mitigation: Avoid publishing sensitive content unless local plaintext backups are acceptable, and delete generated backup files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrpulor-gh/skills/utf8-encoder-skill)
- [Publisher profile](https://clawhub.ai/user/mrpulor-gh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; encoded text and JSON payloads when the tool is invoked.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; network publishing workflows require user-supplied platform credentials.]

## Skill Version(s):

2.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
