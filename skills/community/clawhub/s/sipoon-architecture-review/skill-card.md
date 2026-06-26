## Description: <br>
Reviews a codebase for architecture quality issues such as cyclic dependencies, dead code, oversized modules, high cyclomatic complexity, API boundary problems, and technical debt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run periodic or pre-release architecture audits and receive a prioritized refactoring report. It is also useful when entering an unfamiliar codebase or when a refactoring request needs clearer scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad activation wording and may be invoked for large or private repositories. <br>
Mitigation: Confirm the review scope before running scans, especially for private repositories. <br>
Risk: Suggested follow-on refactoring or agent-team actions could change project behavior if acted on automatically. <br>
Mitigation: Require explicit approval before applying refactors or invoking follow-on agents. <br>
Risk: Some suggested tools may use npx or other package runners that download and execute tooling. <br>
Mitigation: Review and approve command execution and package sources before running downloaded tools. <br>


## Reference(s): <br>
- [Architecture Review skill page](https://clawhub.ai/sipoon/sipoon-architecture-review) <br>
- [Publisher profile: sipoon](https://clawhub.ai/user/sipoon) <br>
- [Packaged skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown architecture review report with issue tables, severity labels, prioritized actions, and suggested command-line checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report may reference optional follow-on skills for refactoring, code indexing, or broader review workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
