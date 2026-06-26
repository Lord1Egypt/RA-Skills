## Description: <br>
Parses and analyzes WeChat Xlog files to extract key log records, error patterns, module statistics, and diagnostic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellllll0world](https://clawhub.ai/user/hellllll0world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to parse local WeChat Xlog files, summarize log levels and modules, identify errors or warnings, and produce diagnostic guidance for troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat Xlog files and generated JSON reports may contain private or sensitive user, device, network, or application data. <br>
Mitigation: Analyze only logs the user is authorized to inspect, redact sensitive fields before sharing outputs, and store or delete generated reports carefully. <br>
Risk: Encrypted Xlog files require external decryption tools that are outside this skill. <br>
Mitigation: Use trusted external decryption tools when needed and validate decrypted files locally before running the parser. <br>
Risk: Unquoted or untrusted file paths in shell commands can cause command-line mistakes or unintended file access. <br>
Mitigation: Quote file paths in commands and run the scripts only against intended local log files. <br>


## Reference(s): <br>
- [Xlog Analysis Guide](references/analysis_guide.md) <br>
- [WeChat Xlog Format Reference](references/xlog_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may contain sensitive log content and should be redacted before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
