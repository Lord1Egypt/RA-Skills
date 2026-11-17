## Description:

Provides daily weather information and clothing advice for Longli County, Guizhou by scraping China Weather data and applying local rule-based recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zonghua-dev](https://clawhub.ai/user/zonghua-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate scheduled Chinese-language Longli County weather reports with clothing advice, including cron configuration for weekday morning delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured weather source uses HTTP, so weather data could be tampered with in transit.

Mitigation: Use an HTTPS endpoint if China Weather supports one, or run the skill only on trusted networks and review unexpected report content.

Risk: The scraper depends on China Weather page structure and may return fallback output if the page changes.

Mitigation: Monitor cron output for fallback messages and update the parser selectors when upstream markup changes.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Run the scripts in a virtual environment and pin tested versions of requests and beautifulsoup4.

## Reference(s):

- [Weather Longli ClawHub page](https://clawhub.ai/zonghua-dev/skills/weather-longli)
- [China Weather Longli forecast source](http://www.weather.com.cn/weather/101260408.shtml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text Chinese weather report with optional YAML cron configuration and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an optional local JSONL weather log when the bundled daily report script runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
