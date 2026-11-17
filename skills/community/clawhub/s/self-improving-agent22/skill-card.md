## Description:

Interact with GitHub using the gh CLI for pull request checks, workflow run details, logs, API queries, and JSON output filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and guidance for inspecting pull request checks, workflow runs, failed logs, GitHub API responses, and structured issue or pull request data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands may run using the user's existing gh login and repository permissions.

Mitigation: Review commands before execution, specify the intended repository explicitly, and be especially cautious with write-capable gh operations.

Risk: Repository, issue, pull request, workflow, or log data may be exposed through gh api queries and jq filters.

Mitigation: Run queries only against intended repositories and review requested fields before sharing command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yequanzheng/skills/self-improving-agent22)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands, gh api examples, JSON field selections, and jq filters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
