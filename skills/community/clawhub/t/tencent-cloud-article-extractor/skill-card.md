## Description:

Extracts public Tencent Cloud Developer Community articles and converts article metadata and body content into Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeteenager](https://clawhub.ai/user/codeteenager)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to fetch public Tencent Cloud Developer Community articles, extract the title, author, publish time, body content, images, links, lists, quotes, and code blocks, and produce Markdown for review, reuse, or archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extractor fetches Tencent Cloud web pages and only works for publicly accessible articles in the expected URL format.

Mitigation: Use it only with intended public Tencent Cloud Developer article URLs and review errors when articles require login, are deleted, or the page structure changes.

Risk: When an output path is provided, the script writes Markdown to that user-specified location.

Mitigation: Review the output path before execution and avoid paths that could overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeteenager/skills/tencent-cloud-article-extractor)
- [Publisher profile](https://clawhub.ai/user/codeteenager)
- [Tencent Cloud Developer article URL format](https://cloud.tencent.com/developer/article/2636150)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown written to stdout or to a user-provided file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes extracted article metadata, source URL, optional article statistics, and converted body content; images remain referenced by their original URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
