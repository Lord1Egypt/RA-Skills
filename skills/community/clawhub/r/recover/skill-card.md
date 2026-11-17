## Description:

Scan for orphaned worktrees and stale branches after crashes or abandoned sessions. Offers safe cleanup options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Recover after crashes, forced session terminations, stale process warnings, or periodic repository hygiene to inspect Git worktrees and branches, preserve useful work, and propose cleanup actions that require approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands can change or discard Git state if approved without reviewing branch names, commit hashes, and uncommitted changes.

Mitigation: Review the reported branches, commits, file changes, and proposed actions before approving cleanup; keep the skill in scan-only mode until approval is explicit.

Risk: Git worktree listings cannot prove whether another session is actively using a worktree.

Mitigation: Classify recently touched worktrees without lock, heartbeat, or process evidence as unknown activity and avoid cleanup until activity is resolved.

## Reference(s):

- [Recover skill page](https://clawhub.ai/conorbronsdon/skills/recover)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan findings are read-only by default; cleanup commands require explicit approval before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
