## Description: <br>
Generate and send a 5-day Tübingen weather graphic (PNG) from open-meteo.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zopyx](https://clawhub.ai/user/zopyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate a local PNG weather graphic and terminal summary for Tübingen forecasts, with optional user-configured scheduling or Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script fetches public forecast data from Open-Meteo and writes a PNG to local storage. <br>
Mitigation: Run it only in environments where outbound access to Open-Meteo and local file creation at the selected output path are acceptable. <br>
Risk: The example cron and Telegram workflow can send automated daily messages if the user installs it. <br>
Mitigation: Add the schedule only when daily delivery is intended, and remove the cron entry when automated messages are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zopyx/tuebingen-weather-graphics) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=48.5216&longitude=9.0576) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration] <br>
**Output Format:** [PNG file plus terminal text summary and optional cron/Telegram configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Open-Meteo forecast data and saves the generated graphic to a user-selected local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
