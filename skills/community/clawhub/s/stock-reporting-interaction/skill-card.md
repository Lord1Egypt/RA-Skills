## Description: <br>
Generates stock investment reports, financial charts, investment logs, alerts, and natural-language investment-assistant interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate premarket, postmarket, weekly, and stock-specific reports; render financial charts and dashboards; manage investment journals; configure alerts; and answer natural-language market questions. Outputs should be treated as informational analysis rather than professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive investment records through persistent logs, scheduled alerts, and external channel notifications. <br>
Mitigation: Enable cron jobs, memory logging, and channel pushes only after reviewing what data will be stored or sent and confirming the destination channels are appropriate. <br>
Risk: Generated buy/sell prices, stop-losses, targets, and market conclusions may be mistaken for regulated financial advice. <br>
Mitigation: Present outputs as informational analysis, retain disclaimers, and require user or professional review before acting on trading decisions. <br>
Risk: The runtime imports unbundled local stock_data_adapter code, so behavior depends on code outside the packaged artifact. <br>
Mitigation: Review and trust the local stock_data_adapter implementation before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuritu/stock-reporting-interaction) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Report generator](artifact/tools/report_generator.py) <br>
- [Chart renderer](artifact/tools/chart_renderer.py) <br>
- [Interactive dashboard](artifact/canvas/dashboard.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports, JSON result objects, PNG chart files, HTML dashboard updates, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY; imports local stock_data_adapter code from the surrounding environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
