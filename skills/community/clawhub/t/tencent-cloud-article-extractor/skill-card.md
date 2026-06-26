## Description: <br>
Extracts public Tencent Cloud Developer Community articles and converts their title, author, publication time, body content, links, code blocks, lists, quotes, and image references into Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeteenager](https://clawhub.ai/user/codeteenager) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agents use this skill to fetch public Tencent Cloud Developer Community articles and save or return them as structured Markdown for review, reuse, or documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs network access to fetch public Tencent Cloud developer articles. <br>
Mitigation: Use it only with public Tencent Cloud developer article URLs that are appropriate for the agent to access. <br>
Risk: A user-provided output path can be overwritten when saving Markdown. <br>
Mitigation: Choose the output filename carefully and review the destination before execution. <br>
Risk: Private, deleted, login-gated, or structurally changed article pages may fail to extract. <br>
Mitigation: Confirm the article is publicly accessible and check the source page when extraction returns an error or empty content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeteenager/tencent-cloud-article-extractor) <br>
- [Tencent Cloud Developer Community article example](https://cloud.tencent.com/developer/article/2636150) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands] <br>
**Output Format:** [Markdown printed to stdout or written to a user-provided file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes article metadata, source URL, optional word count and reading time, and original image URLs without downloading images.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
