## Description:

Fetches live Yahoo Finance market data through a CLI and returns JSON for agent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gddezero](https://clawhub.ai/user/gddezero)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve current quotes, fundamentals, historical prices, options chains, market movers, ETF holdings, and ticker search results from Yahoo Finance. It is intended for data lookup and analysis support, not standalone financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed, unpinned community npm package.

Mitigation: Pin and review a specific yahoo-finance2 version, and prefer installation in a controlled local environment.

Risk: Financial data from Yahoo Finance may be delayed, incomplete, or unsuitable as financial advice.

Mitigation: Treat outputs as data lookup results, verify material decisions against authoritative sources, and avoid presenting results as financial advice.

Risk: Invalid or incorrectly formatted symbols can produce non-JSON output or stale records.

Mitigation: Validate symbols before analysis, handle undefined outputs, and verify market and price fields for Hong Kong symbols.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gddezero/skills/yfinance-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns one symbol per invocation; invalid symbols may return non-JSON undefined output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
