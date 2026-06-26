## Description: <br>
Manage Zoom meetings, webinars, registrants, cloud recordings, and event workflows via the Zoom API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to discover and call Zoom tools through ClawLink for scheduling meetings, managing webinars and registrants, reviewing user settings, and accessing cloud recording workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ClawLink OAuth access to a connected Zoom account, which may expose meetings, recordings, registrants, user settings, and conversation data allowed by the granted permissions. <br>
Mitigation: Install only when the user trusts ClawLink to broker Zoom access, and review the Zoom permissions granted during connection. <br>
Risk: Create, update, registration, or delete actions can change Zoom resources or affect participants. <br>
Mitigation: Require a preview and explicit user approval before executing any write or destructive action. <br>
Risk: Some Zoom operations depend on account plan, add-on, recording, or registration settings. <br>
Mitigation: Check connection status and tool guidance first, then report Zoom plan or settings errors directly instead of assuming the capability is unavailable. <br>


## Reference(s): <br>
- [ClawHub Zoom Skill](https://clawhub.ai/hith3sh/zoom-meetings) <br>
- [Zoom API Documentation](https://developers.zoom.us/docs/api/) <br>
- [Zoom Meeting API Reference](https://developers.zoom.us/docs/api-reference/zoom-api/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live ClawLink Zoom tool catalog as the source of truth before executing calls.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
