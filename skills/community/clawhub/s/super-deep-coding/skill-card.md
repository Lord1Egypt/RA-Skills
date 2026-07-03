## Description: <br>
Super Deep Coding is a multi-agent coding workflow that helps agents decompose complex software projects into modules, coordinate builder and reviewer agents, run reviews and end-to-end checks, and track progress with a local dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molexazwo](https://clawhub.ai/user/molexazwo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to manage large, multi-file software builds through orchestrated planning, builder implementation, reviewer validation, and final end-to-end testing. It is intended for complex project work rather than simple edits or single-file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Builders and reviewers may execute generated or project code while completing requested work. <br>
Mitigation: Use the skill only in workspaces where code execution is acceptable, and isolate untrusted projects in a container or virtual machine. <br>
Risk: The local dashboard serves project files from the workspace and may expose sensitive local content to anyone with access to the localhost service. <br>
Mitigation: Run the dashboard only on localhost, avoid using repositories that contain secrets, and narrow the served file allowlist before use with untrusted content. <br>
Risk: Dashboard rendering is identified by security evidence as unsafe for untrusted agent or project content. <br>
Mitigation: Sanitize rendered Markdown or disable rendering of untrusted content before using the dashboard in shared or sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/molexazwo/skills/super-deep-coding) <br>
- [Deep Coding Harness - Project Architecture](artifact/references/architecture.md) <br>
- [Orchestrator Rules](artifact/references/orchestrator-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce project files, dashboard-compatible project state JSON, per-agent logs, and testing instructions when used by configured agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
