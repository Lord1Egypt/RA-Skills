## Description:

Monitor and manage Rollbar error tracking. List recent items, get item details, resolve/mute issues, track deployments, and manage project access tokens via the Rollbar API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vittor1o](https://clawhub.ai/user/vittor1o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Rollbar projects, triage error items, review occurrences and deployments, and manage project access tokens from an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can execute content from a workspace .env file before calling Rollbar.

Mitigation: Review or patch the skill before installing, avoid running it in untrusted workspaces, and prefer least-privilege token sources until .env loading is parsed as data.

Risk: Account-level write tokens, project-token-create, project-token-update, and --save can create, change, or persist credentials.

Mitigation: Use the least-privilege Rollbar token possible, prefer project-level read tokens for monitoring, and review token-management commands before use.

Risk: State-changing commands can resolve, mute, activate, create, or update Rollbar resources.

Mitigation: Preview state-changing operations with --dry-run and require --yes only after confirming the intended project, item, token, and scope.

## Reference(s):

- [ClawHub Rollbar Skill](https://clawhub.ai/vittor1o/skills/rollbar)
- [Rollbar API Reference](https://docs.rollbar.com/reference)
- [Rollbar API Endpoint](https://api.rollbar.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; reads Rollbar tokens from environment variables or workspace-local configuration files and writes .rollbar-mcp.json when saving project tokens.]

## Skill Version(s):

1.5.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
