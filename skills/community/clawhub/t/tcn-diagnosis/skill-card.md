## Description:

Provides Traditional Chinese Medicine consultation support for symptom intake, pattern differentiation, formula references, and dietary wellness guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

External users seeking educational Traditional Chinese Medicine guidance use the skill to collect symptoms, explore possible TCM patterns, and receive wellness, food therapy, and formula-reference suggestions with safety warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat TCM pattern analysis, formula references, or wellness suggestions as medical diagnosis or treatment.

Mitigation: Present outputs as educational guidance, avoid formal diagnosis or prescriptions, and direct users to licensed clinicians for care decisions.

Risk: Urgent symptoms or special populations may require professional medical care instead of agent guidance.

Mitigation: Stop TCM guidance for acute warning signs or high-risk populations and advise immediate medical attention or clinician consultation.

Risk: Consultation-derived health information could be retained in persistent memory without clear user consent.

Mitigation: Keep consultation data ephemeral unless the user explicitly opts in to retention, and avoid storing sensitive medical details by default.

Risk: The artifact describes an always-active TCM role, which could apply health guidance outside the user's intended scope.

Mitigation: Use the skill only when the user explicitly asks for TCM, wellness, formula-reference, or related educational guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huamu668/skills/tcn-diagnosis)
- [README](README.md)
- [Skill Overview](SKILL.md)
- [Agent Team Configuration](operations/AGENTS.md)
- [Safety Protocol](operations/HEARTBEAT.md)
- [TCM Role Guide](operations/ROLE-TCM.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown prose with structured consultation sections and inline shell commands for startup or verification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health-related outputs should remain educational and include safety disclaimers; scripts print startup and verification status.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
