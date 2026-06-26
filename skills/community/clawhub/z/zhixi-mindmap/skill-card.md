## Description: <br>
Zhixi Mind Map Cloud File Management lets an agent browse, search, view content, and import Markdown for Zhixi mind-map cloud files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindtwigs](https://clawhub.ai/user/mindtwigs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Zhixi cloud mind-map files, including browsing folders, searching by keyword, reading map content, and importing Markdown into a target folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token can grant access to Zhixi cloud files. <br>
Mitigation: Prefer ZHIXI_API_KEY or a secure secret store, avoid plaintext token files, and rotate the token if it is exposed. <br>
Risk: The import command uploads Markdown content to Zhixi. <br>
Mitigation: Run imports only for Markdown files the user intends to upload and confirm the target folder before importing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindtwigs/zhixi-mindmap) <br>
- [Zhixi account center](https://www.zhixi.com/account) <br>
- [Zhixi pricing](https://www.zhixi.com/pricing?from=openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Zhixi API token and can upload selected Markdown files to Zhixi.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
