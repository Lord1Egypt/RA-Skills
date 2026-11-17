## Description:

用优稿把文章排成公众号图文，浏览真实主题预览，交付可编辑稿件和 HTML。适用于公众号排版、Markdown 转公众号、换主题、导出图文；不改写正文，不自动发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to format an article or existing manuscript for a WeChat Official Account, preview themes, and receive editable text, HTML files, and a link for continued editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content is uploaded to Yougao during preview preparation, and the service's retention practices were not verified.

Mitigation: Submit confidential drafts only when that processing is acceptable; use a dedicated formatting-only API key.

Risk: The API key remains stored locally until disconnected, and revoking it on the website is a separate action.

Mitigation: Disconnect the local integration when it is no longer needed and separately revoke the key on the website.

## Reference(s):

- [Usage and connection guide](references/client.md)
- [API guide](references/api.md)
- [Yougao AI integration documentation](https://yougao.top/ai.md)
- [Yougao API OpenAPI specification](https://yougao.top/api/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Files, HTML, Markdown, Text, Guidance]

**Output Format:** [Editable article text and HTML files, theme previews, and editing links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves article content, images, and tables as supported by the input manuscript; does not rewrite or publish the article.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
