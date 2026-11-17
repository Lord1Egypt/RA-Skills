## Description:

发送任意本地文件到飞书，自动处理大文件。视频/音频按 20MB 分段（不重新编码），其他文件压缩为 ZIP。支持大文件自动处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingrongx](https://clawhub.ai/user/jingrongx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace operators use this skill to send specified local files to Feishu recipients while automatically preparing files that exceed the 20 MB upload limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads specified local files to Feishu and sends messages as the configured Feishu app.

Mitigation: Use least-privilege Feishu app credentials and invoke the skill only with intended file paths and recipient identifiers.

Risk: The skill can install Python dependencies at runtime.

Mitigation: Preinstall and review dependencies in the target environment instead of relying on automatic runtime installation.

Risk: Large non-media files may be duplicated into ZIP archives or split archives during processing.

Mitigation: Run the skill in a controlled working directory and remove generated archives after confirming delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingrongx/skills/sendfiles-to-feishu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown-compatible text with command examples and runtime status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create media segments or ZIP archives while preparing files for Feishu upload.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
