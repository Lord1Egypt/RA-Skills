## Description:

Helps agents analyze the distribution of a brand's popular Shopee products across subcategories, ordered by sales over the past 30 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee merchants and analysts use this skill to identify which product subcategories contribute to a brand's recent sales at a selected site and category level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node or qhkit, contact package registries and Qinghu, and store an API token locally.

Mitigation: Review the installation and configuration steps before allowing persistent local changes; protect the token.

Risk: A mismatched Qinghu account region can cause authentication errors or incorrect configuration.

Mitigation: Confirm the intended Qinghu site and account region before changing configuration.

Risk: Analytics calls can consume paid Qinghu credits.

Mitigation: Review the estimated credit cost and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-categories)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise analysis with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover a selected Shopee site, brand, date and category; subcategories are ordered by recent sales.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
