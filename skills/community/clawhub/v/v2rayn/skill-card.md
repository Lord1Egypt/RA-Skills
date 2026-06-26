## Description: <br>
Manage V2RayN on macOS to list nodes, test proxy connections, check current node status, view logs, and support auto-failover via scripted health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiangwang375-wq](https://clawhub.ai/user/qiangwang375-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators using V2RayN on macOS use this skill to inspect proxy status, list configured nodes, test connectivity, review logs, and prepare local health-check automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: V2RayN node names, logs, and configuration-derived details may expose sensitive local proxy information if shared. <br>
Mitigation: Review command output before sharing it and redact node names, log entries, and configuration details that are not needed. <br>
Risk: The cron example can create recurring background checks against the local proxy setup. <br>
Mitigation: Create or enable the cron job only when recurring health checks are intended, and review the script path and log location first. <br>
Risk: Restart commands can interrupt the active V2RayN proxy client session. <br>
Mitigation: Run restart commands only when a proxy client restart is intended and after confirming current network activity can tolerate interruption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiangwang375-wq/v2rayn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local process, port, log, and V2RayN configuration details from the user's machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
