## Description:

Use when scaling a recipe up or down, converting a recipe to a different pan size, or diagnosing why a doubled recipe tastes wrong. Computes non-linear ingredient scaling (salt, chilies, dried spices, leavening, fat, alcohol scale with exponents, not multiplication), pan-area yield factors, and bake/roast-time corrections with the food-science reason for every adjustment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home cooks use this skill to scale ingredient quantities, adapt recipes to different pans, and estimate bake or roast time changes. It explains why adjustments apply and when the scaling model is unsuitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saving adjusted quantities into the original recipe could overwrite the source recipe.

Mitigation: Work from a copy when preserving the original matters, and specify whether adjustments should be saved or only displayed.

## Reference(s):

- [Scaling science](artifact/references/scaling-science.md)
- [ClawHub skill release](https://clawhub.ai/vorinindenis5/skills/recipe-scale-chemist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Readable text reports with ingredient tables and warnings, plus Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include adjusted quantities, ingredient classes and scaling notes, pan yield factors, time corrections, and food-safety reminders.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
