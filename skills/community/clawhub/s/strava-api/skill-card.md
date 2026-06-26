## Description: <br>
Official Strava OAuth integration for OpenClaw. Use to connect/authorize Strava, store+refresh tokens, and fetch workout/activity data (runs/rides/etc.) for today/yesterday or a date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swang62](https://clawhub.ai/user/swang62) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to authorize Strava, refresh stored tokens, and fetch workout activity data for daily summaries, weekly mileage, activity lists, or wellness workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Strava OAuth credentials, refresh tokens, and workout activity data. <br>
Mitigation: Install only if the publisher is trusted, keep the token file private, and set STRAVA_TOKEN_PATH to an appropriate private location. <br>
Risk: Loopback OAuth mode can expose authorization flow risk if used with a non-local redirect URI. <br>
Mitigation: Use loopback mode only with a localhost or 127.0.0.1 redirect URI, as documented by the skill. <br>


## Reference(s): <br>
- [Strava API Quick Reference](references/strava_api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/swang62/strava-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON activity output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Strava OAuth configuration and writes fetched activity data to a caller-specified JSON file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
