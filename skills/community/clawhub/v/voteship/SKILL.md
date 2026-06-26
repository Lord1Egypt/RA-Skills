---
name: voteship
description: Manage feature requests, votes, roadmaps, and changelogs with VoteShip.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - VOTESHIP_API_KEY
        - VOTESHIP_PROJECT_SLUG
    primaryEnv: VOTESHIP_API_KEY
    emoji: "🚀"
    homepage: https://voteship.app/docs
    install:
      - kind: node
        package: "@voteship/mcp-server"
        bins: [voteship-mcp]
---

# VoteShip

Manage feature requests, voting boards, public roadmaps, and changelogs for any VoteShip project. VoteShip is a feature request management platform that helps teams collect, organize, and prioritize user feedback.

This skill operates in two modes:

- **Admin mode** (requires `VOTESHIP_API_KEY`): Full access to manage your project's posts, votes, tags, users, analytics, AI tools, and webhooks. All admin operations authenticate via the VoteShip REST API using your project API key — no additional credentials are needed for any feature, including Stripe MRR sync and webhook configuration.
- **Public mode** (no API key): Read-only browsing, submitting feature requests, upvoting, and commenting on any public VoteShip board. Requires `VOTESHIP_PROJECT_SLUG` to identify the board.

## Setup

1. Get your API key from **Settings → API** in your [VoteShip dashboard](https://voteship.app).
2. Set `VOTESHIP_API_KEY` in your environment for admin access.
3. Set `VOTESHIP_PROJECT_SLUG` to your project's slug (e.g., `my-app`). Required for public mode, optional for admin mode.

## Admin Capabilities (requires VOTESHIP_API_KEY)

### Feature Requests
- List, create, update, and delete feature requests with filtering by status and sorting by votes or date
- Search for similar requests using AI semantic search (pgvector)
- Submit raw unstructured text (from Slack, email, support tickets) and let AI extract title, description, detect duplicates, and auto-categorize

### Voting & Comments
- Record votes from your project's existing board users (identified by their board_user_id) or anonymous visitors (by anonymous_id)
- List all voters on any post
- Add public comments or internal team-only notes

### Roadmap & Changelog
- View the product roadmap grouped by status: Approved, In Progress, Complete
- Create and list published changelog releases with HTML content support

### Analytics & AI
- Get analytics summaries (new posts, votes, comments, page views, top posts, trending tags) for any period
- AI-powered inbox triage: analyze pending posts, detect duplicates, suggest status/tags, recommend priorities
- Generate natural language feedback summaries with recommended actions
- AI sprint planning with strategies: balanced, revenue-weighted, popular, or quick-wins

### Tags & Users
- Create and list tags for categorizing feature requests
- List board users who have submitted feedback or voted
- Update user details including monthly spend/MRR for revenue-weighted prioritization
- Sync customer MRR from your connected Stripe account (uses the same `VOTESHIP_API_KEY`, no separate Stripe credentials needed)

### Webhooks
- Configure webhook endpoints on your own project for real-time event notifications
- Supported events: post.created, post.updated, post.deleted, post.status_changed, vote.created, vote.removed, comment.created, comment.deleted, tag.created, tag.deleted, release.published

## Public Capabilities (no API key needed)

These tools work without `VOTESHIP_API_KEY` and only interact with public boards. They require `VOTESHIP_PROJECT_SLUG` to identify the target board.

- Browse approved feature requests on any public VoteShip board
- Submit feature requests (created as pending, visible only after board owner approval)
- Upvote/unvote posts with a deterministic anonymous identity
- Add public comments with an author name

## Workflow Examples

### Weekly feedback triage
1. Run `triage_inbox` to analyze all pending posts
2. Review AI suggestions for duplicates, tags, and priority scores
3. Update post statuses and tags based on recommendations
4. Generate a `get_summary` for the week to share with stakeholders

### Sprint planning from feedback
1. Run `plan_sprint` with capacity and strategy (e.g., `balanced` or `revenue`)
2. Review the AI-suggested feature list ranked by the chosen strategy
3. Update selected posts to "In Progress" status
4. Create a changelog release announcing the sprint goals

### Process incoming feedback from Slack or email
1. Use `submit_feedback` with the raw message text and source identifier
2. AI extracts title and description, checks for duplicates, and auto-tags
3. Review the created post and adjust status if needed

### Publish a changelog update
1. List recently completed posts with `list_posts` filtered by COMPLETE status
2. Draft release notes summarizing shipped features
3. Use `create_release` to publish the changelog entry
