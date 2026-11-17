## Description:

Facilitate the installation and management of VPS solutions using the Setup Automatik engine (powered by Orion Design). Use when the user wants to install, configure, or manage tools like Traefik, Portainer, Chatwoot, N8N, and other open-source applications on a Linux VPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alltomatos](https://clawhub.ai/user/alltomatos)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to prepare a Linux VPS, collect deployment details, run the SetupOrion installer for common open-source application stacks, and verify the resulting services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require root-equivalent control of a VPS.

Mitigation: Use it only with trusted publishers and on systems where you are comfortable granting full administrative control.

Risk: The installer workflow may involve unsafe install practices such as pipe-to-shell commands.

Mitigation: Review downloaded scripts before execution and avoid pipe-to-shell installation where possible.

Risk: The installer may create or handle service credentials and Portainer access tokens.

Mitigation: Rotate generated credentials and tokens after installation and store replacement secrets in an approved secret manager.

Risk: Improper TLS configuration can expose management interfaces.

Mitigation: Require valid TLS before using Portainer or other exposed administrative services.

Risk: Undisclosed telemetry may be present in the installer workflow.

Mitigation: Disable or remove telemetry before production use.

## Reference(s):

- [Setup Automatik skill page](https://clawhub.ai/alltomatos/skills/setup-automatik)
- [Orion Design VPS Solutions](references/tools.md)
- [SetupOrion installer script](assets/SetupOrion.sh)
- [Mundo Automatik](https://mundoautomatik.com/)
- [Orion Design setup](https://oriondesign.art.br/setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or adapt bundled shell and Python scripts when the agent has VPS access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
