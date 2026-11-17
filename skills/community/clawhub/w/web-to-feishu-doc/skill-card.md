## Description:

将任意网页链接转为结构化 Markdown 并保存到飞书云文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn user-provided web links or local files into structured Markdown and save the result as Feishu cloud documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided web pages or local files may be uploaded into Feishu, including private or sensitive content.

Mitigation: Use the skill only with content that is acceptable to store in the configured Feishu workspace, and review private URLs or local files before upload.

Risk: Broad default Feishu destinations can place documents in an unintended space or folder.

Mitigation: Review FEISHU_SPACE_ID and FEISHU_TARGET_FOLDER before use and prefer explicit destination confirmation before each upload.

Risk: Automatic content classification can select an incorrect knowledge base or category.

Mitigation: Require user confirmation when the destination is uncertain or when the content has privacy, business, or access-control implications.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown document content, Feishu document creation actions, and concise user-facing status or confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu credentials from environment variables and may use configured default Feishu space and folder destinations.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
