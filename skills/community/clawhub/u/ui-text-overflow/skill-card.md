## Description:

Audits UI text fit across sibling components, checks truncation and layout resilience, and provides line-count findings and character budgets without rewriting copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monikazapisek](https://clawhub.ai/user/monikazapisek)

### License/Terms of Use:

MIT

## Use Case:

Designers and developers use this skill to audit UI text in cards and lists, identify clipped or unreachable content, and give writers a practical character budget before handoff or localization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The draft Figma line-count estimate and resilience check have not been validated in a Figma file.

Mitigation: Label estimated line counts and check findings against the actual design before relying on them.

Risk: A resilience check or requested fix can modify Figma nodes.

Mitigation: Allow edits only on explicit request; run resilience checks on a duplicate and remove it afterwards.

## Reference(s):

- [UI Text Overflow on ClawHub](https://clawhub.ai/monikazapisek/skills/ui-text-overflow)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports line-count comparisons, character-budget ranges, truncation reachability, and resilience findings; does not rewrite copy.]

## Skill Version(s):

0.1.2 (source: ClawHub release; source files label themselves 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
