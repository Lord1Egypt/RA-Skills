## Description: <br>
Revenium Budget Enforcement helps OpenClaw agents meter usage, check Revenium budget guardrails, warn at thresholds, and halt autonomous work when configured rules block execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johndemic](https://clawhub.ai/user/johndemic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agent sessions to Revenium budget metering and guardrail workflows. It is intended for teams that need spend visibility, budget warnings, and best-effort autonomous halt behavior during agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill installs persistent monitoring and needs access to OpenClaw session logs, local agent configuration, cron, plugin hooks, and Revenium credentials. <br>
Mitigation: Install only in environments where that access is acceptable, review the installed files and permissions, and remove the cron jobs or plugins when budget enforcement is no longer needed. <br>
Risk: The security review says the skill is a metering and best-effort guardrail integration, not a guaranteed hard safety boundary. <br>
Mitigation: Treat local halt behavior as advisory defense in depth, keep independent Revenium or provider-side spend controls in place, and monitor budget state outside the agent when hard limits matter. <br>
Risk: The release requires sensitive Revenium credentials. <br>
Mitigation: Use scoped credentials where available, avoid sharing credential values in prompts or logs, and rotate credentials if an agent workspace is exposed. <br>


## Reference(s): <br>
- [Revenium for AI Agents](https://docs.revenium.io/for-ai-agents) <br>
- [Revenium Budget Enforcement on ClawHub](https://clawhub.ai/johndemic/revenium) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Agents Metering Directives](artifact/references/agents-metering-directives.md) <br>
- [Job Declaration Reference](artifact/references/job-declaration.md) <br>
- [Task Classification Reference](artifact/references/task-classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for operator confirmation when budget warning mode is active; may emit halt guidance when a configured hard-limit is active.] <br>

## Skill Version(s): <br>
0.6.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
