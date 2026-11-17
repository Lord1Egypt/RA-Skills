## Description:

Guides OpenClaw agents to construct and run Kimi Code CLI commands for headless automation, CI/CD, background, and no-TTY workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to prepare Kimi CLI headless runs for scripts, CI/CD jobs, background tasks, and no-TTY environments. It helps select execution mode, construct commands, handle output, and surface approval risks before file or shell actions run automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless Kimi CLI modes can automatically approve file changes and shell commands, especially when --yolo is used or implied by print-style execution.

Mitigation: Use automatic approval only in a scoped project directory or disposable CI workspace, avoid privileged accounts and home or system roots, and ask for explicit confirmation before enabling mutation-capable execution.

Risk: Installing or invoking an unreviewed CLI package can expose the environment to supply-chain or unexpected execution behavior.

Mitigation: Review package provenance before installing kimi-cli and verify authentication, working directory, and command arguments before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiyouwolegequ/skills/test-rate-limit)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include constructed Kimi CLI commands, execution result summaries, exit codes, warnings, and next steps.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
