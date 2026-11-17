## Description:

Find store-specific Publix weekly ads and BOGO deals, savings and coupons, products and available prices, nutrition details, deli and bakery menus, store locations, and search suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and developers use this skill to find store-specific Publix deals, coupons, product details, available prices, nutrition information, Pub Sub menus, and nearby stores.

### Deployment Geography for Use:

United States: Florida, Georgia, Alabama, South Carolina, North Carolina, Tennessee, Virginia, and Kentucky.

## Known Risks and Mitigations:

Risk: The skill may send a user's location and shopping queries to Scavio, and the scan found no user-facing privacy warning.

Mitigation: Explain what information is sent to Scavio and avoid sending more location or query detail than needed.

Risk: The security scan was partial because some local references could not be resolved, so the evidence is incomplete.

Mitigation: Review unresolved references and complete the security checks before relying on the skill.

## Reference(s):

- [Scavio Publix API documentation](https://scavio.dev/docs/publix-weekly-ad?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api)
- [Scavio Publix API overview](https://scavio.dev/publix-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=publix-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are store-specific; prices appear only where Publix provides them. Each endpoint costs 1 credit.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
