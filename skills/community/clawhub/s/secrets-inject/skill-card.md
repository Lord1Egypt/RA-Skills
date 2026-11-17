## Description:

Secrets Inject is a high-privilege companion to secrets-manager that substitutes encrypted secrets into command strings and either writes executable shell scripts containing plaintext secrets or prints resolved commands to stdout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an existing secret in secrets-manager must be passed inline to a shell command. It is intended for deliberate, opt-in secret materialization where safer secret-passing methods are not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decrypted credentials can be written into temporary shell scripts that remain on disk.

Mitigation: Use the skill only on a trusted single-user machine, keep credentials narrowly scoped, and run cleanup immediately after the injected command is used.

Risk: Printing injected commands to stdout can expose plaintext secrets in logs, shell history, terminal scrollback, or CI output.

Mitigation: Avoid stdout injection unless explicitly required; prefer safer secret-passing methods and review the generated command before execution.

Risk: Using this skill in shared containers, CI runners, or other multi-user environments can expose plaintext secret material.

Mitigation: Do not use it on shared, containerized, or CI hosts that are not fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/secrets-inject)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce executable temporary shell scripts containing plaintext secrets or print resolved commands to stdout when explicitly confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
