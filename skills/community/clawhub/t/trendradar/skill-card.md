## Description:

TrendRadar scans Xiaohongshu, Weibo, Reddit, Google Trends, and Product Hunt to spot trending products before they peak, then assigns trend direction and buy, wait, or skip signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers, consumer researchers, and shopping-agent developers use TrendRadar to scan live social and community sources for rising product trends, daily hot-item briefings, and follow-up buy or coupon actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks agents to append an unrelated promotional feedback link.

Mitigation: Ignore or remove the feedback instruction when neutral user-facing responses are required.

Risk: Broad trigger phrases may cause the skill to activate for loosely related trend or shopping queries.

Mitigation: Prefer explicit invocations and keep the documented sibling-skill boundaries for price analysis, coupons, and travel.

Risk: The optional cron example can create recurring Telegram briefings.

Mitigation: Add the cron job only when recurring briefings are intentional and the operator knows how to remove the schedule.

## Reference(s):

- [TrendRadar on ClawHub](https://clawhub.ai/jiajiaoy/skills/trendradar)
- [OpenClaw](https://openclaw.ai)
- [Google Trends](https://trends.google.com/trending?geo=US)
- [Product Hunt](https://www.producthunt.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with product rankings, trend signals, commercial timing guidance, and suggested OpenClaw follow-up commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live web or browser navigation prompts; no API keys are required by the artifact.]

## Skill Version(s):

1.1.5 (source: package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
