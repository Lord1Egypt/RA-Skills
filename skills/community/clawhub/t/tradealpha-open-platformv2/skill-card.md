## Description:

Fetch realtime TradeAlpha news across Reuters, Bloomberg, Truth Social, research alerts, and domestic news sources via `POST /api/v1/news/realtime_news`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwei2](https://clawhub.ai/user/jiuwei2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and filter TradeAlpha realtime news by source, category, importance level, page size, and time range. It is intended for users who already have a TradeAlpha API token and want agent-assisted news retrieval through that provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends news requests to TradeAlpha's external quantaccess.lxaa.top service using a user-provided token.

Mitigation: Use it only for TradeAlpha news workflows, set TradeAlphaToken through the environment, and do not expose the token in prompts, logs, or responses.

Risk: Users may treat the skill as a generic news fetcher even though results come through one provider.

Mitigation: Disclose that retrieved results are TradeAlpha API results and direct users to another source when they need provider-independent news.

## Reference(s):

- [TradeAlpha Realtime News Skill](https://clawhub.ai/jiuwei2/skills/tradealpha-open-platformv2)
- [TradeAlpha Open Platform](https://quantaccess.lxaa.top/)
- [TradeAlpha realtime news API reference](reference.md)
- [TradeAlpha realtime news examples](examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON-backed news results and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a TradeAlphaToken environment variable; requests are sent to TradeAlpha's quantaccess.lxaa.top service.]

## Skill Version(s):

0.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
