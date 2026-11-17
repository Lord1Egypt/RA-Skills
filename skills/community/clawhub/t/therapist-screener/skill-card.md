## Description:

Therapist Screener helps users assess therapist qualifications, training, experience, ethics, and professional focus to support therapist selection across Chinese and English contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to screen therapist profiles and generate structured competence reports with red-flag checks and next-step questions. The skill supports decision-making only and does not provide therapy, diagnose conditions, guarantee outcomes, or replace the user's final choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A therapist may practice in a jurisdiction that does not match the conversation language, leading to the wrong qualification checklist.

Mitigation: Ask for the therapist's practice location or licensing jurisdiction before relying on the evaluation.

Risk: Users may over-treat a screening report as medical, legal, licensing, or treatment advice.

Mitigation: Frame the report as decision-support only and preserve the skill's disclaimers that it does not diagnose, provide therapy, guarantee outcomes, or replace user judgment.

Risk: Profile URLs may be incomplete or hard to parse, which can weaken the evaluation.

Mitigation: Prefer pasted profile text when possible and verify credentials through official licensing or qualification sources.

## Reference(s):

- [China Therapist Qualification Reference](references/china-qualifications.md)
- [Overseas Mental Health Professional Qualifications](references/overseas-qualifications.md)
- [ClawHub Skill Page](https://clawhub.ai/zhuqingsonga/skills/therapist-screener)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured evaluation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language-aware Chinese or English report with qualification review, red-flag warnings, next-step questions, and disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
