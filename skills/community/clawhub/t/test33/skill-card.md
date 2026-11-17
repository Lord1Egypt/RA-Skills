## Description:

Interact with GitHub using the gh CLI to manage pull requests, check CI status, view workflow runs, and access advanced API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate GitHub through the gh CLI for pull request checks, workflow run inspection, logs, API queries, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands can operate on private or sensitive repositories when run with an authenticated account.

Mitigation: Review proposed commands before execution and confirm the target repository with --repo or a direct URL.

Risk: Advanced gh api use may access data beyond the read-only examples shown in the skill.

Mitigation: Inspect gh api endpoints, filters, and jq expressions before running them, and limit use to the intended repository and operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yequanzheng/skills/test33)
- [Publisher profile](https://clawhub.ai/user/yequanzheng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the caller's existing GitHub CLI authentication and repository access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
