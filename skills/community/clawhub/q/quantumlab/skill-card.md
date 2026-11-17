## Description:

Run quantum_lab scripts and demos in the qiskit venv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bramdo](https://clawhub.ai/user/bramdo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run commands, demos, notebooks, tests, and localhost server modes from a local quantum_lab checkout inside a configured Qiskit virtual environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local quantum_lab commands, including notebooks, application modes, localhost server processes, and dependency installation.

Mitigation: Confirm the exact subcommand before execution, and verify QUANTUM_LAB_ROOT and VENV_PATH point to the intended repository and virtual environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bramdo/skills/quantumlab)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume QUANTUM_LAB_ROOT and VENV_PATH point to the intended local repository and virtual environment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
