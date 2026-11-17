## Description:

Matches industrial-product inquiries against an MRO catalog by model, category, brand, and key specifications, and returns preferred and alternative candidates plus items needing confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfanlu](https://clawhub.ai/user/cfanlu)

### License/Terms of Use:

Apache 2.0

## Use Case:

Procurement teams and engineers use the skill to match industrial-product inquiries, individually or in spreadsheets, to catalog candidates by model, category, brand, and key specifications. It identifies preferred and alternative items and flags uncertain matches for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inquiry terms, model numbers, specifications, and selected product-detail requests are sent to the MRO API; matching and detail calls may consume account credits.

Mitigation: Use the service only when comfortable sharing those inquiry details and possible charges; keep MRO_API_KEY in secret or environment settings, and use a replacement API endpoint only when fully trusted.

Risk: Catalog results may be incomplete or unsuitable as a final purchasing decision.

Mitigation: Review generated spreadsheet outputs and confirm product suitability, price, availability, and delivery with source data or the supplier before purchasing.

## Reference(s):

- [Skill homepage](https://github.com/cfanlu/mro-inquiry-match)
- [MRO API platform](https://mro-api.iwilley.com/)
- [Marketplace setup and costs](artifact/references/marketplace-setup.md)
- [Matching rules](artifact/references/matching-rules.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Structured Markdown or text, with optional updated Excel or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates preferred and alternative candidates from items requiring confirmation; spreadsheet results may include product-detail links.]

## Skill Version(s):

1.2.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
