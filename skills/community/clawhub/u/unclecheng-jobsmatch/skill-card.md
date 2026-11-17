## Description:

Matches uploaded resumes to job openings, investigates employer background signals, evaluates role fit, and produces structured job assessment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to parse resumes, search for matching openings across recruitment and employer sources, check employer and job risk signals, and produce a job assessment report with links and application guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsed resumes can contain personal contact details, employment history, education history, and other sensitive personal data; the security summary notes that full parsed resume text is saved to a predictable local plaintext file.

Mitigation: Run the skill only in a private working directory, avoid shared folders, redact contact details before web search or AI analysis, and delete resume_parsed_result.json after use.

Risk: Optional parser and OCR dependencies are described but not pinned in the artifact.

Mitigation: Verify dependency sources and pin versions before installing optional packages for resume parsing or OCR.

Risk: Job listings, company registry details, and employer reputation signals may be incomplete, stale, or misleading.

Mitigation: Verify recommendations against official recruitment pages, authoritative company registry sources, and current public records before acting on the report.

## Reference(s):

- [Recruitment sites](references/recruitment_sites.md)
- [Enterprise inquiry sources](references/enterprise_inquiry_sources.md)
- [Assessment report template](assets/assessment_report_template.md)
- [Tesseract OCR installation reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON parsed resume data, generated search queries, and optional PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files such as resume_parsed_result.json and PDF exports when scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
