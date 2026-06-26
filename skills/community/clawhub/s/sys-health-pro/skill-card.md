## Description: <br>
System health monitoring tool that checks CPU, memory, disk, and network usage and alerts when anomalies are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and personal-computer users use this skill to inspect local system resource health, generate on-demand reports, and run foreground monitoring for CPU, memory, disk, and network usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and display local system resource metrics and process names. <br>
Mitigation: Install and run it only on machines where that local operational information is acceptable to expose, and avoid sharing generated reports from sensitive hosts. <br>
Risk: The artifact depends on an unpinned psutil package. <br>
Mitigation: Review or pin the dependency before deployment in managed or sensitive environments. <br>
Risk: Watch mode performs continuous foreground monitoring. <br>
Mitigation: Use watch mode only when continuous monitoring is intentional, and stop it when the monitoring task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/sys-health-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Python script that displays host resource metrics and process names.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
