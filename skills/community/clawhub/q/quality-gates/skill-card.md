## Description: <br>
Quality Gates provides quality checkpoints at every development stage, from pre-commit through post-deploy, with configuration examples, threshold tables, bypass protocols, and CI/CD integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up quality automation, CI gate checks, coverage thresholds, security scanning, performance budgets, review requirements, and deployment controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated hooks, branch protections, or required CI checks could unexpectedly block normal development or releases. <br>
Mitigation: Review proposed hooks and CI settings before applying them, then roll out required checks and branch protections carefully. <br>
Risk: Commands that fetch or execute external tooling may rely on upstream package or repository sources. <br>
Mitigation: Verify GitHub and npx sources before running installation or setup commands. <br>


## Reference(s): <br>
- [Quality Gates on ClawHub](https://clawhub.ai/wpank/quality-gates) <br>
- [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks) <br>
- [Ruff pre-commit](https://github.com/astral-sh/ruff-pre-commit) <br>
- [mypy pre-commit mirror](https://github.com/pre-commit/mirrors-mypy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reference guidance for quality gates; users should review commands and CI settings before applying them.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
