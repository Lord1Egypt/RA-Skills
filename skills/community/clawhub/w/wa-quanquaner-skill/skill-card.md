## Description:

Chinese mainland food-delivery coupon assistant for discovering current Meituan, Ele.me, and JD delivery promotions through a single activity link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w5543081](https://clawhub.ai/user/w5543081)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to recognize Chinese food-delivery coupon requests, fetch current promotion data, and render concise coupon guidance for Meituan, Ele.me, and JD delivery services.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill requests broad command and script access for fetching and rendering coupon data.

Mitigation: Install with tightly scoped permissions, limiting network access to expected HTTPS endpoints and allowing only the documented curl or Node.js execution paths.

Risk: Returned promotion links and claims are third-party content that may be unvalidated or change over time.

Mitigation: Treat promotions as informational, verify destinations and offer terms before sharing or acting on them, and avoid presenting them as platform-endorsed recommendations.

Risk: Broad everyday trigger phrases can cause the skill to surface promotional links during casual food-ordering queries.

Mitigation: Review trigger configuration before deployment and require user confirmation before opening or forwarding coupon links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/w5543081/skills/wa-quanquaner-skill)
- [WaQuanquaner compact activity API](https://waquanquaner.cn/api/v1/activities/channel/skill_compact)
- [WaQuanquaner coupon landing page](https://waquanquaner.cn/go)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Chinese coupon summaries, WeChat-style text, Feishu card JSON, plain text, and inline curl or Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Promotion data is fetched from HTTPS endpoints and may include third-party coupon links or claims.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
