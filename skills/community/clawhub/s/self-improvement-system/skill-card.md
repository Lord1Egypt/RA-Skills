## Description:

Runs a continuous self-improvement loop that helps the agent learn from mistakes, extract lessons, and refine its behaviour over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assafster](https://clawhub.ai/user/assafster)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain privacy-safe self-improvement notes, record abstract process errors, extract lessons, update playbooks, and audit recurring reasoning patterns across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable local behaviour files can broadly influence future agent sessions.

Mitigation: Review or isolate soul.md, lessons.md, playbook.md, session-log.md, and mistakes.md before use, and avoid untrusted project directories until a dedicated data directory and instruction-priority boundaries are clear.

## Reference(s):

- [Self-Improvement Protocol Reference](references/protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown process notes and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local behaviour files such as mistakes.md, lessons.md, soul.md, playbook.md, session-log.md, and archive entries.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
