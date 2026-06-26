# Userorbit API Reference

Base URL: `https://api.userorbit.com/api/v1`

All endpoints use POST. Auth via `Authorization: Bearer $USERORBIT_API_KEY` header. Optionally add `x-team-id` header for multi-team users.

## Table of Contents

- [Feedbacks](#feedbacks)
- [Feedback Boards](#feedback-boards)
- [Feedback Board Tags](#feedback-board-tags)
- [Feedback Comments](#feedback-comments)
- [Announcements](#announcements)
- [Announcement Comments](#announcement-comments)
- [Collections (Announcement Categories)](#collections)
- [Roadmaps](#roadmaps)
- [Stages](#stages)
- [Topics (Roadmap Items)](#topics)
- [Topic Comments](#topic-comments)
- [Topic Collaborators](#topic-collaborators)
- [Articles (Help Center)](#articles)
- [Article Collections](#article-collections)
- [Article Votes](#article-votes)
- [Tags](#tags)
- [Subscribers](#subscribers)
- [Projects](#projects)

---

## Feedbacks

### feedbacks.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | yes | |
| text | string | no | |
| status | string | no | Default: `in_review`. Values: `in_review`, `planned`, `in_progress`, `completed`, `closed` |
| priority | string | no | Default: `medium`. Values: `low`, `medium`, `high` |
| boardId | UUID | no | |
| tagIds | UUID[] | no | |
| assignee | UUID | no | User ID |
| creatorId | UUID | no | Subscriber ID |
| creatorName | string | no | Used if no creatorId |
| creatorEmail | string | no | Used if no creatorId |

Response: `{ data: { id, title, text, status, priority, boardId, ... } }`

### feedbacks.list

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| status | string | no | Filter by status |
| search | string | no | Full-text search |
| boardId | UUID | no | |
| sortBy | string | no | Default: `newest`. Values: `newest`, `top`, `trending` |

Response: `{ pagination: { offset, limit, total }, data: [...], count }`

### feedbacks.info

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### feedbacks.update

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| title | string | no | |
| text | string | no | |
| status | string | no | |
| priority | string | no | |
| boardId | UUID | no | Set null to unassign |
| assignee | UUID | no | Set null to unassign |
| tagIds | UUID[] | no | |
| meta | object | no | |

### feedbacks.delete / feedbacks.archive / feedbacks.restore

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### feedbacks.archived

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| boardId | UUID | no | |
| sort | string | no | Default: `updatedAt` |
| direction | string | no | `ASC` or `DESC` |

### feedbacks.vote

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | Feedback ID |
| subscriberId | UUID | no | Auto-created from auth user email if omitted |

Response: `{ voted: boolean }`

---

## Feedback Boards

### feedback-boards.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | |
| slug | string | no | |
| configuration | object | no | |
| public | boolean | no | Default: false |

### feedback-boards.list

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| type | string | no | `public` or `private` |
| search | string | no | |
| sortBy | string | no | Default: `name` |
| sortOrder | string | no | Default: `asc` |

### feedback-boards.info

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### feedback-boards.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| configuration | object | no |
| public | boolean | no |

### feedback-boards.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Feedback Board Tags

### feedback-board-tags.create

| Field | Type | Required |
|-------|------|----------|
| boardId | UUID | yes |
| tagId | UUID | yes |

### feedback-board-tags.list

| Field | Type | Required |
|-------|------|----------|
| boardId | UUID | yes |

### feedback-board-tags.update

| Field | Type | Required |
|-------|------|----------|
| boardId | UUID | yes |
| oldTagId | UUID | yes |
| newTagId | UUID | yes |

### feedback-board-tags.delete

| Field | Type | Required |
|-------|------|----------|
| boardId | UUID | yes |
| tagId | UUID | yes |

---

## Feedback Comments

### feedback-comments.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | Feedback ID |
| text | string | yes | |
| subscriberId | UUID | no | Auto-created from auth user if omitted |
| parentId | UUID | no | For threaded replies |
| source | string | no | Default: `admin` |
| type | string | no | Default: `public`. Values: `public`, `private` |

### feedback-comments.list

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | no | Feedback ID filter |
| sort | string | no | Default: `updatedAt` |
| direction | string | no | `ASC` or `DESC` |

### feedback-comments.update

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | Comment ID |
| text | string | yes | |
| type | string | no | `public` or `private` |

### feedback-comments.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Announcements

### announcements.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| collectionId | UUID | yes | Category ID |
| title | string | no | |
| text | string | no | Markdown content |
| meta | object | yes | `{ ctaTitle, ctaLink, ctaImage, description, feedback }` |
| publish | boolean | no | Publish immediately |
| parentAnnouncementId | UUID | no | For nested announcements |
| index | integer | no | Sort order (>= 0) |
| collaboratorIds | UUID[] | no | |

### announcements.list

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| collection | UUID | no | Collection ID filter (also accepts `category`) |
| search | string | no | |
| user | UUID | no | Filter by author |
| sort | string | no | Default: `updatedAt` |
| direction | string | no | `ASC` or `DESC` |

### announcements.info

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | conditional | One of `id` or `shareId` required |
| shareId | UUID | conditional | |

### announcements.update

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| title | string | no | |
| text | string | no | |
| meta | object | no | |
| publish | boolean | no | |
| scheduledAt | ISO date | no | Set null to cancel schedule |
| sendEmailBroadcast | boolean | no | |
| collectionId | UUID | no | Move to different category |
| append | boolean | no | Append text instead of replace |
| collaboratorIds | UUID[] | no | |
| lastRevision | integer | no | Optimistic locking |

### announcements.search

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| query | string | yes | |
| collectionId | UUID | no | |
| userId | UUID | no | |
| includeArchived | string | no | `"true"` or `"false"` |
| dateFilter | string | no | `day`, `week`, `month`, `year` |

### announcements.delete / announcements.archive / announcements.pin / announcements.unpin / announcements.star / announcements.unstar

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### announcements.restore

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| revisionId | UUID | no | Restore to specific revision |

### announcements.move

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| collectionId | UUID | yes | Target category |
| parentAnnouncementId | UUID | no | |
| index | integer | no | |

### announcements.revisions

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### announcements.pinned / announcements.starred / announcements.drafts / announcements.archived

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| collection | UUID | no | Required for `pinned` |
| sort | string | no | |
| direction | string | no | |

---

## Announcement Comments

### announcement-comments.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | Announcement ID |
| text | string | yes | |
| subscriberId | UUID | no | |
| parentId | UUID | no | For replies |
| source | string | no | Default: `widget` |

### announcement-comments.list

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| sort | string | no |
| direction | string | no |

### announcement-comments.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| text | string | yes |

### announcement-comments.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Collections

### collections.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | |
| description | string | no | |
| color | string | no | |

### collections.list

No required fields.

### collections.info

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### collections.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| description | string | no |
| color | string | no |

### collections.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Roadmaps

### roadmaps.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | |
| description | string | no | |
| feedback | boolean | no | Enable feedback on roadmap |
| private | boolean | no | |
| stages | array | no | `[{ title, icon }]` to create stages inline |

### roadmaps.list

No required fields.

### roadmaps.info / roadmaps.stages / roadmaps.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### roadmaps.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| description | string | no |
| order | array | no |
| private | boolean | no |

---

## Stages

### stages.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | yes | |
| roadmapId | UUID | yes | |
| description | string | no | |
| meta | object | no | `{ icon }` |
| private | boolean | no | |

### stages.list

| Field | Type | Required |
|-------|------|----------|
| roadmapId | UUID | yes |

### stages.info / stages.delete

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| force | boolean | no | (delete only) Force-delete associated topics |

### stages.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| title | string | no |
| meta | object | no |

---

## Topics

### topics.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | yes | |
| text | string | no | Markdown content |
| description | string | no | |
| roadmapId | UUID | no | |
| stageId | UUID | no | |
| meta | object | no | `{ ctaTitle, ctaLink, ctaImage, description, feedback, projectId }` |
| collaboratorIds | UUID[] | no | |
| publish | boolean | no | |

### topics.list / topics.all

| Field | Type | Required |
|-------|------|----------|
| roadmapId | UUID | yes |
| stageId | UUID | yes |

### topics.info / topics.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### topics.update

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| title | string | no | |
| text | string | no | |
| stageId | UUID | no | Move to different stage |
| meta | object | no | |
| collaboratorIds | UUID[] | no | |
| publish | boolean | no | |
| private | boolean | no | |
| notifySubscribers | boolean | no | Default: true |
| recipientSubscriberIds | UUID[] | no | |

### topics.count

No required fields.

### topic-subscribers.list

| Field | Type | Required |
|-------|------|----------|
| topicId | UUID | yes |

---

## Topic Comments

### topic-comments.create

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| text | string | yes |
| subscriberId | UUID | no |
| parentId | UUID | no |
| source | string | no |

### topic-comments.list

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### topic-comments.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| text | string | yes |

### topic-comments.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Topic Collaborators

### topic-collaborators.create

| Field | Type | Required |
|-------|------|----------|
| topicId | UUID | yes |
| role | string | yes |

### topic-collaborators.list

| Field | Type | Required |
|-------|------|----------|
| topicId | UUID | yes |

### topic-collaborators.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| role | string | no |
| topicId | UUID | no |

### topic-collaborators.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Articles

### articles.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | yes | |
| text | string | yes | Markdown content |
| collectionIds | UUID[] | yes | Non-empty array |
| language | string | no | Default: `en` |
| tags | string[] | no | |
| urlSlug | string | no | Custom URL slug |
| seoTitle | string | no | |
| metaDescription | string | no | |
| authorIds | UUID[] | no | |
| assigneeIds | UUID[] | no | |

### articles.list

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| collectionId | UUID | no | |
| status | string | no | `draft`, `published`, `archived` |
| language | string | no | |
| tags | string[] | no | |
| search | string | no | |
| sort | string | no | Default: `updatedAt` |
| direction | string | no | Default: `DESC` |

### articles.info

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | conditional | ID or urlSlug |
| urlSlug | string | conditional | |

### articles.update

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| title | string | no | |
| text | string | no | |
| collectionIds | UUID[] | no | |
| language | string | no | |
| tags | string[] | no | |
| urlSlug | string | no | |
| authorIds | UUID[] | no | |
| assigneeIds | UUID[] | no | |
| meta | object | no | |
| publish | boolean | no | |
| autosave | boolean | no | Default: false |

### articles.publish / articles.unpublish / articles.archive / articles.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### articles.search

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| query | string | yes | |
| collectionId | UUID | no | |
| status | string | no | Default: `published` |
| language | string | no | |
| tags | string[] | no | |

### articles.revisions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| sort | string | no | Default: `createdAt` |
| direction | string | no | Default: `DESC` |

### articles.restore

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| revisionId | UUID | yes |

---

## Article Collections

### article-collections.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | |
| description | string | no | |
| icon | string | no | |
| meta | object | no | |
| privacy | string | no | Default: `public`. Values: `public`, `private` |
| parentId | UUID | no | For nested collections |
| sortOrder | integer | no | Default: 0 |

### article-collections.list

| Field | Type | Required |
|-------|------|----------|
| parentId | UUID | no |
| includeChildren | boolean | no |

### article-collections.info

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### article-collections.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| description | string | no |
| icon | string | no |
| meta | object | no |
| privacy | string | no |
| sortOrder | integer | no |

### article-collections.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Article Votes

### article-votes.info

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

Response: `{ data: { helpful, not_helpful, hasUserVoted, userVoteValue } }`

### article-votes.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | Article ID |
| value | string | yes | `helpful` or `not_helpful` |
| comment | string | no | |

### article-votes.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

---

## Tags

### tags.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | 1-50 chars |
| color | string | no | Default: `#3B82F6` |
| description | string | no | |

### tags.list

| Field | Type | Required |
|-------|------|----------|
| search | string | no |

### tags.info / tags.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### tags.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | yes |
| color | string | no |
| description | string | no |

---

## Subscribers

### subscribers.create

| Field | Type | Required |
|-------|------|----------|
| email | string | yes |
| name | string | yes |
| password | string | yes |

### subscribers.list

| Field | Type | Required |
|-------|------|----------|
| sort | string | no |
| direction | string | no |

### subscribers.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| email | string | no |

### subscribers.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### subscribers.count

No required fields. Response: `{ count: integer }`

---

## Projects

### projects.create

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | |
| color | string | no | |
| description | string | no | |

### projects.list

No required fields.

### projects.info / projects.delete

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |

### projects.update

| Field | Type | Required |
|-------|------|----------|
| id | UUID | yes |
| name | string | no |
| color | string | no |
| description | string | no |

---

## Response Objects

### Feedback
```json
{
  "id": "UUID",
  "title": "string",
  "text": "string",
  "status": "in_review|planned|in_progress|completed|closed",
  "priority": "low|medium|high",
  "boardId": "UUID|null",
  "assigneeId": "UUID|null",
  "creatorId": "UUID",
  "teamId": "UUID",
  "publishedAt": "ISO date|null",
  "archivedAt": "ISO date|null",
  "createdAt": "ISO date",
  "updatedAt": "ISO date",
  "subscriber": {},
  "board": {},
  "tags": [{ "id": "", "name": "", "color": "" }]
}
```

### Announcement
```json
{
  "id": "UUID",
  "title": "string",
  "text": "string",
  "collectionId": "UUID",
  "teamId": "UUID",
  "publishedAt": "ISO date|null",
  "archivedAt": "ISO date|null",
  "scheduledAt": "ISO date|null",
  "meta": {},
  "revisionCount": 0,
  "collaboratorIds": [],
  "createdAt": "ISO date",
  "updatedAt": "ISO date",
  "createdBy": {},
  "updatedBy": {}
}
```

### Topic (Roadmap Item)
```json
{
  "id": "UUID",
  "title": "string",
  "description": "string",
  "text": "string",
  "roadmapId": "UUID",
  "stageId": "UUID",
  "creatorId": "UUID",
  "publishedAt": "ISO date|null",
  "meta": {},
  "collaboratorIds": [],
  "createdAt": "ISO date",
  "updatedAt": "ISO date",
  "votes_count": 0
}
```

### Article (Help Center)
```json
{
  "id": "UUID",
  "title": "string",
  "text": "string",
  "status": "draft|published|archived",
  "language": "en",
  "tags": [],
  "urlSlug": "string",
  "seoTitle": "string|null",
  "metaDescription": "string|null",
  "publishedAt": "ISO date|null",
  "createdAt": "ISO date",
  "updatedAt": "ISO date",
  "collections": [],
  "authors": [],
  "assignees": []
}
```

### Subscriber
```json
{
  "id": "UUID",
  "email": "string",
  "name": "string",
  "teamId": "UUID",
  "source": "string",
  "createdAt": "ISO date",
  "updatedAt": "ISO date"
}
```
