## Description: <br>
Display file or filesystem status information for checking file permissions, sizes, timestamps, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Stat Tool to inspect local path metadata such as size, modified time, and mode when troubleshooting or documenting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal basic metadata for local files or filesystem paths it is asked to inspect. <br>
Mitigation: Use it only on paths the user is authorized to inspect and avoid sensitive locations unless metadata disclosure is acceptable. <br>
Risk: Documentation describes broader stat-style options than the current script evidence demonstrates. <br>
Mitigation: Validate required flags and output behavior in the target environment before relying on the skill for operational workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/stat-tool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect local filesystem metadata for paths the user asks about; security evidence does not show file-content reads or external data transfer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
