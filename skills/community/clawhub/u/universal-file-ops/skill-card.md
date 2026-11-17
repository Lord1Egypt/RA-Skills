## Description:

Universal File Ops helps agents perform structured file operations, manage Python environments, run Python code-quality workflows, execute sandbox tests, and produce structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to standardize local file CRUD, Python environment setup, package installation, code review, test generation, sandbox execution, and final reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local file mutation can overwrite, delete, move, or rename user files.

Mitigation: Run the skill only in a disposable or tightly scoped workspace, keep backups enabled, avoid no-backup operations on important data, and review requested paths before execution.

Risk: Python execution and package installation can run untrusted code or install untrusted dependencies.

Mitigation: Use sandbox testing only on trusted code, approve package installs only from trusted package names and sources, and avoid running the skill against untrusted repositories.

Risk: The release security summary reports weak scoping and overstated safety controls.

Mitigation: Treat safety controls as defense in depth, validate generated changes before keeping them, and prefer a restricted workspace with minimal privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/universal-file-ops)
- [guide.md](references/guide.md)
- [permissions.md](references/permissions.md)
- [py_standards.md](references/py_standards.md)
- [report_templates.md](references/report_templates.md)
- [error_codes.md](references/error_codes.md)
- [changelog.md](references/changelog.md)
- [Python Downloads](https://www.python.org/downloads/)
- [Python Package Index](https://pypi.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON command outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, move, delete, back up, or roll back workspace files when the agent invokes bundled scripts.]

## Skill Version(s):

1.3.0 (source: server release evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
