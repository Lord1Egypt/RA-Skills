## Description:

Helps an agent organize WeChat Channels, Douyin, Xiaohongshu, public-account articles, and local files into a Tencent Docs knowledge base by downloading or capturing content, uploading it, and adding index records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to save social-media links, articles, videos, and local documents into a Tencent Docs-backed personal knowledge base with searchable index rows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded or local content may be uploaded into an unintended Tencent Docs space or index.

Mitigation: Review and replace the Tencent Docs space, index file, and sheet IDs before use; avoid uploading private files until the destination is confirmed.

Risk: Tencent Docs authorization can grant access to cloud document storage and sheet operations.

Mitigation: Install the Tencent Docs dependency only from a trusted, reviewed source, check the granted authorization scopes, and know how to revoke access.

Risk: The release artifact describes parser and upload scripts that are not present in the submitted artifact.

Mitigation: Treat missing scripts as a blocker unless they are supplied from a verified package version before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/wechat-knowledge)
- [Tencent Docs](https://docs.qq.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON parser outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded or converted local files, upload content to Tencent Docs, and add knowledge-base index records.]

## Skill Version(s):

2.2.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
