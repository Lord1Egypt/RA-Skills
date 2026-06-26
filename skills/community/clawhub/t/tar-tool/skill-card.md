## Description: <br>
Create and extract tar archives with optional compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, list, and extract tar archives for file bundling, backup, and distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracting a crafted archive can overwrite files unexpectedly. <br>
Mitigation: Use the skill only with trusted archives or inside an empty disposable working directory, and prefer a version that validates archive paths, rejects unsafe links and special files, and extracts into an explicit user-approved destination. <br>


## Reference(s): <br>
- [Tar Tool on ClawHub](https://clawhub.ai/dinghaibin/tar-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and archive files created or extracted by the tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archive operations run on local filesystem paths supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
