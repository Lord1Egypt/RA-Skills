---
name: userorbit
description: Manage Userorbit resources via the public API. Create and manage feedback, announcements, roadmap topics, help center articles, boards, tags, subscribers, and more.
metadata:
  clawdbot:
    requires:
      env:
        - USERORBIT_API_KEY
        - USERORBIT_TEAM_ID
---

# Userorbit API

Manage Userorbit resources programmatically via the REST API.

## Setup

Before the first API call, verify that `USERORBIT_API_KEY` and `USERORBIT_TEAM_ID` environment variables are set. If they are missing, ask the user to provide them (available in Settings → API or from the Userorbit onboarding page).

## Making API calls

Use `curl` directly with the environment variables:

- Base URL: `https://api.userorbit.com/api/v1`
- All endpoints use **POST**
- Endpoint format: `<resource>.<action>` (e.g., `announcements.list`, `feedbacks.create`)
- Success response: `{ "data": ... }`
- List response: `{ "pagination": { "offset", "limit", "total" }, "data": [...] }`
- Error response: `{ "error": "..." }`

Usage:
```bash
curl -s -X POST "https://api.userorbit.com/api/v1/<endpoint>" \
  -H "Authorization: Bearer ${USERORBIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-team-id: ${USERORBIT_TEAM_ID}" \
  -d '<json body>'
```

Example:
```bash
curl -s -X POST "https://api.userorbit.com/api/v1/announcements.list" \
  -H "Authorization: Bearer ${USERORBIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-team-id: ${USERORBIT_TEAM_ID}" \
  -d '{"limit": 5}' | jq '.data'
```

## Resources

### Feedback

User-submitted feedback with voting, status tracking, and board organization.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `feedbacks.create` | `title` |
| List | `feedbacks.list` | - |
| Get | `feedbacks.info` | `id` |
| Update | `feedbacks.update` | `id` |
| Delete | `feedbacks.delete` | `id` |
| Archive | `feedbacks.archive` | `id` |
| Restore | `feedbacks.restore` | `id` |
| Vote | `feedbacks.vote` | `id` |

Statuses: `in_review`, `planned`, `in_progress`, `completed`, `closed`

Sort modes for list: `newest`, `top` (by votes), `trending` (activity)

### Feedback Boards

Organize feedback into boards.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `feedback-boards.create` | `name` |
| List | `feedback-boards.list` | - |
| Get | `feedback-boards.info` | `id` |
| Update | `feedback-boards.update` | `id` |
| Delete | `feedback-boards.delete` | `id` |

### Feedback Comments

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `feedback-comments.create` | `id` (feedbackId), `text` |
| List | `feedback-comments.list` | - |
| Update | `feedback-comments.update` | `id`, `text` |
| Delete | `feedback-comments.delete` | `id` |

Comments support `type`: `"public"` or `"private"` (internal notes).

### Announcements

Product updates and changelogs. Require a `collectionId` (category).

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `announcements.create` | `collectionId`, `title`, `text`, `meta` |
| List | `announcements.list` | - |
| Get | `announcements.info` | `id` |
| Update | `announcements.update` | `id` |
| Delete | `announcements.delete` | `id` |
| Search | `announcements.search` | `query` |
| Archive | `announcements.archive` | `id` |
| Restore | `announcements.restore` | `id` |
| Pin | `announcements.pin` | `id` |
| Unpin | `announcements.unpin` | `id` |

The `meta` object supports: `ctaTitle`, `ctaLink`, `ctaImage`, `description`, `feedback`.

Set `publish: true` to publish immediately. Use `scheduledAt` (ISO date) to schedule.

### Announcement Comments

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `announcement-comments.create` | `id` (announcementId), `text` |
| List | `announcement-comments.list` | `id` (announcementId) |
| Update | `announcement-comments.update` | `id`, `text` |
| Delete | `announcement-comments.delete` | `id` |

### Roadmaps

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `roadmaps.create` | `name` |
| List | `roadmaps.list` | - |
| Get | `roadmaps.info` | `id` |
| Update | `roadmaps.update` | `id` |
| Delete | `roadmaps.delete` | `id` |
| Stages | `roadmaps.stages` | `id` |

### Stages

Columns within a roadmap (e.g., "Planned", "In Progress", "Done").

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `stages.create` | `title`, `roadmapId` |
| List | `stages.list` | `roadmapId` |
| Get | `stages.info` | `id` |
| Update | `stages.update` | `id` |
| Delete | `stages.delete` | `id` |

### Topics (Roadmap Items)

Items that live on a roadmap stage.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `topics.create` | `title` |
| List | `topics.list` | `roadmapId`, `stageId` |
| Get | `topics.info` | `id` |
| Update | `topics.update` | `id` |
| Delete | `topics.delete` | `id` |
| Count | `topics.count` | - |

### Topic Comments

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `topic-comments.create` | `id` (topicId), `text` |
| List | `topic-comments.list` | `id` (topicId) |
| Update | `topic-comments.update` | `id`, `text` |
| Delete | `topic-comments.delete` | `id` |

### Articles (Help Center)

Knowledge base articles with publishing workflow.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `articles.create` | `title`, `text`, `collectionIds` |
| List | `articles.list` | - |
| Get | `articles.info` | `id` |
| Update | `articles.update` | `id` |
| Delete | `articles.delete` | `id` |
| Search | `articles.search` | `query` |
| Publish | `articles.publish` | `id` |
| Unpublish | `articles.unpublish` | `id` |
| Archive | `articles.archive` | `id` |
| Revisions | `articles.revisions` | `id` |
| Restore | `articles.restore` | `id`, `revisionId` |

Article statuses: `draft`, `published`, `archived`

### Article Collections (Help Center Categories)

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `article-collections.create` | `name` |
| List | `article-collections.list` | - |
| Get | `article-collections.info` | `id` |
| Update | `article-collections.update` | `id` |
| Delete | `article-collections.delete` | `id` |

### Article Votes

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Get | `article-votes.info` | `id` (articleId) |
| Vote | `article-votes.create` | `id` (articleId), `value` (`helpful` or `not_helpful`) |
| Remove | `article-votes.delete` | `id` (articleId) |

### Collections (Announcement Categories)

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `collections.create` | `name` |
| List | `collections.list` | - |
| Get | `collections.info` | `id` |
| Update | `collections.update` | `id` |
| Delete | `collections.delete` | `id` |

### Tags

Labels for organizing feedback.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `tags.create` | `name` |
| List | `tags.list` | - |
| Get | `tags.info` | `id` |
| Update | `tags.update` | `id`, `name` |
| Delete | `tags.delete` | `id` |

### Subscribers

Public users who interact with your product.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `subscribers.create` | `email`, `name`, `password` |
| List | `subscribers.list` | - |
| Update | `subscribers.update` | `id` |
| Delete | `subscribers.delete` | `id` |
| Count | `subscribers.count` | - |
| Search | `subscribers.search` | - |

### Projects

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `projects.create` | `name` |
| List | `projects.list` | - |
| Get | `projects.info` | `id` |
| Update | `projects.update` | `id` |
| Delete | `projects.delete` | `id` |

### Feedback Board Tags

Associate tags with feedback boards.

| Operation | Endpoint | Required fields |
|-----------|----------|-----------------|
| Create | `feedback-board-tags.create` | `boardId`, `tagId` |
| List | `feedback-board-tags.list` | `boardId` |
| Update | `feedback-board-tags.update` | `boardId`, `oldTagId`, `newTagId` |
| Delete | `feedback-board-tags.delete` | `boardId`, `tagId` |

## Common Workflows

### Create and publish an announcement
1. Call `collections.list` to find the right `collectionId`
2. Call `announcements.create` with `collectionId`, `title`, `text`, `meta`, and `publish: true`

### Add a topic to a roadmap
1. Call `roadmaps.list` to find the `roadmapId`
2. Call `roadmaps.stages` with the `id` to find the `stageId`
3. Call `topics.create` with `title`, `roadmapId`, `stageId`, and `publish: true`

### Publish a help center article
1. Call `article-collections.list` to find collection IDs
2. Call `articles.create` with `title`, `text`, and `collectionIds`
3. Call `articles.publish` with the article `id`

## Detailed API Reference

For full request/response schemas with all optional fields, see `references/api.md`.
