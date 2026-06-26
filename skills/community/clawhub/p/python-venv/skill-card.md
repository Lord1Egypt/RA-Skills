## Description: <br>
Python environment management skill. Automatically detect project type and existing environments, recommend based on popularity. Minimize interruptions, only ask when necessary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cikichen](https://clawhub.ai/user/cikichen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to choose, reuse, create, activate, and troubleshoot Python virtual environments based on project files and existing environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create environments, install dependencies, synchronize project dependencies, remove broken environments, or run package-manager commands in a project. <br>
Mitigation: Confirm before install, sync, delete, or environment-recreation commands, reuse existing environments when possible, and review generated commands before execution. <br>
Risk: Troubleshooting guidance includes remote uv installer one-liners that fetch and execute scripts. <br>
Mitigation: Prefer verified package-manager installation steps; if a remote installer is needed, review the script and get explicit user approval before running it. <br>


## Reference(s): <br>
- [Python Virtual Environment - Common Patterns](artifact/references/patterns.md) <br>
- [Python Virtual Environment - Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment detection steps, package-manager recommendations, and activation or troubleshooting commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
