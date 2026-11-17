## Description:

Traditional Chinese medicine wellness advisor for constitution assessment, symptom-pattern analysis, food therapy, seasonal wellness, acupoint self-care, and Chinese medicine education.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tix007](https://clawhub.ai/user/tix007)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for Traditional Chinese Medicine-oriented wellness guidance, including intake questions, pattern differentiation, lifestyle suggestions, food therapy, acupoint self-care, and educational discussion of classic formulas. It is positioned as wellness and educational support, not as a substitute for clinical diagnosis or treatment by a licensed professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive health histories persistently.

Mitigation: Require explicit opt-in before storing health information, provide deletion and export controls, and avoid persistent medical memory by default.

Risk: Unsafe user-record handling can expose or mix health records in shared or multi-user environments.

Mitigation: Add strong per-user identity binding, validate user IDs, and apply restrictive file permissions before installation in shared environments.

Risk: Wellness guidance can be mistaken for medical diagnosis or treatment.

Mitigation: Keep clinical boundaries visible, avoid prescriptions or drug dosing, and direct users with urgent or serious symptoms to licensed medical care.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tix007/skills/tcm-wellness)
- [Classic prescriptions reference](references/classic_prescriptions.md)
- [Acupoints reference](references/acupoints.md)
- [Syndrome differentiation reference](references/syndrome_differ.md)
- [Seasonal diet reference](references/seasonal_diet.md)
- [Memory system reference](references/memory_system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Files]

**Output Format:** [Markdown wellness guidance with structured sections; optional local memory files created by bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store user health histories persistently when its memory workflow is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
