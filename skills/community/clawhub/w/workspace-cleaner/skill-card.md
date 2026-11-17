## Description:

Automates safe cleanup of OpenClaw workspaces by previewing and moving temporary files, logs, duplicate repositories, and other workspace cruft to the system trash with configurable filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:


## Use Case:

Developers and workspace maintainers use this skill to preview cleanup candidates and remove temporary files, logs, generated root-level assets, stray dependencies, virtual environments, and duplicate repositories while preserving configured protected files and directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup execution can move valuable workspace files or whole repositories to trash when automatic or custom cleanup rules are too broad.

Mitigation: Run preview mode first, inspect every target, keep custom configs trusted and narrow, and avoid unattended --execute runs.

Risk: Duplicate repository cleanup can be high risk if local repository state is not fully verified.

Mitigation: Before executing duplicate cleanup, confirm clean working trees, matching commits, and no local-only data.

Risk: Root-level generated assets, virtual environments, or logs may be intentionally retained even when they match cleanup patterns.

Mitigation: Use age and size filters, maintain protected patterns, and review suspicious matches before moving them to trash.

## Reference(s):

- [Safe Defaults Reference](references/safe-defaults.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text cleanup previews and status messages, with optional JSON summaries for automation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run preview is the default; execution mode moves matched items to system trash when a supported trash command is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
