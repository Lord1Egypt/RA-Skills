## Description: <br>
论文阅读报告生成器，从PDF提取结构化内容并生成全中文阅读报告。触发关键词：/readpaper、论文阅读、论文分析、PDF分析 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenbhxmu](https://clawhub.ai/user/chenbhxmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to extract structured content from academic PDFs and produce Chinese paper-reading reports covering metadata, abstracts, methods, figures, findings, critique, and reproducibility notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically installs PDF parsing packages during normal use. <br>
Mitigation: Run it in a virtual environment or sandbox and review package installation behavior before use. <br>
Risk: Extracted paper content is saved in the workspace and cached under ~/.workbuddy/cache/readpaper. <br>
Mitigation: Inspect and delete generated reports, extracted-content files, and cache entries when processing sensitive papers. <br>
Risk: PDF text extraction and AI-generated summaries can be incomplete or misleading. <br>
Mitigation: Review generated reports against the source paper before relying on conclusions or reproduction guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenbhxmu/readpaper) <br>
- [Analysis Guidelines](references/analysis_guidelines.md) <br>
- [Report Template](references/report_template.md) <br>
- [Usage Examples](EXAMPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown reports and structured text extraction files, with command-line usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local extracted-content files and Chinese paper-reading reports; caches extracted paper content locally when caching is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
