## Description:

Analyzes adolescents' camera footage while they use phones or gaming devices to estimate screen-looking posture and cumulative viewing time, then produces a structured report with gentle reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and guardians use it to review adolescents' screen-use posture and viewing time and receive gentle family reminders. The reports are observational and are not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says account registration, identity handling, and token storage are not adequately explained.

Mitigation: Wait for the publisher to explain why registration is needed, what identity and token data is stored, and how it is protected and retained.

Risk: The security evidence flags remote transmission and privacy-sensitive processing of adolescents' video.

Mitigation: Use only after the publisher explains video processing, consent, and export-only safeguards; obtain informed consent from both the guardian and adolescent before submitting footage.

Risk: The security evidence flags broad activation behavior.

Mitigation: Require explicit caregiver intent before processing footage and review the activation triggers before enabling the skill.

Risk: The security scan is partial and could not resolve a local reference, so its evidence is incomplete.

Mitigation: Treat the scan as provisional and request a complete review and publisher clarification before installation.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-teen-screen-addiction-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown report listings, with report export links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes posture and duration summaries, reminder levels, and suggested actions; reports are observational, not medical diagnoses.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
