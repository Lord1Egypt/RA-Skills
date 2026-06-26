## Description: <br>
Runs local quantum_lab Python scripts, notebooks, and demos inside the existing ~/.venvs/qiskit virtual environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BramDo](https://clawhub.ai/user/BramDo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a local quantum_lab Python project in a configured Qiskit virtual environment, including scripts, notebooks, self-tests, playground commands, and a local web server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local commands inside a user-selected quantum_lab repository and virtual environment. <br>
Mitigation: Install and use it only when the local repository, notebooks, and ~/.venvs/qiskit environment are trusted. <br>
Risk: Dependency installation can execute package-install behavior from requirements.txt. <br>
Mitigation: Review requirements.txt before running dependency installation commands. <br>
Risk: Telegram or OpenClaw requests could prompt command execution from an untrusted requester. <br>
Mitigation: Treat chat requests as proposals and run qexec commands only when the requester and command intent are trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume a local quantum_lab repository and Qiskit virtual environment; QUANTUM_LAB_ROOT and VENV_PATH can override defaults.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
