## Description: <br>
Provides a Chinese-language workflow for safely modifying OpenClaw configuration files with documentation checks, user confirmation, validation, backup comparison, and Gateway status verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to make OpenClaw Gateway and configuration changes through a documented, confirmation-first workflow that checks validity, summarizes fixes, and verifies runtime status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow could be applied outside its intended OpenClaw configuration scope. <br>
Mitigation: Use it only for OpenClaw configuration work and confirm the target is ~/.openclaw/openclaw.json or another OpenClaw component before allowing changes. <br>
Risk: Configuration changes can affect Gateway behavior or availability. <br>
Mitigation: Review the proposed change, backup path, and documented impact before proceeding, then run validation and Gateway status checks after changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nicoxia/safe-config-workflow-zh) <br>
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor) <br>
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md) <br>
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting) <br>
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses output on user-relevant configuration changes, backup paths, warnings, and Gateway status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
