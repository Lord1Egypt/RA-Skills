## Description:

Helps agents advise on SaaS operating work across subscription revenue, packaging, trials, retention, expansion, enterprise readiness, multi-tenancy, compliance, support, reporting, and ARR quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, operators, and revenue teams use this skill to compute and explain SaaS metrics, design plans and entitlements, diagnose retention and failed-payment leaks, prepare enterprise readiness, and maintain local operating notes for durable decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local SaaS operating notes can contain confidential business data such as account names, ARR, renewal dates, churn reasons, and commercial commitments.

Mitigation: Review files under ~/Clawic/data/ periodically and avoid storing secrets, full customer exports, card data, or unnecessary personal data.

Risk: Guidance about live billing actions such as cancellations, refunds, migrations, or access suspension could affect customers or revenue if acted on without review.

Mitigation: Require explicit confirmation and check the affected customer count and revenue before taking any live billing or access-changing action.

## Reference(s):

- [ClawHub SaaS skill page](https://clawhub.ai/ivangdavila/skills/saas)
- [Clawic SaaS skill homepage](https://clawic.com/skills/saas)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown prose, tables, formulas, and local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update plain local notes under configured ~/Clawic/data/ paths when durable SaaS operating decisions or records are produced.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
