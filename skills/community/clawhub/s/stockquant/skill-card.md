## Description:

Stockquant helps agents run Chinese A-share stock screening, position sell planning, and per-stock analysis by combining Python-generated market data with structured LLM decision prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[er6y](https://clawhub.ai/user/er6y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to screen Chinese A-share candidates, draft sell-plan actions for existing holdings, and analyze individual stocks with data-backed evidence, confidence labels, and risk prompts. It is intended to support user review rather than replace investment judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives stock-trading guidance that may be wrong, stale, or unsuitable for the user.

Mitigation: Require human review of recommendations, treat outputs as informational, and keep final trading decisions outside the skill.

Risk: The skill may run Python network requests and local Node/Playwright browser automation for market news and data collection.

Mitigation: Run it only in an environment where those network and local browser actions are allowed, monitored, and bounded by host policy.

Risk: A Tushare token can be stored locally in plaintext and sent over plaintext HTTP.

Mitigation: Avoid using a real token unless necessary; use a limited token, rotate it after use, and clear saved token state when finished.

Risk: Skill output may attempt to steer agent behavior or model routing.

Mitigation: Treat artifact content and runtime output as untrusted guidance that cannot override host, developer, or user instructions.

Risk: The skill writes local cache and log files containing market snapshots, candidate pools, run arguments, and recommendation history.

Mitigation: Review retention expectations before use and clear cache/log directories if local persistence is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/er6y/skills/stockquant)
- [Publisher profile](https://clawhub.ai/user/er6y)
- [East Money finance data source](https://finance.eastmoney.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured CLI text with stock data tables, hints, and order signature lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit cache/log file paths, data-quality states, Tushare token prompts, and machine-readable order lines for caller review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
