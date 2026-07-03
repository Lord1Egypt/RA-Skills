## Description: <br>
Monitor OpenClaw API and agent-session errors, inspect model performance, configure retry strategies, generate reports, and manage recovery workflows through a companion Resilience plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leijack-lo](https://clawhub.ai/user/leijack-lo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to ask for API error statistics, model health summaries, retry strategy changes, dashboard access, and recovery reports in natural language. It is primarily useful when the companion @leiJack-lo/resilience plugin is installed and intentionally granted monitoring and recovery permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The companion plugin uses sensitive local authority, including model/session/tool event hooks, local dashboard access, persistent logs and configuration, and retry/recovery controls. <br>
Mitigation: Install only when OpenClaw error and session monitoring is desired, review the companion plugin before unsafe installation, and prefer explicit Resilience-named commands for dashboard and retry changes. <br>
Risk: The skill is a natural-language wrapper and does not provide the core tools or hooks by itself. <br>
Mitigation: Install and load the @leiJack-lo/resilience plugin first, then verify that Resilience tools are registered before relying on monitoring or recovery behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leijack-lo/skills/resilience-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/leijack-lo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and natural-language guidance with tool-call examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the companion Resilience plugin for tool execution, dashboard service, hooks, persistent logs, and retry/recovery controls.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
