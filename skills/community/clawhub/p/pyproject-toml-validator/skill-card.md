## Description: <br>
Validate Python project pyproject.toml files against PEP 517 and PEP 621 rules for project metadata, build system settings, dependencies, and common tool configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to check Python project pyproject.toml files before local development, packaging, or CI publication. It helps identify metadata, build-system, dependency, and formatter or linter configuration issues with actionable validation output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict validation mode can fail local or CI builds based on reported pyproject.toml issues. <br>
Mitigation: Review the reported issues and run the validator on intended project files before enabling strict mode in CI. <br>
Risk: The bundled Python script is executable local code. <br>
Mitigation: Treat it like any bundled script: review it before CI use and run it only against intended project files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/pyproject-toml-validator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with command examples and text, JSON, or summary validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports validate, project, build, and tools commands; strict mode can return a failing exit code for CI workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
