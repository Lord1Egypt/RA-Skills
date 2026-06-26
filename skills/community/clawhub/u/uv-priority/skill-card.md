## Description: <br>
Prioritize uv over pip for Python package management and execution, and guide agents to wrap Python commands and CLI tools with uv run or uvx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcoracer](https://clawhub.ai/user/marcoracer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to standardize Python dependency management, virtual environment setup, command execution, testing, and Python CLI usage around uv. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change how Python commands are run and how dependencies are installed. <br>
Mitigation: Review dependency-changing commands before approving them. <br>
Risk: The skill may be inappropriate for projects that require pip, Poetry, Conda, system Python, or direct interpreter execution. <br>
Mitigation: Explicitly override the skill when a project requires a different Python package manager or execution model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcoracer/uv-priority) <br>
- [Project homepage](https://github.com/marcoracer/uv-priority) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv to be available and changes how Python, dbt, pytest, and Python CLI commands are selected.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
