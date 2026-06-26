## Description: <br>
Monitors Linux server CPU, memory, disk, load, network, and process status with read-only commands, optional thresholds, and scheduled checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinsuso](https://clawhub.ai/user/yinsuso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site reliability engineers use this skill to inspect Linux server health, summarize resource usage, identify high-load processes, and configure deliberate threshold checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server status output can expose infrastructure-sensitive details such as hostnames, process names, and resource metrics. <br>
Mitigation: Share results only with appropriate operators and redact sensitive host or process details before forwarding them. <br>
Risk: Optional cron, heartbeat, or notification setup can repeat metrics or send alerts unexpectedly if enabled without review. <br>
Mitigation: Review scheduling and notification configuration before enabling automated checks, and keep alert destinations limited to intended recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinsuso/yinsuso-server-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Linux shell command blocks and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Linux status commands and may include threshold recommendations for optional monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
