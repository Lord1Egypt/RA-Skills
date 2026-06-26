## Description: <br>
Semi-automates WeChat replies by reading chat content with OCR, sending high-confidence replies automatically, asking for confirmation on lower-confidence replies, or sending a specified message directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjdzliu](https://clawhub.ai/user/bjdzliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate routine WeChat replies on macOS, either by letting the tool inspect recent chat text and propose a reply or by sending a specified message to a named contact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private WeChat conversations through OCR and macOS desktop automation. <br>
Mitigation: Use it only on accounts and conversations where this access is acceptable, and avoid sensitive or high-stakes conversations. <br>
Risk: The skill can send messages from the user's WeChat account automatically for high-confidence matches. <br>
Mitigation: Prefer manual confirmation for every send by reviewing or adjusting the confidence threshold and reply rules before use. <br>
Risk: Installation relies on a Homebrew tap and installed automation scripts. <br>
Mitigation: Review the Homebrew tap and installed script before running the global command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bjdzliu/wechat-auto-reply) <br>
- [Publisher profile](https://clawhub.ai/user/bjdzliu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [WeChat message text with Markdown usage instructions and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send messages automatically when confidence exceeds the configured threshold; lower-confidence replies require confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
