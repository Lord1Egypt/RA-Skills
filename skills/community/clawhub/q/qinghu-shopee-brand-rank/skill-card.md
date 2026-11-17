## Description:

按类目查询 Shopee 各站点品牌热销榜和飙升榜，支持日榜、周榜和月榜。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee merchants and market analysts use this skill to identify top-selling or fast-rising brands in a chosen category, site, and reporting period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill may install or upgrade qhkit or Node and change local PATH or configuration.

Mitigation: Review environment changes before use and prefer a pre-provisioned qhkit installation.

Risk: A Qinghu API token must be configured to access the service.

Mitigation: Use a scoped token and confirm credential configuration before running lookups.

Risk: Ambiguous requests or repeated paid lookups may consume Qinghu credits unnecessarily.

Mitigation: Confirm missing site, category, and period; review estimated credits and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-rank)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise ranking summary with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports site, category, period, sample size, and credits used when a paid lookup runs.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
