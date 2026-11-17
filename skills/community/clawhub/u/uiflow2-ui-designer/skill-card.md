## Description:

Design, generate, beautify, optimize, or review UIFlow2 interfaces, graphics, dashboards, gauges, animations, round-screen layouts, e-paper screens, and LED-matrix experiences for M5Stack devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyun2000](https://clawhub.ai/user/yuyun2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review UIFlow2 interfaces for M5Stack devices, including embedded dashboards, gauges, animations, round screens, e-paper layouts, and LED matrix experiences. It helps choose visual direction, layout structure, rendering strategy, interaction states, and validation steps while reserving API correctness checks for official UIFlow2/M5Stack documentation or the companion coder skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UIFlow2 or MicroPython code can be incorrect or incompatible with a target M5Stack device if API details, firmware capabilities, fonts, memory, or display hardware are assumed.

Mitigation: Check generated code against official UIFlow2/M5Stack documentation or the companion coder skill, then test on the target device before deployment.

Risk: The skill defaults to Chinese-language design guidance, which can reduce review clarity for non-Chinese users.

Mitigation: Ask the agent to respond in the desired language when needed and review generated UI text for the deployment audience.

Risk: Visual design guidance may look plausible without proving that the interface renders correctly on constrained embedded displays.

Mitigation: Require simulator screenshots, fresh device photos, or explicit human observation before treating a visual result as passed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyun2000/skills/uiflow2-ui-designer)
- [UIFlow2 API Patterns](references/api-patterns.md)
- [Design Directions](references/design-directions.md)
- [Display Profiles](references/display-profiles.md)
- [Layout Recipes](references/layout-recipes.md)
- [Motion And Effects](references/motion-and-effects.md)
- [Rendering Strategy](references/rendering-strategy.md)
- [UI Review Checklist](references/review-checklist.md)
- [Visual Quality Gate](references/visual-quality-gate.md)
- [Visual System](references/visual-system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with optional MicroPython code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI design direction, layout tokens, state plans, review findings, assumptions, validation status, and device-specific implementation guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
