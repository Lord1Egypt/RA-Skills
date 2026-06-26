## Description: <br>
AI-powered financial data assistant for stock analysis and global market overview that combines QVeris data sources for company profiles, quotes, fundamentals, valuation, analyst ratings, and news sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buxibuxi](https://clawhub.ai/user/buxibuxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve QVeris-backed market data and generate stock analysis or global market overview summaries. It is intended for informational financial data workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-related prompts, tickers, and parameters are sent to qveris.ai using QVERIS_API_KEY. <br>
Mitigation: Install only when that data sharing is acceptable, scope and monitor the API key, and track QVeris usage or quota. <br>
Risk: Market data and analysis summaries may be delayed, incomplete, or mistaken for investment advice. <br>
Mitigation: Require timestamps, delay notices, unavailable-data notes, and the skill's investment-advice disclaimer in user-facing output. <br>
Risk: Ambiguous triggers or helper-script usage may cause unexpected QVeris calls. <br>
Mitigation: Confirm the user's finance-data intent before auto-invocation when the request is unclear, and keep helper execution limited to the bundled QVeris client. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [Tool Routing](references/tool-routing.md) <br>
- [Output Templates](references/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with tables, timestamps, disclaimers, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data timestamps, note possible quote delay, cite unavailable dimensions when calls fail, and state that results are not investment advice.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
