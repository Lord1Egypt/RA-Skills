## Description: <br>
Sets up the OpenClaw iOS app by detecting the local OpenClaw environment, starting the stats server when needed, and guiding the user through domain, Tailscale, LAN, or manual connection setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parham-dev](https://clawhub.ai/user/parham-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill after installing OpenClaw or when the iOS app cannot connect. It helps prepare the local gateway and stats server, then provides the connection URL and token details needed by the app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and displays the local OpenClaw gateway token, which can grant access if copied into logs, screenshots, or chat transcripts. <br>
Mitigation: Treat the token like a password, avoid sharing outputs that contain it, and rotate the token if it is exposed. <br>
Risk: Remote access setup can expose the OpenClaw gateway or stats paths outside the local machine. <br>
Mitigation: Prefer HTTPS or Tailscale for remote access and review reverse proxy settings before use. <br>
Risk: The skill may run an existing workspace stats_server.py or ensure_stats_server.sh file. <br>
Mitigation: Inspect those local files before letting the skill start them in environments with higher security requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parham-dev/skill-ios-setup) <br>
- [Publisher profile](https://clawhub.ai/user/parham-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and connection details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local gateway URLs, stats server status, and a gateway token that should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
