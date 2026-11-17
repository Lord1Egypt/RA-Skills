## Description:

Tide Watch helps OpenClaw users monitor local session capacity, receive configurable threshold warnings, manage resumption prompts, and optionally run a local CLI for dashboards, reports, and session archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisagiddings](https://clawhub.ai/user/chrisagiddings)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill during long-running or multi-channel work to detect context-window capacity issues before sessions lock, preserve continuity through resumption prompts, and review local session status. Users who need active management can optionally install the CLI for reports, dashboards, and archive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional CLI has a path-validation weakness around session handling.

Mitigation: Prefer directives-only mode; if using the CLI, provide only trusted session IDs and avoid hand-crafted identifiers.

Risk: Archive and delete operations can modify local OpenClaw session files.

Mitigation: Use dry-run review before archive/delete actions and keep independent backups for sensitive workspaces.

Risk: Documentation may overstate automatic backup or reset behavior.

Mitigation: Treat backup and reset claims as workflow guidance unless verified in the installed version and test behavior before relying on it.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/chrisagiddings/skills/tide-watch)
- [README](README.md)
- [Usage examples](docs/USAGE-EXAMPLES.md)
- [FAQ](docs/FAQ.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Parsing behavior](PARSING.md)
- [Security advisory CVE-2026-001](SECURITY-ADVISORY-CVE-2026-001.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directives-only mode can avoid code installation; optional CLI mode operates on local OpenClaw session files.]

## Skill Version(s):

1.3.6 (source: SKILL.md metadata, package.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
