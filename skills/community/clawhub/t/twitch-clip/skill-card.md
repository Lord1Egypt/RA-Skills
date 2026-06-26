## Description: <br>
Creates Twitch clips of the current live stream via the Twitch API using configured Twitch credentials and a 30-second cooldown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Streamers, moderators, and agent operators use this skill to create Twitch clips from the current live broadcast when an explicit clip request is made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short trigger phrases may create unwanted Twitch clips if the agent listens too broadly. <br>
Mitigation: Configure the agent to run the skill only after explicit authorized clip requests, and rely on the built-in 30-second cooldown to reduce repeated clip creation. <br>
Risk: The skill requires Twitch credentials that can create clips for the configured broadcaster. <br>
Mitigation: Use a narrow Twitch token with only the clips:edit scope, keep it private, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Twitch App Console](https://dev.twitch.tv/console/apps) <br>
- [Twitch OAuth Authorization](https://id.twitch.tv/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=token&scope=clips:edit) <br>
- [Twitch Helix Users API](https://api.twitch.tv/helix/users) <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/twitch-clip) <br>
- [Publisher Profile](https://clawhub.ai/user/djc00p) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Shell output with clip identifiers and Twitch clip URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and Twitch environment variables; exits with a cooldown status when clip requests occur too frequently.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
