## Description:

Audit and maintain workspace file structure, memory quality, and project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevemichael001](https://clawhub.ai/user/stevemichael001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to audit OpenClaw-style workspaces, identify misplaced files, check memory-log health, and generate a prioritized hygiene report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted or untrusted workspace may cause reads or writes outside the selected workspace because of filesystem handling weaknesses.

Mitigation: Use the skill only on trusted workspaces and review its behavior before installation.

Risk: Running with --fix can modify workspace files before symlink containment, backup, and clearer dry-run behavior are added.

Mitigation: Run report-only audits first and avoid --fix until those safeguards are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevemichael001/skills/workspace-hygiene-publish)
- [Audit rules](artifact/audit.md)
- [Memory format](artifact/memory-format.md)
- [RAG index guidance](artifact/rag-index.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with command-line summary text and suggested remediation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated hygiene report under the selected workspace and may consolidate timestamped memory files when run with --fix.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
