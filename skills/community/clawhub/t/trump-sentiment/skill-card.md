## Description:

Monitors Trump-related political and market sentiment across Truth Social, Google News, X-style searches, and market reaction signals to produce concise investment research briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and market-research agents use this skill to collect recent Trump-related geopolitical signals, arrange them into a timeline, compare them with market reactions, and draft a Chinese-language sentiment brief for research review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Nasdaq and four-hour monitoring triggers could run without clear scope controls.

Mitigation: Disable automatic triggers by default or define narrow trigger thresholds, schedule, data sources, and review ownership before use.

Risk: Feishu delivery could send market-sensitive summaries without explicit user confirmation.

Mitigation: Require confirmation before every Feishu send and make the destination channel visible to the operator.

Risk: Browser-based collection may use a personal or broadly authenticated profile.

Mitigation: Use only an intentionally configured browser profile with the minimum accounts and permissions needed for collection.

Risk: Investment conclusions may be mistaken for trading advice.

Mitigation: Treat reports as research notes and require independent verification before trading or portfolio decisions.

Risk: Artifact reports show some runs relying on cached, blocked, or partial external data.

Mitigation: Label stale or blocked-source runs clearly and confirm live sources before acting on urgent geopolitical or market claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/trump-sentiment)
- [Truth Social @realDonaldTrump](https://truthsocial.com/@realDonaldTrump)
- [Google News Trump Iran RSS](https://news.google.com/rss/search?q=Trump+Iran+ceasefire+when:1h&hl=en-US&gl=US&ceid=US:en)
- [Google News Trump Iran search](https://news.google.com/search?q=Trump+Iran&when=1h)
- [XCancel search fallback](https://xcancel.com/search?q=Trump%20Iran%20deal)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain-text research brief with timestamped timeline, source summaries, market reaction notes, contradiction flags, TACO notes when relevant, and investment implications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language reporting style; may include Feishu delivery identifiers when sent through that channel.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
