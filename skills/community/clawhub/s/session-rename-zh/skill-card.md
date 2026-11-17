## Description:

改会话名、rename session、会话标签、修改会话标题、session label.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhekg](https://clawhub.ai/user/fhekg)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to rename the current or selected conversation by setting a label in OpenClaw session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits OpenClaw session state and the security evidence reports an unsafe command template that can execute unintended code if given a crafted session name.

Mitigation: Review before installing, use only simple trusted labels, close OpenClaw, and back up sessions.json before editing.

Risk: Interpolating the session key or label into python3 -c source can make crafted input unsafe.

Mitigation: Prefer a safer release that passes the session key and label as command arguments or uses an official OpenClaw API.

## Reference(s):

- [Project homepage](https://github.com/fhekg/openclaw-session-rename)
- [ClawHub skill page](https://clawhub.ai/fhekg/skills/session-rename-zh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets OpenClaw session metadata and should preserve unrelated session fields.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
