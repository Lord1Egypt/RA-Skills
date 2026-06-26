## Description: <br>
TG Cam Test helps an agent query bound camera devices, capture current snapshots, review events and event images, and check online status or battery level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub users with TG Cam/webcamapp.cc camera credentials use this skill to inspect authorized devices, request snapshots, review event history and images, and check device status. It is intended for device-list, snapshot, event lookup, event-image, online-status, and battery queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera credentials can grant access to device information, snapshots, event images, status, and battery data. <br>
Mitigation: Configure credentials through secure OpenClaw environment or secret settings, avoid pasting API keys in chat, and rotate the API key if it is exposed. <br>
Risk: Snapshot and event-image requests can capture private scenes and may consume service storage or traffic. <br>
Mitigation: Request images only for authorized devices and only when needed; avoid repeated or unnecessary snapshot calls. <br>
Risk: The skill depends on the TG Cam/webcamapp.cc service and publisher-operated API. <br>
Mitigation: Install and use it only if the user trusts the publisher and the camera service. <br>


## Reference(s): <br>
- [TG Cam Test ClawHub page](https://clawhub.ai/flyfinec/tg-cam-api-test) <br>
- [TG Cam Skill API base](https://skill-test.webcamapp.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown or concise text responses, with optional image content and JSON-backed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIVS_CLI_ID and TIVS_API_KEY; image results may use signed URLs that should remain intact.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata and X-Skill-Version header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
