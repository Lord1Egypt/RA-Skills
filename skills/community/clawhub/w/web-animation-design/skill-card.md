## Description:

Design and implement web animations that feel natural and purposeful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aa-on-ai](https://clawhub.ai/user/aa-on-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and frontend agents use this skill to choose, review, and implement purposeful web motion, including easing, timing, transitions, springs, performance, and reduced-motion accessibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad UI phrasing may invoke animation guidance when the user needs general frontend layout or performance help.

Mitigation: Clarify whether the request is specifically about animation, motion, transitions, easing, or interaction feel before applying the skill's recommendations.

Risk: Motion-heavy recommendations can create discomfort or accessibility barriers for users who prefer reduced motion.

Mitigation: Respect prefers-reduced-motion and replace transform-based movement, scaling, sliding, parallax, and autoplay motion with simpler effects such as opacity or color changes.

Risk: Animation code suggestions can still introduce jank or misleading UI behavior if applied without review.

Mitigation: Review generated changes before deployment, favor transform and opacity for performance-sensitive motion, and test interaction-heavy animations in context.

## Reference(s):

- [Web Animation Design on ClawHub](https://clawhub.ai/aa-on-ai/skills/web-animation-design)
- [Practical Animation Tips](artifact/PRACTICAL-TIPS.md)
- [Easing Functions Cheat Sheet](https://easings.co/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with tables and inline CSS or JSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no tool calls, persistence, credential access, or executable behavior are added by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
