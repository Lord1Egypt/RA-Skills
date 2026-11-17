## Description:

悟道 · A股市场情报 helps agents query China A-share market intelligence, including dragon-tiger board records, research reports, auction data, intelligent hotlists, and daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdreamjc](https://clawhub.ai/user/jcdreamjc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to retrieve read-only A-share market intelligence from the documented API endpoints. It is appropriate for informational workflows around hot topics, analyst research, pre-market auction data, daily market briefs, and dragon-tiger board activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API key and configurable API base URL.

Mitigation: Keep LB_API_KEY secret and set LB_API_BASE to the documented official URL, https://stock.quicktiny.cn/api/openclaw.

Risk: Market intelligence can be misread as trading advice.

Mitigation: Use returned data for informational analysis only and avoid presenting outputs as buy, sell, or hold recommendations.

Risk: The artifact scope wording excludes limit-up boards and capital flow while some returned briefing data may mention related fields.

Mitigation: Keep agent responses within the five documented endpoint categories and clarify scope before answering requests about limit-up boards or capital-flow analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcdreamjc/skills/wudao-intel)
- [Publisher profile](https://clawhub.ai/user/jcdreamjc)
- [悟道 API service](https://stock.quicktiny.cn)
- [OpenClaw API base](https://stock.quicktiny.cn/api/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE. Treat returned market data as information, not trading advice.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
