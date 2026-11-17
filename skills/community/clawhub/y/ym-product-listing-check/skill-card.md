## Description:

Audits product listing text for missing required fields, specification inconsistencies, wording risks, and actionable pre-listing fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, merchants, and listing reviewers use this skill to check product titles, parameter tables, descriptions, specifications, prices, and inventory before publication. It identifies missing information, conflicting details, risk words, and suggested edits without making legal compliance determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a live platform compliance checker or legal review.

Mitigation: Use it as a product-listing completeness and wording-risk checklist, and have users or legal reviewers make final platform and legal compliance decisions.

Risk: Broad pre-listing language may invoke the skill for product-launch reviews outside its intended listing-text scope.

Mitigation: Confirm the user wants product listing completeness, consistency, and wording-risk review before applying the checklist.

Risk: The skill does not fetch current platform rules or inspect seller-platform data.

Mitigation: Base conclusions only on user-provided listing text and clearly state unchecked platform-specific assumptions or missing fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-product-listing-check)
- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-product-listing-check)
- [Required fields and consistency rules](artifact/references/required-fields.md)
- [Description risk word library](artifact/references/risk-words.md)
- [Product listing check template](artifact/templates/check-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist with tables and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs check scope and assumptions, missing-field findings, consistency conflicts, description risk words, must-fix items, and optimization suggestions.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
