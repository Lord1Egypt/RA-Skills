## Description:

Provides Sichuan cuisine product R&D guidance for recipe formulation, industrial process design, quality standards, and food safety compliance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h-beatman](https://clawhub.ai/user/h-beatman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, food product teams, and culinary R&D users can use this skill to draft Sichuan-style product formulas, translate recipes into scalable production processes, and identify food safety or labeling issues that need expert review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a large unrelated requirements.txt dependency manifest, which can create avoidable installation and supply-chain exposure if processed automatically.

Mitigation: Remove the dependency manifest or reduce it to only packages the skill actually requires; use hash-locked installs and an isolated non-privileged environment when installation is necessary.

Risk: Food safety, labeling, and production guidance can vary by jurisdiction and product category.

Mitigation: Confirm applicable regulations, standards, process controls, and labels with qualified food safety or regulatory professionals before production or sale.

## Reference(s):

- [Sichuan Flavor Profile](artifact/sichuan-cuisine-rd/references/sichuan-flavor-profile.md)
- [Production Process Guide](artifact/sichuan-cuisine-rd/references/production-process-guide.md)
- [Food Safety Standards](artifact/sichuan-cuisine-rd/references/food-safety-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with structured lists, process steps, formulation notes, and safety review points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calculations or validation frameworks for users to execute separately; does not perform lab validation or production execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
