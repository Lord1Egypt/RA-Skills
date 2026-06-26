## Description: <br>
SecondMind gives an OpenClaw agent persistent three-tier memory, social-context extraction, project tracking, and proactive proposal generation using OpenRouter-hosted models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Emphaiser](https://clawhub.ai/user/Emphaiser) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use SecondMind to configure persistent conversation memory, search prior sessions, archive reset-bound sessions, manage proposals and projects, and receive proactive suggestions through CLI or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw session history and stores long-term memory, including emotional or social-context inferences. <br>
Mitigation: Enable it only for workspaces where that retention is acceptable, review config.json before first run, and verify database retention or reset behavior before use on sensitive conversations. <br>
Risk: Selected content may be sent to OpenRouter-hosted models and, when notifications are enabled, to Telegram. <br>
Mitigation: Configure OpenRouter and notification settings deliberately, keep Telegram disabled unless needed, and avoid processing confidential sessions that should not leave the local environment. <br>
Risk: Setup can create recurring background jobs that continue ingesting and processing session files. <br>
Mitigation: Review installed cron or Task Scheduler entries after setup and remove or pause recurring jobs when background processing is not desired. <br>


## Reference(s): <br>
- [SecondMind ClawHub Release](https://clawhub.ai/Emphaiser/secondmind) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [OpenRouter Models](https://openrouter.ai/models) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Node.js scripts that read OpenClaw session files, update a SQLite database, call OpenRouter, and optionally send Telegram notifications.] <br>

## Skill Version(s): <br>
1.4.0 (source: evidence release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
