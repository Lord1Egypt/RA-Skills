## Description:

Use maskrun to run potentially sensitive shell commands while masking configured secret values from stdout and stderr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctxinf](https://clawhub.ai/user/ctxinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before running commands that may expose environment variables, API keys, tokens, passwords, credentials, .env values, or cloud and CI secrets in terminal output or logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat output masking as sandboxing or data-loss prevention.

Mitigation: Review commands before execution; maskrun filters stdout and stderr but does not block file reads, file writes, network access, credential access, or child process behavior.

Risk: Sensitive values can still appear if the relevant environment variable names are not covered by the maskrun configuration.

Mitigation: Configure exact, glob, or regex rules for secret-bearing variable names, and use verbose mode only to inspect matched variable names without printing raw values.

## Reference(s):

- [agent-env-guard GitHub repository](https://github.com/ctxinf/agent-env-guard)
- [agent-env-guard latest release](https://github.com/ctxinf/agent-env-guard/releases/latest)
- [Use Maskrun on ClawHub](https://clawhub.ai/ctxinf/skills/use-maskrun)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance preserves the wrapped child command after maskrun -- and describes TOML masking rules.]

## Skill Version(s):

0.1.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
