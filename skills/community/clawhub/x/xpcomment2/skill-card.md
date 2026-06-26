## Description: <br>
Reads, writes, and removes JPEG XPComment metadata, including Windows photo Comments, by producing exiftool commands for single files, batches, and recursive folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyturbo](https://clawhub.ai/user/happyturbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill when they need an agent to read, add, overwrite, or remove XPComment metadata on local JPEG/image files using exiftool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write, remove, wildcard, or recursive operations can change image files in place. <br>
Mitigation: Confirm the exact files or directory scope before execution and keep backups when the metadata matters. <br>
Risk: The generated commands require exiftool and can fail or behave differently if it is missing or unavailable. <br>
Mitigation: Verify exiftool is installed before using write or read commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may modify image metadata in place and depend on exiftool being installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
