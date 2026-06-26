## Description: <br>
Interact with Strava via the strava-client-cli Python tool. Use for viewing activities, athlete profiles, stats, and exporting data. Covers setup (creating a Strava account, API app, and OAuth) and all CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geodeterra](https://clawhub.ai/user/geodeterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Strava users use this skill to install and operate a Strava CLI for OAuth setup, profile and activity queries, stats review, and JSON data export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through Strava OAuth and stores access and refresh tokens locally in ~/.config/strava-cli/tokens.json. <br>
Mitigation: Treat the token file as a secret, avoid committing or sharing it, and use restrictive private-directory and 600-style file permissions where possible. <br>


## Reference(s): <br>
- [ClawHub Strava CLI skill page](https://clawhub.ai/geodeterra/strava-cli) <br>
- [Strava API application settings](https://www.strava.com/settings/api) <br>
- [Strava OAuth authorization endpoint](https://www.strava.com/oauth/authorize) <br>
- [Strava OAuth token endpoint](https://www.strava.com/oauth/token) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
