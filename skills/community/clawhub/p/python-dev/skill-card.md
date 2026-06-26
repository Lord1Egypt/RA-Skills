## Description: <br>
Opinionated Python development setup with uv, ty, ruff, pytest, and just for creating or modernizing Python projects and configuring pyproject.toml, linting, type checking, testing, and build tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or modernize Python projects with a standardized uv, ty, ruff, pytest, pre-commit, and just workflow. It helps produce pyproject.toml, Justfile, CI, and pre-commit configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested commands can add dependencies, rewrite project configuration, install pre-commit hooks, and remove build or cache directories. <br>
Mitigation: Review commands before execution and apply them in a version-controlled worktree so changes can be inspected and reverted. <br>
Risk: Reference workflows include package publishing steps that could affect external registries if run with active credentials. <br>
Mitigation: Confirm package targets and credentials before publishing; use test registries or dry-run-style review where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/python-dev) <br>
- [uv reference](references/uv-reference.md) <br>
- [ty reference](references/ty-reference.md) <br>
- [ruff reference](references/ruff-reference.md) <br>
- [pytest reference](references/pytest-reference.md) <br>
- [justfile reference](references/justfile-reference.md) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [ty documentation](https://docs.astral.sh/ty/) <br>
- [Ruff documentation](https://docs.astral.sh/ruff/) <br>
- [pytest documentation](https://docs.pytest.org/en/stable/) <br>
- [just manual](https://just.systems/man/en/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline TOML, YAML, Justfile, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project setup recommendations and copyable configuration snippets; users choose whether to execute commands.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
