## Description: <br>
Automates the Windows WeChat desktop app to search for contacts and send user-specified messages, including single-recipient and comma-separated batch sends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloud44552731-arch](https://clawhub.ai/user/cloud44552731-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to drive a logged-in Windows WeChat client for contact lookup and message sending. It is intended for intentional, user-reviewed messages rather than unattended or unsolicited bulk outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sends messages immediately from the user's logged-in WeChat account. <br>
Mitigation: Verify the contact name and message text before execution, and test first with a harmless contact. <br>
Risk: Batch mode can send the same message to multiple contacts in sequence. <br>
Mitigation: Use batch sends only when every recipient is intentional and consented. <br>
Risk: Desktop automation depends on a visible, correctly focused WeChat window and may select the first search result. <br>
Mitigation: Keep WeChat visible, confirm search behavior in the local client, and adjust delays or contact names before sending important messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloud44552731-arch/wechat-sender-win) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown instructions with command-line examples and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, a visible logged-in WeChat desktop window, Python, and pywinauto.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
