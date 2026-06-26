## Description: <br>
Recursively extracts nested ZIP, 7z, and RAR archives, including archives with Chinese filenames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang-dafa](https://clawhub.ai/user/tang-dafa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and support staff use this skill to unpack a single archive or a folder of archives that may contain multiple nested ZIP, 7z, or RAR files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archive extraction can write files outside the selected folder. <br>
Mitigation: Run the skill only on trusted archives or copied test folders, and add path containment checks before using it on sensitive directories. <br>
Risk: Successfully extracted source archives are deleted automatically. <br>
Mitigation: Keep backups or require an explicit delete-original option before processing important archives. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tang-dafa/unzip-all) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text or Markdown with shell commands and extraction status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create extracted files and folders, and may delete source archives after successful extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
