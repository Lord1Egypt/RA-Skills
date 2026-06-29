---
name: stack-exchange
description: Stack Exchange API integration with managed OAuth for Q&A knowledge automation. Search questions, retrieve answers, browse tags, manage user profiles, track reputation, list collectives, and analyze community activity across all Stack Exchange sites. Use this skill when users want to search Stack Overflow for solutions, find answers to technical questions, browse tags and badges, track user reputation, or analyze community activity patterns.
---

# Stack Exchange

![Stack Exchange](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/stack-exchange.svg)

Stack Exchange is a network of Q&A communities including Stack Overflow, Server Fault, Super User, and more. This integration uses managed OAuth through ClawLink to search questions, retrieve answers, track reputation, browse tags, and analyze community activity across the entire Stack Exchange network.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Stack Exchange |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Stack Exchange |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Stack Exchange API│
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

Search for questions on Stack Overflow:

```
clawlink_execute_tool --integration stack-exchange --tool stack_exchange_get_search_results --args '{"site": "stackoverflow", "tagged": "python", "intitle": "async await"}'
```

Get answers for a specific question:

```
clawlink_execute_tool --integration stack-exchange --tool stack_exchange_get_question_answers --args '{"ids": "12345678", "site": "stackoverflow"}'
```

Search with advanced filters:

```
clawlink_execute_tool --integration stack-exchange --tool stack_exchange_search_advanced --args '{"site": "stackoverflow", "q": "docker compose networking", "accepted": true, "sort": "votes"}'
```

## Authentication

Stack Exchange uses OAuth 2.0 managed by ClawLink. No API keys are needed. Some endpoints (user-specific data, inbox, achievements) require authentication. Authorize access through the ClawLink dashboard.

Connect at: **https://claw-link.dev/dashboard?add=stack-exchange**

## Connection Management

**List connections:**
```
clawlink_list_integrations
```

**Verify connection:**
```
clawlink_execute_tool --integration stack-exchange --tool stack_exchange_get_me --args '{"site": "stackoverflow"}'
```

**Reconnect:** If a connection expires, visit the dashboard URL above and reconnect Stack Exchange.

## Security & Permissions

- **Read** operations are safe and require no confirmation. All Stack Exchange tools in this integration are read-only or create filters.
- **Write** operations are limited to creating custom filters, which are safe helper objects.
- The Stack Exchange API has a daily request quota. Monitor `quota_remaining` in responses.

## Tool Reference

### Search Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_search_results` | Search questions by tags, title, or keywords | Read |
| `stack_exchange_search_advanced` | Advanced search with filters (accepted, closed, body, title, user, views) | Read |
| `stack_exchange_search_excerpts` | Search with highlighted excerpt snippets | Read |
| `stack_exchange_find_similar_questions` | Find questions similar to a hypothetical title and tags | Read |

### Question Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_questions` | List questions (newest, most voted, date-filtered) | Read |
| `stack_exchange_get_questions_by_ids` | Retrieve specific questions by ID (up to 100) | Read |
| `stack_exchange_get_question_answers` | Retrieve all answers for specific question IDs | Read |
| `stack_exchange_get_question_comments` | Retrieve comments on specific questions | Read |
| `stack_exchange_get_question_timeline` | Retrieve timeline events for questions | Read |
| `stack_exchange_get_question_flag_options` | Fetch valid flag options for a question | Read |
| `stack_exchange_get_question_close_options` | Fetch close reason options for a question | Read |
| `stack_exchange_get_linked_questions` | Find questions linked to specific question IDs | Read |
| `stack_exchange_get_questions_by_answer_ids` | Find parent questions for specific answer IDs | Read |
| `stack_exchange_list_featured_questions` | List all questions with active bounties | Read |
| `stack_exchange_list_no_answer_questions` | List questions with zero answers | Read |
| `stack_exchange_list_unanswered_questions` | List questions lacking upvoted answers | Read |

### Answer Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_answers` | List all undeleted answers from a site | Read |
| `stack_exchange_get_answers_by_ids` | Retrieve specific answers by ID (up to 100) | Read |
| `stack_exchange_get_answer_comments` | Retrieve comments on specific answers | Read |
| `stack_exchange_get_answer_flag_options` | Fetch valid flag options for an answer | Read |
| `stack_exchange_render_answer` | Render a preview of an answer (markdown to HTML) | Read |

### Post Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_posts` | List all posts (questions and answers) from a site | Read |
| `stack_exchange_get_posts_by_ids` | Retrieve posts by ID (handles both questions and answers) | Read |
| `stack_exchange_get_post_comments` | Retrieve comments on posts regardless of type | Read |
| `stack_exchange_get_post_suggested_edits` | Retrieve suggested edits on specific posts | Read |
| `stack_exchange_get_revisions_by_ids` | Retrieve edit history for posts | Read |

### Comment Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_comments` | Retrieve recent comments from a site | Read |
| `stack_exchange_get_comments_by_ids` | Retrieve specific comments by ID (up to 100) | Read |
| `stack_exchange_get_comment_flag_options` | Fetch valid flag options for a comment | Read |

### Tag Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_tags` | List all tags on a site (by popularity, activity, name) | Read |
| `stack_exchange_get_tag_info` | Retrieve detailed info about specific tags | Read |
| `stack_exchange_get_tag_faq` | Retrieve frequently asked questions for tags | Read |
| `stack_exchange_get_tag_synonyms` | Retrieve synonyms for specific tags | Read |
| `stack_exchange_get_tag_wikis` | Retrieve wiki content for tags | Read |
| `stack_exchange_get_tag_top_answerers` | Top 30 answerers for a tag (all-time or 30 days) | Read |
| `stack_exchange_get_tag_top_askers` | Top askers for a tag (all-time or 30 days) | Read |
| `stack_exchange_get_related_tags` | Find tags most related to specified tags | Read |
| `stack_exchange_list_tag_synonyms` | List all tag synonyms on a site | Read |
| `stack_exchange_list_tag_badges` | List badges awarded for tag participation | Read |
| `stack_exchange_list_moderator_only_tags` | List tags only moderators can use | Read |
| `stack_exchange_list_required_tags` | List required tags for questions | Read |

### Badge Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_badges` | List all available badges | Read |
| `stack_exchange_list_named_badges` | List explicitly named (general) badges | Read |
| `stack_exchange_list_badge_recipients` | List recently awarded badges | Read |
| `stack_exchange_get_badges_by_ids` | Retrieve specific badges by ID | Read |
| `stack_exchange_get_badge_recipients_by_ids` | List recent recipients of specific badges | Read |

### User Operations (General)

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_users` | List all users on a site | Read |
| `stack_exchange_get_users_by_ids` | Retrieve user profiles by ID | Read |
| `stack_exchange_get_user_answers` | List answers posted by specific users | Read |
| `stack_exchange_get_user_questions` | List questions asked by specific users | Read |
| `stack_exchange_get_user_posts` | List all posts by specific users | Read |
| `stack_exchange_get_user_comments` | List comments by specific users | Read |
| `stack_exchange_get_user_comments_to_user` | List comments between two specific users | Read |
| `stack_exchange_get_user_favorites` | List questions favorited by users | Read |
| `stack_exchange_get_user_badges` | List badges earned by users | Read |
| `stack_exchange_get_user_tags` | List tags users are active in | Read |
| `stack_exchange_get_user_timeline` | Retrieve timeline of user actions | Read |
| `stack_exchange_get_user_privileges` | List privileges a user has earned | Read |
| `stack_exchange_get_user_mentions` | List comments mentioning specific users | Read |
| `stack_exchange_get_user_merge_history` | Track account merge history for users | Read |
| `stack_exchange_get_user_associated_accounts` | List all SE accounts for users | Read |
| `stack_exchange_get_user_suggested_edits` | List suggested edits by users | Read |

### User Reputation Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_user_reputation` | Retrieve reputation changes for users | Read |
| `stack_exchange_get_user_reputation_history` | Retrieve public reputation history for users | Read |
| `stack_exchange_get_user_full_reputation_history` | Retrieve full (including private) reputation history | Read |

### User Top Tags & Answers

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_user_top_tags` | Top 30 tags by combined score for a user | Read |
| `stack_exchange_get_user_top_answer_tags` | Top 30 tags by answer score for a user | Read |
| `stack_exchange_get_user_top_question_tags` | Top 30 tags by question score for a user | Read |
| `stack_exchange_get_user_top_answers_in_tags` | Top 30 answers by a user in specific tags | Read |
| `stack_exchange_get_user_top_questions_in_tags` | Top 30 questions by a user in specific tags | Read |
| `stack_exchange_get_user_unanswered_questions` | Unanswered questions by specific users | Read |
| `stack_exchange_get_user_unaccepted_questions` | Questions with no accepted answer by users | Read |
| `stack_exchange_get_user_no_answer_questions` | Questions with zero answers by users | Read |
| `stack_exchange_get_user_featured_questions` | Questions with bounties by specific users | Read |

### User Notifications & Inbox

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_user_notifications` | Retrieve notifications for a user | Read |
| `stack_exchange_get_user_unread_notifications` | Retrieve unread notifications for a user | Read |
| `stack_exchange_get_user_inbox` | Retrieve a user's inbox | Read |
| `stack_exchange_get_user_unread_inbox` | Retrieve unread inbox items for a user | Read |

### Authenticated User (Me) Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_me` | Retrieve the authenticated user's profile | Read |
| `stack_exchange_get_my_achievements` | Retrieve recent network-wide achievements | Read |
| `stack_exchange_get_my_associated_accounts` | List all SE accounts for the authenticated user | Read |
| `stack_exchange_get_my_posts` | List posts owned by the authenticated user | Read |
| `stack_exchange_get_my_questions` | List questions owned by the authenticated user | Read |
| `stack_exchange_get_my_featured_questions` | List user's questions with active bounties | Read |
| `stack_exchange_get_my_mentions` | List comments mentioning the authenticated user | Read |
| `stack_exchange_get_my_merge_history` | Retrieve account merge history | Read |
| `stack_exchange_get_my_network_activity` | Retrieve network-wide activity summary | Read |
| `stack_exchange_get_my_no_answer_questions` | List user's questions with zero answers | Read |
| `stack_exchange_get_my_posts` | List all posts (Q&A) by the authenticated user | Read |
| `stack_exchange_get_my_privileges` | List privileges for the authenticated user | Read |
| `stack_exchange_get_my_reputation` | Retrieve reputation changes | Read |
| `stack_exchange_get_my_reputation_history` | Retrieve chronological reputation history | Read |
| `stack_exchange_get_my_suggested_edits` | List suggested edits by the user | Read |
| `stack_exchange_get_my_tag_preferences` | Retrieve favorite and ignored tags | Read |
| `stack_exchange_get_my_tags` | List tags the user is active in | Read |
| `stack_exchange_get_my_timeline` | Retrieve timeline of user actions | Read |
| `stack_exchange_get_my_top_answer_tags` | Top 30 tags by answer score | Read |
| `stack_exchange_get_my_top_answers_in_tags` | Top 30 answers in specific tags | Read |
| `stack_exchange_get_my_top_question_tags` | Top 30 tags by question score | Read |
| `stack_exchange_get_my_top_questions_in_tags` | Top 30 questions in specific tags | Read |
| `stack_exchange_get_my_top_tags` | Top 30 tags by combined score | Read |
| `stack_exchange_get_my_unaccepted_questions` | User's questions with no accepted answer | Read |
| `stack_exchange_get_my_unanswered_questions` | User's questions considered unanswered | Read |
| `stack_exchange_list_unanswered_questions_my_tags` | Unanswered questions in the user's tags | Read |

### Collective Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_collectives` | List all collectives on a site | Read |
| `stack_exchange_get_collectives_by_slugs` | Retrieve collectives by slug identifiers | Read |
| `stack_exchange_get_collective_questions` | Retrieve questions for a collective | Read |
| `stack_exchange_get_collective_answers` | Retrieve answers for a collective | Read |
| `stack_exchange_get_collective_users` | List members of a collective | Read |
| `stack_exchange_get_collective_tags` | Retrieve tags associated with collectives | Read |

### Suggested Edits

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_list_suggested_edits` | List all suggested edits on a site | Read |
| `stack_exchange_get_suggested_edits_by_ids` | Retrieve specific suggested edits by ID | Read |

### Site & Network Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_get_sites` | List all Stack Exchange network sites with API identifiers | Read |
| `stack_exchange_get_site_info` | Retrieve statistics and info about a site | Read |
| `stack_exchange_get_events` | Retrieve recent events stream (15-minute window) | Read |
| `stack_exchange_list_errors` | List all API error codes | Read |
| `stack_exchange_list_privileges` | List all earnable privileges on a site | Read |
| `stack_exchange_list_moderators` | List users with moderation powers | Read |
| `stack_exchange_list_elected_moderators` | List elected moderators only | Read |

### Filter & Authentication Operations

| Tool | Description | Mode |
|------|-------------|------|
| `stack_exchange_create_filter` | Create a custom response filter | Write |
| `stack_exchange_get_filters_by_ids` | Retrieve filter field definitions | Read |
| `stack_exchange_get_access_tokens` | Verify and inspect OAuth access tokens | Read |

## Code Examples

Search Stack Overflow for Python async questions:

```json
{
  "tool": "stack_exchange_get_search_results",
  "args": {
    "site": "stackoverflow",
    "intitle": "async await",
    "tagged": "python",
    "sort": "votes"
  }
}
```

Get answers for a specific question:

```json
{
  "tool": "stack_exchange_get_question_answers",
  "args": {
    "ids": "12345678",
    "site": "stackoverflow",
    "sort": "votes",
    "order": "desc"
  }
}
```

Advanced search with multiple filters:

```json
{
  "tool": "stack_exchange_search_advanced",
  "args": {
    "site": "stackoverflow",
    "q": "kubernetes pod crashloopbackoff",
    "accepted": true,
    "sort": "relevance"
  }
}
```

Get user's top tags:

```json
{
  "tool": "stack_exchange_get_my_top_tags",
  "args": {
    "site": "stackoverflow"
  }
}
```

List all Stack Exchange sites:

```json
{
  "tool": "stack_exchange_get_sites",
  "args": {}
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm stack-exchange is connected.
2. Call `clawlink_list_tools --integration stack-exchange` to see the live catalog.
3. Use `stack_exchange_get_sites` to discover available Stack Exchange sites and their API identifiers.
4. Use `stack_exchange_get_search_results` or `stack_exchange_search_advanced` to find relevant content.
5. Use `stack_exchange_get_question_answers` to retrieve solutions.

## Execution Workflow

```
Read Flow:
  get_sites → get_search_results → get_questions_by_ids → get_question_answers

User Flow:
  get_me → get_my_questions / get_my_reputation / get_my_tags

Tag Flow:
  list_tags → get_tag_info → get_tag_faq / get_tag_top_answerers
```

## Notes

- The `site` parameter is required for most operations. Use values like `stackoverflow`, `serverfault`, `superuser`, `askubuntu`, etc. Obtain the full list from `stack_exchange_get_sites`.
- IDs can be semicolon-delimited for batch operations (up to 100 IDs at once).
- The API has a daily request quota. Monitor `quota_remaining` in responses to avoid hitting the limit.
- Events from `get_events` are only accessible for 15 minutes after they occurred.
- Site info from `get_site_info` is heavily cached; query sparingly (no more than once per hour).
- User-specific endpoints (inbox, notifications, achievements) require the `read_inbox` OAuth scope.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 400 Bad Request | Invalid parameter or missing required field |
| 401 Unauthorized | OAuth token expired or missing for authenticated endpoints |
| 403 Forbidden | Access denied; check OAuth scopes |
| 404 Not Found | Invalid question, answer, or user ID |
| 429 Too Many Requests | Daily API quota exhausted; wait until quota resets |
| 500 Internal Server Error | Stack Exchange API issue; retry later |

## Troubleshooting

### Tools Not Visible
Run `clawlink_list_tools --integration stack-exchange` to verify the integration is active. If empty, reconnect at https://claw-link.dev/dashboard?add=stack-exchange.

### Search Returns No Results
Ensure the `site` parameter is correct (e.g., `stackoverflow` not `stack-overflow`). Verify that `tagged` or `intitle` is provided for `get_search_results` (at least one is required).

### Quota Exceeded
The Stack Exchange API enforces a daily quota. Monitor `quota_remaining` in each response. Consider creating a custom filter with `create_filter` to reduce response sizes.

### User-Specific Data Not Available
Authenticated endpoints require a valid OAuth connection. Ensure you have connected your Stack Exchange account and granted the `read_inbox` scope.

## Resources

- Stack Exchange API Docs: https://api.stackexchange.com/docs
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stack-exchange
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stack-exchange)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
