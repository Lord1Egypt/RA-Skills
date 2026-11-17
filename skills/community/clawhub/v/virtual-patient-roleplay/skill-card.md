## Description:

Simulate standardized patient encounters for medical training, supporting OSCE-style history-taking practice, communication skills rehearsal, and educational debriefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, learners, and training facilitators use this skill for standardized-patient interview practice, OSCE-style rehearsal, communication feedback, and debrief preparation. It is limited to educational simulation and is not for real clinical triage, diagnosis, treatment selection, or emergency guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training simulation output could be mistaken for real clinical advice or emergency guidance.

Mitigation: Treat outputs strictly as educational simulation; stop requests for real diagnosis, treatment, triage, or emergency advice and direct users to appropriate clinical channels.

Risk: The packaged simulator supports only a small fixed set of scenarios and can fail or reject unsupported cases.

Mitigation: Use manual roleplay scaffolds for unsupported scenarios and clearly state assumptions, limits, and faculty review needs.

Risk: The release guidance flags requirements.txt entries for review before installation.

Mitigation: Install only in an isolated environment or remove unnecessary requirements before deployment.

## Reference(s):

- [Virtual Patient Roleplay References](references/references.md)
- [Audit Reference](references/audit-reference.md)
- [Virtual Patient Roleplay - References](references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/virtual-patient-roleplay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with simulated patient responses, structured debrief guidance, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes educational-use limits and manual fallback guidance; packaged scenarios are chest_pain, headache, and abdominal_pain.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
