## Description:

Guides users in organizing locally saved WeChat attachments by contact, decrypting supported image files, and preparing local or Tencent ima knowledge-base archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

People with authorized access to locally saved WeChat attachments use this skill to sort documents, images, and videos by contact and prepare them for local archives or an ima knowledge base. It does not export chat messages or access unopened or expired attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default organization workflow can move original WeChat attachments.

Mitigation: Use --copy unless removing originals from WeChat-managed storage is intentional.

Risk: Private attachments and decryption material may be exposed through archives or sharing.

Mitigation: Process only authorized attachments and keep secret_hit.json local and out of synced or shared folders.

Risk: Cloud upload may disclose private material and API credentials.

Mitigation: Review files before ima upload and rotate the ima API key after use.

Risk: The bundled ima uploader omits the actual COS file-upload step.

Mitigation: Do not treat it as a complete backup until COS upload is implemented and verified.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/wechat-archive-to-ima)
- [WeChat PC attachment paths](artifact/references/wechat_paths.md)
- [WeChat image decryption reference](artifact/references/dat_decryption.md)
- [Tencent ima API reference](artifact/references/ima_api.md)
- [Tencent ima API setup](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local archive scripts can produce organized files, indexes, and summaries.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
