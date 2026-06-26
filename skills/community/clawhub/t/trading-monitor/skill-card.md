## Description: <br>
盘中股票盯盘定时任务管理。创建、配置和管理A股交易时段的自动分析任务，包括定时行情播报、深度分析、收盘前最终分析。使用场景：设置盯盘、调整分析频率、查看任务状态、停止/启动任务。触发词：盯盘、设置分析、开盘监控、调整频率、盯盘任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cle87937-code](https://clawhub.ai/user/cle87937-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to create, configure, and manage scheduled A-share trading-session monitoring tasks, including periodic market reports, deeper analysis, and pre-close final analysis. It helps users set monitoring cadence, push reports to a configured channel, check task status, and stop or restart cron tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent cron jobs that can repeatedly send financial analysis and portfolio-related details to an external messaging destination. <br>
Mitigation: Verify the Feishu channel and recipient before creating jobs, and review active cron tasks regularly with the documented list and delete commands. <br>
Risk: The skill documentation suggests setting command execution security to full when troubleshooting allowlist errors. <br>
Mitigation: Prefer the documented manual OpenClaw cron create, list, delete, and trigger commands; do not weaken global command-execution protections unless the environment owner intentionally accepts that risk. <br>
Risk: Automated trading-session reports may contain incorrect, stale, or misleading financial analysis. <br>
Mitigation: Review generated recommendations before acting on them and treat reports as decision support rather than autonomous trading instructions. <br>


## Reference(s): <br>
- [trading-monitor configuration guide](references/config-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/cle87937-code/trading-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell and OpenClaw cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and management guidance for persistent scheduled monitoring tasks and Feishu delivery targets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
