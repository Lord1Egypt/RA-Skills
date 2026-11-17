## Description:

Windows WeChat desktop automation for opening chats and sending messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to drive Windows WeChat Desktop for single-recipient sends, serial batch sends, personalized recipient-list sends, and template-variable campaign sends. It is intended for accounts, chats, and recipient lists the user controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real outbound WeChat messages to many recipients.

Mitigation: Use only accounts and recipient lists you control, verify recipients before sending, test on File Transfer Assistant first, and treat batch modes as live messaging workflows.

Risk: Message bodies, contact lists, screenshots, logs, and summary files may contain sensitive data.

Mitigation: Avoid confidential message bodies, keep contact files and logs private, and disable screenshots unless they are needed for troubleshooting.

Risk: Desktop automation and text or OCR verification do not prove final message delivery.

Mitigation: Review success, verification, failure, and retry fields after each run and manually confirm important sends in WeChat.

## Reference(s):

- [Single Send](references/single-send.md)
- [Batch Send](references/batch-send.md)
- [Personalized Send](references/personalized-send.md)
- [Template Variable Send](references/template-send.md)
- [ClawHub Skill Page](https://clawhub.ai/jinhuadeng/skills/wechat-desktop-sender)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus runtime logs and JSON summary files from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch and campaign modes may write per-recipient status, verification counts, retry recommendations, logs, screenshots, and control-tree dumps under wechat_automation_logs/.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
