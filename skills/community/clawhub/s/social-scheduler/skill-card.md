## Description: <br>
Schedules and publishes text, media, and thread posts across Discord, Reddit, Twitter/X, Mastodon, Bluesky, Moltbook, LinkedIn, and Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrsHorrid](https://clawhub.ai/user/MrsHorrid) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents, developers, and content operators use this skill to schedule, queue, publish, and monitor social posts across multiple platforms from a local CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured social platform credentials can enable public posting if exposed or misused. <br>
Mitigation: Use test or least-privilege social accounts first, store secrets outside command arguments and content calendars, and protect credential files. <br>
Risk: Scheduled queue files and dashboard access can expose or change pending public posts. <br>
Mitigation: Protect or disable storage/queue.json and the dashboard, and bind dashboard use to trusted local environments. <br>
Risk: Automated publishing can post unintended or harmful content publicly. <br>
Mitigation: Require explicit human or agent review before publishing or responding from production accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrsHorrid/social-scheduler) <br>
- [README](README.md) <br>
- [Complete usage guide](SKILL.md) <br>
- [Media upload guide](MEDIA-GUIDE.md) <br>
- [Moltbook usage guide](MOLTBOOK-USAGE.md) <br>
- [API research notes](API-RESEARCH.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local queue and analytics files, use stored credentials, and publish public posts through configured social platform APIs.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
