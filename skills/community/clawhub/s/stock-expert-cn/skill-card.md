## Description: <br>
Professional stock analysis agent for technical and fundamental analysis, market reports, stock screening, and risk-aware trading guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sionyugg-a11y](https://clawhub.ai/user/sionyugg-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stock market reports, inspect technical indicators, screen candidate stocks, and produce portfolio risk notes. Outputs should be reviewed as informational analysis rather than treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the artifact publishes a real-looking Tushare API token. <br>
Mitigation: Treat the published token as compromised, revoke and rotate it, replace it with a placeholder, and require users to store their own credential outside skill files. <br>
Risk: Cron examples can generate recurring stock reports automatically. <br>
Mitigation: Enable scheduled jobs only when recurring reports are intended and review generated outputs before taking action. <br>
Risk: Stock analysis and buy, hold, or sell guidance may be inaccurate or unsuitable for a user's circumstances. <br>
Mitigation: Use outputs as informational analysis only and require independent financial review before investment decisions. <br>


## Reference(s): <br>
- [Stock Expert ClawHub page](https://clawhub.ai/sionyugg-a11y/stock-expert-cn) <br>
- [sionyugg-a11y publisher profile](https://clawhub.ai/user/sionyugg-a11y) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external market data services through configured Tushare and Finnhub credentials; stock analysis should be independently reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
