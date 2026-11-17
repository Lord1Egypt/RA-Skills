## Description:

Validates CI/CD workflow files offline for GitHub Actions, GitLab CI, Keep, and other YAML-based workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bamontejano](https://clawhub.ai/user/bamontejano)

### License/Terms of Use:


## Use Case:

Developers and DevOps engineers use this skill to check workflow syntax and CI logic before committing, running pipelines, or proposing automation changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the inspected artifact contains instructions but does not include the validator scripts it references.

Mitigation: Confirm the validator scripts are supplied by the installed package before relying on generated validation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bamontejano/skills/skill-doctorbot-ci-validator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference package-provided validator scripts when available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
