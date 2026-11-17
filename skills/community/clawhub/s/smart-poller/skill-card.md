## Description:

Periodically polls a Feishu task board to detect tasks assigned to the current AI agent, run simple task-handling logic, and write completion feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socneo](https://clawhub.ai/user/socneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an AI agent to a Feishu task board, poll for assigned pending tasks, and record status feedback back into the shared document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The poller can run persistently and act on task text from a shared Feishu document without an approval step or strong verification that work was completed.

Mitigation: Use it only with a trusted, access-restricted task board; test with --once first; and add approval, audit logging, and clear task-creation rules before continuous use.

Risk: The skill requires Feishu app credentials and a document token in local configuration.

Mitigation: Use a least-privilege Feishu app, keep config.json out of source control, and restrict file permissions for credential-bearing configuration.

## Reference(s):

- [Smart Poller ClawHub release](https://clawhub.ai/socneo/skills/smart-poller)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [README.md](README.md)
- [README.zh-CN.md](README.zh-CN.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON configuration examples, CLI commands, runtime text or JSON status summaries, and Feishu document feedback entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run continuously or once, fetch tasks from a configured Feishu document, and append completion feedback to that document.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
