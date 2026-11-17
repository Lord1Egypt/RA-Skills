## Description:

Stock Deep Dive helps agents run modular stock and crypto research for a ticker, combining market analysis, fundamentals, dividend checks, valuation models, investor-rule review, and concise report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cplog](https://clawhub.ai/user/cplog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for a deep stock or crypto review by ticker, including quantitative signals, fundamentals, valuation notes, investor-panel checks, caveats, and a concise final recommendation. Its outputs are informational research aids, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter integration handles live session tokens broadly.

Mitigation: Use a dedicated environment, avoid unrelated secrets in the skill .env, and scope secret injection to AUTH_TOKEN and CT0 only.

Risk: The skill depends on unpinned external tools or dependencies for some data collection paths.

Mitigation: Pin and audit dependencies before installation, and avoid global bird installation unless the tool and source are trusted and verified.

Risk: Generated financial analysis can be stale, incomplete, or misleading if market data sources lag or fail.

Mitigation: Treat outputs as informational research only, review cited data manually, and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cplog/skills/stock-deep-dive)
- [Credits](references/CREDITS.md)
- [Stock Analysis README](stock-analysis/README.md)
- [Hot Scanner documentation](stock-analysis/docs/HOT_SCANNER.md)
- [Yahoo Finance](https://finance.yahoo.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown and JSON-style analysis summaries with command snippets when setup or execution is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ticker recommendations, conviction scoring, caveats, valuation notes, dividend details, trend signals, and report or deployment status.]

## Skill Version(s):

1.3.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
