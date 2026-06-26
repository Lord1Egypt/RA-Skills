## Description: <br>
Monitors OpenClaw API errors, model performance, retry strategies, reports, and task recovery status through a companion Resilience plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leijack-lo](https://clawhub.ai/user/leijack-lo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect API error trends, view per-model reliability, manage retry strategies, generate resilience reports, and open a local monitoring dashboard. It is most useful when the companion Resilience plugin is installed and loaded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a companion plugin for tools, gateway hooks, dashboard service, and local data storage. <br>
Mitigation: Install and enable the companion plugin intentionally, restart the gateway, and verify the tools are available before relying on the skill. <br>
Risk: API error, retry, and model performance data may be stored locally by the companion plugin. <br>
Mitigation: Use the skill only in workspaces where local operational logging is acceptable, and review local retention practices for resilience data. <br>
Risk: Broad natural-language triggers could open the dashboard or change retry strategy settings unexpectedly. <br>
Mitigation: Use explicit resilience-related commands and confirm the selected instance and strategy before applying retry configuration changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leijack-lo/resilience-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/leijack-lo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance, tool-oriented instructions, and report text with shell and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the companion @leiJack-lo/resilience plugin for tool execution, dashboard service, hooks, and local data persistence.] <br>

## Skill Version(s): <br>
0.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
