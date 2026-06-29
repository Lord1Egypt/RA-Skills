## Description: <br>
Quant Strategy Searcher connects to a remote strategy database to search quantitative stock strategies and generate AI-assisted individual stock analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdyz](https://clawhub.ai/user/gdyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find quantitative stock strategies, inspect holdings, and generate traceable research-style reports covering financial metrics, news sentiment, and follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a password for a stated remote MySQL strategy database. <br>
Mitigation: Use a least-privilege database password supplied through DB_PASSWORD and avoid sharing the credential outside the runtime environment. <br>
Risk: Proxy environment values may be logged when proxy variables contain credentials. <br>
Mitigation: Avoid running with credential-bearing proxy variables, restrict log access, or review the skill before installation to remove proxy value logging. <br>
Risk: Outputs may be mistaken for investment advice. <br>
Mitigation: Treat generated reports as investment research support and require human review before any trading or portfolio decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdyz/quant-strategy-searcher) <br>
- [ClawHub metadata homepage](https://clawhub.ai/GDYZ/quant-strategy-searcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured analysis sections and JSON-style scoring blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and DB_PASSWORD for the remote MySQL strategy database.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
