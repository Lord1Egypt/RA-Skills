## Description: <br>
SciSurvey guides an agent through Sciverse-based academic literature search, screening, evidence mapping, and structured survey or review writing with Markdown, LaTeX, DOCX, or PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweixiaogui10](https://clawhub.ai/user/liweixiaogui10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use SciSurvey to produce systematic surveys, systematic reviews, scoping reviews, or narrative reviews for a chosen research topic using bilingual keyword planning, Sciverse search, evidence extraction, and citation integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested DOCX, PDF, or LaTeX output may create files in the working directory and may invoke local conversion tools if available. <br>
Mitigation: Use Markdown for the lowest-side-effect path, or run the skill in a disposable workspace and review generated files before relying on them. <br>
Risk: A generated literature review may include unsupported or misleading claims if evidence extraction or citation mapping is incomplete. <br>
Mitigation: Review the evidence mappings, citation list, and generated claims before publication or operational use. <br>


## Reference(s): <br>
- [Scisurvey on ClawHub](https://clawhub.ai/liweixiaogui10/scisurvey) <br>
- [SciSurvey source homepage](https://github.com/liweixiaogui10/Systematic_Survey_skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown, LaTeX, DOCX, or PDF review artifacts with structured citations and evidence notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create files in the working directory when DOCX, PDF, or LaTeX output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
