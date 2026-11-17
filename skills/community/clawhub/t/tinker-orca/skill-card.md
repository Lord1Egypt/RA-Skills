## Description:

Tinker ORCA coordinates parallel multi-agent code edits by drafting changes concurrently, applying them with per-file leases, and checking declared repo-relative write lists before and after apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to split multi-file coding work into declared edit units, run subagents in parallel, apply non-conflicting changes, and optionally commit results after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A subagent may bypass advertised file write limits when commit mode is enabled.

Mitigation: Use disposable branches or repositories first, keep commit mode off, and avoid enabling both commit and confirmedCommit until the worktree result identity validation issue is fixed.

Risk: The workflow can modify repository files and git history through subagents running as the user.

Mitigation: Review the workflow before use, declare narrow writes lists, inspect results before committing, and run project tests or the included selftest where appropriate.

Risk: Boundary checks rely on ordinary checker subagents with self-reported output and cannot see all writes, such as gitignored files or writes outside the repository.

Mitigation: Treat the checks as detection rather than sandboxing, use the default worktree mode, and run in repositories where unintended writes can be reviewed or discarded.

## Reference(s):

- [Tinker ORCA on ClawHub](https://clawhub.ai/globalcaos/skills/tinker-orca)
- [Publisher profile: globalcaos](https://clawhub.ai/user/globalcaos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JavaScript workflow invocation examples, and structured workflow status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can modify repository files and git history only through the workflow options the user supplies; subagents run on the user's configured provider.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
