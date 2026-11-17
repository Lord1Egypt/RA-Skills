## Description: <br>
Whatsapp Master Free helps agents send WhatsApp text, media, stickers, voice notes, and GIFs through WhatsApp channel commands, with JID formatting and rate-limit guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users and independent developers use this skill to prepare WhatsApp send commands for text, images, documents, stickers, voice notes, and GIF-style media. Operators should use it for explicit messaging tasks where the recipient, message content, and any attached file are known before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unintended WhatsApp messages or attachments could be sent if the recipient, message text, JID, or file path is not confirmed. <br>
Mitigation: Use the skill only for explicit WhatsApp send tasks and verify the recipient, message content, and attached file before each send. <br>
Risk: Broad local execution or ffmpeg use on untrusted paths could process unsafe files or user-supplied filenames. <br>
Mitigation: Avoid unsupervised shell or ffmpeg execution and restrict media conversion to trusted absolute paths. <br>
Risk: Vague routing and limited send-confirmation guidance can make messaging outcomes hard to audit. <br>
Mitigation: Record returned message IDs and execution logs, and require operator review for bulk, scheduled, or high-impact sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/whatsapp-master-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline message commands, bash command examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a linked WhatsApp account and channel integration; media workflows may require trusted absolute file paths and optional ffmpeg conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
