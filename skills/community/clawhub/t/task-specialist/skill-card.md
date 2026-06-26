## Description: <br>
A robust, local SQLite-backed task management system designed to help AI agents plan, track, coordinate, and verify multi-step project work without relying on fragile memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OBODA0](https://clawhub.ai/user/OBODA0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI agents use this skill to maintain a local SQLite-backed task board, decompose work, manage dependencies, coordinate parallel workers, and preserve task context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores task notes and verification commands in a workspace-local .tasks.db file, which could expose sensitive information if users add secrets to notes or commands. <br>
Mitigation: Do not store API keys or secrets in task notes or verification commands; use secure local environment variables for sensitive values. <br>
Risk: Verification commands are user-provided shell commands and may perform unsafe actions if run without inspection. <br>
Mitigation: Inspect printed verification commands before manually executing them; the skill prints these commands instead of running them automatically. <br>
Risk: Optional symlink installation changes commands in ~/.local/bin, which affects the user's shell environment. <br>
Mitigation: Use --symlink only when the user intentionally wants task and task-heartbeat added to ~/.local/bin. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OBODA0/task-specialist) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [CLI text and Markdown guidance with optional JSON exports from task data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local .tasks.db SQLite database in the active workspace; verification commands are printed for manual review rather than executed automatically.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
