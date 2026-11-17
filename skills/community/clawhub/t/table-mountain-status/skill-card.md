## Description:

Fetches and reports Table Mountain Aerial Cableway operating status, weather, queue, schedule, and update time from the official weather API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zopyx](https://clawhub.ai/user/zopyx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to check Table Mountain cableway availability and related weather, queue, and schedule information. It can also support short-lived polling jobs that send status summaries through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script makes network requests to fetch live status data.

Mitigation: Use the default official API URL unless there is a reviewed need to override it, and keep the HTTP timeout bounded.

Risk: The helper script writes local files at a caller-provided output path.

Mitigation: Keep output under a dedicated directory such as data/table-mountain and review custom output paths before running automation.

Risk: Automation examples can create recurring Telegram reporting jobs.

Mitigation: Use temporary schedules for alert windows and review, disable, or remove cron jobs after the alert period ends.

## Reference(s):

- [Official Table Mountain weather API](https://cms.tablemountain.net/admin/actions/submissions/default/weather-api)
- [ClawHub skill page](https://clawhub.ai/zopyx/skills/table-mountain-status)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus text or JSON status output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can write status summaries under a local output path and prints the same status to stdout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
