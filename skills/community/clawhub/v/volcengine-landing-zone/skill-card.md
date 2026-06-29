## Description: <br>
Use when the user asks to analyze, consult, setup, manage, configure, or design a Volcengine Landing Zone, including organization, accounts, finance, identity, cloudtrail, or network infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud infrastructure teams use this skill to consult on, prepare, deploy, manage, and recover Volcengine Landing Zone foundations across organization, account, finance, identity, audit, network, and account baseline workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact changes to real Volcengine infrastructure. <br>
Mitigation: Confirm the target account or profile, expected cloud changes, and workspace path before execution. <br>
Risk: The skill may store an initial administrator password in a local markdown file. <br>
Mitigation: Treat identity-login-info.md as sensitive, restrict file access, and rotate or replace the initial administrator password immediately after first login. <br>
Risk: Temporary CLI profiles or login state may persist after a run. <br>
Mitigation: Verify local CLI profile state after runs that use temporary profiles or login. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-landing-zone) <br>
- [Local file display protocol](references/display-protocol.md) <br>
- [Preflight checks](references/preflight-checks.md) <br>
- [Volcengine Landing Zone setup guide](references/landing-zone-setup/guidebook.md) <br>
- [Account Factory workflow](references/account-factory/guidebook.md) <br>
- [Failure recovery workflow](references/failure-recovery.md) <br>
- [Account Factory baseline schema](references/account-factory/baseline.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, generated local files, and HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace-local execution files, solution confirmation HTML, login information, initial password records, and summary reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
