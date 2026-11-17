## Description:

Session Closer guides OpenClaw and coding agents through a structured end-of-session closeout that records a journal entry, full file surface, one self-caught failure, a behavioral fingerprint, optional pattern updates, and a close summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to close work sessions consistently, capture what changed, document one self-caught failure, and preserve a behavioral fingerprint for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad session logging can capture sensitive file names, external API references, decisions, or other operational details.

Mitigation: Review and redact the journal entry before storing it in a shared location or sending any close summary externally.

Risk: The suggested repository sync step can publish unintended changes if run without inspecting the exact diff.

Mitigation: Require explicit approval and a diff review before staging, committing, or pushing; avoid broad staging commands unless the full file set is intentional.

Risk: External close summaries can disclose session details to an unintended channel.

Mitigation: Confirm the destination and payload before sending, and skip notification when no approved channel is configured.

Risk: Optional local helper scripts can modify workspace state.

Mitigation: Review the helper script files and command arguments before execution, and use the manual journal path when script behavior is not approved.

## Reference(s):

- [Journal Format](references/journal-format.md)
- [Pattern Keys](references/pattern-keys.md)
- [ClawHub Skill Page](https://clawhub.ai/highnoonoffice/skills/session-closer)
- [Project Homepage](https://github.com/highnoonoffice/hno-skills)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown journal entry with inline shell commands and a short text close summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally use local journal-writer.js and pattern-update.js helper scripts when present.]

## Skill Version(s):

1.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
