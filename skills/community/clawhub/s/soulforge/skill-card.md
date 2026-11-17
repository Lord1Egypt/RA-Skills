## Description:

Run high-signal autonomous coding loops with Soulforge (feature-dev/bugfix/review-loop) using strict worktree isolation, review gates, and scoped fix cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesrp13](https://clawhub.ai/user/jamesrp13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering operators use this skill as an operating guide for running Soulforge feature development, bugfix, and PR review-loop workflows in trusted repositories with isolated worktrees and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Soulforge workflows can perform autonomous coding, PR creation, callbacks, and local CLI execution in a repository.

Mitigation: Install and run the skill only in trusted operator-controlled repositories where this level of automation is appropriate.

Risk: Running workflows in a main checkout or dirty worktree can mix autonomous changes with active work.

Mitigation: Use a dedicated isolated worktree for each run and start workflows only from clean worktrees.

Risk: Untrusted task text or custom variables can become unsafe if embedded into shell command fragments or callback commands.

Mitigation: Review task text and variables before launch, avoid shell concatenation, and pass callback_message through trusted callback wrappers.

## Reference(s):

- [Workflow YAML Format](references/workflow-format.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the soulforge and gh binaries; no environment variables are declared in release metadata.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
