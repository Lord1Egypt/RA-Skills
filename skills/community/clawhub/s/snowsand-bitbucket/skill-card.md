## Description:

Interact with Bitbucket Cloud via REST API for repository management, pull request operations, branch management, commit history, pipeline status, and workspace/team queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to let an agent inspect and manage Bitbucket Cloud repositories, pull requests, branches, commits, pipelines, workspaces, and users through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent direct write access to Bitbucket repositories and pull requests.

Mitigation: Use the narrowest Bitbucket token scopes and workspace access possible, and require explicit human confirmation before write operations.

Risk: Repository creation, branch deletion, pull request approval, merge, decline, comment, raw curl, and pipeline-run actions can change project state.

Mitigation: Review the exact target workspace, repository, branch, pull request, and command arguments before allowing those actions to run.

Risk: Credentials are supplied through environment variables and may authorize access beyond the intended repository.

Mitigation: Provide credentials only for the intended workspace, rotate tokens regularly, and avoid broad account-level permissions.

## Reference(s):

- [Bitbucket Cloud API Reference](references/api.md)
- [Bitbucket Cloud REST API documentation](https://developer.atlassian.com/cloud/bitbucket/rest/)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Bitbucket App Passwords](https://bitbucket.org/account/settings/app-passwords/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Bitbucket workspace and credential environment variables; API responses depend on the authenticated account permissions.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
