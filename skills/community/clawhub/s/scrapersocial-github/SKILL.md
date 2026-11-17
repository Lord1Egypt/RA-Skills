---
name: github-api
version: 1.0.4
description: GitHub data toolkit via ScraperSocial — repositories, commits, contributors, issues, releases, languages, user profiles, repo search and trending.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - github
  - repos
  - developer-data
  - trending
  - social-media
  - api
  - mcp
allowed-tools: Bash(node:*)
metadata:
  openclaw:
    primaryEnv: SCRAPERSOCIAL_KEY
    homepage: https://scrapersocial.com
    requires:
      env:
        - SCRAPERSOCIAL_KEY
    network:
      allow:
        - api.scrapersocial.com
    shell:
      only: scripts/*.js
---

# GitHub API skill

Read public GitHub data as clean JSON. This GitHub API skill covers repositories and their commits, contributors, issues, releases and language breakdown, plus user and organisation profiles, repo search and the trending list. Every endpoint costs 1 credit, making this the cheapest platform in the repo and a good one to test your key against.

This skill wraps **11 live GitHub endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are evaluating a dependency or a project and want its activity, contributors or release history.
- You need issue lists for triage, changelog generation or research.
- You are tracking what is trending, or searching repos by keyword.
- A user pastes a GitHub URL and asks what the project is or how active it is.

### Do not use this skill when

- **You are authenticated and near no rate limit.** GitHub's own REST and GraphQL APIs are free, richer and support writes. Use this when you want one uniform client across many platforms, or want to avoid managing another token.
- **You need private repositories.** Public data only.
- **You need to open issues, push code or comment.** Read-only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 11 documented `/v1/github/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_repo.js` | Get GitHub repo. | handle | 1 credit |
| `get_repo.js` `--section=commits` | List GitHub repo commits. | handle | 1 credit per commit |
| `get_repo.js` `--section=contributors` | List GitHub repo contributors. | handle | 1 credit per contributor |
| `get_repo.js` `--section=issues` | List GitHub repo issues. | handle | 1 credit per issue |
| `get_repo.js` `--section=languages` | List GitHub repo languages. | handle | 1 credit per language |
| `get_repo.js` `--section=releases` | List GitHub repo releases. | handle | 1 credit per release |
| `get_repo.js` `--section=search` | List GitHub repo search. | query | 1 credit per repo |
| `get_repos.js` `--section=org-repos` | List GitHub org repos. | handle | 1 credit per repo |
| `get_repos.js` `--section=user-repos` | List GitHub user repos. | handle | 1 credit per repo |
| `get_profile.js` | Get GitHub profile. | handle | 1 credit |
| `get_trending.js` | List GitHub trending. | query | 1 credit per repo |
| `call_endpoint.js` | Call any `/v1/github/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/github-api/scripts/get_profile.js torvalds
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/github/org-repos` | handle | repo | 1 credit per repo | yes |
| `/v1/github/profile` | handle | profile | 1 credit | no |
| `/v1/github/repo` | handle | repo | 1 credit | no |
| `/v1/github/repo-commits` | handle | commit | 1 credit per commit | yes |
| `/v1/github/repo-contributors` | handle | contributor | 1 credit per contributor | yes |
| `/v1/github/repo-issues` | handle | issue | 1 credit per issue | yes |
| `/v1/github/repo-languages` | handle | language | 1 credit per language | yes |
| `/v1/github/repo-releases` | handle | release | 1 credit per release | yes |
| `/v1/github/repo-search` | query | repo | 1 credit per repo | yes |
| `/v1/github/trending` | query | repo | 1 credit per repo | yes |
| `/v1/github/user-repos` | handle | repo | 1 credit per repo | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get a repo's commits as JSON?

`get_repo.js --section=commits` with the `owner/name` handle. Commits, contributors, issues, languages and releases are all sections of the same script.

### How do I list a user's or an organisation's repositories?

`get_repos.js --section=user-repos` or `get_repos.js --section=org-repos`, passing the handle.

### Why use this instead of GitHub's own API?

Mostly consistency: same envelope, same auth and same client as the other 32 platforms here. If GitHub is the only source you need, their official API is free and a better fit.

### Is this an official GitHub API?

No. ScraperSocial is independent and not affiliated with GitHub. It returns publicly available data only.

## Links

- [GitHub data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
