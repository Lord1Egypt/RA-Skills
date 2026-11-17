## Description:

Renames local image files in batches by using a Qwen vision model to identify image type and subject, with commands for single-image description, dry-run plans, applied renames, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiya-code](https://clawhub.ai/user/huiya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect image content and generate concise content-based filenames for local image folders. It is suited to organizing image collections when the user accepts remote vision processing and local filename changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private images and the DashScope API key may be sent to a configured remote vision endpoint.

Mitigation: Use the skill only on image folders you explicitly choose, avoid sensitive images unless remote processing is acceptable, and keep endpoint settings limited to trusted providers.

Risk: Applied rename operations can change local filenames in bulk.

Mitigation: Run a dry run first, review the generated plan file, and keep the rollback file from applied runs until the results are confirmed.

Risk: Public media URL mode can make local images leave the machine or remain publicly reachable.

Mitigation: Do not enable custom base URLs or public media URL mode unless the endpoint and publishing location are trusted and appropriate for the image contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huiya-code/skills/qwen-vision-rename)
- [Publisher profile](https://clawhub.ai/user/huiya-code)
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON plan or rollback file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON plan files and rollback files when renaming images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
