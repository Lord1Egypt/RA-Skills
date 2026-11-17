## Description:

Run quantum_lab scripts and demos inside an existing qiskit virtual environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bramdo](https://clawhub.ai/user/bramdo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run quantum_lab scripts, demos, notebooks, tests, and a local quantumapp server from a configured repository and qiskit virtual environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can run arbitrary local commands in the configured quantum_lab repository.

Mitigation: Use the skill only in environments where local command execution is acceptable, and prefer reviewed command lists over free-form qexec usage.

Risk: The repository and virtual environment paths are configurable and may point to untrusted local content.

Mitigation: Review and trust QUANTUM_LAB_ROOT and VENV_PATH before installation or execution.

Risk: Dependency installation may pull packages from the configured repository's requirements file.

Mitigation: Use reviewed and pinned dependency files before running pip install commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable repository and virtual environment paths through QUANTUM_LAB_ROOT and VENV_PATH.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
