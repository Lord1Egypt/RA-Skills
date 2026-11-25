## Description:

Analyzes fixed-camera images or videos to estimate adolescents’ phone or gaming screen-use posture and duration, then returns activity summaries and gentle reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers can review fixed-camera footage for estimated screen-use posture and duration, while developers can integrate the analysis into family monitoring tools. Results are behavioral estimates, not medical diagnoses, and use involving minors requires informed consent from both the guardian and the adolescent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unclear account and credential handling and potentially broad remote processing of sensitive video, including footage of minors.

Mitigation: Before use, verify where footage is sent, how credentials are handled, and what retention and access controls apply; obtain informed consent from both the guardian and adolescent and avoid uploading footage until these checks are complete.

Risk: Posture estimates may mistake ordinary study activities for screen use or be treated as a diagnosis.

Mitigation: Review results in context, keep reminders respectful, and use the output only as a non-diagnostic estimate rather than a basis for punitive or high-stakes decisions.

## Reference(s):

- [API interface and input guidance](references/api_doc.md)
- [Skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-teen-screen-addiction-detection-analysis)
- [Skill introduction video](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured analysis results with activity summaries, reminders, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual behavior and duration estimates; not a medical diagnosis.]

## Skill Version(s):

1.0.11 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
