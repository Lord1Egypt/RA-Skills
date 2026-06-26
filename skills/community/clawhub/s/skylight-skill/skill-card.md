## Description: <br>
Interact with a Skylight Calendar smart display to manage calendar events, chores, lists, task box items, rewards, frame information, and devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riyadchowdhury](https://clawhub.ai/user/riyadchowdhury) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Skylight Calendar users and household administrators use this skill to ask an agent for curl-based guidance to view or create calendar events, chores, lists, task box items, rewards, frame details, and devices for their own Skylight smart display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle Skylight account credentials or authorization tokens. <br>
Mitigation: Use only your own account, keep credentials and tokens out of shared logs or prompts, and rotate tokens or passwords if exposed. <br>
Risk: The optional token-capture path uses HTTPS proxy interception and a trusted proxy certificate. <br>
Mitigation: Prefer the email/password path when acceptable, use proxy-token capture only when you understand TLS interception, and remove the trusted proxy certificate afterward. <br>
Risk: The integration uses an unofficial, reverse-engineered API whose endpoints may change. <br>
Mitigation: Review generated commands before running them and re-check behavior after Skylight app or API changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/riyadchowdhury/skylight-skill) <br>
- [Publisher profile](https://clawhub.ai/user/riyadchowdhury) <br>
- [Skylight homepage](https://ourskylight.com) <br>
- [Skylight app endpoint](https://app.ourskylight.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Skylight frame ID and either Skylight account credentials or a pre-captured authorization token.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact README lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
