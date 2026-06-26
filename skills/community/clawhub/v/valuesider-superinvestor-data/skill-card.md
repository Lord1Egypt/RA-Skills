## Description: <br>
Fetches Superinvestors' 13F portfolio holdings and buy/sell activity from ValueSider for guru portfolio, holdings, and trading-activity questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and financial researchers use this skill to fetch and summarize public ValueSider 13F portfolio holdings and buy/sell activity for named superinvestors or funds. Results should be treated as public financial data, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public ValueSider pages for manager or fund lookups. <br>
Mitigation: Avoid including confidential research notes or private investment context in lookup text. <br>
Risk: The skill returns public financial portfolio data that may be stale, incomplete, or unsuitable for investment decisions. <br>
Mitigation: Present results as public data from ValueSider and do not treat them as financial advice. <br>
Risk: Optional local parsing can require installing Python dependencies. <br>
Mitigation: Review the dependency list before installation and run parsing in an appropriate local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laimiaohua/valuesider-superinvestor-data) <br>
- [ValueSider](https://valuesider.com) <br>
- [ValueSider value investors](https://valuesider.com/value-investors) <br>
- [ValueSider guru portfolio](https://valuesider.com/guru/{guru_slug}/portfolio) <br>
- [ValueSider guru portfolio activity](https://valuesider.com/guru/{guru_slug}/portfolio-activity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional JSON parsed from ValueSider page content and inline shell commands for local parsing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require web fetching public ValueSider pages and optional Python dependencies for local parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
