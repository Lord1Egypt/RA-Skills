## Description:

Sends proactive Yuanbao Pai group or private messages and selected file uploads through the Yuanbao bot channel for scheduled jobs, cross-session notifications, and background automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Yuanbao Pai group or private notifications and upload selected local files from cron jobs, background scripts, or other agent sessions without waiting for an inbound mention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages and upload selected local files to Tencent/Yuanbao infrastructure using local bot credentials.

Mitigation: Install only for trusted publishers and intended Yuanbao messaging workflows; use a dedicated bot credential, restrict who can invoke the skill, and avoid sending secrets or personal data.

Risk: Message recipients and upload paths are provided at invocation time, and the evidence reports no built-in guardrails.

Mitigation: Add recipient and path allowlists where possible, review message and file content before use, and run the skill in a reviewed dependency environment.

Risk: The artifact notes that using the same bot identity can disconnect the active OpenClaw Yuanbao plugin session.

Mitigation: Use the skill only when the plugin does not need an active connection, avoid frequent calls, and schedule proactive sends during acceptable interruption windows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luhuiwang/skills/yuanbao-send)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, websocket-client, cos-python-sdk-v5, and local Yuanbao appKey/appSecret configuration.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
