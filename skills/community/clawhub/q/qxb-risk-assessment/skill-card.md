## Description:

全面排查企业的经营风险情况，适用于供应商准入尽调、贷前风险筛查、合作伙伴背景调查等场景，全方位预警潜在经营风险，辅助决策者规避合作隐患。

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx-26](https://clawhub.ai/user/llx-26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Qixin enterprise risk signals for supplier onboarding, pre-loan screening, and partner background checks. It returns shell-company indicators, contract breach history, operating risk counts and details, and survival-status risk information for the requested enterprise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names or enterprise IDs are sent to Qixin using the configured API token.

Mitigation: Install and run the skill only when this external lookup is intended, and avoid submitting enterprises that should not be shared with Qixin.

Risk: Fuzzy enterprise-name matching can resolve to a different company than intended.

Mitigation: Prefer an exact enterprise ID for important diligence decisions and confirm that the returned ename matches the intended company.

Risk: Dependency versions may change during installation because the artifact does not include a lockfile.

Mitigation: Review and pin resolved npm dependency versions before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx-26/skills/qxb-risk-assessment)
- [getRiskAssessment API reference](references/getRiskAssessment.md)
- [Qixin skill quota page](https://www.qixin.com/app-center/home?route=skill-quota)
- [Qixin external API base](https://external-api.qixin.com/skill/ent/public)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text summaries with optional TypeScript code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, axios, and QXBENT_API_TOKEN; queries may use an enterprise name or enterprise ID.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
