## Description: <br>
智能文档处理助手 - 一站式文档处理工具，支持 PDF 转换、智能摘要、多语言翻译、格式转换等功能。自动提取关键信息，生成结构化报告，提升文档处理效率10倍。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and document-processing agents use this skill to extract text from local documents, summarize document content, translate extracted text, and produce Markdown or structured extraction reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says PDF path handling can let a crafted filename run unintended shell commands. <br>
Mitigation: Use only trusted local files, avoid unusual or untrusted filenames, and replace shell interpolation with an argument-array API before broader deployment. <br>
Risk: Generated outputs may contain sensitive copies or excerpts of the original document. <br>
Mitigation: Treat outputs as sensitive document derivatives and review storage, sharing, and retention practices before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/smart-doc-processor) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands] <br>
**Output Format:** [Markdown, plain text, or JSON-style structured data generated from local document inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and pdftotext for the documented PDF processing path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
