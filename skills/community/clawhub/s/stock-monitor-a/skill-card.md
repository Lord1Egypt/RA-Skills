## Description: <br>
stock-monitor-a monitors selected China A-share prices using Sina Finance quotes, supports threshold-based alerts, skips invalid pre-market and post-market quotes, and records local price logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likepost](https://clawhub.ai/user/likepost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to check configured A-share prices, receive price or percentage-change alerts during configured trading windows, and review daily or recent price logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect stock codes, thresholds, trading schedule, or delivery target can cause missed, repeated, or unintended alerts. <br>
Mitigation: Review stock_config.json before installing or scheduling the skill, especially the stock list, price thresholds, cron expression, timezone, and delivery_target. <br>
Risk: The skill creates local monitoring history and once-per-day alert state files in the skill directory. <br>
Mitigation: Restrict access to the skill directory and clear or disable those local files if retained stock-monitoring history is not desired. <br>
Risk: Market quote fetches can fail or return invalid data outside supported trading conditions. <br>
Mitigation: Treat alerts and summaries as monitoring aids, verify important prices against an authoritative source, and do not rely on the skill as sole financial decision support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/likepost/stock-monitor-a) <br>
- [Publisher profile](https://clawhub.ai/user/likepost) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Skill metadata](artifact/skill.json) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Files] <br>
**Output Format:** [Plain text responses with local JSON state and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports check, query, log, and log_history actions; creates local alert state and daily price log files when run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
