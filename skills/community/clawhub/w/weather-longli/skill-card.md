## Description: <br>
Weather Longli fetches public Longli County, Guizhou weather data and generates a daily clothing recommendation with optional OpenClaw cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zonghua-dev](https://clawhub.ai/user/zonghua-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to get a scheduled Longli County weather summary and practical clothing advice without using a paid weather API. It is suited for OpenClaw cron delivery or manual command-line runs. <br>

### Deployment Geography for Use: <br>
Global, for weather reporting about Longli County, Guizhou, China. <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public web requests to fetch Longli County weather data. <br>
Mitigation: Run it only in environments where this outbound request is acceptable and expect failures if the weather page is unavailable or changes structure. <br>
Risk: The included cron example can run the report automatically on a recurring schedule. <br>
Mitigation: Review and adjust the cron schedule before enabling it. <br>
Risk: The daily report script can keep a local JSONL weather log. <br>
Mitigation: Review the log path and retention expectations for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zonghua-dev/weather-longli) <br>
- [Publisher profile](https://clawhub.ai/user/zonghua-dev) <br>
- [China Weather Network Longli page](http://www.weather.com.cn/weather/101260408.shtml) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text weather report with YAML cron and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report may include temperature range, weather conditions, wind, clothing advice, and a local JSONL weather log when the daily script runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
