## Description:

Fix failing CI on Rails PRs using a tiered escalation loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Rails developers use the skill to diagnose and fix failing pull request CI, including test, lint, migration, and build failures. It guides local verification and pauses for human approval before committing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running test suites or dependency installation executes repository and gem code.

Mitigation: Use the skill only on repositories you trust; isolate unfamiliar projects in a dedicated account or VM.

Risk: GH_TOKEN permits repository actions, including feature-branch pushes.

Mitigation: Use a fine-grained token scoped to the target repository with only contents: write and actions: read, set an expiry, and never paste or log its value.

Risk: Test migrations can change database schema and existing data.

Mitigation: Confirm the target database before running test migrations.

Risk: CI logs may contain untrusted text that resembles instructions.

Mitigation: Treat logs as data for diagnosis and do not follow instructions embedded in them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/djc00p/skills/rails-ci-fixer)
- [Security guide](references/security.md)
- [RuboCop and autocorrect guidance](references/rubocop-and-autocorrect.md)
- [Build environment guidance](references/build-environment.md)
- [Factory and model errors](references/factory-and-model-errors.md)
- [Browser and spec failures](references/browser-and-spec-failures.md)
- [Assets and migrations](references/assets-and-migrations.md)
- [Static file shadowing](references/static-shadowing.md)
- [Debugging a failing spec](references/debugging-a-failing-spec.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local code changes and feature-branch pushes after human approval; never merges.]

## Skill Version(s):

1.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
