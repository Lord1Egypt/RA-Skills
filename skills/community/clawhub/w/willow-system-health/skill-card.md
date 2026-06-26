## Description: <br>
Audits the Willow local AI stack for subsystem failures, drift, and resource bloat, including Postgres, Ollama, MCP, forks, tasks, sessions, stores, and model health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining Willow use this skill to run boot, daily, weekly, or full diagnostics for the local AI stack. It helps diagnose slow or broken sessions, service availability, open forks or tasks, database bloat, store growth, and stale local model state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local Willow services, database health, directories, and git worktrees. <br>
Mitigation: Install and run it only when local Willow environment inspection is intended, and review path overrides before execution. <br>
Risk: Suggested cleanup actions can remove worktrees or Ollama models, run database maintenance, or write memory summaries. <br>
Mitigation: Review each proposed action and require explicit confirmation before making changes; use dry-run cleanup options where available. <br>
Risk: Diagnostic reports may expose local operational state. <br>
Mitigation: Treat reports as local system diagnostics and avoid sharing them outside the intended troubleshooting context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rudi193-cmd/willow-system-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text diagnostic reports, optional JSON output, and Markdown guidance with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports HEALTHY, WARN, CRITICAL, and SKIP statuses per subsystem; cleanup actions are recommendations that require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
