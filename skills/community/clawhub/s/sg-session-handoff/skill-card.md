## Description:

Summarize the current session into a precise, file-saved handoff document covering goals, files changed, commands run, errors, decisions, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or update a concise handoff document that preserves session goals, changed files, commands run, errors, decisions, current state, and next steps for another person or AI instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist detailed session history, including sensitive context if secrets or private details appeared earlier in the session.

Mitigation: Review generated handoffs before committing or sharing them, and avoid invoking the skill after secrets appeared in the session.

Risk: The skill may update existing handoff routing files without redaction or path-safety checks.

Mitigation: Check any CURRENT file before letting the skill update an existing handoff, and review modified handoff files before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/sg-session-handoff)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown file with optional pointer and index files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a handoff file, and may maintain CURRENT and INDEX.md routing files when a handoff directory is used.]

## Skill Version(s):

1.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
