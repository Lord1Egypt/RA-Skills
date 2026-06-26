## Description: <br>
Long-term Telegram memory for AI agents that searches conversations, gets digests, extracts decisions, and connects to Telegram channels through the user's own account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may4vfx](https://clawhub.ai/user/may4vfx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, summarize, and extract decisions from Telegram channels and groups connected through the user's own account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Telegram channel or chat content may be sent to and processed by a third-party service. <br>
Mitigation: Use the skill only with Telegram sources the user is authorized to sync, and review consent, privacy, and retention expectations before connecting channels. <br>
Risk: The API key is persistent credential material and the artifact guides users to save it in local agent configuration. <br>
Mitigation: Store the key only in approved local configuration or secret storage, avoid sharing it in chat logs, and revoke or remove it when access is no longer needed. <br>
Risk: API calls can consume paid points and may return Telegram source URLs. <br>
Mitigation: Confirm the requested scope and operation before running high-cost digest or decision calls, and handle returned source links as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/may4vfx/telegram-agent-memory) <br>
- [Publisher profile](https://clawhub.ai/user/may4vfx) <br>
- [Agent Memory Telegram bot](https://t.me/AgentMemoryBot) <br>
- [Agent Memory API base URL](https://agent.ai-vfx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_MEMORY_API_KEY and curl; API responses may include Telegram source URLs.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
