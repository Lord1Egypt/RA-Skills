## Description: <br>
Proactive session capacity monitoring and management for OpenClaw that warns at configurable thresholds, supports session resumption prompts, and includes optional CLI tools for capacity checks, dashboards, archive management, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisagiddings](https://clawhub.ai/user/chrisagiddings) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Tide Watch to monitor session capacity, receive threshold warnings, prepare session resumption prompts, and optionally run local CLI commands for dashboards, reports, and archive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional local CLI can read OpenClaw session files, discover sessions across agents, and move or delete session-related files when management commands are invoked. <br>
Mitigation: Prefer Directives-Only mode for capacity warnings, inspect the CLI before installation, use dry-run or read-only commands first, and avoid running archive or delete workflows on sessions that have not been backed up. <br>
Risk: Session archive, reset, restore, cleanup, or backup behavior can cause data loss if the artifact's backup and restore claims do not match local behavior. <br>
Mitigation: Create independent backups of session files before using session-changing workflows and verify archive or restore results before deleting originals. <br>
Risk: The skill can add or modify local AGENTS.md and HEARTBEAT.md guidance that affects future agent behavior. <br>
Mitigation: Review proposed AGENTS.md and HEARTBEAT.md changes before applying them and keep edits scoped to session-capacity monitoring. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chrisagiddings/tide-watch) <br>
- [README](README.md) <br>
- [Installation Guide](INSTALLATION.md) <br>
- [Usage Examples](docs/USAGE-EXAMPLES.md) <br>
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) <br>
- [Security Advisory CVE-2026-001](SECURITY-ADVISORY-CVE-2026-001.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional CLI text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional CLI mode requires Node.js 14+ and can read, move, or delete local OpenClaw session-related files when invoked.] <br>

## Skill Version(s): <br>
1.3.6 (source: SKILL.md metadata, package.json, CHANGELOG, ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
