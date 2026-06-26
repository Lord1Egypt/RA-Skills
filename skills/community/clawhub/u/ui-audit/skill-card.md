## Description: <br>
AI skill for automated UI audits. Evaluate interfaces against proven UX principles for visual hierarchy, accessibility, cognitive load, navigation, and more. Based on Making UX Decisions by Tommy Geoco. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommygeoco](https://clawhub.ai/user/tommygeoco) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Designers, product teams, and developers use this skill to review interfaces, choose UI patterns, evaluate design trade-offs, and produce structured audit reports covering visual hierarchy, accessibility, navigation, usability, onboarding, forms, and related UX concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing through npm runs a postinstall script. <br>
Mitigation: The reviewed postinstall script only prints setup instructions; inspect package scripts before npm installation and install from trusted sources. <br>
Risk: UI audit recommendations can be subjective or miss product-specific context. <br>
Mitigation: Review generated audit findings against product goals, accessibility requirements, user research, and implementation constraints before making design changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tommygeoco/ui-audit) <br>
- [Guidelines](https://audit.uxtools.co) <br>
- [Making UX Decisions](https://uxdecisions.com) <br>
- [Core Framework](references/00-core-framework.md) <br>
- [Anchors](references/01-anchors.md) <br>
- [Information Scaffold](references/02-information-scaffold.md) <br>
- [New Interfaces Checklist](references/10-checklist-new-interfaces.md) <br>
- [Fidelity Checklist](references/11-checklist-fidelity.md) <br>
- [Visual Style Checklist](references/12-checklist-visual-style.md) <br>
- [Innovation Checklist](references/13-checklist-innovation.md) <br>
- [Accessibility Patterns](references/27-patterns-accessibility.md) <br>
- [Navigation Patterns](references/31-patterns-navigation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with optional structured JSON audit fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pass, warn, fail, or not-applicable checks and prioritized fixes with framework references.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
