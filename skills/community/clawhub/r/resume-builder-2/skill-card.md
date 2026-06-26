## Description: <br>
Build, rewrite, and tailor premium white-collar resumes from real candidate information, then render the final resume to PDF with Typst. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hilaraklesantosw-art](https://clawhub.ai/user/hilaraklesantosw-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals and career-support agents use this skill to build, rewrite, or tailor factual white-collar resumes from real candidate information and render a polished PDF resume with Typst. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume and job-description inputs can contain personal or sensitive career information. <br>
Mitigation: Use the skill only in an agent workflow where that content is appropriate to process, and review or delete generated JSON, Typst, and PDF files when finished. <br>
Risk: PDF rendering depends on local Typst tooling and the resume template being trusted and available. <br>
Mitigation: Confirm the local typst binary and required template before relying on the generated PDF output. <br>
Risk: Resume claims can become misleading if the agent adds unsupported facts or metrics. <br>
Mitigation: Review generated resume content against the candidate's real experience and keep unsupported gaps explicit. <br>


## Reference(s): <br>
- [Resume Schema](references/resume-schema.md) <br>
- [Role Writing Guidelines](references/role-writing-guidelines.md) <br>
- [Project Homepage](https://github.com/hilaraklesantosw-art/skills) <br>
- [ClawHub Release Page](https://clawhub.ai/hilaraklesantosw-art/resume-builder-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with structured resume content, JSON input, Typst source, and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and typst; completion depends on successful PDF compilation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
