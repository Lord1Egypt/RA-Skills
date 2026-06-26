## Description: <br>
Enables an agent to query bound Tange camera devices, capture current snapshots, retrieve event summaries and images, and check device online status and battery state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a credentialed camera service: list bound devices, request snapshots, review camera events and event images, and report online status or battery information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private camera data and trigger snapshots through the configured service. <br>
Mitigation: Install only when the user intends to grant this camera access, and use explicit camera and device wording before requesting snapshots or event images. <br>
Risk: The skill relies on persistent TIVS_CLI_ID and TIVS_API_KEY credentials. <br>
Mitigation: Confirm where credentials are stored, avoid exposing the API key in chat output, and protect or rotate credentials as needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flyfinec/tg-cam-api) <br>
- [Camera Skill API Base](https://skill.webcamapp.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with concise answers, API-derived summaries, images when available, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIVS_CLI_ID and TIVS_API_KEY credentials; avoids exposing raw API keys and long raw JSON responses.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
