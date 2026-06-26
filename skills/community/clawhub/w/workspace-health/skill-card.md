## Description: <br>
检测并修复OpenClaw工作目录嵌套问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxkandel99-arch](https://clawhub.ai/user/maxkandel99-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to detect nested `.openclawworkspace` directories, validate workspace paths, and repair workspace configuration issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The live repair command can delete directories and change configuration paths. <br>
Mitigation: Inspect the referenced PowerShell scripts, run dry-run mode first, confirm affected directories and configuration files, and keep a backup before running with DryRun set to false. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxkandel99-arch/workspace-health) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides dry-run and live repair command guidance; live repair may delete nested directories and change workspace configuration paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
