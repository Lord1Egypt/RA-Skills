## Description:

Diagnose always-loaded workspace context files such as AGENTS.md, SOUL.md, USER.md, MEMORY.md, and TOOLS.md. Use when you want to reduce context bloat, detect duplicated rules, spot misplaced content, identify overweight sections, or audit whether core context files still match their intended roles before reorganizing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lethehades](https://clawhub.ai/user/lethehades)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to audit always-loaded context files and produce concise cleanup reports before reorganizing them. It helps identify duplicated rules, overweight sections, misplaced content, and suggested moves without automatically rewriting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace context files may contain private preferences or environment details.

Mitigation: Keep generated reports local unless they have been reviewed for sensitive workspace or user-specific content.

Risk: The optional --output path can create directories and overwrite the selected report file.

Mitigation: Choose an explicit report path intentionally and avoid reusing paths that may contain important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lethehades/skills/workspace-context-linter)
- [rules.md](references/rules.md)
- [report-format.md](references/report-format.md)
- [file-roles.md](references/file-roles.md)
- [move-guidelines.md](references/move-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain-text or Markdown-style diagnostic report, optionally saved to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are local diagnostics; an explicit output path can create directories and overwrite the selected report file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
