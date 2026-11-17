## Description:

将论文保存到 Zotero 文库，请按照 userid:apiKey 的格式配置 ZOTERO_CREDENTIALS 环境变量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifenglei](https://clawhub.ai/user/lifenglei)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and knowledge workers use this skill to save academic paper metadata, optional abstracts, AI-generated summaries, tags, and arXiv PDF attachments into a Zotero library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Zotero API key that can add items and attachments to the user's library.

Mitigation: Use a least-privilege Zotero API key, keep ZOTERO_CREDENTIALS secret, and revoke the key when it is no longer needed.

Risk: Weak arXiv URL handling can trigger unintended network requests and upload the downloaded response to Zotero.

Mitigation: Use only trusted paper URLs and prefer broad deployment after the publisher strengthens arXiv URL validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifenglei/skills/zotero-skills)
- [Zotero](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with command-line examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ZOTERO_CREDENTIALS for Zotero API access and requires uv to run the bundled Python script.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
