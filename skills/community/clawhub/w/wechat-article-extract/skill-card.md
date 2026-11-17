## Description:

Extract public WeChat Official Account articles from mp.weixin.qq.com links or saved HTML into clean Markdown or structured JSON, including title, account name, publish time, article text, tables, image markers, and image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joannaxing](https://clawhub.ai/user/joannaxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content operations users use this skill to extract public WeChat Official Account articles from a public article URL or saved HTML into Markdown archives or JSON records for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional image download mode can fetch arbitrary image URLs from article HTML and save unbounded responses.

Mitigation: Use --download-images only with trusted public WeChat articles or saved HTML, review extracted image URLs before downloading, and run downloads in a disposable output directory until host, redirect, and response size restrictions are added.

Risk: Extracted article content may include third-party material that the user does not have rights to republish.

Mitigation: Use extracted content for private analysis, summaries, transformations, or authorized archives; do not republish full articles unless the user has the necessary rights.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joannaxing/skills/wechat-article-extract)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON, optionally written to stdout or a user-provided file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves image positions with markers; local image downloads are optional and should be requested explicitly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
