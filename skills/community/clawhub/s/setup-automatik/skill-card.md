## Description: <br>
Facilitate the installation and management of VPS solutions using the Setup Automatik engine (powered by Orion Design). Use when the user wants to install, configure, or manage tools like Traefik, Portainer, Chatwoot, N8N, and other open-source applications on a Linux VPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alltomatos](https://clawhub.ai/user/alltomatos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, and manage self-hosted open-source applications on Linux VPS infrastructure. It helps collect deployment inputs, run SetupOrion-based installation steps, and verify services such as Docker, Traefik, Portainer, and application stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require administrative VPS access and make broad server changes. <br>
Mitigation: Use scoped, temporary access where possible, take a server snapshot first, and review the exact SetupOrion commands before execution. <br>
Risk: SSH, Portainer, SMTP, and application credentials may be exposed or retained during deployment workflows. <br>
Mitigation: Prefer OpenClaw node pairing over sharing root passwords or private keys in chat, and rotate credentials after use. <br>
Risk: The bundled installer includes telemetry to Orion that is under-disclosed in the skill documentation. <br>
Mitigation: Review the telemetry behavior before running the installer and remove or disable it if it is not acceptable for the deployment. <br>


## Reference(s): <br>
- [Setup Automatik on ClawHub](https://clawhub.ai/alltomatos/setup-automatik) <br>
- [tools.md](references/tools.md) <br>
- [SetupOrion.sh](assets/SetupOrion.sh) <br>
- [Mundo Automatik](https://mundoautomatik.com/) <br>
- [Orion Design setup page](https://oriondesign.art.br/setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and deployment steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run commands that install Docker services and modify VPS configuration when the agent has approved server access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
