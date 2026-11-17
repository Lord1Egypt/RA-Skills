## Description:

中考短文填空识别与格式化技能，在用户上传题目图片和可选答案图片时，识别并标准化短文填空内容，输出 Word 文档结构或推送到飞书多维表格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[abendeng](https://clawhub.ai/user/abendeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and content operators use this skill to convert Chinese middle-school cloze exam images into clean, reusable question-and-answer formats. It helps preserve paragraph structure, numbering, blanks, punctuation, answer alignment, and Feishu delivery format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images and generated text may contain student information, unpublished exam content, or copyrighted material before Feishu sharing.

Mitigation: Review the source images, generated text, and selected Feishu destination before sending or storing the output.

Risk: OCR errors can misread blanks, numbering, answer words, punctuation, or paragraph breaks in low-quality images.

Mitigation: Check the formatted output against the original images before using it as assessment material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abendeng/skills/zk-cloze-format)
- [中考短文填空格式规范参考](artifact/references/format-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, API Calls, Guidance]

**Output Format:** [OCR-derived formatted text, Markdown or Word document structure, and Feishu table or message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original paragraphs, fill-in numbering, blanks, punctuation, candidate-word order, and answer-number alignment when evidence is legible.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
