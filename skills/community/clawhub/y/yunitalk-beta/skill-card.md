## Description: <br>
该技能用于 OpenClaw 接入与你聊聊，实现聊聊与 OpenClaw 的对话 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackbeans](https://clawhub.ai/user/blackbeans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to connect OpenClaw with Talk Robots so users can converse through the Yunitalk chat interface and send text or file events back to a robot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated QR/base64 initialization commands and signed request URLs can expose usable OpenClaw or Talk Robots access details. <br>
Mitigation: Run setup in a private terminal, avoid sharing screenshots or logs, and redact initialization strings, request URLs, signatures, and tokens before storing output. <br>
Risk: The skill intentionally connects live OpenClaw and Talk Robots credentials. <br>
Mitigation: Install only from a trusted publisher and use it only in environments where those credentials are meant to be connected. <br>
Risk: Dry-run or troubleshooting output can print signed request details. <br>
Mitigation: Keep dry-run output out of shared logs and rotate affected robot keys or OpenClaw tokens if those details are exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blackbeans/skills/yunitalk-beta) <br>
- [README.md](README.md) <br>
- [ROBOT_SEND_API.md](ROBOT_SEND_API.md) <br>
- [yntalk-openclaw-init README](npm/yntalk-openclaw-init/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON payloads, multipart form requests, and QR/base64 initialization strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce signed request URLs and initialization strings that contain credential-bearing material.] <br>

## Skill Version(s): <br>
0.8.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
