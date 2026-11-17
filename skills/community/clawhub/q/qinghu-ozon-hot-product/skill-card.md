## Description:

Analyzes Ozon bestsellers and Chinese seller listings to identify promising products, check sales trends, and recommend resale or differentiation strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and product researchers compare bestseller rankings with Chinese seller listings, inspect product details and trends, and shortlist items for resale or product improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qinghu API token exposure during authenticated product-data queries.

Mitigation: Provide the token only to a trusted workflow and avoid sharing it in responses or exports.

Risk: Locally exported results may reveal sensitive product research or business plans.

Mitigation: Review exported files before sharing them and restrict access to saved datasets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-hot-product)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown summary and optional exported table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product shortlists include price, sales, ratings, trend direction, and a recommended strategy; larger result sets may be saved locally.]

## Skill Version(s):

0.1.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
