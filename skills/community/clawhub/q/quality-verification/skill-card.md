## Description:

Quality Verification helps agents run post-edit diagnostics, gate commits with project tests, record session metrics, configure hook profiles, and apply state hygiene patterns for coding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add quality checks around agent coding sessions, including immediate diagnostics after edits, test checks before commits, and session metric tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hooks can automatically run local project tools such as TypeScript, Python, Rust, Go, shell diagnostics, and test commands.

Mitigation: Install only in projects where automatic local tool execution is acceptable, prefer pinned project-local tools, and review hook configuration before enabling it.

Risk: Diagnostic and test output can be injected into the agent context as untrusted data.

Mitigation: Treat hook output as diagnostic text rather than instructions, and review suspicious output before acting on it.

Risk: Session metrics and cleanup patterns write or modify local state and include cleanup behavior that can affect session or worktree state.

Mitigation: Validate session identifiers before writes, review cleanup scripts, run cleanup in dry-run mode first, and require explicit confirmation before removal or pruning.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lanyasheng/skills/quality-verification)
- [Atomic Writes](references/atomic-writes.md)
- [Extended Patterns](references/extended-patterns.md)
- [Hook Pair Bracket](references/hook-bracket.md)
- [Hook Runtime Profiles](references/hook-profiles.md)
- [Post-Edit Diagnostics](references/post-edit-diagnostics.md)
- [Session Hygiene](references/session-hygiene.md)
- [Test Before Commit](references/test-before-commit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON hook outputs, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local hook scripts that can emit additional context, deny commit attempts when tests fail, and write session metric JSON.]

## Skill Version(s):

2.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
