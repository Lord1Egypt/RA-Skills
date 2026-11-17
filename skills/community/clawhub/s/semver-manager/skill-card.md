## Description:

Parse, validate, compare, sort, bump, and filter semantic versions (semver). Use when asked to check version compatibility, bump version numbers, sort releases, find latest matching version, or validate semver strings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to validate, compare, sort, bump, filter, and find matching semantic versions during release and dependency management work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled semantic-version parser may not match every edge case expected by a specific release workflow.

Mitigation: Review the bundled script's behavior against the versions and constraints used in your workflow before relying on exact semver edge-case handling.

Risk: The skill executes a local Python utility on user-provided version strings.

Mitigation: Run it only in environments where local script execution is acceptable and inspect the script before installation when execution policy requires review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/semver-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; bundled script output can be text, JSON, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Python CLI on version strings supplied by the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
