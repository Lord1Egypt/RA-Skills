## Description: <br>
Soccer Lottery helps agents fetch soccer match data, analyze historical head-to-head results, and generate Markdown match-analysis reports with betting-style recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veezvg](https://clawhub.ai/user/veezvg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect Football-Data.org match data, run H2H-based analysis, and prepare Markdown reports for soccer match review. It is suited for informational pre-match analysis, not definitive betting advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive API keys could be exposed if users paste tokens into chat or prompts. <br>
Mitigation: Configure API keys locally or through a platform secret manager, and avoid sharing tokens in conversations. <br>
Risk: Betting recommendations may overstate confidence because current odds, injury, and broader recent-form integrations are incomplete. <br>
Mitigation: Treat outputs as informational analysis, review the data sources and assumptions, and avoid relying on the recommendations as financial advice. <br>
Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk over time. <br>
Mitigation: Pin and review dependencies before running the skill in a managed environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veezvg/veezvg-soccer-lottery) <br>
- [Football-Data.org](https://www.football-data.org/) <br>
- [Football-Data.org matches API](https://api.football-data.org/v4/matches) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON match data, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a locally configured Football-Data.org API key; odds and injury integrations are incomplete unless additional data sources are added.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
