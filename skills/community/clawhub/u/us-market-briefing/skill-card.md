## Description:

Generate US pre-market outlooks and post-market recaps in a fixed 3-section format using finance news plus structured market-data pages for index snapshots and top gainers/losers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinksaji](https://clawhub.ai/user/kevinksaji)

### License/Terms of Use:

MIT-0

## Use Case:

Market-focused users use this skill to generate one-shot or scheduled US pre-market outlooks and post-market recaps with structured index snapshots, top mover rankings, and concise inline source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance sources and structured market-data pages can be stale, delayed, incomplete, or inconsistent with narrative articles.

Mitigation: Prefer structured quote and movers pages for rankings and percentages, use trusted finance/news sources for catalysts, and label partial or stale data clearly.

Risk: Optional scheduled delivery can create or update OpenClaw cron jobs.

Mitigation: Review cron jobs before enabling automation, avoid system cron or external schedulers, and require explicit approval when schedule tooling or scope is unclear.

Risk: The 2026 holiday helper contains a fixed calendar and a user-specific early-close exception.

Mitigation: Confirm holiday behavior before relying on automation and replace user-specific exceptions with explicit user-controlled settings when needed.

## Reference(s):

- [Skill page](https://clawhub.ai/kevinksaji/skills/us-market-briefing)
- [Briefing templates](references/templates.md)
- [US market holidays 2026](references/us-market-holidays-2026.md)
- [Yahoo Finance stock gainers](https://finance.yahoo.com/markets/stocks/gainers/)
- [Yahoo Finance stock losers](https://finance.yahoo.com/markets/stocks/losers/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings with three fixed sections, inline source links, and optional scheduling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current web search/fetch for finance sources; optional automation can use OpenClaw cron scheduling and a workspace-local request budget tracker.]

## Skill Version(s):

1.1.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
