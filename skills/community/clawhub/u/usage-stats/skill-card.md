## Description: <br>
Analyzes local OpenClaw session logs to generate usage reports covering token consumption, cost estimates, model distribution, tool usage, errors, and activity trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqq664590975-del](https://clawhub.ai/user/qqq664590975-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect their local main-agent usage history, understand costs and token consumption, identify frequent tools and errors, and compare trends over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local OpenClaw main-agent session logs, which may contain sensitive usage details, prompts, command output, or error text. <br>
Mitigation: Install and run it only when local log analysis is intended, and review generated reports before sharing them. <br>
Risk: The skill saves derived usage history and the latest Markdown report under ~/.qclaw/workspace/memory. <br>
Mitigation: Delete usage_stats_latest.md and usage_stats_history.json if retained reports are no longer wanted. <br>
Risk: Cost figures are estimates derived from recorded usage data and may differ from actual billing. <br>
Mitigation: Use the report for local trend analysis and verify billing-sensitive conclusions against the provider bill. <br>


## Reference(s): <br>
- [Usage Stats changelog](references/changelog.md) <br>
- [Usage Stats output format](references/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report with tabular sections plus JSON history snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the latest report and rolling history under ~/.qclaw/workspace/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and references/changelog.md, released 2026-04-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
