## Description:

Reviews shadcn/ui components for CVA patterns, composition with asChild, accessibility states, and data-slot usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review React components built with shadcn/ui, Radix primitives, and Tailwind for component API patterns, composition, accessibility states, and data-slot usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce incorrect or overbroad code review findings if source locations, valid shadcn/ui patterns, or Radix wrappers are not checked first.

Mitigation: Apply the hard gates before reporting findings: require location evidence, exemption checks, context-sensitive import or wrapper checks, and completion of the review-verification protocol or an equivalent manual check.

Risk: The referenced review-verification protocol may be unavailable in environments where that related skill is not installed.

Mitigation: Confirm the related protocol exists before relying on it, or perform equivalent pre-report verification manually.

## Reference(s):

- [Accessibility Patterns](references/accessibility.md)
- [Component Composition](references/composition.md)
- [CVA Patterns](references/cva-patterns.md)
- [data-slot Pattern](references/data-slot.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown code review findings and checklist-guided guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include source-location evidence and pass the skill's hard gates before being reported.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
