## Description: <br>
Skill Compass diagnoses, fixes, and helps prevent agent skill trigger failures by auditing descriptions, YAML frontmatter, token budgets, conflicts, and discovery paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit existing agent skills, diagnose why skills do not activate, and optionally apply scoped fixes to SKILL.md descriptions and frontmatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix mode can persistently change local skill files with weak scoping and safeguards. <br>
Mitigation: Prefer audit-only mode, use a narrow target path when applying fixes, review diffs before accepting changes, and keep version control or backups available for rollback. <br>
Risk: The skill needs access to inspect local skill files and may surface or alter local configuration guidance. <br>
Mitigation: Run it only in trusted workspaces and review its findings before acting on proposed shell commands, configuration changes, or file edits. <br>


## Reference(s): <br>
- [Failure Pattern Reference](artifact/references/failure-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, optional JSON audit reports, and proposed code or configuration changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit results may include scores, issue descriptions, suggestions, conflict findings, token budget status, and optional file edits when fix mode is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
