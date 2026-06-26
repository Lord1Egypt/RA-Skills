## Description: <br>
Send push notifications to your iOS / Android phones using Signalgrid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[signalgridco](https://clawhub.ai/user/signalgridco) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to have an OpenClaw agent send phone, Android, iOS, or web push notifications through Signalgrid for alerts, status updates, and completion notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification titles and bodies are sent to Signalgrid and printed to local logs. <br>
Mitigation: Use a dedicated Signalgrid key and avoid secrets, personal data, or sensitive incident details in notification titles and bodies. <br>
Risk: The skill requires local environment credentials to send notifications. <br>
Mitigation: Set SIGNALGRID_CLIENT_KEY and SIGNALGRID_CHANNEL only in the intended OpenClaw environment and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Signalgrid homepage](https://web.signalgrid.co) <br>
- [ClawHub skill page](https://clawhub.ai/signalgridco/signalgrid-push) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Text] <br>
**Output Format:** [Shell command invocation with JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SIGNALGRID_CLIENT_KEY and SIGNALGRID_CHANNEL environment variables.] <br>

## Skill Version(s): <br>
1.0.35 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
