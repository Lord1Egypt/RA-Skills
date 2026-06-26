## Description: <br>
Safe Config Modifier guides agents through backing up, previewing, validating, confirming, and editing OpenClaw configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to inspect or modify OpenClaw configuration, including model, channel, tool, and skill settings. It emphasizes backup, redacted preview, JSON validation, explicit user confirmation, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preview output may expose API keys, bot tokens, or other secrets if masking misses a field or format. <br>
Mitigation: Manually review and redact preview output before sharing it, and avoid relying on the helper scripts as the only secret-control measure. <br>
Risk: Edits to the core OpenClaw configuration can break model, channel, gateway, tool, or skill behavior. <br>
Mitigation: Create a timestamped backup, validate JSON before and after changes, review the exact diff, and restore from backup if verification fails. <br>
Risk: A user may approve an unintended change without understanding what will be modified. <br>
Mitigation: Require an explicit confirmation phrase only after showing the redacted proposed change, validation result, and expected operational impact. <br>


## Reference(s): <br>
- [OpenClaw Configuration Examples](references/examples.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/justaboyhai-wq/safe-config-momo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes redacted previews, validation steps, backup commands, and confirmation-gated edit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
