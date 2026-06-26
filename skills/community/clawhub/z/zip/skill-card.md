## Description: <br>
Compress, extract, list, inspect, compare, and encrypt ZIP archives in batch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local ZIP archives from an agent workflow, including creating archives, extracting packages, listing contents, checking integrity, comparing archives, searching entries, and creating encrypted ZIP files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracting an archive can overwrite files in the destination directory. <br>
Mitigation: Extract untrusted archives into a new empty folder and avoid extracting into important directories. <br>
Risk: Encrypted ZIP passwords are passed on the command line and can appear in logs, shell history, or process metadata. <br>
Mitigation: Avoid sensitive reusable passwords with the password command and prefer one-time or low-sensitivity archive passwords. <br>


## Reference(s): <br>
- [Zip ClawHub listing](https://clawhub.ai/xueyetianya/zip) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ZIP archive operations through bash commands that require zip and unzip.] <br>

## Skill Version(s): <br>
3.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
