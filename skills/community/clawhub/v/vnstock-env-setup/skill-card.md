## Description: <br>
Comprehensive environment diagnostic, setup, and agent guide installation for the Vnstock ecosystem (Free or Sponsored). Validates OS, Python, venv, and performs migrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinh-vu](https://clawhub.ai/user/thinh-vu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose and set up local or cloud Python environments for the Vnstock ecosystem. It guides virtual environment creation, package installation, optional Sponsor setup, Agent Guide installation, and migration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow can run remote installers, including pipe-to-shell Sponsor installation commands. <br>
Mitigation: Verify the remote installer source before execution, prefer a safer manual installer when available, and avoid passing API keys through inline remote shell commands. <br>
Risk: The Agent Guide installer can overwrite docs, AGENTS.md, CLAUDE.md, and selected skill directories in the target project. <br>
Mitigation: Run only in a clean or backed-up project, review the files that will be changed, and require explicit user confirmation before overwriting existing docs. <br>
Risk: The workflow can make persistent Git changes while preparing backups. <br>
Mitigation: Inspect the working tree before and after execution and confirm any generated commits or file changes before continuing project work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thinh-vu/vnstock-env-setup) <br>
- [Publisher profile](https://clawhub.ai/user/thinh-vu) <br>
- [Vnstock Agent Guide repository](https://github.com/vnstock-hq/vnstock-agent-guide.git) <br>
- [Vnstock requirements file](https://vnstocks.com/files/requirements.txt) <br>
- [Vnstock Sponsor installer](https://vnstocks.com/files/vnstock-cli-installer.run) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite project documentation, agent guidance files, skill directories, and Git commits when the Agent Guide workflow is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
