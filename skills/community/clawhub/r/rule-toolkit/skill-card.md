## Description:

Scans AI coding-agent constraint files, identifies rules that can be enforced automatically, and helps generate linters, hooks, validators, wrapper functions, and a conversion report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachunggan](https://clawhub.ai/user/dachunggan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when setting up or onboarding projects that keep coding-agent rules in files such as CLAUDE.md, agents.md, soul.md, tools.md, bootstrap.md, .cursorrules, or Copilot instructions. It helps convert suitable prompt-level rules into enforceable project tooling while reporting rules that still need human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect sensitive agent context files, including memory or identity-oriented files.

Mitigation: Review the exact files before scanning and exclude memory, identity, or other sensitive context files unless they are necessary for the conversion.

Risk: Generated hooks may run persistent, unpinned commands automatically.

Mitigation: Require a diff before writing hooks and replace bare npx commands with pinned local dependencies or lockfile-backed package scripts.

Risk: Cleanup behavior may remove prompt-level rules from source constraint files.

Mitigation: Keep original rules until reviewers confirm the generated tooling enforces the intended behavior and preserve non-toolable rules in the prompt files.

## Reference(s):

- [Tool Generation Patterns](references/tool-patterns.md)
- [OpenClaw Hooks Reference](references/openclaw-hooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with code, configuration snippets, shell commands, and proposed file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create project tooling such as linter configs, hooks, validators, wrapper functions, and cleanup edits after review.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
