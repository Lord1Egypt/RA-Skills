## Description: <br>
Get stock prices, quotes, fundamentals, earnings, options, dividends, and analyst ratings using Yahoo Finance. Uses yfinance library - no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajanraj](https://clawhub.ai/user/ajanraj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to look up market data from Yahoo Finance, including prices, quotes, fundamentals, earnings, dividends, analyst ratings, options chains, history, comparison tables, and symbol search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact suggests piping remote uv installer scripts directly into a shell. <br>
Mitigation: Prefer package-manager installation for uv, such as Homebrew or pip, before using remote installer scripts. <br>
Risk: The artifact references a yf executable script that is not included in the provided artifact files. <br>
Mitigation: Confirm the yf script is supplied by the installed release before relying on the CLI workflow. <br>
Risk: Yahoo Finance data requests may be rate limited or unavailable for some symbols or data categories. <br>
Mitigation: Handle connection errors, verify symbols with search, and treat unavailable options, dividends, or other data as expected service limitations. <br>


## Reference(s): <br>
- [Yahoo Finance skill page](https://clawhub.ai/ajanraj/yahoo-finance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI-formatted financial data tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; data availability and rate limits depend on Yahoo Finance and yfinance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
