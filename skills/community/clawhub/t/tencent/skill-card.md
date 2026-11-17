## Description:

Navigate Tencent products, Tencent Cloud services, and WeChat ecosystem decisions with region-aware planning and official-source verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business teams use this skill to route Tencent-related requests, compare Tencent Cloud, WeChat, WeCom, payments, ads, and regional rollout options, and turn ambiguous Tencent work into source-verified plans and decision records.

### Deployment Geography for Use:

Global, with explicit mainland China, Hong Kong, Singapore, and international rollout checks when geography affects product availability, documentation, compliance, payments, or operations.

## Known Risks and Mitigations:

Risk: Local Tencent notes under ~/tencent may capture durable account labels, region defaults, source preferences, and decision records.

Mitigation: Save only non-secret planning context that the user explicitly shares or approves; do not store passwords, QR-login secrets, SMS codes, cookies, access keys, billing exports, raw customer data, or console tokens.

Risk: Research queries and page requests may be sent to Tencent documentation and product sites.

Mitigation: Use the skill only when the user is comfortable sharing Tencent-related research queries with those sites, and request approval before adding non-Tencent comparison sources.

Risk: Tencent product behavior, regional availability, pricing, quotas, SDK support, and launch requirements can vary by region and change over time.

Mitigation: Verify time-sensitive or region-sensitive claims against official Tencent-owned sources, record source freshness, and mark legal, compliance, payment, identity, or public-launch dependencies for human review.

Risk: Account-changing work across Tencent Cloud, WeChat, WeCom, ads, payments, or partner consoles could affect production resources or business operations.

Mitigation: Treat planning and verification as the default posture; require explicit user approval and correct account context before login, resource changes, submissions, payment actions, or other execution steps.

## Reference(s):

- [ClawHub Tencent skill page](https://clawhub.ai/ivangdavila/skills/tencent)
- [Tencent corporate and product overview](https://www.tencent.com)
- [Tencent Cloud mainland documentation](https://cloud.tencent.com)
- [Tencent Cloud international documentation](https://www.tencentcloud.com)
- [WeChat developer documentation](https://developers.weixin.qq.com)
- [WeCom documentation](https://work.weixin.qq.com)
- [Tencent Ecosystem Map](ecosystem-map.md)
- [Tencent Decision Framework](decision-framework.md)
- [Mainland Vs Global](mainland-vs-global.md)
- [Tencent Source Validation](source-validation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with decision records, checklists, source-validation notes, and occasional bash setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown memory under ~/tencent after user approval; does not require credentials for planning or research.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
