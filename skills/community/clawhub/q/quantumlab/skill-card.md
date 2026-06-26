## Description: <br>
Run quantum_lab Python scripts and demos inside an existing Qiskit virtual environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BramDo](https://clawhub.ai/user/BramDo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run local quantum_lab scripts, demos, notebooks, tests, and the quantumapp.server command through a configured Qiskit virtual environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local quantum_lab commands that install dependencies or start a local service when invoked. <br>
Mitigation: Install only when that local command execution is intended; review requirements.txt before dependency installation and confirm before starting a web server or notebook. <br>
Risk: Ambiguous or untrusted external prompts could trigger unintended command execution through shorthand commands. <br>
Mitigation: Ask for a clear subcommand before execution and avoid triggering the skill from ambiguous chat messages or untrusted external prompts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands execute against a local quantum_lab checkout and a preconfigured Qiskit virtual environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
