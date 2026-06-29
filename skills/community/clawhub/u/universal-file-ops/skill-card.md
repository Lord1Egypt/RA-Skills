## Description: <br>
Universal File Ops helps agents perform standardized file CRUD, Python environment management, code quality checks, sandbox testing, and structured workflow reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to make file operations, Python script generation, code review, test generation, sandbox test runs, and environment setup more repeatable. It is intended for agent workflows that need structured reports, backups, rollback IDs, and phased execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, overwrite, move, or delete user-specified files. <br>
Mitigation: Use it in a constrained workspace, review target paths before execution, keep backups enabled, record rollback IDs, and avoid --no-backup unless the files are disposable. <br>
Risk: The skill can create persistent backups, logs, and virtual environments. <br>
Mitigation: Review storage locations and clean backup, log, and venv directories according to local retention requirements. <br>
Risk: The skill can install Python packages from the network. <br>
Mitigation: Install only trusted packages, prefer pinned dependencies where possible, and avoid package installation on untrusted projects. <br>
Risk: The skill can execute tests and subprocess-backed workflows. <br>
Mitigation: Run sandbox tests and orchestration only on code you trust, and keep execution inside a restricted workspace. <br>


## Reference(s): <br>
- [Skill Overview](SKILL.md) <br>
- [User Guide](references/guide.md) <br>
- [Permissions and Risk Notes](references/permissions.md) <br>
- [Python Coding Standards](references/py_standards.md) <br>
- [Report Templates](references/report_templates.md) <br>
- [Error Codes](references/error_codes.md) <br>
- [Changelog](references/changelog.md) <br>
- [Python Downloads](https://www.python.org/downloads/) <br>
- [Python Package Index](https://pypi.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include file-operation results, rollback IDs, generated Python code or tests, review findings, sandbox-test summaries, and phased workflow reports.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence, SKILL.md frontmatter, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
