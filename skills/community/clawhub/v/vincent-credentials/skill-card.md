## Description:

Secure credential management for agents that helps store API keys, passwords, OAuth tokens, or SSH keys and write them to .env files without exposing values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an application needs credentials written to environment files without asking the user to paste secrets into the agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release handles high-impact secrets and depends on the Vincent service and @vincentai/cli package.

Mitigation: Use only if the Vincent service and CLI package are trusted; pin or preinstall a reviewed CLI version before use.

Risk: Supplying credential values through an agent command can expose human-provided secrets to the agent workflow.

Mitigation: Prefer the dashboard claim flow so the agent never receives the secret value.

Risk: The skill can write credential material to .env files and local credential configuration paths.

Mitigation: Restrict writes to the intended project .env file, ensure .env files are gitignored and permission-limited, and review declared credential config paths.

## Reference(s):

- [Vincent homepage](https://heyvincent.ai)
- [ClawHub skill page](https://clawhub.ai/glitch003/skills/vincent-credentials)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON CLI confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update .env files and local Vincent credential configuration.]

## Skill Version(s):

1.0.69 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
