# LinkedIn

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets LinkedIn.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`linkedin/companies`](https://docs.socq.ai/api-manual/linkedin/companies) | LinkedIn Companies API | urls | `company@1.0` | 2 credits/result |
| [`linkedin/company-jobs`](https://docs.socq.ai/api-manual/linkedin/company-jobs) | Collect public LinkedIn company jobs. | urls | `job@1.0` | 0.5 credits/result |
| [`linkedin/company-posts`](https://docs.socq.ai/api-manual/linkedin/company-posts) | Collect public LinkedIn company posts. | urls | `post@1.0` | 1 credits/result |
| [`linkedin/jobs`](https://docs.socq.ai/api-manual/linkedin/jobs) | LinkedIn Jobs API | urls | `job@1.0` | 0.8 credits/result |
| [`linkedin/post-comments`](https://docs.socq.ai/api-manual/linkedin/post-comments) | Collect public LinkedIn post comments. | url | `comment@1.0` | 0.5 credits/result |
| [`linkedin/posts`](https://docs.socq.ai/api-manual/linkedin/posts) | LinkedIn Posts API | urls | `post@1.0` | 1 credits/result |
| [`linkedin/profile-posts`](https://docs.socq.ai/api-manual/linkedin/profile-posts) | Collect public LinkedIn profile posts. | urls | `post@1.0` | 1 credits/result |
| [`linkedin/profiles`](https://docs.socq.ai/api-manual/linkedin/profiles) | LinkedIn Profiles API | urls | `account@1.0` | 2.5 credits/result |
| [`linkedin/search-jobs`](https://docs.socq.ai/api-manual/linkedin/search-jobs) | Search public LinkedIn jobs. | location | `job@1.0` | 0.5 credits/result |
| [`linkedin/search-people`](https://docs.socq.ai/api-manual/linkedin/search-people) | Search public LinkedIn people. | urls | `account@1.0` | 1 credits/result |
| [`linkedin/search-posts`](https://docs.socq.ai/api-manual/linkedin/search-posts) | Search public LinkedIn posts. | query | `post@1.0` | 0.5 credits/result |

## Validated examples

### `linkedin/companies`

Typed MCP tool: `socq_linkedin_companies`

```json
{
  "urls": [
    "https://www.linkedin.com/company/microsoft/"
  ]
}
```

### `linkedin/company-jobs`

Typed MCP tool: `socq_linkedin_company_jobs`

```json
{
  "urls": [
    "https://www.linkedin.com/jobs/microsoft-jobs/"
  ],
  "results_limit": 20
}
```

### `linkedin/company-posts`

Typed MCP tool: `socq_linkedin_company_posts`

```json
{
  "urls": [
    "https://www.linkedin.com/company/microsoft/"
  ],
  "results_limit": 20
}
```

### `linkedin/jobs`

Typed MCP tool: `socq_linkedin_jobs`

```json
{
  "urls": [
    "https://www.linkedin.com/jobs/view/1234567890/"
  ]
}
```

### `linkedin/post-comments`

Typed MCP tool: `socq_linkedin_post_comments`

```json
{
  "url": "https://www.linkedin.com/posts/aagupta_what-you-need-to-know-ai-agents-activity-7354600338621906944-RvXR"
}
```

### `linkedin/posts`

Typed MCP tool: `socq_linkedin_posts`

```json
{
  "urls": [
    "https://www.linkedin.com/posts/microsoft_ai-activity-1234567890"
  ]
}
```

### `linkedin/profile-posts`

Typed MCP tool: `socq_linkedin_profile_posts`

```json
{
  "urls": [
    "https://www.linkedin.com/in/satyanadella/"
  ],
  "only_authored_posts": true,
  "results_limit": 20
}
```

### `linkedin/profiles`

Typed MCP tool: `socq_linkedin_profiles`

```json
{
  "urls": [
    "https://www.linkedin.com/in/satyanadella/"
  ]
}
```

### `linkedin/search-jobs`

Typed MCP tool: `socq_linkedin_search_jobs`

```json
{
  "location": "Seattle",
  "keyword": "Python",
  "country": "US",
  "results_limit": 20
}
```

### `linkedin/search-people`

Typed MCP tool: `socq_linkedin_search_people`

```json
{
  "urls": [
    "https://www.linkedin.com/search/results/people/?keywords=Aakash%20Gupta"
  ]
}
```

### `linkedin/search-posts`

Typed MCP tool: `socq_linkedin_search_posts`

An explicit no-posts response completes successfully with an empty results.items list. Other access or service errors remain failures. Empty results follow the normal empty-result billing policy.

```json
{
  "query": "AI agents",
  "date_posted": "last-week",
  "results_limit": 20
}
```
