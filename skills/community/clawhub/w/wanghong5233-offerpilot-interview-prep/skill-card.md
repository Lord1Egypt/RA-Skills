## Description:

Generate interview question bank and answer strategy from JD and company intel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and interview coaches use this skill to generate likely interview focus areas, question banks, answer tips, and concise storylines from a job description, role, company name, or recent job ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form job or company data could be unsafely interpolated into shell commands when using the documented curl workflow.

Mitigation: Use safe structured HTTP or JSON serialization, review generated commands before execution, and avoid direct shell-string substitution.

Risk: The skill sends interview-prep inputs to a local service at 127.0.0.1:8010.

Mitigation: Install and use the skill only when that localhost service is trusted, available, and has acceptable handling and retention practices for job descriptions and company material.

Risk: Interview focus areas and answer strategies are probabilistic guidance, not guarantees about an employer's interview process.

Mitigation: Present recommendations as likely focus areas with confidence, and avoid claiming interview certainty.

## Reference(s):

- [Interview Prep Skill Page](https://clawhub.ai/wanghong5233/skills/wanghong5233-offerpilot-interview-prep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured interview-prep sections and optional curl command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents likely focus, key storylines, questions, intents, and answer tips without claiming certainty.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
