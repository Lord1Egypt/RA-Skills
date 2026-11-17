## Description:

用优稿把主题和参考资料生成可编辑文章，按目标篇幅预览费用并交付正文。适用于公众号写稿、观点文章、知识科普、内容初稿；链接导入和多图创作可接优稿工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content teams use this skill to turn a topic and optional reference material into an editable article draft. It previews expected cost and returns the draft with a link to continue editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Material submitted for writing is sent to Yougao.

Mitigation: Submit only material appropriate to share with that service.

Risk: Requests have no per-task spending cap by default.

Mitigation: Use a generation-only API key and set a spending limit before running tasks.

Risk: The workflow supports publishing to external destinations.

Mitigation: Publish only to destinations the user has authorized. Disconnect the saved connection when finished and revoke the key on Yougao when it should no longer work.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dunkong/skills/yougao-write)
- [Yougao AI documentation](https://yougao.top/ai.md)
- [Yougao API contract](https://yougao.top/api/v1/openapi.json)
- [API guide](references/api.md)
- [Assistant operating guide](references/client.md)

## Skill Output:

**Output Type(s):** [Article text, Markdown, Files, Guidance]

**Output Format:** [Editable article draft with a file and link for continued editing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The requested topic, references, audience, style, and target length shape the draft; the default target is 1,500 characters.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
