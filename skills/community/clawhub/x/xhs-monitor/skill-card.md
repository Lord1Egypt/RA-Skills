## Description:

小红书竞品监控 - 自动采集竞品笔记，推送飞书通知，写入数据看板

This skill is ready for commercial/non-commercial use.

## Publisher:

[cstdr](https://clawhub.ai/user/cstdr)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, and competitive intelligence teams use this skill to monitor configured Xiaohongshu competitor accounts, collect recent notes, identify product or livestream signals, and prepare Feishu notifications or local records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an authenticated browser against third-party web content and may keep persistent session data.

Mitigation: Use a dedicated, non-personal browser profile and account, and remove saved browser session data when monitoring is no longer needed.

Risk: Browser execution has weak containment when no-sandbox flags are used.

Mitigation: Remove no-sandbox flags where possible, or run the browser only inside a hardened disposable container.

Risk: Dependency installation can introduce supply-chain exposure.

Mitigation: Pin and review npm dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cstdr/skills/xhs-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript configuration, shell commands, Feishu card payloads, and local CSV/JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, a Chrome or Chromium executable, configured Xiaohongshu account targets, and optional Feishu app settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
