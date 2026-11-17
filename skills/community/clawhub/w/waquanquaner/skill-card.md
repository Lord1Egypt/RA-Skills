## Description:

挖券券儿 helps agents query current Meituan, Ele.me, and JD Food delivery coupon promotions and return a single redemption link without user registration or API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w5543081](https://clawhub.ai/user/w5543081)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer food-delivery coupon requests by fetching current promotions and rendering a shareable redemption message for Chinese delivery platforms.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill contacts waquanquaner.cn to retrieve coupon data.

Mitigation: Install only where outbound HTTPS access to waquanquaner.cn is acceptable and organization-approved.

Risk: Returned coupon URLs are third-party promotional links supplied by the service.

Mitigation: Treat returned links as promotional content, show them to the user before opening, and avoid automatic link following.

Risk: Broad coupon and food-ordering triggers can activate in ambiguous user conversations.

Mitigation: Use confirmation or narrower trigger policy in environments where automatic coupon lookup is not expected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/w5543081/skills/waquanquaner)
- [Publisher Profile](https://clawhub.ai/user/w5543081)
- [WaQuanquaner Homepage](https://waquanquaner.cn)
- [Coupon Data API](https://waquanquaner.cn/api/v1/activities/channel/skill_compact)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Chinese coupon recommendation text, Feishu card JSON, or plain text with third-party promotional links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches current coupon data from waquanquaner.cn over HTTPS and formats service-supplied links for the user.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact SKILL.md and package.json state 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
