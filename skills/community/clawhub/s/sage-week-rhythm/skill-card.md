## Description:

A personalized weekly rhythm system built on top of sage-cognitive that supports Week Start alignment, Daily Pulse reflection, Week End review, and cross-week growth tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanl1](https://clawhub.ai/user/evanl1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to run personalized weekly reflection conversations that draw on sage-cognitive profile and memory context. It helps users align the week, capture daily signals, review whether the week matched their values, and notice longer-term growth patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sage-cognitive profile data plus calendar or memory context and save personal work, energy, and values reflections over time.

Mitigation: Use explicit invocations, avoid sharing sensitive information unless appropriate, and confirm save-prevention and deletion behavior before recording private reflections.

Risk: Broad reflection triggers and repeated memory writes may preserve personal patterns longer than the user expects.

Mitigation: Review generated memory notes before saving, skip growth tracking when there is insufficient or sensitive data, and require confirmation before promoting stable observations to a core profile.

## Reference(s):

- [Sage homepage](https://github.com/nicholasgasior/sage)
- [ClawHub skill page](https://clawhub.ai/evanl1/skills/sage-week-rhythm)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Conversational markdown with short prompts, reflections, and optional memory notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save daily energy words, meaningful daily signals, weekly summaries, and growth observations to sage-cognitive memory when used.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
