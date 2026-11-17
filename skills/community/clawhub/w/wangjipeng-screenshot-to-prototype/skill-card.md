## Description:

Use when a user pastes a UI screenshot and needs an editable frontend code prototype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to turn a clear UI screenshot into editable frontend prototype code. It helps identify layout regions, common UI components, typography, spacing, and color assumptions before producing HTML/CSS or framework-oriented code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided UI screenshots may contain sensitive product, customer, or internal interface details.

Mitigation: Share only screenshots intended for agent inspection and redact private information before using the skill.

Risk: The README contains auto-generated placeholder guidance about read/write modes and API keys that may not match the actual skill behavior.

Mitigation: Use SKILL.md and validated release metadata as the source for expected behavior, and avoid relying on placeholder README usage sections.

Risk: Generated prototypes depend on visual estimation and may contain inaccurate spacing, styling, hierarchy, or interaction assumptions.

Mitigation: Review and edit generated code before using it in production UI work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/skills/wangjipeng-screenshot-to-prototype)
- [Metadata Source Repository](https://github.com/MiniMax-AI/skills)
- [Local References Index](references/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown response with frontend prototype code and brief implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTML/CSS, React, or Vue code depending on the request and screenshot context.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
