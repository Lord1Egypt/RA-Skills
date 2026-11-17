## Description:

Reviews WidgetKit code for timeline management, view composition, configurable intents, and performance when reviewing Swift code that imports WidgetKit or defines widget entry points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift WidgetKit implementations for timeline behavior, widget view composition, configurable intents, refresh budgeting, memory use, and caching patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled parent-directory review verification protocol that may be missing or mutable and could suppress valid review findings.

Mitigation: Review the external protocol dependency before installation and prefer bundling or pinning the full verification checklist used by the skill.

## Reference(s):

- [Timeline Management](references/timeline.md)
- [Widget Views](references/views.md)
- [Configurable Widgets](references/intents.md)
- [Widget Performance](references/performance.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review findings and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to include concrete file and line locations when reported.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
