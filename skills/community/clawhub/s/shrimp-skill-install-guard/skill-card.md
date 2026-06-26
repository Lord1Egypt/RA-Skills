## Description: <br>
Guard OpenClaw skill installation with a productized five-step flow: source check, local-state check, mandatory all-files review, risk review, install execution, and post-install verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyunting555](https://clawhub.ai/user/wuyunting555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and security-sensitive teams use this skill to review unfamiliar OpenClaw skills before installation, make go/no-go decisions, execute approved installs, and verify that expected files landed afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a user-provided install command during the execution phase. <br>
Mitigation: Start with --dry-run or --stop-before-install, review the report, and only proceed with a simple trusted install command. <br>
Risk: A review report can miss context or produce an incomplete safety conclusion. <br>
Mitigation: Treat the result as review support, not a guarantee; verify the target source, expected directory, and key files before accepting the install. <br>
Risk: Privileged commands, shell interpreters, chaining, pipes, or redirects can broaden installation impact. <br>
Mitigation: Avoid privileged or shell-interpreted commands and provide a direct executable invocation with an expected install directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyunting555/shrimp-skill-install-guard) <br>
- [Publisher profile](https://clawhub.ai/user/wuyunting555) <br>
- [README](README.md) <br>
- [Local verification report](VERIFICATION-2026-04-08.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional JSON reports and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports source completeness, file-review coverage, red flags, permissions, risk level, recommendation, install status, and post-install verification.] <br>

## Skill Version(s): <br>
0.4.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
