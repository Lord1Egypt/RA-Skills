## Description:

Provides agent tool safety and reliability guidance for repeated tool failures, permission-denial retries, destructive Bash operations, and tool input validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add guardrails around agent tool use, including retry escalation, denial tracking, pre-command checkpoints, and Bash input checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hook scripts can steer or block agent tool use.

Mitigation: Review and test hook behavior before installation, especially deny thresholds and additional-context messages.

Risk: Checkpoint logic can mutate Git state and should be treated as best-effort rollback.

Mitigation: Use it in a clean repository, verify stash behavior, and keep independent backups for high-value work.

Risk: Weak session ID or path validation could allow unsafe state-file paths or incomplete Bash command filtering.

Mitigation: Validate session IDs before using them in paths and harden path-boundary checks before deployment.

Risk: Raw tool errors replayed into agent context can introduce misleading or unsafe guidance.

Mitigation: Sanitize captured errors and avoid replaying sensitive or untrusted output into model context.

## Reference(s):

- [Checkpoint Rollback](references/checkpoint-rollback.md)
- [Denial Circuit Breaker](references/denial-circuit-breaker.md)
- [Extended Patterns](references/extended-patterns.md)
- [Graduated Permissions](references/graduated-permissions.md)
- [Scoped Hooks](references/scoped-hooks.md)
- [Tool Error](references/tool-error.md)
- [Tool Input Guard](references/tool-input-guard.md)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/tool-governance)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local hook state files such as tool-errors.json, denials.json, and git stash checkpoints when scripts are installed.]

## Skill Version(s):

2.4.0 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
