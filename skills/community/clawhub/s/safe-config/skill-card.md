## Description: <br>
Helps agents modify OpenClaw configuration files through a backup, redacted preview, validation, explicit confirmation, and post-change verification workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when updating OpenClaw configuration for models, channels, tools, or skill installation. It guides the agent to preview redacted changes, validate JSON, require explicit user confirmation, back up the file, apply the change, and verify the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the promised secret masking is unreliable for sensitive configuration files. <br>
Mitigation: Review any preview output before sharing it, provide explicit file paths, and do not rely on the bundled masking scripts until they are fixed. <br>
Risk: Backups may contain full secrets from the OpenClaw configuration file. <br>
Mitigation: Confirm backups exist before editing, store them only in trusted locations, and handle backup files as sensitive material. <br>


## Reference(s): <br>
- [OpenClaw configuration examples](artifact/references/examples.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/justaboyhai-wq/safe-config) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted previews, validation results, backup commands, configuration patches, and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
