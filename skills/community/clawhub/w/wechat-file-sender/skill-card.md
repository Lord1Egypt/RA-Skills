## Description: <br>
Send files via the Windows WeChat desktop client by automating window control, clipboard actions, and keyboard input with Node.js and PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users with the WeChat desktop client installed use this skill to send a local file to a named WeChat contact through desktop automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can transmit local files through a logged-in WeChat account without strong recipient verification or a final confirmation. <br>
Mitigation: Use only non-sensitive files and trusted contacts, verify the exact recipient before execution, and require confirmation immediately before sending. <br>
Risk: The Node.js wrapper expects a bundled PowerShell helper, but the submitted artifact includes the helper source in documentation rather than as the script file the wrapper executes. <br>
Mitigation: Install or release only a fixed package that includes the expected PowerShell helper file and review it before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/26048608982lp-ai/wechat-file-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, a logged-in WeChat desktop client, Node.js, and the bundled PowerShell helper.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
