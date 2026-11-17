## Description:

Analyzes WeChat Xlog log files, extracts key information, and generates diagnostic reports for troubleshooting and log statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellllll0world](https://clawhub.ai/user/hellllll0world)

### License/Terms of Use:


## Use Case:

Developers and support engineers use this skill to parse local WeChat Xlog files, summarize levels, modules, warnings, and errors, and produce diagnostic guidance after any required external decryption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decrypted WeChat Xlog files and generated JSON reports may contain sensitive account, device, network, chat, payment, or diagnostic details.

Mitigation: Analyze logs locally, redact sensitive fields before sharing, and choose output paths deliberately.

Risk: Encrypted Xlog files are not decrypted by this skill.

Mitigation: Decrypt files with an external trusted tool before parsing and only provide plaintext logs that are appropriate for local analysis.

Risk: WeChat Xlog formats may vary by client version, which can reduce parser coverage or produce UNKNOWN entries.

Mitigation: Review parser output and validate key findings against representative raw log lines before acting on recommendations.

## Reference(s):

- [Xlog Format Reference](references/xlog_format.md)
- [Xlog Analysis Guide](references/analysis_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/hellllll0world/skills/weixin-xlog-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON report files produced by the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts read local user-provided log files and write local JSON outputs such as parsed logs and analysis reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
