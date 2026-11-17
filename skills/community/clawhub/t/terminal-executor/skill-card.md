## Description:

Execute terminal commands with optional sudo privileges and return command output upon user request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choasx](https://clawhub.ai/user/choasx)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill when they want an agent to run system commands, inspect machine state, install software, or perform terminal-based maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute arbitrary shell commands, including sudo commands, without strong built-in controls.

Mitigation: Use only in a tightly controlled environment where shell execution is expected, with command review and explicit approval for sensitive operations.

Risk: Untrusted prompts or broad machine access could lead to destructive commands, exposure of sensitive environment variables, or privileged system changes.

Mitigation: Avoid untrusted prompts, shared machines, sensitive environment variables, passwordless sudo, and broad filesystem access unless additional sandboxing and command restrictions are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/choasx/skills/terminal-executor)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Structured command result text with stdout, stderr, success status, and command metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute commands in a provided working directory with merged environment variables and command timeouts.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
