## Description:

Validate Vite configuration files exported as JSON for structural correctness, build settings, server security, resolve/CSS hygiene, plugin deprecations, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Vite configuration snapshots during local review, CI checks, or changes to vite.config.ts. It reports structural issues, security-sensitive server settings, deprecated plugins, and practical configuration suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating the JSON snapshot by importing vite.config.ts can execute project code.

Mitigation: Use the documented import command only with trusted Vite configs, or generate the snapshot in a sandbox without secrets, tokens, writable release artifacts, or broad network access.

Risk: The validator analyzes JSON snapshots and cannot prove that the original vite.config.ts uses defineConfig or still matches the snapshot.

Mitigation: Regenerate the snapshot from reviewed source before validation and treat defineConfig-related output as a review reminder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/vite-config-validator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Text, summary, or JSON validation reports with optional command examples and fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports validate, check, explain, and suggest commands; strict mode can treat warnings as errors for CI use.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
