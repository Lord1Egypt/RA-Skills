## Description:

Reversible-action infrastructure for AI agents. Use before any side-effecting action (writing/deleting/moving files, config changes, git pushes, sending messages, deploys, API calls) when the user asks "can we roll this back?", "make this safe to try", or when executing risky multi-step work. Provides hash-verified snapshots, a risk gate that demands an undo or compensation plan before acting, byte-identical restore, and a tamper-evident audit journal. Philosophy - no undo path, no action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thiennhant95](https://clawhub.ai/user/thiennhant95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before risky work that changes files, configuration, or external services. It helps them snapshot file state, require an undo or compensation plan, and verify or restore changes when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some referenced files could not be resolved to bundled files.

Mitigation: Review the release's unresolved references and their contents before installing.

Risk: Restoring a snapshot can overwrite changed files and remove files created after the snapshot within its roots.

Mitigation: Use snapshots for specific affected paths, confirm the target coverage, and use --keep-created when new files should remain.

## Reference(s):

- [Undo Plan Schema](references/plan-schema.md)
- [ClawHub release page](https://clawhub.ai/thiennhant95/skills/undo-first)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell command examples and JSON action plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans guide agent actions; remote changes depend on the agent's compensation steps.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
