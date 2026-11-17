## Description:

Exports a selected WeChat contact's files, full-size images, and videos from a date range on macOS, decrypts and converts images, and checks the local archive for missing items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized WeChat users and project archivists use this skill to gather a contact's documents, original images, and videos from a specified period into a local archive for handover or knowledge-base preparation. It supports macOS and WeChat desktop 4.x.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private chat content may be exported without appropriate authorization or shared beyond its intended audience.

Mitigation: Export only accounts and conversations you own or are authorized to handle; obtain the data owner's approval before uploading archives to a knowledge base.

Risk: Desktop automation may capture the wrong contact or period when the selected session and boundaries are not confirmed.

Mitigation: Before execution, confirm the account, contact or session hash, target month, and destination directory; review the resulting archive.

Risk: Decryption material or exported archives may be exposed through command output or shared machines.

Mitigation: Avoid shared machines, keep CODE, WXID, derived keys, and archives confidential, and remove or redact key-printing output.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/wechat-chat-export-mac)
- [Export procedure](references/sop.md)
- [Decryption parameter guide](references/code-finding.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and local exported files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-organized documents, images, and videos with a completeness check.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
