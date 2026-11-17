## Description:

Searches RedFox-backed WeChat Official Account hot articles by keyword and helps agents present ranked trend results, topic-expansion hints, and subscription setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, WeChat operators, brand teams, and agents use this skill to search recent WeChat Official Account articles with 5,000+ reads, compare ranking signals, and produce concise trend summaries. It can also guide setup for RedFox API credentials and recurring article subscription prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and date ranges are sent to RedFox.

Mitigation: Use the skill only for queries that are appropriate to share with RedFox, and disclose this data flow to users before operation.

Risk: The skill requires a RedFox API key in the agent environment.

Mitigation: Store REDFOX_API_KEY in managed environment configuration, avoid hard-coding or logging it, and rotate or revoke it if exposure is suspected.

Risk: The skill pushes users toward recurring calendar subscriptions.

Mitigation: Create subscriptions only after explicit user confirmation and make the keyword, date range, cadence, and cancellation path clear.

Risk: Optional HTML reports have unsafe escaping and link handling according to the security evidence.

Mitigation: Prefer JSON or Markdown output and avoid the optional HTML report until the rendering path is fixed and reviewed.

Risk: The security summary reports an undisclosed promotional message.

Mitigation: Review generated responses before deployment and remove or clearly disclose promotional content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/wechat-search-redfox)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [WeChat trend data format reference](artifact/references/gzh_trend_data_format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and prose for the agent response; JSON from the helper script; optional HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends search terms plus date ranges to RedFox. Optional HTML output should be avoided until escaping and link handling are fixed.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
