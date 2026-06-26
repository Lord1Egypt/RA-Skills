---
name: sprint-release-notes
description: >
 Automatically generate sprint release notes from a GitHub Project Board and publish
 to their respective repositories. Groups completed items by repository, generates
 per-repo markdown, and publishes it as each repo's GitHub Release description (create
 or update by tag), not as committed files under docs/. Optionally posts a summary
 comment to a designated issue.
 Use this skill whenever the user mentions sprint release notes, sprint summary, sprint review,
 project board summary, GitHub project board, release notes from sprints, "what shipped this sprint",
 "generate release notes", "sprint report", or wants to compile documentation from completed sprint items.
 Also trigger when the user wants to publish release notes to their respective repos.
 This skill requires a GitHub PAT token and a GitHub Project Board URL.
---

# Sprint Release Notes Generator

Generate executive-ready sprint release notes by reading a GitHub Project Board (v2),
analyzing completed items, reading associated documentation, evaluating contributor performance,
and publishing a polished markdown release note to a designated repo.

## Required Inputs

Collect these from the user before starting:

1. **GitHub Project Board URL** — e.g., `https://github.com/orgs/{org}/projects/{number}` or `https://github.com/users/{user}/projects/{number}`
2. **GitHub PAT Token** — must have scopes: `repo`, `read:org`, `project` (read access to Projects v2)
3. **Sprint identifier** (optional) — if not provided, auto-detect the current/latest completed sprint iteration

If any of these are missing, ask the user before proceeding.

## Workflow Overview

The skill executes in 7 phases. Run them sequentially:

1. **Discover Sprint** — Query the GitHub Project Board for the current sprint iteration
2. **Categorize Items** — Separate completed vs. deferred/carried-over items, and group by repository
3. **Deep-Read Completed Items** — For each completed item, read associated repo docs, PRs, commits
4. **Evaluate Contributors** — Score engineers for Lead Engineer & MVP recognition
5. **Compile Per-Repo Release Notes** — Generate separate markdown for each repository
6. **Publish to Respective Repos** — Create or update a GitHub Release per repo with the markdown as the release body
7. **Post to Project Issue** (Optional) — Comment on a designated issue with summary links

## Phase 1: Discover Sprint

Read the reference file for the full GraphQL queries:
```
view /path/to/skill/references/github-queries.md
```

Use the GitHub GraphQL API (`https://api.github.com/graphql`) with the user's PAT token.

**Step 1.1**: Fetch the project ID from the board URL.
- Extract org/user and project number from the URL
- Query for the project node ID using `organization.projectV2(number: N)` or `user.projectV2(number: N)`

**Step 1.2**: Fetch iteration fields.
- Query the project's fields to find the iteration-type field (usually named "Sprint" or "Iteration")
- Identify the current iteration by checking iteration configurations — pick the iteration whose date range includes today, or the most recently completed one

**Step 1.3**: Fetch all items in the current sprint iteration.
- Query project items filtered by the iteration field value
- For each item, extract: title, status, linked repository, associated PRs/issues, labels, assignees

## Phase 2: Categorize Items & Group by Repo

Separate items into:
- **Completed**: Status is "Done" or "Closed" or equivalent
- **Carried Over**: Items that were in the sprint but are not Done (moved to next sprint)
- **Bugs Fixed**: Items labeled as "bug" that are completed

**Group by Repository:**
- For each completed item, identify its linked repository (from the project item's field or linked PR)
- Create a map: `Map<repo_name, List<completed_items>>`
- Each repo will get its own GitHub Release (same sprint markdown as the release `body`)

Also extract metadata:
- Sprint name/number from the iteration field
- Sprint date range (start and end dates)
- Derive version as `v1.{sprint_number}.0`

## Phase 3: Deep-Read Completed Items

For each completed item, gather context from the associated repository. This is the intelligence-gathering phase. Read the reference file for API patterns:
```
view /path/to/skill/references/github-queries.md
```

For each completed item:

**3a. PR Descriptions & Commits**
- Find linked pull requests via the issue timeline or cross-references
- Read PR descriptions (these often contain the best context on what changed and why)
- Read commit messages on merged PRs
- Note: PR descriptions are gold — they often explain the "why" behind changes

**3b. Documentation Changes**
- Check if the PR modified any files in `/docs`, `README.md`, or wiki-related paths
- If docs were changed, fetch the new content to understand feature documentation
- Use the GitHub Contents API: `GET /repos/{owner}/{repo}/contents/{path}`

**3c. README Files**
- Fetch the repo's root `README.md` for overall project context
- Only do this once per unique repo (cache it)

**3d. Labels & Metadata**
- Collect labels to categorize: feature, bug, infrastructure, security, performance, tech-debt
- Use labels to sort items into the correct release notes sections

**Categorization heuristic for release notes sections:**
- Labels containing "feature", "enhancement", "user-facing" → **New User-Facing Features**
- Labels containing "infra", "tech-debt", "performance", "security", "devops", "scalability" → **Infrastructure & Tech Debt**
- Labels containing "bug", "fix", "hotfix" → **Stability & Bug Fixes**
- If no clear label, infer from the PR title and description

## Phase 4: Evaluate Contributors

Score each contributor who worked on completed items. Read the scoring reference:
```
view /path/to/skill/references/contributor-scoring.md
```

Collect per-contributor metrics:
- **PRs merged count** — from completed items' linked PRs
- **Code complexity** — approximate from lines changed (additions + deletions) across their PRs
- **Review contributions** — count of PR reviews given to others (use the PR reviews API)
- **Bug fixes** — count of completed items labeled "bug" assigned to them
- **Challenge score** — estimate difficulty of cards they completed based on: labels (e.g., "complex", "critical"), story points if available, or item description length as a rough proxy

**Scoring formula:**
```
Score = (PRs_merged × 2) + (lines_changed / 100) + (reviews_given × 3) + (bugs_fixed × 4) + (challenge_score × 5)
```

- **Lead Engineer**: Highest overall score (reflects breadth and depth of contribution)
- **MVP**: Highest score on the single hardest item OR highest bug-fix impact (the "unsung hero" who tackled the toughest problem)

If scores are very close (within 10%), note both contributors.

## Phase 5: Compile Per-Repo Release Notes

For each repository group, generate a separate release notes document using the template below (this becomes the GitHub Release body).

**Repository Mapping:**
- Collect all unique repo names from completed items
- For each repo, filter its completed items
- Generate one markdown document per repo

Use the exact template below. Replace all `[placeholders]` with real data. If a section has no items, write "No changes this sprint." instead of removing the section.

```markdown
# 🚀 Sprint Release Notes: [Sprint Name/Number] - [Repo Name]

**Date:** [YYYY-MM-DD] | **Version:** v1.[sprint_number].0 | **Status:** Shipped | **Repository:** [repo_name]

---

## 🎯 Summary

[2-3 sentences: What was the primary objective for this repository? What shipped?]

---

## ✨ New Features

* **[Issue Title]**: [Short description of what changed].

---

## 🛠️ Infrastructure & Tech Debt

* **[Issue Title]**: [Description of work done].

---

## 🐛 Bug Fixes

* **[Issue Title]**: [Description of fix].

---

## 📊 Items Completed

- [ ] #[issue_number] [issue_title]

---

*Generated from GitHub Project Board - Sprint [sprint_name]*
```

## Phase 6: Publish to Respective Repos (GitHub Releases)

For each repository that had completed items, publish the sprint markdown as that repo’s **Release** (the Releases page / `releases/latest` UI), not as a file in the tree.

**Step 6.1**: Derive the release **tag** and **name** from the sprint (aligned with Phase 2):
- **Tag name** and **release name**: `v1.[sprint_number].0` (same as the Version line in the template)

**Step 6.2**: Resolve whether a release for that tag already exists:
```
GET /repos/{owner}/{repo}/releases/tags/v1.[sprint_number].0
```
- If the response is **404**, create a new release (Step 6.3).
- If the response includes a release **`id`**, update it (Step 6.4).

**Step 6.3**: Create a new release (creates the tag on the default branch if the tag does not exist yet):
```
POST /repos/{owner}/{repo}/releases
```
JSON body (minimal):
- `tag_name`: `v1.[sprint_number].0`
- `target_commitish`: the repo’s **default branch** (e.g. `main`)
- `name`: same as `tag_name` (or a short sprint title if the user prefers)
- `body`: the full markdown from Phase 5
- `draft`: `false`
- `prerelease`: `false`

**Step 6.4**: Update an existing release’s notes and title flags:
```
PATCH /repos/{owner}/{repo}/releases/{release_id}
```

Example (curl; use the user’s PAT and API version header as appropriate):
```bash
curl -L -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  https://api.github.com/repos/OWNER/REPO/releases/RELEASE_ID \
  -d '{
    "name": "v1.2.3",
    "body": "Updated release notes",
    "draft": false,
    "prerelease": false
  }'
```

**Step 6.5**: Track each repo’s **`html_url`** from the create/update response for Phase 7 and the user summary.

**Notes:**
- The PAT needs permission to create releases and push tags (typically **`repo`** on private repos).
- Prefer **`Authorization: Bearer`** with **`Accept: application/vnd.github+json`** for REST calls; include **`X-GitHub-Api-Version`** when using calendar-dated API versions.
- If a repo must not auto-create tags, create the tag (or draft release) out of band and only **PATCH** the `body`.

## Phase 7: Post Summary to Project Issue (Optional)

If the user specifies a **designated issue** to post the summary:

**Step 7.1**: Collect all published release URLs (`html_url` from each create/update response).

**Step 7.2**: Use GitHub Issues API to add a comment:
```
POST /repos/{owner}/{repo}/issues/{issue_number}/comments
```

**Comment template:**
```markdown
## 🚀 Sprint [sprint_number] Release Notes Published

Release notes have been published to each repository’s Releases:

| Repository | Release |
|------------|---------|
| [repo_1] | [release_link_1] |
| [repo_2] | [release_link_2] |
| ... | ... |

---
*Generated automatically from GitHub Project Board*
```

**Step 7.3**: Confirm success and provide the user with all published links.

## Error Handling

- **Rate limiting**: If GitHub API returns 403 with rate limit headers, wait and retry. Inform the user.
- **Missing permissions**: If 404 on project queries, the PAT likely lacks `project` scope. Tell the user which scopes are needed.
- **Empty sprint**: If no items found in the current iteration, inform the user and ask if they want to check a different sprint.
- **No linked PRs**: Some items may not have linked PRs. Use the item title/description as the best available context.
- **No linked repo**: If an item has no repository link, use a default repo or ask the user for clarification.
- **Large sprints**: If >50 items, batch API calls and summarize in groups to stay within context limits.
- **Release publish failures**: If creating or updating a release fails (permissions, tag policy, etc.), continue with other repos and report failures at the end.

## Important Notes

- Always use the GitHub GraphQL API for project board queries (REST API doesn't support Projects v2 well)
- Use the REST API for repo contents (read), PR details, and **Releases** (create/update) for publishing
- Cache repo READMEs — don't fetch the same README twice
- The PAT token is sensitive — never log it, echo it, or include it in output files
- All API calls go through `https://api.github.com` — ensure network access is available
