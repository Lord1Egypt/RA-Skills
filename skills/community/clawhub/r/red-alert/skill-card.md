## Description: <br>
Israel Red Alert API - real-time and historical rocket/missile alert data. Query alerts by city, time range, generate shelter time stats. Uses redalert.orielhaim.com (socket.io for real-time) and tzevaadom.co.il (REST for history). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query recent Israeli emergency alert history, monitor real-time alert events, and generate city-level shelter-time summaries for downstream reporting or visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated real-time access can use RED_ALERT_API_KEY. <br>
Mitigation: Set RED_ALERT_API_KEY only when authenticated real-time access is needed, store it as a secret, and rotate it according to local credential policy. <br>
Risk: Persistent listeners can write local alert logs under /data/clawd/tmp/redalert-*.jsonl. <br>
Mitigation: Periodically delete or rotate the JSONL files when running persistent monitoring. <br>
Risk: Real-time monitoring depends on the npm socket.io-client dependency. <br>
Mitigation: Review the npm dependency before installing or enabling real-time scripts. <br>


## Reference(s): <br>
- [Red Alert Skill Endpoint Inventory](references/ENDPOINTS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dannyshmueli/red-alert) <br>
- [RedAlert API](https://redalert.orielhaim.com/) <br>
- [Tzeva Adom Alert History API](https://api.tzevaadom.co.il/alerts-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can emit text summaries, JSON summaries, chart JSON, table JSON, and JSON lines for real-time alerts.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
