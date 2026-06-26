## Description: <br>
Track and manage Strava workouts, athlete stats, routes, segments, and club activities via the Strava API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Strava account through ClawLink, inspect athlete and activity data, explore routes and segments, and perform confirmed account-changing Strava actions from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use OAuth-backed Strava access and may expose or modify account, activity, route, club, gear, kudos, comment, or upload data according to granted scopes. <br>
Mitigation: Install only when the user trusts ClawLink to broker the Strava OAuth connection, review requested Strava scopes during OAuth, and require a clear preview plus explicit confirmation before any write or account-changing action. <br>
Risk: Activity uploads may process personal workout files and must represent activity data the user owns. <br>
Mitigation: Confirm the user owns the uploaded activity data and preview upload parameters before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/strava-activities) <br>
- [Strava API Documentation](https://developers.strava.com/docs/reference/) <br>
- [Strava API Overview](https://developers.strava.com/) <br>
- [Strava Authentication](https://developers.strava.com/docs/auth/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Strava OAuth account through ClawLink; write actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
