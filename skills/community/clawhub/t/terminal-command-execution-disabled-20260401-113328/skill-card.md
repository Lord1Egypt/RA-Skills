## Description:

Execute terminal commands safely and reliably with clear pre-checks, output validation, and recovery steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmundi3210](https://clawhub.ai/user/tmundi3210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan, execute, validate, and recover from shell or CLI commands with explicit pre-checks and post-run verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command guidance can include package installs, service changes, privileged actions, or destructive filesystem operations.

Mitigation: Review risky commands before execution, prefer scoped non-destructive probes first, and require explicit approval for privileged or destructive actions.

Risk: Terminal output and logs can expose secrets or sensitive environment details.

Mitigation: Keep secrets out of command output and logs, and summarize sensitive diagnostics without reproducing secret values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tmundi3210/skills/terminal-command-execution-disabled-20260401-113328)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise command plans, diagnostic interpretations, recovery steps, and verification checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
