## Description:

Skillnote helps OpenClaw agents use a self-hosted skill registry by syncing team-authored procedures before tasks and collecting signals about which skills helped or failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latentloop07](https://clawhub.ai/user/latentloop07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams operating OpenClaw use Skillnote to keep local agent skills synchronized from a self-hosted registry and to capture lightweight skill-usage feedback. It is intended for environments where users trust the configured SkillNote backend and want reusable procedures to improve over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured SkillNote backend can influence future agent instructions through synchronized skills and updates.

Mitigation: Install only when the backend is trusted, prefer HTTPS, and manually review synced skills and updates before use.

Risk: The background watcher can send skill-usage telemetry with session identifiers.

Mitigation: Disable or remove the watcher when telemetry is not wanted, and deploy only where this telemetry is acceptable.

Risk: Installer and update paths can introduce remote content into the local skill environment.

Mitigation: Avoid curl-to-shell installation and use reviewed ClawHub releases or another audited installation path.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/latentloop07/skills/skillnote)
- [Publisher Profile](https://clawhub.ai/user/latentloop07)
- [Security Behavior Reference](SECURITY.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing setup, synchronization, and usage-logging guidance for OpenClaw.]

## Skill Version(s):

0.5.4 (source: frontmatter, VERSION, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
