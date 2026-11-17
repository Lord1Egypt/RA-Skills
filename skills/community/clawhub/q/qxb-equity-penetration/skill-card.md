## Description:

基于工商数据源，深度解析企业股权结构，清晰呈现企业股权架构与控制关系，辅助决策者把握企业核心控制脉络。

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx-26](https://clawhub.ai/user/llx-26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Qixinbao for direct and indirect shareholder relationships, ownership percentages, and shortest equity-control paths for enterprise due diligence, mergers and acquisitions, investment review, and related-party analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, enterprise IDs, and the user's Qixinbao API token are sent to Qixinbao.

Mitigation: Install and use the skill only when Qixinbao is trusted for the queried entities and credential handling.

Risk: Fuzzy company-name lookup can automatically select the first or best match and may return data for an unintended enterprise.

Mitigation: Prefer exact enterprise IDs for sensitive due-diligence work and verify the returned company name before relying on results.

Risk: Runtime dependencies may change because package metadata allows a semver range for axios.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [查询企业股权穿透](references/getEquityPenetration.md)
- [Qixinbao Skill Quota Portal](https://www.qixin.com/app-center/home?route=skill-quota)
- [Qixinbao External API Base](https://external-api.qixin.com/skill/ent/public)
- [ClawHub Skill Page](https://clawhub.ai/llx-26/skills/qxb-equity-penetration)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Structured shareholder data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns direct shareholder counts and up to 10 direct holders, plus indirect shareholder counts, up to 100 indirect holders, shortest levels, and ownership paths when provided by Qixinbao.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
