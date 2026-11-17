## Description:

Read a line from standard input into a variable. Use for interactive shell prompts and script input handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture one line of interactive input for shell prompts and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password and silent-input claims are misleading and could expose secrets in plaintext.

Mitigation: Do not use this skill for passwords, API keys, tokens, or other secrets unless the implementation is fixed to use secure no-echo input and avoid writing sensitive values to stdout.

Risk: Prompt, timeout, and silent-mode options may not behave as documented.

Mitigation: Review and test option behavior before relying on the skill in interactive scripts or production workflows.

## Reference(s):

- [Read Tool on ClawHub](https://clawhub.ai/dinghaibin/skills/read-tool)
- [dinghaibin publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads one line from standard input and writes the captured value to standard output.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
