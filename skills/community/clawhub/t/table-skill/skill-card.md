## Description: <br>
Provides table preprocessing and analysis workflows for splitting, cleaning, merging headers, describing datasets, and producing controlled exploratory analysis outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutesxy](https://clawhub.ai/user/cutesxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data operations teams use this skill to preprocess CSV and Excel tables, generate table descriptions, and guide controlled exploratory data analysis and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-assisted features can send table headers, schema, samples, or other table content to an OpenAI-compatible provider. <br>
Mitigation: Use only datasets authorized for the configured provider, minimize shared fields and rows, and disable LLM-assisted paths for confidential or regulated spreadsheets. <br>
Risk: Generated reports can expose raw samples or sensitive fields. <br>
Mitigation: Review report outputs before sharing, prefer aggregate statistics, and redact or anonymize identifiers and sensitive columns. <br>
Risk: Exploratory analysis may involve agent-generated Python code and generated report assets. <br>
Mitigation: Keep generated code limited to the requested data analysis task, review code before execution, and avoid report modes that load CDN scripts when that is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cutesxy/table-skill) <br>
- [Skill Instructions](SKILL.md) <br>
- [Table Processing Documentation](script/docs/README.md) <br>
- [Split Table Documentation](script/docs/01_split_table_skill.md) <br>
- [Clean Table Documentation](script/docs/02_clean_table_skill.md) <br>
- [Describe Table Documentation](script/docs/03_describe_table_skill.md) <br>
- [Merge Header Documentation](script/docs/04_merge_header_skill.md) <br>
- [EDA and Visualization Documentation](script/docs/05_eda_mining_skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python commands and generated CSV, JSON, chart, and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use OPENAI_API_KEY for LLM-assisted header merging, summaries, and analysis; local-only modes are available for sensitive data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
