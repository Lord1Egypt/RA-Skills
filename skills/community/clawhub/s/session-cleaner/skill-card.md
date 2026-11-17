## Description:

Clean up stale OpenClaw session files. Keep the current main session and all group chat sessions; move everything else to a backup directory. Use when performing periodic maintenance, heartbeat cleanup, or when the user asks to clean up sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw installations use this skill to move stale session transcript files into a recoverable backup directory while keeping the active main session and group chat sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup script may classify the wrong session file as stale because it uses heuristics to identify the active main session and group chat sessions.

Mitigation: Run the skill with --dry-run first and review the listed files before allowing any move operation.

Risk: Moved session transcripts may be difficult to recover if backup filenames collide or a needed transcript is moved unexpectedly.

Mitigation: Keep a separate backup of important session transcripts before cleanup and inspect the backup directory after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqunabc/skills/session-cleaner)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash command usage and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a dry-run mode before moving files to backup.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
