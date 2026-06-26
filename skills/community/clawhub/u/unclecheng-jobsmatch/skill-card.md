## Description: <br>
This skill parses uploaded resumes, searches public job sources, checks company background signals, and produces job-match assessment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to turn a resume into matched role suggestions, company background checks, risk notes, and structured application guidance. <br>

### Deployment Geography for Use: <br>
China-focused, with use elsewhere dependent on available recruitment and company-information sources. <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes resume content and may use job-relevant personal details during web searches. <br>
Mitigation: Share only necessary resume details, run it in a controlled workspace, and delete generated parsed-result or report files after use. <br>
Risk: Job listings and company background data from public sources may be incomplete, outdated, or misleading. <br>
Mitigation: Verify application links, company records, and risk judgments against official or primary sources before applying or making decisions. <br>


## Reference(s): <br>
- [Recruitment Sites](references/recruitment_sites.md) <br>
- [Enterprise Inquiry Sources](references/enterprise_inquiry_sources.md) <br>
- [Assessment Report Template](assets/assessment_report_template.md) <br>
- [Tesseract OCR Setup](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, structured JSON extracts, and optional PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include job links, match scores, company-risk notes, and application guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
