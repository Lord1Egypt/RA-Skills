## Description: <br>
Generate ATS-optimized resumes and tailored cover letters matched to specific job descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanwyngaard](https://clawhub.ai/user/seanwyngaard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers, career coaches, and recruiting-support teams use this skill to create or tailor resumes, CVs, cover letters, and keyword match reports for specific job descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume, profile, and generated career documents can contain sensitive personal information. <br>
Mitigation: Use only files intended for the agent to read, avoid unnecessary sensitive details, and review generated files before sharing, syncing, or committing them. <br>
Risk: Generated resume or cover letter content may overstate experience or include inaccurate claims. <br>
Mitigation: Review the generated documents and keyword match report for factual accuracy before submitting them to an employer. <br>
Risk: Optional LaTeX output may be compiled outside the skill with unsafe compiler settings. <br>
Mitigation: Compile optional .tex output with shell escape disabled. <br>
Risk: Bash-capable tool access can run commands if approved during use. <br>
Mitigation: Do not approve Bash commands unless they were specifically requested and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seanwyngaard/resume-and-cover-letter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and generated career document files, with optional HTML and LaTeX outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include resume, cover letter, keyword match report, customization notes, and print-ready document variants.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
