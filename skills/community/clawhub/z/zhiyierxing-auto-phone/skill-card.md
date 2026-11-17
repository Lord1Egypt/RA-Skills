## Description:

Helps agents deploy, verify, operate, and troubleshoot a local Zhipu AutoGLM-Phone / Open-AutoGLM phone automation workflow for Android, HarmonyOS, and iPhone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuoo](https://clawhub.ai/user/zimuoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to set up a phone-agent environment, verify host, device, and model readiness, and run natural-language phone tasks. It also provides exact troubleshooting and takeover guidance when device, model, login, captcha, payment, biometric, or platform security blockers appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change local tooling and download or run upstream code.

Mitigation: Install and run it only in an environment where those changes are acceptable, and review the setup actions before using it on sensitive machines.

Risk: The skill can control a connected phone and perform the requested phone task with limited final confirmation.

Mitigation: Use a dedicated test phone or account where possible, and rely on takeover pauses for login, captcha, payment, biometric, or platform security prompts.

Risk: Model endpoint credentials can be exposed through environment configuration or shared host access.

Mitigation: Prefer HTTPS model endpoints, avoid shared machines for configured runs, and rotate any model API key that may have been exposed.

Risk: Remembered device connection details can enable future device reuse.

Mitigation: Clear ~/.openclaw/workspace/.device-memory/zhiyierxing-auto-phone.json when persistent device reuse is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zimuoo/skills/zhiyierxing-auto-phone)
- [Zhipu AutoGLM-Phone Documentation](https://docs.bigmodel.cn/cn/guide/models/vlm/autoglm-phone)
- [Open-AutoGLM Repository](https://github.com/zai-org/Open-AutoGLM)
- [ADB Keyboard](references/adb-keyboard.md)
- [Deployment Flow](references/deployment-flow.md)
- [Troubleshooting](references/troubleshooting.md)
- [Runbook](references/runbook.md)
- [Source Notes](references/source-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline commands, configuration values, status labels, and exact next-step guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local setup, readiness, verification, and phone-task scripts; pauses for takeover only when login, captcha, payment, biometrics, or platform security prompts require the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
