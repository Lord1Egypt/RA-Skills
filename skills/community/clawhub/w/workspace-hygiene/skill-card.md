## Description:

Audit and maintain workspace file structure, memory quality, and project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevemichael001](https://clawhub.ai/user/stevemichael001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to audit OpenClaw agent workspaces, identify structure and memory hygiene issues, and generate prioritized cleanup reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted workspace could redirect file reads or writes outside the intended folder through unsafe file handling.

Mitigation: Run the skill only against trusted workspaces, review symlinks before use, and avoid elevated privileges.

Risk: Using --fix can change workspace memory files by merging timestamped entries.

Mitigation: Use --report-only first on shared or unfamiliar workspaces, review the generated report, and apply fixes only after confirming the target files.

Risk: --report-only still writes a report file.

Mitigation: Treat report-only mode as no-fix mode rather than a dry run, and run it only where creating projects/system/hygiene-YYYY-MM-DD.md is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevemichael001/skills/workspace-hygiene)
- [audit.md](artifact/audit.md)
- [memory-format.md](artifact/memory-format.md)
- [rag-index.md](artifact/rag-index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with command-line summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a hygiene report to projects/system/hygiene-YYYY-MM-DD.md and may merge timestamped memory files when --fix is used.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
