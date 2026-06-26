## Description: <br>
Decode QR codes, trace redirects, inspect gated destinations, and explain what the link actually needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vicky-v7](https://clawhub.ai/user/vicky-v7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to decode local QR images, trace URL redirects, identify app or login gates, and produce a clear diagnosis with next steps. It can also generate QR codes from text or URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local QR image files supplied to the agent. <br>
Mitigation: Use it only with images you intend the agent to inspect, and avoid sensitive QR images unless local analysis is acceptable. <br>
Risk: Tracing decoded URLs can contact external destinations and reveal that the link was accessed. <br>
Mitigation: Avoid tracing sensitive login, payment, invitation, or one-time QR codes unless making that external request is intended. <br>
Risk: The setup script may install the Python qrcode dependency into the current Python environment. <br>
Mitigation: Review setup.sh before running it, or run setup in an isolated environment if you do not want package changes in the current Python environment. <br>


## Reference(s): <br>
- [QR Bridge on ClawHub](https://clawhub.ai/vicky-v7/qr-bridge) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Structured Markdown diagnosis with JSON decoder output and inline shell, Swift, or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May compile a local Swift decoder, read local image paths, generate QR image files, and make outbound HTTP requests when tracing redirects.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
