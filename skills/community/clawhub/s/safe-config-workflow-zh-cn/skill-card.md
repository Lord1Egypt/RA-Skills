## Description: <br>
Provides a Chinese-language workflow for safely modifying OpenClaw configuration, including confirmation, validation, backup comparison, troubleshooting, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI assistants who manage OpenClaw installations use this skill to plan, confirm, validate, repair, and verify configuration changes while keeping users informed about important impacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or unreviewed configuration edits could disrupt OpenClaw Gateway, authentication, channels, or sessions. <br>
Mitigation: Confirm the requested change and impact, consult OpenClaw documentation and schema guidance, run validation and repair commands, compare the backup diff, and verify Gateway status. <br>
Risk: Tokens, authentication values, private endpoints, or session details could be exposed in MEMORY.md or user-facing status summaries. <br>
Mitigation: Review proposed edits and summaries before approval, and redact secrets or private operational details before recording or sharing them. <br>
Risk: Automatic doctor repairs may hide meaningful configuration changes from the user. <br>
Mitigation: Filter diagnostic output for relevant repair details, inspect the backup diff, and explain field-level changes before considering the workflow complete. <br>


## Reference(s): <br>
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor) <br>
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md) <br>
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting) <br>
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration-change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language responses with confirmation prompts, filtered diagnostic summaries, backup diff explanations, and gateway status reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
