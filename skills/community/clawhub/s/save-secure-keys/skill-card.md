## Description: <br>
Securely stores OpenClaw configuration and key information by backing up the default configuration file to keys.txt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yegou777](https://clawhub.ai/user/yegou777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create a local backup of OpenClaw configuration data that may include API keys and endpoint settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up sensitive OpenClaw credentials to a predictable plaintext file. <br>
Mitigation: Run it only when a plaintext backup is deliberately needed, set restrictive file permissions, and prefer an encrypted secrets manager or encrypted backup. <br>
Risk: Incorrect source or destination paths could copy credentials to an unintended location. <br>
Mitigation: Verify the exact source and destination paths before execution and avoid elevated privileges unless strictly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yegou777/save-secure-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file copy output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies the OpenClaw configuration backup to a local plaintext target path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
