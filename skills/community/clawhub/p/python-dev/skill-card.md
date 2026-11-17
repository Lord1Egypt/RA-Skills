## Description:

Opinionated Python development setup with uv, ty, ruff, pytest, lefthook, and just. Use when creating a new Python project, writing or fixing pyproject.toml, or configuring linting, formatting, type checking, testing, git hooks, or CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to start or modernize Python projects and configure their package metadata, linting, formatting, type checking, tests, Git hooks, and CI with a consistent toolchain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git hooks may automatically fix and restage files.

Mitigation: Review the generated changes in the intended repository, especially changes made by automatic hooks.

Risk: The clean recipe removes build and cache directories.

Mitigation: Run cleanup from the project root.

Risk: Project configuration or commands may expose environment secrets.

Mitigation: Protect .env values and retain a reviewed lockfile.

Risk: Downloaded third-party packages have not been audited.

Mitigation: Review the selected dependencies and their lockfile before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tenequm/skills/python-dev)
- [Skill homepage (as listed in metadata)](https://github.com/tenequm/skills/tree/main/skills/python-dev)
- [uv documentation](https://docs.astral.sh/uv/)
- [ty documentation](https://docs.astral.sh/ty/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [just manual](https://just.systems/man/en/)
- [Lefthook documentation](https://lefthook.dev/)
- [uv-reference.md](artifact/references/uv-reference.md)
- [ty-reference.md](artifact/references/ty-reference.md)
- [ruff-reference.md](artifact/references/ruff-reference.md)
- [pytest-reference.md](artifact/references/pytest-reference.md)
- [justfile-reference.md](artifact/references/justfile-reference.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Development guidance]

**Output Format:** [Markdown with Python, shell, TOML, YAML, and Justfile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and configuration templates for adapting to a project]

## Skill Version(s):

0.3.1 (source: SKILL.md frontmatter, released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
