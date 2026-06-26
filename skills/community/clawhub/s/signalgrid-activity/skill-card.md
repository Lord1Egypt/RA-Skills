## Description: <br>
Send Live-Activities & Ongoing-Notifications to your iOS / Android phones using Signalgrid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[signalgridco](https://clawhub.ai/user/signalgridco) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to start, update, and finish Signalgrid live activities or ongoing notifications for mobile devices during tasks such as deployments, backups, imports, or CI jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification titles, bodies, progress values, and related metadata are sent to Signalgrid. <br>
Mitigation: Avoid sending secrets or sensitive operational details in notification content. <br>
Risk: The skill requires a Signalgrid client key and channel in the OpenClaw environment. <br>
Mitigation: Use a revocable or scoped Signalgrid key where available and store it only in the configured environment variable mechanism. <br>
Risk: Start, update, and end behavior is externally visible and depends on the Signalgrid service and local tool access. <br>
Mitigation: Test the full notification lifecycle before relying on it for important alerts. <br>


## Reference(s): <br>
- [Signalgrid Activity on ClawHub](https://clawhub.ai/signalgridco/signalgrid-activity) <br>
- [Signalgrid account and service](https://web.signalgrid.co) <br>
- [Signalgrid publisher profile](https://clawhub.ai/user/signalgridco) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON status output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the SIGNALGRID_CLIENT_KEY and SIGNALGRID_CHANNEL environment variables.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
