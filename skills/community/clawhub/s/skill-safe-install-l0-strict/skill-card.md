## Description: <br>
Skill Safe Install (L0 Strict) enforces a conservative workflow for safely installing ClawHub/OpenClaw skills by requiring target confirmation, risk review, sandbox verification, explicit consent, and guarded trust-list changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1231qaz2wsx](https://clawhub.ai/user/1231qaz2wsx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when installing or reviewing ClawHub/OpenClaw skills to force identity confirmation, pre-install risk assessment, sandbox installation, and explicit consent before formal install or trust persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A target skill may request broad permissions, credentials, command execution, filesystem mutation, or persistent trust-list changes. <br>
Mitigation: Use the skill's mandatory inspect, risk-rating, sandbox, and explicit consent gates before any formal install or config change. <br>
Risk: Sandbox installation in a temporary workdir may not provide full isolation from all system effects. <br>
Mitigation: Treat sandbox results as limited evidence and continue reviewing each target skill's permissions and behavior before approval. <br>
Risk: Persistent trust-list changes can reduce future review pressure for a skill. <br>
Mitigation: Skip trust persistence by default and only update allowBundled after explicit user authorization, backup, and rollback guidance. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/1231qaz2wsx/skill-safe-install-l0-strict) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with structured step-status lines and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires step-by-step risk rating and consent status before install actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
