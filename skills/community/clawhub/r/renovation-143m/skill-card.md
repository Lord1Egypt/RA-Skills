## Description:

A home renovation planning assistant for a fixed 143 m² three-bedroom apartment, covering inspection, layout, storage, utilities, budgeting, materials, and visual concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners planning this 143 m² apartment can use it to organize renovation requirements, compare layout and furnishing options, plan budgets and utilities, and identify measurements or building conditions that need verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household layout details may be shared with an image-generation provider, whose processing and retention practices are unknown, and layout files may be stored in Git history.

Mitigation: Avoid including identifying or security-sensitive details, review the provider's privacy terms before sharing layouts, and check repository history before committing them.

Risk: The security evidence says three referenced images were not fully inspected, so image-based layout details may be incomplete or uncertain.

Mitigation: Review source images and verify dimensions and building conditions against measured plans or an on-site survey before relying on a layout.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/z-zihan/skills/renovation-143m)
- [House geometry model](references/house-geometry.json)
- [Geometry validation rules](references/geometry-validation.md)
- [Design pipeline](references/design-pipeline.md)
- [Renovation requirements registry](references/requirements.md)
- [Open questions](references/open-questions.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Image-generation prompts]

**Output Format:** [Structured natural language, checklists, tables, and image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conceptual planning aid; estimated measurements require on-site verification, and generated images are visual references rather than construction documents.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
