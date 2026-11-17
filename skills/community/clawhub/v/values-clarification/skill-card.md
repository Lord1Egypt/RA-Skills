## Description:

Structured process for identifying personal values and life purpose. Use when someone feels directionless, is making a major life decision, suspects their life is misaligned with what they actually want, or is rebuilding after a crisis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to clarify personal values, examine whether daily life aligns with those values, and turn the results into concrete daily, weekly, quarterly, and annual actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt users to share sensitive personal reflections about values, family, work, budget, calendar, and life direction.

Mitigation: Tell users not to share information they do not want retained by the agent environment, especially if state or follow-up reminders are enabled.

Risk: The installer command depends on the `clawhub` package supply chain.

Mitigation: Pin or otherwise verify the `clawhub` installer package before installing.

Risk: State-tracking fields and follow-up reminders could retain personal values-work details longer than the user expects.

Mitigation: Use state retention only when needed and review stored values, actions, scores, and reminder dates with the user.

## Reference(s):

- [Values Clarification skill page](https://clawhub.ai/howtousehumans/skills/values-clarification)
- [Publisher profile: howtousehumans](https://clawhub.ai/user/howtousehumans)
- [VIA Character Strengths](https://www.viacharacter.org/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown and conversational text with structured exercises, prompts, action plans, and optional state-tracking fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user for sensitive personal reflections about values, family, work, budget, calendar, and life direction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
