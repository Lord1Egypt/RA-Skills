## Description: <br>
Install, configure, validate, or troubleshoot the TeamClaw OpenClaw plugin for virtual software-team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topcheer](https://clawhub.ai/user/topcheer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install TeamClaw, choose a local, process, Docker, or Kubernetes worker topology, generate minimal OpenClaw configuration, and validate the first run with health checks and a smoke-test task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and worker setup guidance may lead users to run package, container, Docker, or Kubernetes workflows from external sources with workspace permissions. <br>
Mitigation: Verify package, repository, and container image sources before running commands; start with local setup and enable Docker or Kubernetes workers only in scoped workspaces with appropriate permissions. <br>
Risk: Distributed, Docker, or Kubernetes workers can fail or affect unintended workspaces if controller URLs, networking, permissions, or storage are misconfigured. <br>
Mitigation: Use the smallest matching topology, confirm controller reachability from workers, and validate with the health check, UI, and smoke-test task before larger workflows. <br>


## Reference(s): <br>
- [TeamClaw Setup on ClawHub](https://clawhub.ai/topcheer/teamclaw-setup) <br>
- [TeamClaw repository](https://github.com/topcheer/teamclaw) <br>
- [TeamClaw installation documentation](https://github.com/topcheer/teamclaw/blob/main/INSTALL.md) <br>
- [TeamClaw releases](https://github.com/topcheer/teamclaw/releases) <br>
- [TeamClaw install modes](references/install-modes.md) <br>
- [TeamClaw validation checklist](references/validation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation commands, startup commands, topology configuration snippets, validation commands, smoke-test guidance, and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
