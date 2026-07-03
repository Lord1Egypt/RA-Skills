## Description: <br>
Helps an agent install, configure, verify, and remove backend services in WSL Ubuntu from a Windows host using wsl.exe, root shell commands, and aptitude. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[microsnow](https://clawhub.ai/user/microsnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy and manage WSL Ubuntu services such as MySQL, Redis, Nginx, PostgreSQL, and MongoDB from a Windows host. It provides command guidance for package discovery, installation, service startup, configuration backup, verification, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes root-level service management patterns and weak example credentials. <br>
Mitigation: Review commands before use, replace all example passwords, and run only in disposable or tightly controlled WSL environments. <br>
Risk: The skill can expose services such as Redis beyond localhost. <br>
Mitigation: Avoid remote exposure unless firewall rules and strong authentication are configured. <br>
Risk: Cleanup examples include destructive purge and rm -rf steps that can erase service data. <br>
Mitigation: Create backups and run destructive cleanup only when data removal is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/microsnow/wsl-service-deploy) <br>
- [Server-resolved GitHub source](https://github.com/microsnow/wsl-service-deploy.git) <br>
- [WSL command reference](references/wsl-commands.md) <br>
- [Ubuntu mirror referenced by the skill](https://mirrors.aliyun.com/ubuntu/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for review before execution in a controlled WSL environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
