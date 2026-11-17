## Description:

Bridge between SDF COM chatroom and Feishu-Lark messaging platform with bidirectional English/Chinese translation, command relay, and real-time chat synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an existing SDF COM session to Feishu or Lark, relay chat commands, parse terminal output, and queue English/Chinese translation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an existing SSH session and local workspace queues while message-sending, translation, and file-write behavior are under-scoped.

Mitigation: Review before installing, use an isolated account or environment, and do not run it against a sensitive SSH session.

Risk: `com:` and `s:` inputs are treated as outbound messages to another chat system.

Mitigation: Treat those prefixes as message-sending commands and review message routing before deployment.

Risk: The security guidance calls out translation-result path validation as a prerequisite before enabling the queue processor.

Mitigation: Fix translation-result path validation before enabling translation queue processing.

Risk: Dependency guidance includes system or sudo Python installation paths.

Mitigation: Install dependencies in an isolated Python environment and avoid system or sudo Python installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ykaixu/skills/sdf-com-bridge)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bridge setup steps, Python integration examples, COM and Feishu command guidance, and operational cautions.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
