## Description: <br>
Automated self-healing system for the OpenClaw gateway that monitors the process, backs up and rolls back configuration, and switches to a fallback model after repeated health check failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bptravel2017](https://clawhub.ai/user/bptravel2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate a local OpenClaw gateway watchdog that can restart the gateway, protect its configuration, and fail over to another configured model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent automation can restart OpenClaw and change the configured model without further confirmation. <br>
Mitigation: Review the launchd setup, test with DRY_RUN=1, confirm backups exist, and keep the unload command available before unattended use. <br>
Risk: The failover path includes unsafe shell evaluation and string interpolation around state and configuration values. <br>
Mitigation: Patch or review the failover script before installation, especially in environments where state or configuration files may be modified by other users. <br>
Risk: Incorrect health-check or failover settings can cause repeated restarts or unexpected model changes. <br>
Mitigation: Verify the local gateway URL, failure threshold, fallback model list, and rollback behavior in dry-run mode before enabling scheduled execution. <br>


## Reference(s): <br>
- [Configuration reference](references/config.md) <br>
- [ClawHub release page](https://clawhub.ai/bptravel2017/self-heal-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/bptravel2017) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands, configuration details, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup, status, watchdog, health-check, and model-failover workflows for OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
