## Description: <br>
Token-efficient command execution patterns for AI agents using vx-managed tools such as `vx rg` and `vx jq` to filter verbose build, test, lint, GitHub, and version-control output across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to choose compact, cross-platform command patterns for builds, tests, linting, GitHub workflows, CI logs, and repository inspection. It helps agents preserve context by filtering command output before returning it to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI and API examples may read authenticated repository, pull request, issue, or CI information. <br>
Mitigation: Run the examples only in the intended project context and review filtered output before sharing or storing it. <br>
Risk: Log-saving examples can write full command output to local files that may contain sensitive project details. <br>
Mitigation: Use temporary or ignored log paths, inspect and redact sensitive content when needed, and delete logs after debugging. <br>
Risk: Command recipes are examples and may not match every project or shell environment exactly. <br>
Mitigation: Review each command before execution and adapt paths, flags, and filters to the current toolchain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loonghao/vx-agent-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples should be reviewed before execution in the user's environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
