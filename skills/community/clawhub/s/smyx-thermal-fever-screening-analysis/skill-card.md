## Description:

Analyzes multi-person thermal-camera footage for relative skin-temperature differences and suggests follow-up measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Families and organizations can use the skill to review multi-person thermal-camera footage, flag relative surface-temperature differences, and receive a prompt to confirm readings with a thermometer. It provides screening cues rather than medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unexpected identity and credential handling, external data transmission, and behavior beyond the stated screening purpose.

Mitigation: Review identity and credential handling, video processing destinations, and the reported export-only behavior before installation; avoid sending sensitive footage until these behaviors are understood.

Risk: Thermal footage can contain sensitive health and personal information.

Mitigation: Obtain participants' informed consent and protect footage and reports with appropriate access controls and encryption.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-thermal-fever-screening-analysis)

## Skill Output:

**Output Type(s):** [JSON, text, Markdown]

**Output Format:** [Structured analysis results, text alerts, and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-person surface-temperature estimates and group-relative differences; screening cues only, not diagnoses.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
