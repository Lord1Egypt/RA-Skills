## Description:

Tracks daily Xiaohongshu trends and analyzes popular posts to surface reusable topics, messaging, and presentation ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand teams, and social media operators use this skill to find currently popular Xiaohongshu posts by topic or category, review engagement trends, and develop ideas for future content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recharge workflow may be initiated when the service reports insufficient credits.

Mitigation: Require approval of the verified recipient and amount before each recharge, and approve any pinned payment-tool installation separately.

Risk: API keys may be exposed during setup or use.

Mitigation: Keep the API key scoped to this skill, never print it, and rotate any key that has already been exposed.

Risk: Generated HTML may execute untrusted content.

Mitigation: Avoid opening generated HTML until escaping is fixed.

Risk: Daily rankings may be delayed.

Mitigation: Treat ranking results as time-sensitive and allow for reporting delays.

## Reference(s):

- [ClawHub release](https://clawhub.ai/redfox-data/skills/xiaohongshu-dailytop)
- [Core workflow](references/core_workflow.md)
- [Alipay recharge guidance](references/alipay-recharge.md)
- [RedFox Hub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, HTML files]

**Output Format:** [Markdown tables and summaries, with optional HTML report pages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports keyword, category, and date queries; configurable top-N results and optional HTML export.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
