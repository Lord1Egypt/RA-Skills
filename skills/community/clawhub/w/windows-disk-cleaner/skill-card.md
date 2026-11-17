## Description:

Safe Windows disk cleanup assistant that scans Windows drives, analyzes temporary files, developer caches, browser caches, Windows Update leftovers, large files, duplicate files, and node_modules, then generates an interactive report with safe, review, and never-touch cleanup tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guge0](https://clawhub.ai/user/guge0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT staff, and Windows power users use this skill to inspect disk usage, identify cleanup candidates, and generate reviewable cleanup commands and reports before deleting local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cleanup commands may delete important Firefox profile data or Docker volumes.

Mitigation: Inspect every generated command before execution, remove Docker `--volumes`, and avoid any command targeting Firefox profile roots.

Risk: Generated reports can expose local usernames, file paths, and file inventories.

Mitigation: Treat reports as sensitive local artifacts and redact or avoid sharing them outside the intended review workflow.

## Reference(s):

- [Windows Safe Cleanup Paths](references/safe_paths.md)
- [ClawHub Skill Page](https://clawhub.ai/guge0/skills/windows-disk-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands, JSON scan results, and an HTML cleanup report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; generated reports may contain local usernames, paths, and file inventories.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
