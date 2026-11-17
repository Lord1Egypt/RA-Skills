## Description:

X Platform API. Read posts, search tweets, get bookmarks, post tweets, upload media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to read X posts, search recent tweets, inspect bookmarks and profiles, and perform account actions such as posting, deleting, bookmarking, and uploading media through the X Platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use X credentials that allow posting, deleting, bookmarking, and uploading media.

Mitigation: Prefer a read-only bearer token unless write access is required, and use a dedicated X app or account with the least permissions needed.

Risk: Media upload accepts a local file path, which can expose files available to the agent process.

Mitigation: Run the MCP process with minimal filesystem access and do not expose sensitive directories to the skill.

Risk: Credential lookup can use a 1Password shell invocation identified by the security evidence as unsafe.

Mitigation: Use explicit environment variables or avoid the 1Password auto-lookup path until the shell invocation is hardened.

## Reference(s):

- [Skill Homepage](https://github.com/wipcomputer/wip-xai-x)
- [X API v2](https://docs.x.com/x-api)
- [X API Authentication](https://docs.x.com/resources/authentication)
- [X API Base](https://api.x.com/2)
- [XDK SDK](https://github.com/xdevplatform/xdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON API responses, JavaScript examples, shell commands, and MCP tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated read and write actions against an X account when credentials are configured.]

## Skill Version(s):

1.0.4 (source: frontmatter, package.json, changelog released 2026-03-16, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
