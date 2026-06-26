## Description: <br>
Smart Surprise proactively sends personalized casual messages at random intervals, learns user preferences, and schedules future check-ins through an OpenClaw cron chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turingcorp-net](https://clawhub.ai/user/turingcorp-net) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to make an OpenClaw assistant initiate warm, varied check-ins through a configured messaging channel. It is intended for proactive greetings, tips, wellbeing check-ins, weather or news prompts, and optional calendar reminders based on user preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can message users on its own at random intervals until its cron chain is removed. <br>
Mitigation: Confirm the user wants proactive messages, configure timezone, quiet hours, channel target, and interval bounds before activation, and periodically review cron jobs. <br>
Risk: The skill can silently learn and persist user topic preferences. <br>
Mitigation: Review topics.md periodically and correct preferences manually when they do not match the user's intent. <br>
Risk: The optional calendar topic may read Google Calendar OAuth credentials. <br>
Mitigation: Disable the calendar topic unless calendar reminders are needed and provide credential files only after confirming the user trusts this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/turingcorp-net/smart-surprise) <br>
- [Configuration Reference](references/config.md) <br>
- [Setup Procedure](references/setup.md) <br>
- [Topics Reference](references/topics.md) <br>
- [Weather Data Endpoint](https://wttr.in/{location}?format=j1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language messages with Markdown setup guidance, inline shell commands, and JSON configuration or runtime state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update topics.md preferences and next_run.json scheduling state during operation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
