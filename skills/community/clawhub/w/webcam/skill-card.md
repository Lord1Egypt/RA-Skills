## Description: <br>
Webcam helps an agent retrieve bound camera devices, current snapshots, event summaries, event images, online status, and battery state through the camera service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with bound webcam devices use this skill to inspect available cameras, view current snapshots, review recent events or event images, and check online status or battery state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private camera snapshots, event images, device status, and battery data for bound cameras. <br>
Mitigation: Install it only when the user trusts the camera service endpoint and is comfortable granting this level of camera access. <br>
Risk: The skill stores provided TIVS_CLI_ID and TIVS_API_KEY credentials locally in openclaw.json. <br>
Mitigation: Treat those values as private credentials, avoid exposing them in chat, and remove or rotate them when persistent access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyfinec/webcam) <br>
- [Webcam Skill API Base](https://skill.webcamapp.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown summaries with retrieved images or concise status details when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TIVS_CLI_ID and TIVS_API_KEY credentials supplied by the user; avoids echoing the API key in chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
