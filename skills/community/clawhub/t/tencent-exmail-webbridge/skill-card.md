## Description: <br>
Guides agents in operating Tencent Exmail's web UI through Kimi WebBridge, including iframe traversal, Chinese text encoding, reading messages, preparing replies or forwards, appending body content, saving drafts, and folder navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolingrabbit](https://clawhub.ai/user/coolingrabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this documentation-only skill to automate user-directed Tencent Exmail browser workflows in a logged-in mailbox. It helps inspect messages, prepare replies or forwards, append draft body content, and navigate folders while keeping final sending under explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help read email content and prepare replies or forwards in a logged-in Tencent Exmail mailbox. <br>
Mitigation: Use it only with accounts and pages the user intends to automate, and require explicit user confirmation before any send action. <br>
Risk: Tencent Exmail uses nested iframes and dynamic DOM changes, so browser automation can target the wrong frame or state. <br>
Mitigation: Confirm login, WebBridge injection, page load, iframe titles, and current compose mode before acting. <br>
Risk: Chinese text can be corrupted if sent through WebBridge as direct UTF-8 literals. <br>
Mitigation: Use the documented character-code encoding and decoding protocol for Chinese text input and returned strings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coolingrabbit/skills/tencent-exmail-webbridge) <br>
- [README](README.md) <br>
- [REFERENCE](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no runtime scripts are installed.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact frontmatter/config list 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
