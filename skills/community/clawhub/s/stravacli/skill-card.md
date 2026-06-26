## Description: <br>
Use the stravacli terminal tool to access Strava data and perform limited activity update or upload actions when users request Strava metrics, history, exports, or CLI automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brainsoft-Raxat](https://clawhub.ai/user/Brainsoft-Raxat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Strava CLI authentication, read Strava profile and activity data, export routes, and perform confirmed activity updates or uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external stravacli project that can access a user's Strava account. <br>
Mitigation: Install only if the external project is trusted and review Strava permissions during login. <br>
Risk: The skill supports limited write actions such as activity updates and uploads. <br>
Mitigation: Require explicit user confirmation before running any activity update or upload command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Brainsoft-Raxat/stravacli) <br>
- [strava-cli source repository](https://github.com/Brainsoft-Raxat/strava-cli) <br>
- [strava-cli latest release](https://github.com/Brainsoft-Raxat/strava-cli/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers --json for reusable command output; activity updates and uploads require explicit confirmation.] <br>

## Skill Version(s): <br>
2.2.98 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
