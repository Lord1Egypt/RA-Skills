## Description: <br>
Check current Linux system resource usage and report load, memory, swap, disk, and top CPU/memory processes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karryklein](https://clawhub.ai/user/karryklein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to collect and summarize Linux host resource usage for quick health checks, recurring status summaries, and early detection of abnormal load or memory pressure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Top-process output can include command-line arguments from running processes. <br>
Mitigation: Review generated reports before sharing them externally. <br>
Risk: Report accuracy depends on standard Linux tools being available on the host. <br>
Mitigation: Confirm the target environment provides uptime, free, df, ps, head, and /proc/loadavg before relying on the report. <br>


## Reference(s): <br>
- [System Resource Report on ClawHub](https://clawhub.ai/karryklein/system-resource-report) <br>
- [karryklein publisher profile](https://clawhub.ai/user/karryklein) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with shell command output interpreted into concise status sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports load average, memory and swap usage, root disk usage, top CPU processes, and top memory processes from local Linux commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and publishing notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
