## Description: <br>
Smart Model Switcher classifies image, coding, reasoning, writing, and general tasks, then recommends or switches the active OpenClaw session to a matching configured model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route multimodal, coding, reasoning, writing, and general chat tasks to suitable configured models without manually changing model settings for each request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model and provider switching can route prompts, code, images, or attachments to different configured providers. <br>
Mitigation: Install only when automatic model switching is desired, and use provider keys with spending and data limits. <br>
Risk: Session-key based switching could affect a non-active session if the runtime permits arbitrary session targeting. <br>
Mitigation: Confirm the OpenClaw runtime restricts model changes to the active session and avoid workflows that target arbitrary sessionKey values. <br>
Risk: Automatic routing may choose an unsuitable or unavailable model for a task. <br>
Mitigation: Review configured provider availability and fallback behavior before relying on automatic switches. <br>


## Reference(s): <br>
- [Smart Model Switcher ClawHub release](https://clawhub.ai/davidme6/smart-model-switcher-v4) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and model identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single task classification, model recommendation, or switch action for the detected request.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
