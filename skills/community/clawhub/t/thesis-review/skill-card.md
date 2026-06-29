## Description: <br>
Generates structured master's thesis review comments from user-provided thesis text or PDFs and outputs the review as Markdown and a formatted Word document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, academic reviewers, and educators use this skill to generate structured, actionable thesis review reports from thesis text or PDFs. It extracts core thesis details, reviews major sections, identifies strengths and weaknesses, suggests revisions, and produces a final defense recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a formatted .docx review report in the working directory. <br>
Mitigation: Confirm the intended output filename and location before use, and review the generated document before sharing it. <br>
Risk: The skill is specialized for thesis and dissertation review and may be inappropriate for generic review requests. <br>
Mitigation: Use it only when thesis-review behavior is intended and provide sufficient thesis text or a PDF for grounded feedback. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/thesis-review) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown review report plus a formatted Word (.docx) document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Word document is written to the working directory using the skill's review-report naming convention.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
