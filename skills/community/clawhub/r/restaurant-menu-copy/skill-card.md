## Description:

Drafts US restaurant menu item descriptions, allergen wording, and price displays for independent restaurant owners, with reference to federal menu-labeling rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant owners, bar managers, and menu designers use this skill to draft item descriptions, organize prices and sections, and prepare allergen notes, substitutions, and follow-up questions from kitchen-provided details.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The duplicate checker expects CSV input with a menu_item_name column, while the supplied starter template is YAML, so the documented workflow will not work with that template as-is.

Mitigation: Provide a CSV with the required column or repair and verify the input workflow before relying on duplicate results.

Risk: Drafted menu copy may be mistaken for compliance validation, and allergen or labeling statements may be inaccurate.

Mitigation: Have the kitchen confirm recipe and allergen details, and independently verify applicable federal, state, and local requirements before publication.

Risk: The optional Windows application is unnecessary for the bundled workflow, and its checksum alone does not establish safety.

Mitigation: Prefer the documented local Python workflow; use the optional application only after a separate security review.

## Reference(s):

- [Menu labeling rules](references/menu-labeling-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured menu copy and a Markdown duplicate-check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include menu items, allergen statements, duplicates, substitutions, and open items for missing details.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
