## Description: <br>
将非标准简历文件或文本解析为结构化候选人数据，并可输出到飞书多维表格、Excel 或 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and operations users can use this skill to parse single or batch resumes into standardized candidate records, including contact information, education, work experience, skills, quality scores, and export-ready data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive applicant data and can export it to Feishu Bitable or local files without enough disclosed consent, destination, or retention controls. <br>
Mitigation: Before processing, confirm the destination, fields to be written, authorized viewers, retention expectations, and how candidate data can be deleted or redacted. <br>
Risk: Resume parsing and OCR can misread or overstate candidate fields such as identity, contact details, work history, education, skills, or quality scores. <br>
Mitigation: Review low-confidence or marked fields before storing records, contacting candidates, or making screening decisions. <br>


## Reference(s): <br>
- [简历标准字段定义](references/resume-schema.md) <br>
- [技能名称标准化词典](references/skills-dictionary.md) <br>
- [ClawHub release page](https://clawhub.ai/tujinsama/resume-parser-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, table, file export, and shell command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or write structured candidate records, quality scores, deduplicated batch summaries, Feishu Bitable records, Excel files, CSV files, or JSON files depending on the user request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
