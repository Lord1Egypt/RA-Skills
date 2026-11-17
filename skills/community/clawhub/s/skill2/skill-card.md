## Description:

SKILL2 is a fully local password and key generation CLI for creating strong passwords, passphrases, URL-safe tokens, API keys, UUIDs, numeric PINs, and rough password strength estimates with Python's standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q-ian-l](https://clawhub.ai/user/q-ian-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill when they need an agent to generate local command-line passwords, passphrases, tokens, API keys, UUIDs, PINs, or password strength guidance without network access or file persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated secrets and checked passwords can be exposed through terminal output, shell history, or literal command-line arguments.

Mitigation: Use hidden input or safer stdin methods for sensitive password checks, avoid literal echo pipelines and command arguments for real passwords, and clear terminal history where appropriate.

Risk: Password strength ratings are rough composition-based estimates and may overstate the security of human-created passwords.

Mitigation: Treat strength output as advisory, prefer generated secrets or sufficiently long passphrases, and apply organizational password policy before use.

## Reference(s):

- [SKILL2 ClawHub Skill Page](https://clawhub.ai/q-ian-l/skills/skill2)
- [q-ian-l ClawHub Publisher Profile](https://clawhub.ai/user/q-ian-l)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated secrets and strength-check results are intended to print to the terminal only.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
