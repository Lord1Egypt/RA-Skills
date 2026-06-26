## Description: <br>
Computer Use Agent (CUA) for macOS automation using TuriX. Use when you need to perform visual tasks on the desktop, such as opening apps, clicking buttons, or navigating UIs that don't have a CLI or API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tongyu-Yan](https://clawhub.ai/user/Tongyu-Yan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill to delegate macOS GUI workflows to a visual computer-use agent when an application lacks a practical CLI or API. Typical tasks include opening applications, navigating websites, clicking controls, and completing multi-step desktop workflows under supervision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent broad visibility and control over the user's macOS desktop. <br>
Mitigation: Use it only for intended desktop-control workflows, supervise runs, avoid sensitive personal or production accounts, and revoke Screen Recording and Accessibility permissions after use. <br>
Risk: The core desktop automation is delegated to an external TuriX-CUA checkout and runtime. <br>
Mitigation: Use a dedicated trusted checkout, pin or review the runtime before use, and review generated config changes before running tasks. <br>
Risk: The agent may perform consequential GUI actions such as submissions, uploads, account changes, or deletions. <br>
Mitigation: Require explicit user confirmation before consequential actions and prefer narrow, specific task prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Tongyu-Yan/turix-cua) <br>
- [TuriX-CUA GitHub Repository](https://github.com/TurixAI/TuriX-CUA) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the TuriX examples/config.json file and produce local TuriX logs during execution.] <br>

## Skill Version(s): <br>
1.0.8 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
