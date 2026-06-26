## Description: <br>
TG Cam Claw helps an agent query bound camera devices, view current snapshots, retrieve event records and event images, and check device status and battery level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to let an agent inspect authorized TG camera devices, fetch snapshots or event images, summarize camera events, and report online status or battery level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access privacy-sensitive camera snapshots, event images, and device event history. <br>
Mitigation: Install and use it only when authorized to access the linked cameras, and scope requests to the devices and time ranges the user intends. <br>
Risk: The skill requires sensitive credentials, including TIVS_API_KEY, which may be saved in local OpenClaw configuration. <br>
Mitigation: Treat TIVS_API_KEY like a password, avoid echoing it in chat, and rotate or remove it if it is exposed. <br>
Risk: Broad requests such as checking what happened today may cause the agent to inspect camera events more widely than intended. <br>
Mitigation: Clarify the target device and time range before event queries, and summarize only confirmed fields returned by the service. <br>


## Reference(s): <br>
- [TG Cam Claw ClawHub page](https://clawhub.ai/flyfinec/tg-cam-claw) <br>
- [TG Cam Skill API base](https://skill.webcamapp.cc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Concise Markdown summaries with images or structured camera status details when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TIVS_CLI_ID and TIVS_API_KEY credentials; image URLs may be signed and should be handled without exposing raw secrets.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata and skill request header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
