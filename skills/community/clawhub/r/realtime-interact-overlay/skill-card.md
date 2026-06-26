## Description: <br>
Realtime Interact Overlay helps agents request user confirmation, selection, or short input through a macOS dialog or browser overlay near the active task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LightCastlePro](https://clawhub.ai/user/LightCastlePro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators can use this skill when an agent needs explicit user confirmation or brief input before continuing with local or browser-based actions. It is best suited for low-sensitivity confirmations and should not be used for passwords, payments, account approvals, or destructive file actions until the documented security gaps are fixed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser overlay content may be unsafe because the security summary identifies review-worthy gaps around browser injection and unsafe modal rendering. <br>
Mitigation: Review the implementation before installation and use only an updated version that escapes browser modal content and avoids unsafe innerHTML behavior. <br>
Risk: The skill is not suitable for sensitive input because the security guidance says hidden password entry is not genuinely implemented. <br>
Mitigation: Do not use the skill for passwords, payments, account approvals, or other sensitive input until hidden-entry handling is fixed and reviewed. <br>
Risk: The skill can be used to confirm destructive or high-impact actions while local and browser permissions are not clearly documented. <br>
Mitigation: Avoid file-deletion confirmations and other high-impact approvals until required permissions and user-facing approval boundaries are clearly documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LightCastlePro/realtime-interact-overlay) <br>
- [Skill source overview](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON interaction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-injected JavaScript for overlays and JSON status values such as confirmed, cancel, timeout, or error.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
