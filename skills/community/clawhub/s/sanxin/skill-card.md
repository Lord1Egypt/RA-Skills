## Description: <br>
智能申报表填写工具。将申报报告内容智能填入申请表对应位置，保持原文档格式，新内容格式统一。适用于各类 Word 表格申请表自动填写。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanqing203](https://clawhub.ai/user/fanqing203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who prepare Word-based application forms can use this skill to transfer report content into matching form sections while preserving the original table layout and applying consistent formatting to inserted text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit and save local Word documents through pywin32 automation. <br>
Mitigation: Use copies of blank forms, choose a distinct output path, and manually review the generated document before relying on it. <br>
Risk: Word automation depends on a compatible local Windows Office or WPS environment and may fail when files, table indexes, or ranges do not match the expected form structure. <br>
Mitigation: Confirm the document paths, table structure, and generated formatting on a small test form before using the output in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanqing203/sanxin) <br>
- [Publisher profile](https://clawhub.ai/user/fanqing203) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python usage examples and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and Python-driven Word document updates; users choose source, form, output path, table index, and content mapping.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
