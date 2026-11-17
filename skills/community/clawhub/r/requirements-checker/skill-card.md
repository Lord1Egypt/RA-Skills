## Description:

Validate, lint, and sort Python requirements.txt files for best practices and CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI maintainers use this skill to validate, lint, sort, and compare Python requirements.txt files before dependency changes are merged or released.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The in-place sort option can overwrite the user-supplied requirements file.

Mitigation: Preview the default stdout sort first and review the target path before using sort --write.

## Reference(s):

- [Requirements Checker skill page](https://clawhub.ai/charlie-morrison/skills/requirements-checker)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown reports with optional sorted requirements output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Strict mode can return nonzero exit codes for CI; sort --write updates the supplied file in place.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
