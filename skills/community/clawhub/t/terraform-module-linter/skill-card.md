## Description:

Lint Terraform modules and configurations (.tf files) for structure, naming, security, and best practices. 24 rules across structure, naming, security, and best practices categories. Supports HCL syntax parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to lint Terraform modules and .tf files for structure, naming, security, and best-practice issues before publishing or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lint output may include possible secrets or sensitive infrastructure details from the Terraform files being checked.

Mitigation: Run the linter only on intended paths and handle text or JSON reports according to the confidentiality of the Terraform code.

Risk: Static lint checks can be incomplete or require engineering judgment before changes are made.

Mitigation: Review findings before changing infrastructure modules and keep normal Terraform validation, review, and deployment gates in place.

## Reference(s):

- [Terraform Module Linter on ClawHub](https://clawhub.ai/charlie-morrison/skills/terraform-module-linter)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the linter supports text, JSON, and summary report output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 means no errors or warnings only, 1 means errors found, and 2 means invalid input.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
