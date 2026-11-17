## Description:

Execute an approved implementation plan with TDD, visible progress updates, and optional worktree setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to execute an approved plan, keep a task ledger, apply a test-first workflow, and hand off implementation evidence for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify git state by creating branches or worktrees and by editing and committing .gitignore during setup.

Mitigation: Use it only in repositories where branch, worktree, and .gitignore changes are acceptable, and review planned git operations before allowing setup to proceed.

Risk: The skill may install dependencies, run build commands, or execute tests in unfamiliar projects.

Mitigation: Review dependency and build commands before execution, especially in repositories or dependency graphs you do not already trust.

## Reference(s):

- [Taku Build skill page](https://clawhub.ai/kkenny0/skills/taku-build)
- [Test-Driven Development](artifact/references/tdd.md)
- [Git Worktree Isolation](artifact/references/worktrees.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown status reports with task ledgers, verification evidence, code changes, configuration edits, and shell commands when implementation requires them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces BUILD PREFLIGHT, BUILD UPDATE, and BUILD COMPLETE handoff formats.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
