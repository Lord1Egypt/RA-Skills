## Description:

AI Tutor provides Chinese-language tutoring for primary, middle, and high school students across core subjects, with personalized explanations, guided questions, study planning, and multimodal teaching support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[armholder](https://clawhub.ai/user/armholder)

### License/Terms of Use:

MIT-0

## Use Case:

Students, parents, and educators use this skill for homework help, concept explanations, guided practice, and study planning across Chinese primary, middle, and high school curricula. The skill adapts explanations to student level and asks follow-up questions to check understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create and retain local student profiles, learning history, weak points, and progress records.

Mitigation: Use explicit consent before entering real student data, minimize personal information, define retention and deletion rules, and restrict file permissions.

Risk: The profile storage design uses local files and student IDs, which can expose records or mix profiles if not reviewed before use.

Mitigation: Review the storage location before installation, validate student IDs, isolate the runtime workspace, and avoid using sensitive identifiers.

## Reference(s):

- [AI Tutor ClawHub Skill Page](https://clawhub.ai/armholder/skills/tutor-ai)
- [armholder Publisher Profile](https://clawhub.ai/user/armholder)
- [Skill Definition](artifact/SKILL.md)
- [Tutor Prompt](artifact/prompts/tutor_main.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style tutoring responses with structured explanations, check questions, practice exercises, and study guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request student grade, subject, current performance, and learning goal before tailoring the tutoring response.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
