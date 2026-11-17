## Description:

Advanced Python 3.13 on Windows: typed package design, pyproject/src layout, asyncio and cancellation, threads vs processes, robust subprocesses, pytest, ruff/mypy, profiling, C/PyO3 extensions, and Windows-specific failures. Use after the python-advanced basics when code must be typed, packaged, concurrent, testable, or fast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, package, type-check, test, profile, and troubleshoot advanced Python applications, with emphasis on asynchronous and concurrent work and Windows-specific behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adapting file-writing or subprocess examples with unintended paths or command arguments can affect local files or run unintended commands.

Mitigation: Review command arguments and output paths before running examples, use a project virtual environment, and keep backups before reformatting JSON files.

Risk: Outdated development dependencies may expose projects to known issues.

Mitigation: Use patched development dependencies, including pytest 9.0.3 or later, as advised by the release security guidance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/deepseekoracle/skills/python-advanced)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [Python typing](https://docs.python.org/3/library/typing.html)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)
- [Python venv](https://docs.python.org/3/library/venv.html)
- [Python concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [pytest](https://docs.pytest.org/)
- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)
- [PyO3](https://pyo3.rs/)
- [maturin](https://www.maturin.rs/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, PowerShell, and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable examples and troubleshooting guidance focused on Python development on Windows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
