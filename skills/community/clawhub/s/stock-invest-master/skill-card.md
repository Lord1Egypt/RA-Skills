## Description: <br>
Stock Invest Master guides an agent through stock research for A-share, Hong Kong, and U.S. equities using layered qualitative, financial, valuation, risk, and market-cycle analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mickshu](https://clawhub.ai/user/mickshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to structure stock research, due diligence, valuation checks, report generation, and portfolio review for A-share, Hong Kong, and U.S. equities. Outputs should be treated as educational analysis rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report server may expose private investment research from ~/.stock-invest-master. <br>
Mitigation: Run the server only when needed, bind it to 127.0.0.1, restrict served file types, and stop it after reviewing reports. <br>
Risk: The skill may start a background HTTP server on port 8888. <br>
Mitigation: Prefer manual server startup, verify the listening address and port before use, and stop the service after each session. <br>
Risk: Stock analysis outputs may be mistaken for investment advice. <br>
Mitigation: Treat reports as educational research, independently verify data and assumptions, and make final investment decisions outside the agent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mickshu/stock-invest-master) <br>
- [Publisher Profile](https://clawhub.ai/user/mickshu) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Dao Analysis Method](references/dao-analysis-method.md) <br>
- [Data Source Notes](references/data-source-notes.md) <br>
- [A-Stock Data Retrieval](references/a-stock-data-retrieval.md) <br>
- [A-Stock Browser Data Fetch](references/a-stock-data-browser-fetch.md) <br>
- [News Judgment Framework](references/news-judgment-framework.md) <br>
- [Buffett Framework](references/buffett-framework.md) <br>
- [Graham Framework](references/graham-framework.md) <br>
- [Lynch Framework](references/lynch-framework.md) <br>
- [Fisher Framework](references/fisher-framework.md) <br>
- [Munger Framework](references/munger-framework.md) <br>
- [Marks Framework](references/marks-framework.md) <br>
- [Dalio Framework](references/dalio-framework.md) <br>
- [Soros Framework](references/soros-framework.md) <br>
- [Simons Framework](references/simons-framework.md) <br>
- [Duan Framework](references/duan-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with supporting text, generated code or shell commands, and optional local HTML report views.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports under ~/.stock-invest-master and may start a local report server on port 8888.] <br>

## Skill Version(s): <br>
3.9.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
