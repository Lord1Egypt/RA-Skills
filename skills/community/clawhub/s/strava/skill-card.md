## Description: <br>
Load and analyze Strava activities, stats, and workouts using the Strava API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bohdanpodvirnyi](https://clawhub.ai/user/bohdanpodvirnyi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve Strava activities, athlete profile data, workout statistics, and token refresh commands for fitness analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Strava OAuth access and handles access tokens, refresh tokens, client IDs, and client secrets. <br>
Mitigation: Treat all Strava credentials and tokens as secrets, restrict configuration file permissions, and rotate or revoke Strava credentials if token output is exposed. <br>
Risk: Token refresh commands can print live token values, which may be captured in shell history, logs, or shared terminal output. <br>
Mitigation: Avoid running refresh commands in logged environments and do not commit, paste, or share generated token values. <br>


## Reference(s): <br>
- [ClawHub Strava Skill](https://clawhub.ai/bohdanpodvirnyi/strava) <br>
- [Strava Developers](https://developers.strava.com/) <br>
- [Strava API Reference](https://developers.strava.com/docs/reference/) <br>
- [Create Strava API Application](https://www.strava.com/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl against the Strava API and requires STRAVA_ACCESS_TOKEN; token refresh also requires STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, and STRAVA_REFRESH_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
