## Description:

Watchdog for OpenClaw subagent runs: enforce a completion marker by deadline and alert if missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gleb-urvanov](https://clawhub.ai/user/gleb-urvanov)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to monitor delegated subagent work by requiring a completion marker before a deadline. It helps callers detect missing completion signals and optionally send a failure alert through OpenClaw messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes a limited input-validation issue around watchdog labels.

Mitigation: Use simple trusted labels and avoid path separators or '..' in labels.

Risk: OpenClaw messaging can send failure alerts when notification environment variables are configured.

Mitigation: Set WATCHDOG_CHAT_ID only when failure alerts are intentionally expected for the target chat.

## Reference(s):

- [Subagent contract](SUBAGENT_CONTRACT.md)
- [ClawHub skill page](https://clawhub.ai/gleb-urvanov/skills/subagent-watchdog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The watchdog checks local marker files, exits non-zero when the marker is missing, and can optionally send an OpenClaw notification.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
