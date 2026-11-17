## Description:

Plan and execute incremental project rewrites to Rust with architecture mapping, parity verification, idiomatic Rust guidance, dependency preflight checks, and GitHub upstream synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandandujie](https://clawhub.ai/user/dandandujie)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and execute staged rewrites of existing projects into Rust while preserving behavior, tracking upstream changes, and documenting verification strategy. It is especially relevant for backend migrations that need Rust design guardrails, parity checks, and GitHub synchronization notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory, unpinned third-party skill or MCP dependencies can persistently change the agent environment.

Mitigation: Install only trusted helper projects, prefer pinned and reviewed revisions, and review MCP permissions before enabling them.

Risk: The skill may inspect local Codex configuration and run Git or GitHub synchronization commands on repositories selected by the user.

Mitigation: Run it only against intended repositories, review remotes and branches before sync, and inspect generated upstream reports before acting on them.

## Reference(s):

- [Rust Backend Coding Guidelines](references/rust-backend-guidelines.md)
- [GitHub Upstream Synchronization](references/github-upstream-sync.md)
- [Rust Language Update Playbook](references/rust-language-update-playbook.md)
- [Rewrite Pitfalls and Antipatterns](references/rewrite-pitfalls-and-antipatterns.md)
- [grok-search skill dependency](https://github.com/Frankieli123/grok-skill)
- [grok-search MCP dependency](https://github.com/GuDaStudio/GrokSearch)
- [github-helper skill dependency](https://github.com/dandandujie/github-helper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and structured migration sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected sections include rewrite scope, equivalence strategy, Rust design decisions, risk register, and upstream sync notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
