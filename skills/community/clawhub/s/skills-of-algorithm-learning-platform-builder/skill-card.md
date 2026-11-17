## Description:

Builds interactive algorithm learning pages, comparison pages, and reusable teaching platforms with formulas, step-by-step calculations, charts, interaction controls, upgrade guidance, and runnable HTML demos when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doctorfff](https://clawhub.ai/user/doctorfff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to plan, structure, compare, and generate interactive algorithm teaching materials. It is intended for browser-runnable study pages, visualization-heavy algorithm explainers, and reusable learning-platform patterns rather than production training infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include third-party CDN script tags for browser-side libraries.

Mitigation: Review or replace CDN script tags before publishing or sharing generated pages.

Risk: The README links to a sample ZIP whose contents are not verified by the security summary.

Mitigation: Avoid opening the sample ZIP unless it is trusted and inspected first.

Risk: Template language and examples may default to Chinese-language learning content.

Mitigation: Adjust generated wording and templates when a different output language is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/doctorfff/skills/skills-of-algorithm-learning-platform-builder)
- [Skill Definition](SKILL.md)
- [README](README.md)
- [Algorithm Family Maps](references/algorithm-family-maps.md)
- [Algorithm Page Template](references/algorithm-page-template.md)
- [Comparison Page Template](references/comparison-page-template.md)
- [Explanation Patterns](references/explanation-patterns.md)
- [Interaction Patterns](references/interaction-patterns.md)
- [Page Architecture](references/page-architecture.md)
- [Platform Upgrade Rules](references/platform-upgrade-rules.md)
- [Request Routing Rules](references/request-routing-rules.md)
- [Writing Rules](references/writing-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional complete HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce single-file, browser-runnable HTML demos with teaching sections, charts, and interactive controls when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
