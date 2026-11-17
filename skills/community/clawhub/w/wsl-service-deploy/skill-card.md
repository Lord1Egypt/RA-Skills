## Description:

Helps agents deploy and manage backend services in WSL Ubuntu from Windows using local WSL commands and aptitude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microsnow](https://clawhub.ai/user/microsnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent generate WSL Ubuntu service installation, uninstall, status-check, and configuration workflows for packages such as MySQL, Redis, Nginx, PostgreSQL, and MongoDB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded weak passwords and command-line secret handling can expose root or service credentials.

Mitigation: Replace default passwords with unique runtime-supplied secrets, avoid echoing secrets into su or command lines, and rotate any credentials created during testing.

Risk: Remote Redis exposure can make a service reachable beyond the local WSL host.

Mitigation: Bind Redis and other services to localhost by default, and require explicit network and firewall review before enabling external access.

Risk: Package purge and recursive cleanup commands can delete installed services, configuration, and data.

Mitigation: Require explicit confirmation, verified backups, and a disposable WSL environment before running uninstall or data-removal commands.

Risk: Running generated temporary scripts as root increases the impact of command mistakes or script tampering.

Mitigation: Review generated scripts before execution, use restrictive file permissions, and test in a disposable WSL environment until the workflow is revised.

## Reference(s):

- [WSL operations command reference](references/wsl-commands.md)
- [Source repository](https://github.com/microsnow/wsl-service-deploy.git)
- [ClawHub skill page](https://clawhub.ai/microsnow/skills/wsl-service-deploy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root-level WSL service-management commands, generated shell scripts, package operations, and configuration changes.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
