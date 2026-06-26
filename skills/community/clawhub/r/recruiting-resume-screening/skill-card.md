## Description: <br>
Supports Chinese-language recruiting teams in screening resumes against a job description, ranking candidate batches, identifying red flags, and generating follow-up interview questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soulzhong](https://clawhub.ai/user/soulzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and recruiting operations teams use this skill to evaluate Chinese-language resumes against a JD, triage batches, produce candidate assessment cards, compare rankings, flag risks, and prepare interview follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to look through prior conversations, notes, Downloads, or cache folders for older resumes or job descriptions without a clear approval step. <br>
Mitigation: Provide exact files for each screening task, require confirmation before opening any recovered historical file, and keep each batch in a dedicated temporary directory. <br>
Risk: Resume screening handles sensitive candidate data and can leave extracted text, summaries, or reports on local storage. <br>
Mitigation: Delete local extracted text, summary, index, and report files when the hiring review is complete. <br>


## Reference(s): <br>
- [Recruiting Resume Screening Skill](https://clawhub.ai/soulzhong/recruiting-resume-screening) <br>
- [Five-Dimension Rubric](five-dimension-rubric.md) <br>
- [Red Flags Catalog](red-flags-catalog.md) <br>
- [Output Templates](output-templates.md) <br>
- [Batch Screening](batch-screening.md) <br>
- [PDF Extraction](pdf-extraction.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown reports, ranking tables, interview questions, and optional command snippets for resume text extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local extracted text, summary JSON, and Markdown index artifacts during PDF triage; final reports should omit internal extraction logs unless requested.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
