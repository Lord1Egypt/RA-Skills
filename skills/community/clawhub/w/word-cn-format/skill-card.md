## Description: <br>
提供Word文档中文格式标准化功能，统一标题、正文、图片和图表格式，确保符合中文排版规范。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmtea1981](https://clawhub.ai/user/lmtea1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to standardize Chinese Word documents for business documents, academic papers, reports, and other documents that need consistent typography and layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally changes Word document formatting and layout, which may alter important documents in ways the user did not expect. <br>
Mitigation: Keep a backup of the original document and review the formatted output before using it as the final version. <br>
Risk: If no output path is supplied, the script chooses its own timestamped output filename, which may be less predictable in automated workflows. <br>
Mitigation: Provide an explicit output filename when predictable file paths are required. <br>
Risk: The skill depends on python-docx from the Python package ecosystem. <br>
Mitigation: Install dependencies only from a trusted Python environment. <br>


## Reference(s): <br>
- [Format Standard](references/format_standard.md) <br>
- [Usage Guide](references/usage_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lmtea1981/word-cn-format) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and a generated .docx file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats a user-selected .docx document locally and writes a separate output file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
