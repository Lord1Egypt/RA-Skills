## Description: <br>
微信聊天窗口自动监控、翻译和智能回复工具，集成 Qwen 大语言模型和百度翻译 API。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyi001](https://clawhub.ai/user/chaoyi001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat users and agent operators use this skill to monitor desktop WeChat conversations, generate MBTI-style Qwen responses, translate English replies into Chinese, and optionally send replies through the chat window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private WeChat chat content and send message text to configured AI and translation APIs. <br>
Mitigation: Use it only with non-sensitive chats, verify endpoint URLs and API keys yourself, and avoid use where chat participants have not consented to third-party processing. <br>
Risk: The skill can automatically send generated replies into WeChat. <br>
Mitigation: Disable or avoid automatic sending unless replies are reviewed first. <br>
Risk: The skill uses clipboard automation while handling chat content. <br>
Mitigation: Run it in a controlled desktop session and avoid keeping unrelated sensitive data on the clipboard while it is active. <br>


## Reference(s): <br>
- [微信智能聊天(MBTI版) on ClawHub](https://clawhub.ai/chaoyi001/wechatwindowllmtranslate) <br>
- [Publisher profile](https://clawhub.ai/user/chaoyi001) <br>
- [OpenClaw homepage](https://github.com/openclaw/clawhub) <br>
- [Qwen](https://github.com/QwenLM/Qwen) <br>
- [Baidu Translate API](https://fanyi-api.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text chat replies, command-line status logs, and Markdown usage/configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies are intended to be short and may be copied to the clipboard and sent through the active WeChat window.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
