## Description:

Reads WeChat Official Account articles, extracts full text and content images, and helps an agent combine them into a reading analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanmingzhao](https://clawhub.ai/user/hanmingzhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they provide an mp.weixin.qq.com article link and need an agent to read the article text, collect content images, and summarize or analyze the combined content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can open supplied article URLs and download images from unrestricted HTTP(S) URLs.

Mitigation: Use the skill only with genuine WeChat article links, and add or review host allowlists before using it on untrusted links.

Risk: The helper script writes predictable files under a caller-selected output path.

Mitigation: Run it in a dedicated empty output folder and inspect the path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanmingzhao/skills/wechat-article-full-reader)
- [Publisher profile](https://clawhub.ai/user/hanmingzhao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with bash and JavaScript snippets; helper script outputs article.json, image files, and a Markdown summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads content images to a caller-selected local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
