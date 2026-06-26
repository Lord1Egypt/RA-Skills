## Description: <br>
根据需求描述或需求文档生成结构化测试用例，并提供导出、质量评分、测试数据生成、用例评审和增量更新辅助工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newhackerman](https://clawhub.ai/user/newhackerman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to convert requirements text or documents into structured test cases and supporting QA artifacts. It is intended for test-case generation, export, quality review, test-data generation, and incremental update planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local helper scripts read and write requirement, test-case, and export files selected by the user. <br>
Mitigation: Choose input and output paths deliberately and keep backups for important requirement and test-case files. <br>
Risk: Batch review commands can overwrite JSON test-case files when updating priorities or stages. <br>
Mitigation: Run batch updates on a copy or ensure the original JSON file is backed up before using update commands. <br>
Risk: Optional dependencies may be installed to support document parsing and export workflows. <br>
Mitigation: Install optional packages only from trusted package sources and review dependency installation commands before running them. <br>
Risk: Generated test cases may miss coverage or reflect assumptions when requirements are ambiguous or incomplete. <br>
Mitigation: Review generated cases against the source requirements and use the quality scoring, duplicate detection, and incremental review tools before relying on the outputs. <br>


## Reference(s): <br>
- [Default Test Case Prompt](artifact/references/default-prompt.md) <br>
- [Advanced Test Case Prompt](artifact/references/advanced-prompt.md) <br>
- [Prompt Templates](artifact/references/prompt-templates.md) <br>
- [Output Format Examples](artifact/references/format-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables, CSV, JSON, TestLink XML, XMind-compatible JSON, console reports, and local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce generated test cases, quality scores, generated test data, review summaries, export files, and incremental update plans.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
