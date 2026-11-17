## Description:

Drift detection + baseline integrity guard for agent workspace files with automatic alerting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw workspace prompt and instruction files for unexpected drift, generate review artifacts, and optionally restore critical files to approved baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy paths or setup snippets could affect files outside the intended workspace or run unintended shell commands.

Mitigation: Review policy targets before use, reject absolute paths or traversal, and avoid generated shell snippets for paths containing shell metacharacters.

Risk: Restore mode intentionally overwrites protected workspace files with approved baselines.

Mitigation: Start with --no-restore until baselines are trusted, review diffs and quarantine copies, and approve only intentional changes.

Risk: Guardian state can contain sensitive snapshots, diffs, and quarantined copies.

Mitigation: Keep the state directory private with restrictive permissions such as chmod 700 for directories and chmod 600 for files.

Risk: Recurring background checks can run through cron or launchd if enabled.

Mitigation: Treat scheduling as an explicit operator decision and avoid launchd --install unless recurring execution is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/soul-guardian)
- [Publisher profile](https://clawhub.ai/user/davida-ps)
- [Project homepage](https://clawsec.prompt.security)
- [Artifact README](artifact/README.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled scripts can emit plain-text alerts and JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local state, audit logs, diffs, quarantine copies, and optional launchd plist files when invoked.]

## Skill Version(s):

0.0.6 (source: SKILL.md frontmatter, artifact/skill.json, CHANGELOG released 2026-05-14, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
