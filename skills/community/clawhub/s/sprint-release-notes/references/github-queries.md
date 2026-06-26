# GitHub API Queries Reference

This file contains all GraphQL and REST API patterns needed by the sprint release notes skill.
Use these as templates — substitute actual values for placeholders like `{PROJECT_NUMBER}`, `{ORG}`, etc.

---

## Table of Contents

1. [Authentication Setup](#authentication-setup)
2. [Fetch Project ID](#fetch-project-id)
3. [Fetch Iteration Fields](#fetch-iteration-fields)
4. [Fetch Sprint Items](#fetch-sprint-items)
5. [Fetch Issue Details & Linked PRs](#fetch-issue-details--linked-prs)
6. [Fetch PR Details](#fetch-pr-details)
7. [Fetch PR Reviews](#fetch-pr-reviews)
8. [Fetch Repo Contents / Docs](#fetch-repo-contents--docs)
9. [Commit File to Repo](#commit-file-to-repo)
10. [Pagination Pattern](#pagination-pattern)

---

## Authentication Setup

All API calls require the PAT token in the Authorization header.

```bash
# For GraphQL
curl -H "Authorization: bearer {PAT_TOKEN}" \
 -H "Content-Type: application/json" \
 -X POST https://api.github.com/graphql \
 -d '{"query": "..."}'

# For REST
curl -H "Authorization: token {PAT_TOKEN}" \
 -H "Accept: application/vnd.github.v3+json" \
 https://api.github.com/repos/{owner}/{repo}/...
```

When using Python `requests`:
```python
headers = {
    "Authorization": f"bearer {pat_token}",
    "Content-Type": "application/json"
}
# For REST endpoints use "token" instead of "bearer"
rest_headers = {
    "Authorization": f"token {pat_token}",
    "Accept": "application/vnd.github.v3+json"
}
```

---

## Fetch Project ID

### For Organization Projects
```graphql
query {
    organization(login: "{ORG}") {
        projectV2(number: {PROJECT_NUMBER}) {
            id
            title
            shortDescription
            url
        }
    }
}
```

### For User Projects
```graphql
query {
    user(login: "{USERNAME}") {
        projectV2(number: {PROJECT_NUMBER}) {
            id
            title
            shortDescription
            url
        }
    }
}
```

**Parsing the URL:**
- `https://github.com/orgs/{org}/projects/{number}` → use organization query
- `https://github.com/users/{user}/projects/{number}` → use user query

---

## Fetch Iteration Fields

Get all fields on the project, then find the iteration-type field:

```graphql
query {
    node(id: "{PROJECT_ID}") {
        ... on ProjectV2 {
            fields(first: 50) {
                nodes {
                    ... on ProjectV2IterationField {
                        id
                        name
                        configuration {
                            iterations {
                                id
                                title
                                startDate
                                duration
                            }
                            completedIterations {
                                id
                                title
                                startDate
                                duration
                            }
                        }
                    }
                    ... on ProjectV2SingleSelectField {
                        id
                        name
                        options {
                            id
                            name
                        }
                    }
                    ... on ProjectV2Field {
                        id
                        name
                        dataType
                    }
                }
            }
        }
    }
}
```

**How to identify the current sprint:**
1. Look at `configuration.iterations` (active/upcoming) and `configuration.completedIterations`
2. For each iteration, calculate end date: `startDate + duration days`
3. Current sprint = iteration where `startDate <= today <= endDate`
4. If no active sprint, use the most recently completed iteration

---

## Fetch Sprint Items

Fetch all items in the project filtered by iteration. Use pagination (100 items per page):

```graphql
query {
    node(id: "{PROJECT_ID}") {
        ... on ProjectV2 {
            items(first: 100, after: "{CURSOR}") {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                nodes {
                    id
                    content {
                        ... on Issue {
                            id
                            title
                            number
                            state
                            url
                            body
                            labels(first: 20) {
                                nodes {
                                    name
                                }
                            }
                            assignees(first: 10) {
                                nodes {
                                    login
                                    name
                                }
                            }
                            repository {
                                nameWithOwner
                                url
                            }
                            timelineItems(first: 50, itemTypes: [CROSS_REFERENCED_EVENT, CONNECTED_EVENT]) {
                                nodes {
                                    ... on CrossReferencedEvent {
                                        source {
                                            ... on PullRequest {
                                                number
                                                title
                                                url
                                                state
                                                merged
                                                repository {
                                                    nameWithOwner
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        ... on PullRequest {
                            id
                            title
                            number
                            state
                            merged
                            url
                            body
                            labels(first: 20) {
                                nodes {
                                    name
                                }
                            }
                            assignees(first: 10) {
                                nodes {
                                    login
                                    name
                                }
                            }
                            repository {
                                nameWithOwner
                                url
                            }
                        }
                        ... on DraftIssue {
                            title
                            body
                            assignees(first: 10) {
                                nodes {
                                    login
                                }
                            }
                        }
                    }
                    fieldValues(first: 20) {
                        nodes {
                            ... on ProjectV2ItemFieldIterationValue {
                                field {
                                    ... on ProjectV2IterationField {
                                        name
                                    }
                                }
                                title
                                startDate
                                duration
                                iterationId
                            }
                            ... on ProjectV2ItemFieldSingleSelectValue {
                                field {
                                    ... on ProjectV2SingleSelectField {
                                        name
                                    }
                                }
                                name
                            }
                            ... on ProjectV2ItemFieldNumberValue {
                                field {
                                    ... on ProjectV2Field {
                                        name
                                    }
                                }
                                number
                            }
                        }
                    }
                }
            }
        }
    }
}
```

**Filtering logic (do this in code, not in GraphQL):**
1. For each item, check `fieldValues` for the iteration field
2. Match `iterationId` to the target sprint's ID
3. Check the status field (usually a SingleSelectField named "Status") for "Done"/"Closed"

---

## Fetch Issue Details & Linked PRs

If you need more PR details for a specific issue:

```graphql
query {
    repository(owner: "{OWNER}", name: "{REPO}") {
        issue(number: {ISSUE_NUMBER}) {
            title
            body
            timelineItems(first: 100, itemTypes: [CROSS_REFERENCED_EVENT, CONNECTED_EVENT, CLOSED_EVENT]) {
                nodes {
                    ... on CrossReferencedEvent {
                        source {
                            ... on PullRequest {
                                number
                                title
                                url
                                merged
                                mergedAt
                                additions
                                deletions
                                changedFiles
                                author {
                                    login
                                }
                                body
                                commits(first: 50) {
                                    nodes {
                                        commit {
                                            message
                                            author {
                                                name
                                                user {
                                                    login
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## Fetch PR Details

For detailed PR info including file changes:

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
GET /repos/{owner}/{repo}/pulls/{pull_number}/files
```

The files endpoint returns:
```json
[
    {
        "filename": "docs/api-guide.md",
        "status": "modified",
        "additions": 25,
        "deletions": 3,
        "patch": "..."
    }
]
```

Use this to detect documentation changes (files matching `docs/`, `README`, `*.md` in root, `wiki/`).

---

## Fetch PR Reviews

To count review contributions per engineer:

```
GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

Returns:
```json
[
    {
        "user": { "login": "engineer-a" },
        "state": "APPROVED",
        "submitted_at": "2024-01-15T10:30:00Z"
    }
]
```

Count reviews where `state` is "APPROVED", "CHANGES_REQUESTED", or "COMMENTED" (all count as review effort).

---

## Fetch Repo Contents / Docs

### Get file content
```
GET /repos/{owner}/{repo}/contents/{path}
```

Returns base64-encoded content. Decode it:
```python
import base64
content = base64.b64decode(response_json["content"]).decode("utf-8")
```

### Get directory listing
```
GET /repos/{owner}/{repo}/contents/docs
```

Returns array of file objects. Iterate and fetch each relevant `.md` file.

### Get README
```
GET /repos/{owner}/{repo}/readme
```

Shortcut that returns the repo's README regardless of filename.

---

## Commit File to Repo

Create or update a file:

```
PUT /repos/{owner}/{repo}/contents/{path}
```

Request body:
```json
{
    "message": "docs: Sprint {N} release notes - v1.{N}.0",
    "content": "{BASE64_ENCODED_CONTENT}",
    "branch": "main"
}
```

If updating an existing file, you also need the `sha` of the current file:
```json
{
    "message": "docs: Update Sprint {N} release notes",
    "content": "{BASE64_ENCODED_CONTENT}",
    "sha": "{CURRENT_FILE_SHA}",
    "branch": "main"
}
```

To get the SHA, first try to GET the file. If it returns 404, it's a new file (no SHA needed).

---

## Pagination Pattern

For any paginated query, use this pattern:

```python
all_items = []
cursor = None
while True:
    # Build query with after: cursor
    result = execute_graphql(query, variables={"cursor": cursor})
    items = result["data"]["node"]["items"]
    all_items.extend(items["nodes"])
    if not items["pageInfo"]["hasNextPage"]:
        break
    cursor = items["pageInfo"]["endCursor"]
```

Always paginate — sprints can have 50+ items and repos can have many files.
