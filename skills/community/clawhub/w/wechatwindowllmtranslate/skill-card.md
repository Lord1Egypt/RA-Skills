## Description:

Automates WeChat desktop monitoring, translation, MBTI-styled Qwen reply generation, and optional automatic reply sending on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyi001](https://clawhub.ai/user/chaoyi001)

### License/Terms of Use:

MIT-0

## Use Case:

External Windows users use this skill to monitor WeChat Desktop conversations, generate concise MBTI-styled replies with Qwen, translate English responses into Chinese with Baidu Translate, and send replies through clipboard and UI automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads active WeChat messages and can send chat-derived content to external Qwen/Baidu-compatible services.

Mitigation: Use HTTPS-only endpoints, avoid sensitive chats, and run first with a low-risk chat or test account.

Risk: Automatic reply sending can post incorrect or unintended messages into WeChat conversations.

Mitigation: Prefer manual review before sending responses and keep the edge/keyboard stop mechanisms available while the skill runs.

Risk: Interactive credential entry and runtime output may expose configured secrets.

Mitigation: Provide credentials through environment configuration, keep secrets out of shared logs, and rotate exposed API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyi001/skills/wechatwindowllmtranslate)
- [OpenClaw / ClawHub homepage](https://github.com/openclaw/clawhub)
- [Qwen project](https://github.com/QwenLM/Qwen)
- [Baidu Translate Open Platform](https://fanyi-api.baidu.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text chat replies plus Markdown setup guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies are length-limited by REPLY_COUNT and depend on the active Windows UI state plus configured Qwen and Baidu API services.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact files also mention 1.0.0, 1.0.9, and 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
