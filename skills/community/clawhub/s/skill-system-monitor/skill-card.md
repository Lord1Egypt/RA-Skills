## Description: <br>
System Monitor helps agents run system health checks for disk, memory, CPU, services, Docker, network usage, and historical trend reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weznai](https://clawhub.ai/user/weznai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local system health, report resource pressure, compare recent monitoring snapshots, and support scheduled health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and stores local system health details, including process and service information. <br>
Mitigation: Treat the history directory as sensitive operational data, restrict file permissions, and review cleanup behavior before scheduled use. <br>
Risk: The trend script can expose aggregate disk and memory history through a QuickChart URL. <br>
Mitigation: Run trend reporting only where sending aggregate monitoring data to quickchart.io is acceptable, or avoid opening the generated chart link on sensitive systems. <br>
Risk: The artifact documents cross-platform behavior but the included wrapper depends on platform-specific helper scripts being present. <br>
Mitigation: Validate the installed script set on each target platform before relying on scheduled monitoring outside Linux. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weznai/skill-system-monitor) <br>
- [QuickChart](https://quickchart.io/chart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local health reports and history comparisons; trend reporting can include an external QuickChart URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
