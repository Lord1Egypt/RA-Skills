## Description: <br>
Safely run project-local build, test, lint, format, type-check, and dependency install commands with strict restrictions to prevent destructive or system-wide effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run project-local build, test, lint, format, type-check, dependency install, and status checks while avoiding destructive or system-level commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency install commands can execute third-party package scripts when approved without review. <br>
Mitigation: Review dependency install commands before approval and use the skill only in trusted workspaces. <br>
Risk: Shell commands can change project files or produce misleading results if paths or arguments are unsafe. <br>
Mitigation: Keep commands project-local, non-destructive, and limited to the minimum needed for the requested verification. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, text] <br>
**Output Format:** [Text or Markdown summaries with command names, success or failure status, and key error output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stops on failure and limits commands to the current project workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
