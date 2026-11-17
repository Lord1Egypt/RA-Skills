## Description:

AI 驱动验收执行 — 自主运行 [A] 步骤，对 [H] 步骤调用人类并提供精确的微指令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run SDD human-verification checklists, execute automated acceptance steps, ask humans only for manual observations, and update checklist status for resumable acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checklist content can drive Bash command execution.

Mitigation: Use only trusted spec-human-verify.md files and review every backticked command before allowing the skill to run.

Risk: The skill may make automatic code, configuration, or environment-file changes while trying to repair failed checks.

Mitigation: Require explicit approval for changes to .env, source code, or configuration and inspect diffs after each repair attempt.

Risk: Custom or external checklist paths may broaden the files and commands the skill consumes.

Mitigation: Prefer checklist files generated inside the trusted workspace spec directory and avoid unreviewed custom paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with shell command execution and checklist file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese user-facing acceptance summaries, yes/no human verification prompts, and status updates to spec-human-verify.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
