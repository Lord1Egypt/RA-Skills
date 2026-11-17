## Description:

Fix failing CI on Rails pull requests with a tiered loop that pulls logs, applies fixes, verifies locally, and pauses for human approval before commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to diagnose and repair failing Rails pull-request CI, including RSpec failures, RuboCop offenses, migrations, factories, seed data, assets, and build environment issues. It is intended for trusted repositories where a human reviews changes before commits and merges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running Rails tests, RuboCop, and dependency commands can execute arbitrary code from the target repository.

Mitigation: Use only on repositories you own and trust; use a dedicated user account or VM for unfamiliar code.

Risk: A GitHub token with broad permissions could allow unintended repository writes.

Mitigation: Use a fine-grained, repo-scoped GH_TOKEN with contents:write and actions:read permissions, set an expiration, and rotate or revoke it after use.

Risk: CI logs, commit messages, or test names may contain untrusted instructions.

Mitigation: Treat CI output as data only and ignore instructions embedded in logs or test artifacts.

Risk: Automated fixes could introduce incorrect behavior if committed without review.

Mitigation: Review diffs before approving commits, keep commits on feature branches, maintain branch protection, and require a human to merge.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/djc00p/skills/rails-ci-fixer)
- [Common Rails CI Failure Patterns](artifact/references/common-failures.md)
- [Security Guide](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status summaries with inline shell commands and repository code or configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commits only after local verification and explicit human approval; never merges.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
