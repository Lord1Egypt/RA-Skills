## Description:

论文阅读报告生成器，从PDF提取结构化内容并生成全中文阅读报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenbhxmu](https://clawhub.ai/user/chenbhxmu)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking researchers, students, and technical readers use this skill to extract structured content from PDF papers and produce a full Chinese reading report with metadata, summary, methods, figure analysis, critical discussion, and reproduction notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Python packages when PDF parsing dependencies are missing.

Mitigation: Review dependency installation behavior before use and run it in a controlled Python environment with approved package versions when needed.

Risk: The skill can retain extracted paper text in a persistent home-directory cache.

Mitigation: Avoid confidential, unpublished, or proprietary PDFs unless local caching is acceptable, and clear or manage the cache according to local data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenbhxmu/skills/readpaper)
- [analysis_guidelines.md](artifact/references/analysis_guidelines.md)
- [report_template.md](artifact/references/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report plus structured extracted text files and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted paper text and generated reports to local files; may reuse cached extraction results for repeated PDFs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
