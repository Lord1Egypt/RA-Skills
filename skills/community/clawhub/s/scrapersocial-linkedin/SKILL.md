---
name: linkedin-api
version: 1.0.4
description: LinkedIn data toolkit via ScraperSocial — profiles and 20 sub-resources, company data, people/company/job search, posts, comments, reactions and ad search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - linkedin
  - b2b
  - lead-generation
  - jobs
  - recruiting
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

# LinkedIn API skill

Read public LinkedIn data as clean JSON. This LinkedIn API skill is the largest surface in the repo: a profile plus twenty sub-resources — experiences, educations, skills, certifications, publications, patents, recommendations, volunteering and more — alongside company data, funding and insights, people search, company search, job search, post reactions and comment threads, and the LinkedIn ad library.

LinkedIn is the hardest mainstream platform to read programmatically and the one most people want most. Each sub-resource is its own endpoint, so you pay for the slice you need instead of pulling a whole profile to read one field.

This skill wraps **38 live LinkedIn endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are enriching a lead or candidate record from a public profile URL or handle.
- You need one slice of a profile — just the work history, just the skills — rather than everything.
- You are researching a company: headcount, funding, insights, open jobs, employees, posts.
- You are sourcing candidates or prospects through people search or job search.
- You are analysing engagement on a post: reactions, comments and replies.

### Do not use this skill when

- **Watch the cost.** `get_profile.js --section=contact` costs 25 credits, the most expensive non-video call here. Full profiles and company records cost 10. Fetch the specific section you need instead of the whole profile.
- **You are compiling personal data at scale.** This returns information about real people. GDPR, CCPA and LinkedIn's own terms apply to what you do with it. Have a lawful basis, honour deletion requests, and do not build unsolicited bulk-contact lists where that is restricted.
- **You need to send connection requests or InMail.** Read-only.
- **You need private profile fields** or anything behind a login. Public data only.
- **A LinkedIn link appears in passing** with no question attached.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 38 documented `/v1/linkedin/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` | Public profile data for a LinkedIn member: headline, positions, education. | url|handle | 10 credits (25 with include_email=true) |
| `get_profile.js` `--section=about` | Get LinkedIn profile about. | url|handle | 5 credits |
| `get_profile.js` `--section=certifications` | Get LinkedIn profile certifications. | url|handle | 5 credits |
| `get_profile.js` `--section=comments` | List LinkedIn profile comments. | url|handle | 5 credits per comment |
| `get_profile.js` `--section=contact` | Get LinkedIn profile contact. | url|handle | 25 credits |
| `get_profile.js` `--section=courses` | Get LinkedIn profile courses. | url|handle | 5 credits |
| `get_profile.js` `--section=educations` | Get LinkedIn profile educations. | url|handle | 5 credits |
| `get_profile.js` `--section=experiences` | Get LinkedIn profile experiences. | url|handle | 5 credits |
| `get_profile.js` `--section=full` | Get LinkedIn profile full. | url|handle | 10 credits |
| `get_profile.js` `--section=honors` | Get LinkedIn profile honors. | url|handle | 5 credits |
| `get_profile.js` `--section=languages` | Get LinkedIn profile languages. | url|handle | 5 credits |
| `get_profile.js` `--section=patents` | Get LinkedIn profile patents. | url|handle | 5 credits |
| `get_profile.js` `--section=posts` | List LinkedIn profile posts. | url|handle | 5 credits per post |
| `get_profile.js` `--section=projects` | Get LinkedIn profile projects. | url|handle | 5 credits |
| `get_profile.js` `--section=publications` | Get LinkedIn profile publications. | url|handle | 5 credits |
| `get_profile.js` `--section=reactions` | List LinkedIn profile reactions. | url|handle | 5 credits per reaction |
| `get_profile.js` `--section=recommendations` | Get LinkedIn profile recommendations. | url|handle | 5 credits |
| `get_profile.js` `--section=similar` | Get LinkedIn profile similar. | url|handle | 5 credits |
| `get_profile.js` `--section=skills` | Get LinkedIn profile skills. | url|handle | 5 credits |
| `get_profile.js` `--section=stats` | Get LinkedIn profile stats. | url|handle | 5 credits |
| `get_profile.js` `--section=volunteers` | Get LinkedIn profile volunteers. | url|handle | 5 credits |
| `get_company.js` | Company page data: industry, size, followers and description. | url|handle | 10 credits |
| `get_company.js` `--section=funding` | Get LinkedIn company funding. | url|handle | 10 credits |
| `get_company.js` `--section=insights` | Get LinkedIn company insights. | url|handle | 10 credits |
| `get_company.js` `--section=jobs` | List LinkedIn company jobs. | url|handle | 5 credits per job |
| `get_company.js` `--section=people` | List LinkedIn company people. | url|handle | 5 credits per profile |
| `get_company.js` `--section=posts` | Latest posts from a LinkedIn company page with per-post metrics. | url|handle | 5 credits per post |
| `get_company.js` `--section=search` | List LinkedIn company search. | query | 5 credits per company |
| `get_post.js` `--section=comment-replies` | List LinkedIn post comment replies. | url | 5 credits per comment |
| `get_post.js` `--section=reactions` | List LinkedIn post reactions. | url | 5 credits per reaction |
| `people_search.js` | Search public LinkedIn profiles by keyword, title, company or location. | query | 5 credits per profile |
| `people_search.js` `--section=by-name` | List LinkedIn people search by name. | query | 5 credits per profile |
| `people_search.js` `--section=by-services` | List LinkedIn people search by services. | query | 5 credits per profile |
| `job_search.js` | List LinkedIn job search. | query | 5 credits per job |
| `ads_search.js` | List LinkedIn ads search. | query | 5 credits per ad |
| `get_comments.js` | Paginated comments on a LinkedIn post; charged per comment returned. | url | 5 credits per comment |
| `search.js` | Keyword search over public LinkedIn posts. | query | 5 credits per result |
| `get_stats.js` | Reactions, comments and reposts for a LinkedIn post. | url | 5 credits |
| `call_endpoint.js` | Call any `/v1/linkedin/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/linkedin-api/scripts/people_search.js "product manager fintech"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/linkedin/ads-search` | query | ad | 5 credits per ad | yes |
| `/v1/linkedin/comments` | url | comment | 5 credits per comment | yes |
| `/v1/linkedin/company` | url|handle | company | 10 credits | no |
| `/v1/linkedin/company-funding` | url|handle | company | 10 credits | no |
| `/v1/linkedin/company-insights` | url|handle | company | 10 credits | no |
| `/v1/linkedin/company-jobs` | url|handle | job | 5 credits per job | yes |
| `/v1/linkedin/company-people` | url|handle | profile | 5 credits per profile | yes |
| `/v1/linkedin/company-posts` | url|handle | post | 5 credits per post | yes |
| `/v1/linkedin/company-search` | query | company | 5 credits per company | yes |
| `/v1/linkedin/job-search` | query | job | 5 credits per job | yes |
| `/v1/linkedin/people-search` | query | profile | 5 credits per profile | yes |
| `/v1/linkedin/people-search-by-name` | query | profile | 5 credits per profile | yes |
| `/v1/linkedin/people-search-by-services` | query | profile | 5 credits per profile | yes |
| `/v1/linkedin/post-comment-replies` | url | comment | 5 credits per comment | yes |
| `/v1/linkedin/post-reactions` | url | reaction | 5 credits per reaction | yes |
| `/v1/linkedin/profile` | url|handle | profile | 10 credits (25 with include_email=true) | no |
| `/v1/linkedin/profile-about` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-certifications` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-comments` | url|handle | comment | 5 credits per comment | yes |
| `/v1/linkedin/profile-contact` | url|handle | profile | 25 credits | no |
| `/v1/linkedin/profile-courses` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-educations` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-experiences` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-full` | url|handle | profile | 10 credits | no |
| `/v1/linkedin/profile-honors` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-languages` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-patents` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-posts` | url|handle | post | 5 credits per post | yes |
| `/v1/linkedin/profile-projects` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-publications` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-reactions` | url|handle | reaction | 5 credits per reaction | yes |
| `/v1/linkedin/profile-recommendations` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-similar` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-skills` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-stats` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/profile-volunteers` | url|handle | profile | 5 credits | no |
| `/v1/linkedin/search` | query | result | 5 credits per result | yes |
| `/v1/linkedin/stats` | url | post | 5 credits | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get a LinkedIn profile as JSON?

`get_profile.js` with the profile URL or handle returns the core profile for 10 credits; `--section=full` returns the expanded record. For one slice, use the matching section — `--section=experiences`, `--section=skills`, `--section=educations` and so on.

### How do I get someone's contact details?

`get_profile.js --section=contact` returns the contact record for 25 credits. Separately, the default `get_profile.js` accepts `--include_email`, which adds the email to the base profile and reprices that call from 10 credits to 25. `--include_email` applies only to the default section; it is not accepted anywhere else. Only pull either with a lawful basis for processing that person's data.

### Can I search LinkedIn for people, companies or jobs?

Yes: `people_search.js` (with `--section=by-name` or `--section=by-services`), `get_company.js --section=search`, and `job_search.js`. Each costs 5 credits per result returned.

### How do I get company data?

`get_company.js` returns the company for 10 credits. Sections cover `funding`, `insights`, `jobs`, `people` and `posts`.

### Is this an official LinkedIn API?

No. ScraperSocial is independent and not affiliated with LinkedIn or Microsoft. It returns publicly available data only. LinkedIn's own Marketing and Talent APIs are the sanctioned route for partner use cases.

## Links

- [LinkedIn data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
