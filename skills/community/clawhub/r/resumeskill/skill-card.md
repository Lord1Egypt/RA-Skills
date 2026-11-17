## Description:

Resume Tailor helps Chinese-language job seekers research a target role, tailor a resume from real user-provided experience, and prepare interview materials for that role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingjiu061](https://clawhub.ai/user/qingjiu061)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to turn a resume, target company, target role, and job description into role research, a tailored resume, and interview preparation materials. It is especially oriented toward internship, campus recruiting, and experienced-hire workflows in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content can include sensitive personal data.

Mitigation: Handle uploaded resumes and generated outputs as private user data and avoid sharing them outside the intended job-preparation workflow.

Risk: Tailored resume claims or interview talking points may overstate the user's actual experience.

Mitigation: Review every rewritten claim, metric, and suggested answer against the user's real experience before using the output.

Risk: DOCX rendering depends on the unpinned python-docx package.

Mitigation: Install dependencies in an isolated environment and pin python-docx before repeatable or production use.

Risk: The workflow is designed around Chinese-language job-preparation conventions.

Mitigation: Confirm language, market, and recruiting assumptions before using it for non-Chinese hiring contexts.

## Reference(s):

- [Resume Tailor ClawHub Skill Page](https://clawhub.ai/qingjiu061/skills/resumeskill)
- [Resume Playbook](artifact/resume-playbook.md)
- [Interview Playbook](artifact/interview-playbook.md)
- [Example Resume Input](artifact/sample_resume.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, DOCX resume files, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided resume content, target company, target role, and job description; DOCX generation depends on python-docx.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
