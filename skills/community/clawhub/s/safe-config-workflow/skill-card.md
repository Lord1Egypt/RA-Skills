## Description: <br>
Guides agents through confirmed, documented, and validated changes to OpenClaw configuration, including repair, backup comparison, Gateway checks, and concise user feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to modify OpenClaw Gateway, channel, model, session, or authentication configuration while preserving review, validation, repair, and rollback awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live OpenClaw configuration changes, including auth, session, model, and Gateway settings. <br>
Mitigation: Require explicit user confirmation before each change, review doctor --fix output and backup diffs, and verify Gateway status after the change. <br>
Risk: The skill instructs agents to record learned configuration values, which could accidentally persist secrets, hostnames, paths, raw diffs, or credential-like data. <br>
Mitigation: Store only generalized lessons in memory and redact tokens, secrets, hostnames, user-specific paths, and sensitive configuration values. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nicoxia/safe-config-workflow) <br>
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor) <br>
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md) <br>
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting) <br>
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confirmation prompts, repair summaries, backup locations, validation results, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
