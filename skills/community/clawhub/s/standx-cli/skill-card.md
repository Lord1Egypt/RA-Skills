## Description: <br>
Standx Cli helps agents use the StandX crypto trading CLI to query market data, manage account information, execute orders, stream market data, and manage leverage or margin settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjllance](https://clawhub.ai/user/wjllance) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to operate the StandX CLI through an agent for crypto market lookup, account review, trading workflows, streaming data, and trading configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables live financial actions, including order creation, cancel-all operations, leverage changes, and margin changes. <br>
Mitigation: Require dry-run review and explicit confirmation before any order, cancel-all, leverage, or margin change. <br>
Risk: Some install paths download a StandX binary and move it into a system path with elevated privileges. <br>
Mitigation: Prefer Homebrew or a release that can be verified, and avoid sudo-based direct downloads when possible. <br>
Risk: The skill uses sensitive trading credentials, including a JWT and optional private trading key. <br>
Mitigation: Keep credentials out of command history and version control, avoid storing the private trading key in shell startup files, and rotate tokens regularly. <br>


## Reference(s): <br>
- [Standx Cli ClawHub Page](https://clawhub.ai/wjllance/standx-cli) <br>
- [StandX CLI API Documentation](references/api-docs.md) <br>
- [StandX CLI Command Examples](references/examples.md) <br>
- [StandX CLI Troubleshooting](references/troubleshooting.md) <br>
- [StandX Credential Session](https://standx.com/user/session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include guidance for JSON, CSV, quiet, and OpenClaw-optimized CLI output modes.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
