## Description:

Develop refined aesthetic judgment by learning from human feedback, asking genuine questions about quality, and calibrating over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent calibrate aesthetic judgments from human feedback across design, writing, and creative generation tasks. It guides the agent to ask specific feedback questions, record corrections, extract taste patterns, and adjust confidence by domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps open-ended local memory of user feedback that may include sensitive personal preferences, credentials, or operational instructions.

Mitigation: Avoid providing sensitive details as feedback while the skill is active, and periodically inspect or delete stored taste files under ~/taste/.

Risk: Long-lived taste notes may be reused in future sessions after preferences change or without enough user control.

Mitigation: Review, update, or reset correction, preference, pattern, and calibration notes when they no longer reflect current preferences.

## Reference(s):

- [Taste skill page](https://clawhub.ai/ivangdavila/skills/taste)
- [Learning System - Taste Calibration](artifact/learning.md)
- [Visual Taste - Design Judgment](artifact/visual.md)
- [Writing Taste - Prose Judgment](artifact/writing.md)
- [Developing Taste - Training Aesthetic Judgment](artifact/development.md)
- [Taste Anti-Patterns - What Bad Taste Looks Like](artifact/antipatterns.md)
- [Prompting for Taste - Creative Generation](artifact/prompting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational guidance and Markdown taste notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write long-lived correction, preference, pattern, and calibration notes under ~/taste/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
