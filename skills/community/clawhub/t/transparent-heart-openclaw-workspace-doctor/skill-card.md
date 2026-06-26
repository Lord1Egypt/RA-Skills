## Description: <br>
Use when the user wants to inspect, repair, package, or troubleshoot an OpenClaw workspace doctor setup, especially for stale bootstrap state, missing daily memory notes, or codex-cli launch hazards in OpenClaw config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[transparent-heart](https://clawhub.ai/user/transparent-heart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to diagnose OpenClaw workspace startup drift, repair safe workspace-local issues, package the doctor tool, and review companion fixes for codex-cli launch configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The live repair path can change global OpenClaw configuration using code that is not fully included in the reviewed artifacts. <br>
Mitigation: Run diagnostic, --check, or --stdout modes first, review the exact proposed change and backup location, and avoid the live patch until the local workspace_doctor implementation has been inspected. <br>
Risk: Workspace repair commands may modify local workspace files when run with fix options. <br>
Mitigation: Use the diagnostic output before --fix, keep workspace-local changes reviewable, and clearly report any sandbox restriction that prevents an external configuration write. <br>


## Reference(s): <br>
- [Command Map and Fix Boundaries](references/commands.md) <br>
- [Repository Layout](references/repo-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic, fix, check, stdout, packaging, and validation commands for an OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
