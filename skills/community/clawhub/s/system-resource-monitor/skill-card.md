## Description: <br>
A clean, reliable system resource monitor for CPU load, RAM, Swap, and Disk usage. Optimized for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Passersss](https://clawhub.ai/user/Passersss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to request concise local server health reports covering CPU load, memory, swap, disk usage, and uptime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent runs a local shell script to inspect host resource metrics. <br>
Mitigation: Review the included script before installation and run it only in environments where reading uptime, memory, swap, and root disk usage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Passersss/system-resource-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/Passersss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text system resource report with optional Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local host metrics from uptime, free, and df without network transmission according to the provided security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
