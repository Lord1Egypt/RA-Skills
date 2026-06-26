## Description: <br>
Cloud file storage, upload, backup, and file management tool for Tencent Agent Storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnminh](https://clawhub.ai/user/shawnminh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a Tencent Agent Storage cloud drive, including uploading local files or folders, listing and searching stored files, creating folders, and generating download or preview links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files and whole folders to Tencent cloud storage with weak user-confirmation boundaries. <br>
Mitigation: Require explicit user confirmation before uploading files or folders that were not specifically named, and review the selected paths before execution. <br>
Risk: The skill relies on Tencent Agent Storage credentials that can authorize broad storage actions. <br>
Mitigation: Use a dedicated least-privilege SMH token where possible and avoid placing unrelated secrets in the referenced configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnminh/tencent-agent-storage) <br>
- [Publisher profile](https://clawhub.ai/user/shawnminh) <br>
- [Tencent Agent Storage API endpoint](https://api.tencentsmh.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON to stdout and may produce signed download or preview URLs for uploaded files.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
