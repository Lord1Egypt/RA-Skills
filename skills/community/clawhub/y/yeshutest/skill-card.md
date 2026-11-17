## Description:

Interact with GitHub using the gh CLI to check PR CI status, view workflow runs and logs, and perform advanced API queries with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdlrt](https://clawhub.ai/user/xdlrt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to ask an agent for GitHub CLI commands that inspect pull request checks, workflow runs, failed logs, API responses, and structured GitHub output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands, especially gh api, can access more GitHub data than narrow pull request or workflow-run subcommands when run with broad credentials.

Mitigation: Keep commands pointed at the intended repository and review requested API paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdlrt/skills/yeshutest)
- [Publisher profile](https://clawhub.ai/user/xdlrt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples should be scoped to the intended GitHub repository and the user's configured GitHub access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
