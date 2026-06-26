## Description: <br>
Creates local ZIP archives from specified files; the release documentation also describes broader archive-management features that are not implemented in the included script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to create simple local ZIP archives from selected files. Reviewers should independently verify any broader archive-management behavior before relying on it for extraction, encryption, update, delete, or confidential-archive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release documentation advertises password/encryption, list, extract, update, and delete features that the included script does not implement. <br>
Mitigation: Use it only as a simple local ZIP creator unless the release is independently verified against the claimed archive-management behavior. <br>
Risk: Putting real passwords directly in command-line arguments can expose secrets through shell history or process listings. <br>
Mitigation: Avoid command-line password arguments for confidential archives; use a vetted archive tool with secure secret handling when encryption is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/zip-tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, text, JSON] <br>
**Output Format:** [Command-line output, ZIP archive files, and optional JSON metadata described by the release documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem archive operations; advertised password and archive-management features require independent verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
