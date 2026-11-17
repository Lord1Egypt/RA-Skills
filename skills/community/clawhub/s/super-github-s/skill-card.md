## Description:

Interact with GitHub through the gh CLI for issues, pull requests, CI runs, workflow logs, and advanced API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect and manage GitHub issues, pull requests, workflow runs, CI results, logs, and API-backed repository data with the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to propose GitHub mutations using the user's authenticated gh CLI context.

Mitigation: Review mutation commands before approval, including the target repository, operation, and expected effect.

Risk: Advanced gh api usage can access broad repository data or perform non-GET operations.

Mitigation: Prefer read-only API queries when possible and inspect the endpoint, method, payload, and authentication scope before execution.

Risk: Commands run in the wrong repository can inspect or change unintended GitHub resources.

Mitigation: Use explicit --repo owner/repo arguments or direct GitHub URLs when the working directory does not identify the intended repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-github-s)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with GitHub CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON and jq filters when GitHub CLI commands request structured output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
