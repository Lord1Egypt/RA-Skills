## Description:

Quick system test to verify OpenClaw environment, command execution, and basic output validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gustavoziaugra](https://clawhub.ai/user/gustavoziaugra)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to check whether an OpenClaw environment can run Python, inspect the working directory, access files, and execute basic shell commands before or after installing other skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default diagnostics can expose environment variables in command output.

Mitigation: Run the skill only in low-sensitivity environments and avoid invoking it from shells or CI jobs that contain tokens or credentials.

Risk: Broad custom command execution can run unintended shell commands.

Mitigation: Restrict use to trusted diagnostic commands, review commands before execution, and prefer an explicit allowlist in hardened deployments.

## Reference(s):

- [Quick Test skill page](https://clawhub.ai/gustavoziaugra/skills/quick-test)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise pass/fail status for environment checks and command execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
