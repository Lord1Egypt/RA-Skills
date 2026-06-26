## Description: <br>
TG Cam App lets an agent query bound camera devices, current snapshots, events, event images, online status, and battery status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with TG camera credentials use this skill to let an agent check available cameras, retrieve current snapshots, inspect events and event images, generate app links, and report online or battery status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive camera API credentials and may store them in local OpenClaw configuration if they are provided during a session. <br>
Mitigation: Configure TIVS_CLI_ID and TIVS_API_KEY through OpenClaw's secure environment or secret mechanism, and do not paste or echo real API keys in chat. <br>
Risk: Valid credentials allow access to camera device lists, snapshots, event images, status, and battery data. <br>
Mitigation: Install only when the camera provider is trusted, use credentials scoped to the intended account or devices, and review the data access before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyfinec/tg-cam-app) <br>
- [TG camera skill API base](https://skill.webcamapp.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Images, Configuration guidance] <br>
**Output Format:** [Concise natural-language answers with optional Markdown app links and camera images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIVS_CLI_ID and TIVS_API_KEY credentials; avoids echoing API keys and long raw JSON responses.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
