## Description:

X Platform API. Read posts, search tweets, post, upload media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to read X posts, search recent tweets, inspect user profiles and bookmarks, and perform account-changing actions such as posting, deleting, bookmarking, and media uploads when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real X account, including posting, deleting posts, bookmarking, and uploading local media.

Mitigation: Use least-privilege credentials and require explicit human approval for posting, deleting, bookmarking, and uploads.

Risk: Media upload accepts local file paths, which can expose unintended files if an agent is allowed to choose paths freely.

Mitigation: Restrict allowed upload directories and review each upload path before execution.

Risk: The security guidance flags the 1Password fallback until the shell invocation is fixed.

Mitigation: Prefer environment variables or read-only bearer tokens unless the 1Password path has been reviewed in the deployment environment.

## Reference(s):

- [X API v2 documentation](https://docs.x.com/x-api)
- [X API authentication documentation](https://docs.x.com/resources/authentication)
- [@xdevplatform/xdk SDK](https://github.com/xdevplatform/xdk)
- [X Developer Portal](https://developer.x.com/en/portal/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance, JSON API responses, JavaScript examples, shell commands, and MCP tool outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X API credentials; read-only operations can use a bearer token, while posting, deletion, bookmarks, and uploads require OAuth credentials.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
