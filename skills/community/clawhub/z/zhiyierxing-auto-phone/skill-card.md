## Description: <br>
Deploys and runs Zhipu AutoGLM-Phone / Open-AutoGLM workflows that prepare local tooling, connect Android, HarmonyOS, or iPhone devices, configure model endpoints, verify setup, and execute natural-language phone tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuoo](https://clawhub.ai/user/zimuoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced users use this skill to set up and operate local phone-agent workflows for real-device automation. It helps check host prerequisites, connect devices, configure model endpoints, verify deployment, and run natural-language phone tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real phone actions, including actions in shopping or service apps. <br>
Mitigation: Use it only when supervised on trusted devices and accounts, and pause for login, captcha, payment, biometrics, or platform security prompts. <br>
Risk: The workflow uses model API keys and may remember device connection details. <br>
Mitigation: Treat model credentials and remembered device targets as sensitive local data; avoid sharing logs that contain them and clear local device memory when reuse is no longer desired. <br>
Risk: The skill can change the host setup by cloning repositories, creating virtual environments, and installing local tooling or dependencies. <br>
Mitigation: Review the package and repository changes before first run, and prefer a trusted single-user machine or isolated workspace. <br>


## Reference(s): <br>
- [Zhipu AutoGLM-Phone documentation](https://docs.bigmodel.cn/cn/guide/models/vlm/autoglm-phone) <br>
- [Open-AutoGLM repository](https://github.com/zai-org/Open-AutoGLM) <br>
- [ADB Keyboard repository](https://github.com/senzhk/ADBKeyBoard) <br>
- [Deployment flow](artifact/references/deployment-flow.md) <br>
- [ADB Keyboard](artifact/references/adb-keyboard.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Source notes](artifact/references/source-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device-readiness diagnostics, model endpoint checks, and user takeover guidance when phone-side action is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
