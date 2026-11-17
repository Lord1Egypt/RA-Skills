## Description:

基于大模型的安全事件日志分析工具，支持快速提取关键信息和深度攻击链细节分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and incident responders use this skill to triage security logs, identify event type and threat level, extract IOCs, and receive remediation guidance in brief or detailed reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security logs may contain sensitive data and are sent to a configurable external LLM API; server security evidence says automatic redaction is not implemented despite the documentation claim.

Mitigation: Use only logs that are allowed to be shared with the configured provider, manually redact secrets before analysis, and verify the SILICONFLOW_BASE_URL destination before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/security-log-analyzer)
- [Skill usage documentation](artifact/SKILL.md)
- [Design documentation](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown security analysis report with CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports brief and detailed analysis modes; long log inputs may be truncated before analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
