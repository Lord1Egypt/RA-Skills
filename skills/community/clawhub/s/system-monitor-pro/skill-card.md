## Description: <br>
Real-time OpenClaw system monitoring with a terminal-style UI for CPU, memory, disk, GPU, Gateway, cron jobs, model quota, and multi-machine checks on macOS and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect local or trusted remote OpenClaw host health, check system resource usage, and receive concise alert summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote SSH monitoring was flagged by ClawHub security review because unsafe host handling and disabled host key verification can expose users to connection or command risks. <br>
Mitigation: Use local monitoring by default. Use remote monitoring only for explicit trusted hosts after validating the host value, using safe argument passing, and preserving SSH host key verification. <br>
Risk: The skill inspects local system state and runs shell-based monitoring commands. <br>
Mitigation: Review the skill before installation and run it only in environments where local system inspection is acceptable. <br>


## Reference(s): <br>
- [System Monitor Pro ClawHub Release](https://clawhub.ai/dagangtj/system-monitor-pro) <br>
- [dagangtj Publisher Profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal-formatted status text, raw JSON, or alert-only summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local system state by default and can optionally check trusted remote hosts over SSH.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
