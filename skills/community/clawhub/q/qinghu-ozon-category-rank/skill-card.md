## Description:

Queries top-selling Ozon product categories by category ID, reporting sales data with configurable periods, sorting, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and market researchers use this skill to compare top-selling product categories and identify promising subcategories using Qinghu sales data.

### Deployment Geography for Use:

Global; queries Ozon marketplace data.

## Known Risks and Mitigations:

Risk: Installing or updating qhkit or Node.js may modify the host environment.

Mitigation: Review setup steps and package sources first; prefer a trusted, pinned or preinstalled qhkit version, and avoid unapproved global installs or shell startup changes.

Risk: Configuring a Qinghu API token grants access to an account credential.

Mitigation: Provide a token only when intending to use Qinghu, and avoid exposing it in output or shared files.

Risk: Ranking queries may consume Qinghu credits, especially when retrieving many results.

Mitigation: Check estimated costs and obtain user approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-category-rank)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary with optional tabular data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports category, period, sample size, and credits spent when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
