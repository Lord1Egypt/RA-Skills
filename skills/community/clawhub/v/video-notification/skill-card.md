## Description: <br>
Sends video notifications to specified mobile phone numbers through a configured IVVR video-notification service, using a server-side video file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhu-xiao-di](https://clawhub.ai/user/zhu-xiao-di) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to trigger video-notification API calls for one or more recipient phone numbers when the video file already exists on the configured server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipient phone numbers and server file paths are sent to the configured video-notification backend. <br>
Mitigation: Install only with a backend you control or trust, verify recipient numbers and file paths before sending, and avoid exposing unnecessary personal data. <br>
Risk: API credentials could be exposed if the service is configured over an insecure or temporary public tunnel. <br>
Mitigation: Use an HTTPS API_BASE_URL for production, keep API_KEY secret, and avoid temporary public tunnels for production deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhu-xiao-di/video-notification) <br>
- [Publisher profile](https://clawhub.ai/user/zhu-xiao-di) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text, json] <br>
**Output Format:** [JSON API response with success status, file_id, and message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_BASE_URL and secret API_KEY configuration; sends recipient phone numbers and server file paths to the configured backend.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
