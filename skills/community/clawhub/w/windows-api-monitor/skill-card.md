## Description: <br>
Monitors OpenClaw API usage on Windows by reading local usage logs, tracking model calls, costs, trends, and threshold alerts, and generating usage reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowaa223](https://clawhub.ai/user/guowaa223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users on Windows use this skill to inspect local API usage, understand model-level consumption, and decide whether current daily or weekly quotas are sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw usage logs, which may contain sensitive usage patterns or operational details. <br>
Mitigation: Install and run it only when local log analysis is intended, and keep generated reports private unless they have been reviewed. <br>
Risk: The skill can create local report and state files, including reports at user-provided output paths. <br>
Mitigation: Review custom output paths before running commands and before sharing generated files. <br>
Risk: Continuous monitoring and scheduled-task examples can perform repeated local checks over time. <br>
Mitigation: Enable continuous monitoring or scheduled checks only when ongoing API usage monitoring is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guowaa223/windows-api-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/guowaa223) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON, and local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can summarize current, daily, weekly, monthly, or all usage; optional alerts compare usage against configured thresholds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
