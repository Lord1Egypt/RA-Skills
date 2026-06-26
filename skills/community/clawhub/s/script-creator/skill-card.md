## Description: <br>
Create and modify scripts in ~/.nanobot/workspace/test with strict Git versioning, one repository per script, user confirmation before changes, and a shared Python virtual environment for package management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cadot-eu](https://clawhub.ai/user/cadot-eu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to create or modify local scripts through a confirmation-gated workflow that keeps each script in its own Git repository. It is intended for controlled script editing, dependency installation through a dedicated virtual environment, and progress reporting after each step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify local files and Git repositories under ~/.nanobot/workspace/test. <br>
Mitigation: Review the proposed directory, file name, requested edits, and commit message before confirming the plan. <br>
Risk: The skill can install Python packages into ~/.nanobot/workspace/venv. <br>
Mitigation: Approve only trusted and preferably pinned packages before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cadot-eu/script-creator) <br>
- [Publisher profile](https://clawhub.ai/user/cadot-eu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local script files, initialize Git repositories, commit changes, and install Python packages after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
