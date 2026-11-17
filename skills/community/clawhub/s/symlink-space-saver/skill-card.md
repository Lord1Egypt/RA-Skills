## Description:

Helps agents reduce duplicate local storage by safely replacing verified redundant files or directories with symlinks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan cautious local storage deduplication when duplicate large files or directories can be replaced with symlinks. It guides identity checks, physical-storage checks, consumer compatibility review, rollback preservation, and application-level verification before reclaiming space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed symlink can create a fragile dependency or break consumers, especially for directories, privileged paths, caches, mounts, or application-managed data.

Mitigation: Review each proposed symlink before execution, preserve rollback, and keep the rollback copy until the real consumer has been tested.

Risk: A symlink may appear valid while the referenced path or application behavior is still unverified.

Mitigation: Verify the link mechanically and test the application that consumes the path before reclaiming redundant data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinguy/skills/symlink-space-saver)
- [Server-resolved GitHub source](https://github.com/pinguy/Skills/tree/main/skills/symlink-space-saver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with checklists, decision receipts, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inspect-first workflow; proposed filesystem changes should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
