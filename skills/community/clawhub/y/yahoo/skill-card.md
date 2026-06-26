## Description: <br>
Use Yahoo Finance for quotes, symbol search, watchlists, market briefs, and catalyst-aware stock decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve Yahoo Finance symbols, retrieve quote snapshots, compare watchlists, and turn market data into risk-aware thesis or no-trade decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and finance search terms are sent to Yahoo Finance. <br>
Mitigation: Use the skill only when sharing those market lookups with Yahoo is acceptable. <br>
Risk: The skill runs local Python scripts to fetch Yahoo Finance data. <br>
Mitigation: Review commands before execution and allow outbound access only to the disclosed Yahoo Finance endpoints. <br>
Risk: Optional local finance notes can create privacy exposure if sensitive account details are saved. <br>
Mitigation: Create ~/yahoo/ only with user approval and avoid storing broker credentials, account numbers, tax records, exact holdings, or other sensitive records. <br>


## Reference(s): <br>
- [ClawHub Yahoo Skill](https://clawhub.ai/ivangdavila/yahoo) <br>
- [Skill Homepage](https://clawic.com/skills/yahoo) <br>
- [Yahoo Finance Quote Pages](https://finance.yahoo.com/quote/{symbol}) <br>
- [Yahoo Finance Search Endpoint](https://query1.finance.yahoo.com/v1/finance/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally create local finance notes in ~/yahoo/ only with user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
