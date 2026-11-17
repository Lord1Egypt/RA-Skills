## Description:

Provides feature-specific QA checklists for forms, lists, carts, payments, imports and exports, approvals, notifications, and permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA testers and developers use these checklists to plan feature-specific test scenarios, spot common edge cases, and identify areas that need further exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional installation command uses an unpinned external package.

Mitigation: Review the referenced package before running the installation command.

Risk: A generic checklist may miss business-specific rules and historical defect patterns.

Mitigation: Adapt the checklist to the feature requirements and document uncovered areas.

## Reference(s):

- [Full feature-type checklists](artifact/references/checklists.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-heuristic-checklist)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown checklist with covered and uncovered areas and exploratory testing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage claims are scoped to supplied requirements; omitted areas should be identified with reasons.]

## Skill Version(s):

1.8.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
