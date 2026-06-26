## Description: <br>
Send daily 08:00 weather reports for Tübingen using open-meteo.com, including current conditions, today’s high/low, and rain chance, with optional local storage and Telegram forwarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zopyx](https://clawhub.ai/user/zopyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users who want automated local weather updates for Tübingen use this skill to fetch a concise Open-Meteo summary, optionally save it as a text file, and send it through an agent-managed Telegram workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add a daily 08:00 cron workflow that repeatedly fetches and forwards weather summaries. <br>
Mitigation: Only enable the cron job when daily execution is desired and review the schedule, timezone, and notification target before deployment. <br>
Risk: The script can write local weather text files to a user-provided output path. <br>
Mitigation: Confirm the saved output path is acceptable for local text files before running with --output. <br>
Risk: Weather results depend on availability and correctness of a public third-party weather API. <br>
Mitigation: Treat the output as informational weather guidance and check errors or source data when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zopyx/tuebingen-weather) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=48.5216&longitude=9.0576) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text weather summary with optional saved text file and cron configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the public Open-Meteo API without API keys; optional output path controls where the weather summary is saved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
