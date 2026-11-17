## Description:

Send files via the Windows WeChat desktop client by automating window control, clipboard actions, and keyboard input with Node.js and PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on Windows can use this skill to send a chosen local file to a WeChat contact through the installed WeChat desktop client. It is best suited to low-sensitivity file-transfer workflows where UI automation failure or misdelivery would be acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses fragile WeChat UI automation and may select the wrong conversation or send to an unintended recipient.

Mitigation: Use only with non-sensitive files and contacts where misdelivery is acceptable, and add a confirmation step that verifies the exact conversation before sending.

Risk: The packaged artifact references scripts/send-file.ps1, but that PowerShell file is absent.

Mitigation: Review the installed package before use and do not rely on the skill until the missing PowerShell implementation is supplied and audited.

Risk: The skill makes misleading claims about no data transfer even though its purpose is to send a file through WeChat.

Mitigation: Treat file contents as shared with the selected WeChat recipient and apply normal data-classification and approval controls before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/26048608982lp-ai/skills/wechat-file-sender)
- [Artifact skill documentation](artifact/SKILL.md)
- [Node.js launcher script](artifact/scripts/send-file-to-wechat.js)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown instructions with command-line examples and executable script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, WeChat desktop, a local absolute file path, and a target contact name.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
