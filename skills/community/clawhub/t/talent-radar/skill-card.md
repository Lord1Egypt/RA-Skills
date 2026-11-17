## Description:

Talent Radar analyzes Chinese resumes against a specific job description to produce candidate-job fit reports, gap diagnoses, optimization advice, and ranked recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taotao52](https://clawhub.ai/user/taotao52)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and job seekers use this skill to compare a Chinese-language resume with a specified role or job description, understand match strengths and gaps, and generate advisory hiring or job-search reports.

### Deployment Geography for Use:

Global, with primary applicability to Chinese-language recruiting contexts.

## Known Risks and Mitigations:

Risk: The skill processes sensitive resume and job-description data.

Mitigation: Obtain candidate consent, minimize input data, keep processing local where possible, and delete resume and job-description data after analysis.

Risk: Generated match scores or recommendations could be over-relied on in hiring decisions.

Mitigation: Treat reports as advisory, require human review, and combine results with interviews and other appropriate evaluation methods.

Risk: Some bundled reference material contains outdated fairness guidance about school prestige or stability scoring.

Mitigation: Use the current release behavior that excludes school name from education scoring and keeps culture fit out of the total score; fix or ignore outdated references before operational use.

Risk: Optional PDF extraction guidance may require installing third-party packages.

Mitigation: Use an isolated, pinned Python environment and review PDF extraction dependencies before processing candidate files.

## Reference(s):

- [Talent Radar ClawHub Skill Page](https://clawhub.ai/taotao52/skills/talent-radar)
- [README](artifact/references/README.md)
- [Matching Algorithm](artifact/references/matching_algorithm.md)
- [Skill Matrix](artifact/references/skill_matrix.md)
- [PDF Extraction Guide](artifact/references/pdf_extraction_guide.md)
- [Windows PDF Extraction Guide](artifact/references/windows_pdf_extraction.md)
- [PCB Industry Analysis](artifact/references/pcb_industry_analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with scoring summaries, dimension-level analysis, gap diagnosis, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed by a human before hiring or job-search decisions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
