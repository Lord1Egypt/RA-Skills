## Description: <br>
独立审计工具（免费版） helps an agent audit AI agent projects for security, performance, compliance, code quality, configuration issues, vulnerability indicators, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for lightweight audits of AI agent code, configuration, security posture, performance bottlenecks, and compliance concerns. The free edition is described as a single-task, personal-use helper for quick daily checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan classifies the release as suspicious because it asks for exec and write authority and mentions modify/delete operations without clear user controls. <br>
Mitigation: Use the skill only with explicit prompts that limit it to passive analysis or report generation, and require confirmation before shell commands, file writes, modifications, deletions, package installation, network pings, or callback delivery. <br>
Risk: The artifact includes examples for installing packages and running audit code, which can alter the local environment or inspect project files. <br>
Mitigation: Review proposed commands first, run them in a controlled workspace, and avoid granting write or network access unless it is required for the current audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/solo-audit-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured audit findings, execution logs, configuration examples, and report-oriented summaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
