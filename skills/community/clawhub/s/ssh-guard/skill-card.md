## Description:

Intercepts SSH exec calls and pauses them for user approval. Supports one-time and session-wide approval modes, with automatic state cleanup when sessions end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanbo92](https://clawhub.ai/user/yanbo92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and configure an SSH approval plugin that pauses exec-based SSH commands until the user grants one-time or session-wide approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval may apply to the wrong command or session.

Mitigation: Bind approvals to full session identity and the exact tool call before relying on the plugin as a security boundary.

Risk: Sensitive SSH command text can be exposed in prompts or logs.

Mitigation: Redact credentials, avoid inline SSH secrets, and sanitize command rendering and logging.

Risk: Session-wide approval can weaken the intended approval checkpoint.

Mitigation: Prefer one-time approval for normal use and restrict session-wide approval to carefully reviewed sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanbo92/skills/ssh-guard)
- [Repository link from skill documentation](https://github.com/yanbo92/ssh-guard)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with JSON configuration snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend English or Chinese plugin entry files and OpenClaw session routing settings.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
