## Description: <br>
Decide whether OpenClaw should send a spontaneous casual message during periodic checks, and when it should, choose a natural interaction type plus concise guidance for how to deliver it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fjrevoredo](https://clawhub.ai/user/fjrevoredo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agents use this skill during scheduled checks to decide whether to send an occasional low-pressure proactive message and, when appropriate, how to shape that message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use enabled context sources such as calendar, smart-home, traffic, market, news, and weather integrations to make proactive messages feel timely. <br>
Mitigation: Install only when occasional proactive casual messages are desired, and review which OpenClaw integrations are enabled before use. <br>
Risk: Context-aware messages can become misleading or privacy-sensitive if fresh, reliable context is unavailable. <br>
Mitigation: Use real-world or account-backed context only when it is reliable, fresh, and relevant; otherwise keep the message general and low-pressure. <br>


## Reference(s): <br>
- [Simple Random Interaction Designer on ClawHub](https://clawhub.ai/fjrevoredo/simple-random-interaction-designer) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON decision object with optional interaction type and interaction description] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local randomness; outputs only a final yes or no decision, with interaction guidance included only for yes decisions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
