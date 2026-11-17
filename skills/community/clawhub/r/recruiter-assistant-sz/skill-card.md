## Description:

A professional recruitment workflow assistant that evaluates resumes against dynamic requirements and AI proficiency, provides critical pros and cons analysis, and performs Shenzhen-specific market salary benchmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:


## Use Case:

Recruiting and hiring teams use this skill to screen technical candidates for Shenzhen-market roles, compare resumes against senior Go and PHP criteria, benchmark salary expectations, and prepare interview questions or summaries.

### Deployment Geography for Use:

China (Shenzhen market)

## Known Risks and Mitigations:

Risk: Sensitive resume and interview data may be exposed through broad local file access and raw console output.

Mitigation: Use the skill only on trusted files in a contained workspace, redact or minimize resume output, and avoid retaining unnecessary candidate data.

Risk: Unsafe shell command construction around filenames and paths may cause unintended command execution or file handling behavior.

Mitigation: Update scripts to avoid shell command construction, use safe argument passing, and reject attacker-supplied filenames or paths.

Risk: High-scoring candidate summaries may be sent to HR without sufficient confirmation.

Mitigation: Require manual approval before saving reports or messaging HR, especially when candidate data or recommendations are included.

Risk: Resume, PDF, or interview-note content can be mixed with agent instructions during evaluation.

Mitigation: Treat document content as untrusted data and isolate it from agent instructions before summarization, scoring, or question generation.

## Reference(s):

- [Stricter Hiring Criteria (Shenzhen 2026)](references/hiring-criteria.md)
- [Interview Evaluation Report Template](assets/report-template.md)
- [ClawHub skill page](https://clawhub.ai/gakkiismywife/skills/recruiter-assistant-sz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown and console text with candidate scores, pros and cons, recommendations, salary-fit notes, interview questions, and interview summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one evaluation document per candidate and candidate summaries for HR review.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
