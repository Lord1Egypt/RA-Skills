## Description: <br>
Stock and Crypto Data information pull skill with 56+ Yahoo Finance-backed tools for prices, fundamentals, earnings, dividends, options, crypto, forex, commodities, news, and related market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkcair](https://clawhub.ai/user/lkcair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route finance questions to Yahoo Finance-backed stock, crypto, forex, commodity, earnings, dividend, options, news, and comparison lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yahoo Finance-backed self-test, complete analysis, comparison, and bulk query flows can generate many outbound market-data requests. <br>
Mitigation: Use the skill only for expected finance lookups, narrow routing rules to explicit finance questions, and avoid self-test or complete analysis unless the request volume is acceptable. <br>
Risk: Dependency or runtime drift can make finance lookups inconsistent across environments. <br>
Mitigation: Install the skill in an isolated virtual environment and pin dependencies when repeatable behavior matters. <br>
Risk: Market data can be delayed, unavailable, or incomplete and should not be treated as financial advice. <br>
Mitigation: Treat returned data as informational, verify important figures with authoritative sources, and apply normal investment or compliance review before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lkcair/stocks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text finance responses with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on Yahoo Finance availability and may reflect delayed or incomplete market data.] <br>

## Skill Version(s): <br>
4.2.1 (source: server release evidence, created 2026-05-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
