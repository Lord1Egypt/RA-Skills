## Description: <br>
Monitors configured stocks during trading sessions and sends Feishu voice alerts for call-auction moves, limit-up or limit-down events, and 10-minute amplitude changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anightmare2](https://clawhub.ai/user/Anightmare2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers configure a stock watchlist and alert thresholds so an agent can monitor market-session price movement and notify a Feishu chat when configured events occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu and Noiz credentials for alert delivery. <br>
Mitigation: Use dedicated low-privilege credentials and avoid placing secrets in shared shell history, logs, or reusable configuration. <br>
Risk: The monitor can invoke a neighboring feishu-edge-tts voice-sending script when that directory is present. <br>
Mitigation: Inspect or remove the neighboring voice-sending dependency before enabling voice alerts. <br>
Risk: Cron examples can cause recurring Feishu stock-alert messages. <br>
Mitigation: Enable scheduled execution only when recurring stock-alert messages are intended and review the configured cadence. <br>
Risk: The server security verdict is suspicious because the skill mostly matches its purpose but can run an unreviewed neighboring voice-sending script while requiring alert credentials. <br>
Mitigation: Review the skill before installation, scan the shell scripts, and test with non-production credentials before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anightmare2/stock-monitor-siyou) <br>
- [Publisher profile](https://clawhub.ai/user/Anightmare2) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=$stock_code) <br>
- [Tencent stock data endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=$market$code,day,,,1) <br>
- [NetEase stock data endpoint](https://api.money.126.net/data/feed/${prefix}${code}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and stock-alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell execution, stock configuration, Feishu credentials, and a Noiz API key for voice-alert operation.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and clawhub.yaml; package.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
