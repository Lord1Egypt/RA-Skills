## Description: <br>
Use when session files grow too large (>1MB), context compression fails to trigger, or you need to manage long-running session lifecycle; it auto-archives old sessions, scores message importance, flushes memory before compression, and keeps session files small. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangqb666](https://clawhub.ai/user/zhangqb666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes Agent users use this skill to detect oversized session files, archive important session content, and trim session history while preserving structured summaries and recoverable backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite private Hermes session history while trimming oversized session files. <br>
Mitigation: Run --list and --dry-run first, confirm backups are created, and only process sessions you are comfortable modifying. <br>
Risk: Session summaries, archives, and backups may contain prompts, paths, local endpoints, project details, and configuration values. <br>
Mitigation: Treat generated archives and backups as sensitive local files and review them before sharing or syncing them. <br>
Risk: The skill can automatically persist session summaries to Hindsight memory. <br>
Mitigation: Use --no-hindsight or set hindsight_enabled: false unless storing summaries in Hindsight is explicitly intended. <br>
Risk: The setup script can create a recurring job that performs unattended session trimming. <br>
Mitigation: Avoid setup_cron.sh until you are comfortable with automated execution, and prefer manual runs during initial review. <br>


## Reference(s): <br>
- [Hindsight Integration Guide](references/hindsight-integration.md) <br>
- [Structured Summary Template](references/summary-template.md) <br>
- [Hermes Agent Issue #3015](https://github.com/NousResearch/hermes-agent/issues/3015) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, shell commands, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local session archives, backups, and optional Hindsight memory records when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
