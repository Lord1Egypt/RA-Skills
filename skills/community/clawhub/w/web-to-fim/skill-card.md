## Description:

Web To Fim converts web links or local files into structured Markdown and stores the result in an Obsidian vault, Feishu Drive, and Tencent IMA knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to archive web pages, social posts, Feishu wiki pages, and local documents as Markdown while optionally syncing the same material to personal or team knowledge stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected URLs or local files may be written locally and transferred to Feishu or Tencent IMA.

Mitigation: Use --no-feishu and --no-ima unless cloud storage is explicitly required, and avoid processing sensitive or regulated documents.

Risk: Feishu wiki processing may follow content-derived original links.

Mitigation: Review Feishu wiki original links before processing and confirm that each linked source is intended for conversion.

Risk: Dependencies and command-line tools affect fetching and cloud upload behavior.

Mitigation: Pin and review Python dependencies and external tools before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/web-to-fim)
- [Feishu setup guide](references/feishu-setup.md)
- [Feishu block type mapping](references/feishu-blocks.md)
- [Tencent IMA setup guide](references/ima-setup.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, local files, cloud-upload actions, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write converted Markdown locally and upload selected content to Feishu and Tencent IMA when configured.]

## Skill Version(s):

3.7.0 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
