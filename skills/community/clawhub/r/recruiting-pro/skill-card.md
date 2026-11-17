## Description:

Recruiting supports hiring workflows by creating job descriptions, screening criteria, interview materials, pipeline updates, and draft communications while keeping candidate data local and requiring human decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Hiring managers, recruiters, and recruiting coordinators use this skill to structure job descriptions, candidate screening, interview preparation, pipeline tracking, and candidate communications while retaining human review over decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate personal information and evaluative ratings may be stored on disk.

Mitigation: Use privacy controls, restrict access to local recruiting records, avoid sensitive personal data, and maintain a retention and deletion process for candidate records.

Risk: Screening and pipeline outputs may influence hiring decisions even though the skill states it does not make decisions.

Mitigation: Use outputs only as process support, require human review, and document job-related criteria before taking interview, rejection, offer, or hiring actions.

Risk: Structured hiring support can still reflect or reinforce bias.

Mitigation: Apply consistent criteria and interview questions across candidates, keep evidence-based notes, and retain human oversight at every decision point.

## Reference(s):

- [Job Description Creation](references/job-descriptions.md)
- [Resume Screening](references/resume-screening.md)
- [Pipeline Tracking](references/pipeline-tracking.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and plain text responses with inline shell commands; scripts persist local JSON records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local recruiting records are written under ~/.openclaw/workspace/memory/recruiting when scripts are used.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
