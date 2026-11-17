## Description:

Reviews Chinese-language resumes against a job description, ranks candidate batches, flags risks, and generates follow-up interview questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soulzhong](https://clawhub.ai/user/soulzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and recruiting operations teams use this skill to screen Chinese-language resumes against a JD, compare candidates in batches, identify evidence-backed concerns, and prepare interview follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searching historical local folders or attachment caches can expose unrelated private resumes or job materials.

Mitigation: Run the skill in a constrained workspace and process only files explicitly provided or confirmed for the current screening task.

Risk: Plaintext resume extraction outputs can retain sensitive candidate data after screening.

Mitigation: Write extraction outputs to a task-specific temporary directory and delete plaintext resume files after use.

Risk: Feedback-driven changes to screening rules can alter future evaluations without review.

Mitigation: Treat proposed rule changes as maintainer-reviewed updates rather than automatic persistent edits.

Risk: PDF parsing dependencies expand the runtime surface for untrusted resume files.

Mitigation: Install PDF dependencies in an isolated, pinned environment and review the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soulzhong/skills/recruiting-resume-screening)
- [Five-Dimension Rubric](artifact/five-dimension-rubric.md)
- [Red Flags Catalog](artifact/red-flags-catalog.md)
- [Output Templates](artifact/output-templates.md)
- [Batch Screening Guidance](artifact/batch-screening.md)
- [PDF Extraction Guidance](artifact/pdf-extraction.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown reports with candidate assessment cards, ranking tables, risk notes, and interview questions; optional JSON and Markdown extraction summaries when processing PDFs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local extracted resume text and summary files during PDF triage; final reports omit extraction logs unless requested.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
