## Description:

智能文档处理助手 - 一站式文档处理工具，支持 PDF 转换、智能摘要、多语言翻译、格式转换等功能。自动提取关键信息，生成结构化报告，提升文档处理效率10倍。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract text from PDFs and text-like documents, generate markdown summaries, and extract common entities such as dates, amounts, emails, and phone numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A maliciously named PDF can trigger command injection through the pdftotext invocation.

Mitigation: Do not process PDFs or filenames from untrusted sources until the command execution is changed to a non-shell API such as execFileSync or spawnSync with argument arrays.

Risk: Processed document contents may be written to console output or to a user-selected file.

Mitigation: Review inputs and output paths before running the skill, especially for confidential documents.

Risk: Some advertised capabilities, including translation and several document formats, are limited or not fully implemented.

Mitigation: Treat unsupported actions and formats as best-effort behavior and verify outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/smart-doc-processor)
- [Source homepage](https://github.com/openclaw/smart-doc-processor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write processed document content to a chosen output file or print it to the console.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
