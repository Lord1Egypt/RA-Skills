---
name: subclip-github
description: Inspect a connected GitHub MCP account and its repositories, stars, commits, releases, and date-range changelogs. Use when a creator asks Subclip AI to discover or summarize GitHub activity; repository mutations remain separately confirmation-gated.
---

# Connected GitHub

For an explicit public GitHub pull-request URL, call `fetch_public_github_pull_request` first. It reads public PR metadata, changed files, commits, and the exact diff without requiring a connected account. Then use the connected GitHub MCP for authenticated/private context or to cross-check deeper repository history. Do not ask for `owner/repo` when the URL already identifies it.

## Discover the live GitHub tools

1. Call `mcp_remote__list_tools` for the connected GitHub server with a specific capability query and `includeSchemas: true`.
2. For reads, call the chosen exact tool through `mcp_remote__call_read_tool`, passing only arguments allowed by its returned schema. This bridge is pre-authorized only when the remote server declares `readOnlyHint: true`.
3. If the first query has no match, try the provider's common vocabulary before declaring the capability unavailable: repository/repositories/search, commit/history, release/tag, pull request, authenticated user/profile.

The server's catalog is authoritative and may change. Never hardcode one GitHub MCP tool name.

Do not use the side-effect-capable `mcp_remote__call_tool` for profile, repository, PR, commit, file, diff, release, or tag reads. If a provider fails to declare a read operation read-only, use the public PR result when available and report the annotation gap; do not misreport it as missing GitHub capability.

If repository tools are genuinely missing after live catalog discovery, explain the connection boundary without requesting a token in chat. The creator can reconnect the official remote endpoint with Subclip's encrypted API-key option. For a read-oriented fine-grained PAT, repository access must include the intended repositories, with Metadata read for repository discovery and stars plus Contents read for commit history; Starring user read is needed only to list repositories starred by the authenticated user. A classic PAT normally needs `public_repo` for public-only repository reads or `repo` for private repositories, plus `read:org` only when organization membership/team discovery is required. Organization SSO/PAT policy can still restrict either token type.

## Common reads

- **Connected profile:** discover the authenticated-user/profile tool first. Reuse its login when repository search needs an owner qualifier.
- **Available repositories/projects:** prefer an authenticated repository-list tool. If the catalog only offers repository search, search with the connected login or organization qualifier, paginate, and show name, owner, visibility, default branch, stars, and updated time when supplied.
- **Stars:** use repository metadata or search results that explicitly expose `stargazers_count`/stars. Do not substitute watchers, forks, or likes.
- **Commits in a date range:** discover the commit-list/history tool and inspect its schema for repository owner/name, ref or branch, `since`, `until`, pagination, and author filters. Use ISO-8601 bounds derived from the user's timezone; state the effective range. Paginate until the range is covered or a server limit is reached.
- **PR commits:** for a public PR URL, use `fetch_public_github_pull_request` first and read its `commits` plus `exactDiff`. Use the connected read bridge afterward when private access, branch history, check runs, reviews, or additional commit metadata is needed.
- **Changelog in a date range:** combine releases/tags with commits or merged pull requests in the same range. Prefer release notes when present, group changes by feature/fix/maintenance only when evidence supports it, and link or identify the underlying releases, PRs, or commits returned by GitHub.

When a repository name is unique in the connected account, select it without asking for a redundant `owner/repo`. If multiple repositories match, show the short candidate list and ask which one.

Reads may run directly. Before creating or changing issues, pull requests, releases, files, branches, comments, stars, or repository settings, show the exact GitHub account, repository, action, and submitted fields and obtain confirmation unless the current message already authorizes those exact details.
