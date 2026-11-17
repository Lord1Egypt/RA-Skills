## Description:

Wx Echo helps an agent extract WeChat todos, calendar items, and useful group-chat content, then publish structured updates to a Discord Forum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihanghang](https://clawhub.ai/user/lihanghang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual WeChat users use this skill to set up scheduled extraction of private-chat todos, calendar signals, and group-chat digests, with the agent turning the extracted data into Discord Forum posts and follow-up tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to decrypted private WeChat history.

Mitigation: Install only when that access is acceptable, restrict monitored chats before first use, and disable raw source excerpts by default.

Risk: Sensitive keys and message data are stored in local runtime files such as all_keys.json and collector.db.

Mitigation: Use a private work directory with owner-only permissions and keep those files out of backups, shared folders, and source control.

Risk: Recurring workflows can publish chat-derived content to Discord.

Mitigation: Review Discord posts before publishing sensitive personal or work content, and limit the destination Forum to the intended audience.

Risk: Optional remote execution and fallback posting paths can expose SSH passwords or Discord tokens.

Mitigation: Prefer local execution where possible, avoid SSH password configuration and curl token fallbacks, and use managed secrets for required credentials.

## Reference(s):

- [Wx Echo ClawHub page](https://clawhub.ai/lihanghang/skills/wx-echo)
- [OpenClaw](https://openclaw.ai)
- [Artifact source link: openclaw-wx-echo](https://github.com/laolin5564/openclaw-wx-echo)
- [wechat-decrypt reference implementation](https://github.com/bbingz/wechat-decrypt/tree/feat/macos-support)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON-producing CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scheduled agent prompts for Discord Forum posts and local state updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
