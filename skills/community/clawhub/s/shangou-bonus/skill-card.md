## Description:

查询淘宝闪购每日隐藏的大额福利优惠券和红包，包含通用红包、超市红包、夜宵红包、买药红包、零食红包、学生专享等，并通过固定 API 获取当日最新活动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[z65919](https://clawhub.ai/user/z65919)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to fetch and display current Taobao Shāngòu coupon, red-packet, and activity search terms so they can search for those benefits in the Taobao app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill displays coupon instructions supplied by a third-party API, so the content may change, be promotional, or be inaccurate.

Mitigation: Present returned coupon instructions as third-party content and have users verify offers in the Taobao app before relying on them.

Risk: The source text mentions daily reminders, which could be misunderstood as consent to recurring notifications.

Mitigation: Create any reminder only after a separate explicit user request and confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z65919/skills/shangou-bonus)
- [聚满减 API endpoint](https://v.jumanjian.com/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code]

**Output Format:** [Markdown-like text with coupon titles, search terms, descriptions, detailed instructions, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs API-provided coupon content and can cache the latest JSON response locally.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
