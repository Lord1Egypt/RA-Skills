## Description:

A professional recruitment workflow assistant that evaluates resumes against dynamic requirements and AI proficiency, provides Pros/Cons analysis, and performs Shenzhen-specific market salary benchmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:


## Use Case:

Recruiters and hiring teams use this skill to screen technical candidates, compare resumes to role-specific criteria, benchmark expected salary against Shenzhen market ranges, generate follow-up interview questions, and summarize interview notes.

### Deployment Geography for Use:

Global; hiring benchmarks and salary guidance are Shenzhen-specific.

## Known Risks and Mitigations:

Risk: Sensitive candidate data could be exposed through public document links, HR notifications, or uncontrolled external sharing.

Mitigation: Enable Feishu or messaging tools only after document visibility, recipients, candidate consent, and candidate-data handling rules are explicitly controlled.

Risk: Shell-based command execution with user-controlled file paths can create unsafe execution paths.

Mitigation: Use only trusted local files, avoid attacker-supplied filenames, and replace shell-based execSync usage with argument-safe process execution before production use.

Risk: Resume or interview-note content can be mixed with agent instructions and influence generated hiring outputs.

Mitigation: Keep untrusted resume text separate from agent instructions and review generated evaluations before acting on hiring recommendations.

## Reference(s):

- [Stricter Hiring Criteria](references/hiring-criteria.md)
- [Interview Report Template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and command-line text for resume evaluations, interview questions, interview summaries, HR notifications, and Feishu document creation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include candidate scores, Pros/Cons, salary-fit analysis, interview questions, HR summaries, and public document links when external sharing tools are enabled.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
