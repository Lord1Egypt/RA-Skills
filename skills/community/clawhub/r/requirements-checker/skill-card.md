## Description: <br>
Validate, lint, and sort Python requirements.txt files for best practices and CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check Python requirements files for format errors, duplicate packages, risky dependency patterns, and ordering issues before committing or running CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sort --write command can rewrite the selected requirements file. <br>
Mitigation: Preview sorted output first or use version control before running sort --write. <br>
Risk: Dependency lint results may affect CI decisions if used with strict mode. <br>
Mitigation: Review reported rules and use --ignore only for project-approved exceptions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charlie-morrison/requirements-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional text, JSON, or Markdown command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script can print reports to stdout or rewrite a requirements file when sort --write is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
