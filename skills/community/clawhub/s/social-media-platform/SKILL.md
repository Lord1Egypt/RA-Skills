---
name: social-media-platform
description: Build a plugin-based social media management platform with multi-platform publishing, content calendar, brand voices, AI content generation via LangGraph, and analytics. Use when building social media tools, content scheduling systems, or multi-platform publishing pipelines. Covers Facebook, Instagram, YouTube, Twitter/X, TikTok integration patterns.
---

# Social Media Platform Builder

Build a complete social media management system with plugin architecture, AI-powered content generation, and multi-platform publishing.

## Architecture

```
┌─────────────────────────────────────┐
│         Frontend (5 pages)          │
│  Dashboard│Compose│Calendar│Analytics│Settings│
├─────────────────────────────────────┤
│         API Layer (FastAPI)         │
│  Posts CRUD│Publishing│Calendar│AI  │
├─────────────────────────────────────┤
│      Plugin Registry (per-platform) │
│  Twitter│Instagram│YouTube│FB│TikTok│Manual│
├─────────────────────────────────────┤
│    LangGraph Content Pipeline       │
│  Voice→Research→Draft→Optimize→Save │
├─────────────────────────────────────┤
│         Supabase (6 tables)         │
└─────────────────────────────────────┘
```

## Step 1: Supabase Tables

Create 6 tables:
- `social_posts` — id, platform, content, status (draft/scheduled/published/failed), media_urls, published_at, post_url, engagement_metrics (JSONB)
- `platform_connections` — id, platform, account_name, credentials (JSONB), status, scopes
- `content_calendar` — id, post_id (FK), scheduled_for, platform, status
- `brand_voices` — id, name, description, tone, example_phrases (JSONB array), is_default
- `social_analytics` — id, post_id (FK), platform, impressions, clicks, likes, shares, comments, fetched_at
- `publish_queue` — id, post_id (FK), platform, status, retry_count, error_message

Seed 3-5 brand voices. Example voices:
- **Primary Voice** (default) — authoritative, clear, educational
- **Casual** — conversational, friendly, uses contractions
- **Coach** — motivational, direct, action-oriented

## Step 2: Plugin System

Base class pattern:

```python
class SocialPlugin:
    platform: str
    def validate_credentials(self, creds: dict) -> bool
    def publish(self, content: str, media_urls: list = None) -> dict
    def get_analytics(self, post_id: str) -> dict
    def format_content(self, content: str, max_length: int) -> str

class PluginRegistry:
    _plugins: dict[str, SocialPlugin] = {}
    def register(self, plugin: SocialPlugin)
    def get(self, platform: str) -> SocialPlugin
    def list_active(self) -> list[str]
```

Platform-specific implementations:
- **Twitter**: tweepy or requests to v2 API. 280 char limit. Free tier = 100 posts/month.
- **Facebook**: Graph API v21.0. Page Access Token required. Post to `/{page_id}/feed`.
- **Instagram**: Graph API via FB Page Token. Post to `/{ig_user_id}/media` → `/{ig_user_id}/media_publish`. Image required.
- **YouTube**: google-auth + google-api-python-client. OAuth with youtube.upload scope. Upload via resumable upload API.
- **TikTok**: Content Posting API (requires app review + demo video). Use Manual mode as fallback.
- **Manual**: No API — generates copy + suggests optimal posting times. Fallback for any unconnected platform.

## Step 3: LangGraph Content Pipeline

6-node graph:

```
load_voice → research_context → generate_drafts → optimize_per_platform → finalize → END
```

- **load_voice**: Pull selected brand voice from Supabase
- **research_context**: Query knowledge vault / RAG for relevant domain content
- **generate_drafts**: LLM generates 2-3 draft variants in the voice
- **optimize_per_platform**: Adapt each draft per platform (length, hashtags, media suggestions)
- **finalize**: Store drafts in `social_posts` as draft status

## Step 4: API Endpoints

Core routes (~19 endpoints):
- `GET/POST /api/social/posts` — CRUD
- `POST /api/social/posts/{id}/publish` — publish to selected platforms
- `GET/POST /api/social/calendar` — calendar view + scheduling
- `GET /api/social/analytics` — aggregated metrics
- `GET/POST /api/social/voices` — brand voice management
- `GET/POST /api/social/connections` — platform credentials
- `POST /api/social/generate` — AI content generation (triggers LangGraph)

## Step 5: Frontend Pages

5 pages with shared dark-theme shell (sidebar nav, top bar):
1. **Dashboard** — post count by platform, recent activity, quick-publish
2. **Compose** — rich editor, platform multi-select, voice picker, live preview cards per platform
3. **Calendar** — month view, color-coded by platform, drag-to-reschedule
4. **Analytics** — Chart.js line/bar charts for engagement over time
5. **Settings** — platform connection forms (OAuth flows), brand voice editor

## Key Patterns

- **Credentials in JSONB**: Each platform stores different auth shapes (API keys vs OAuth tokens vs page tokens) in a single `credentials` JSONB column
- **Graceful degradation**: Always include Manual plugin as fallback — generates copy even without API access
- **Platform content limits**: Enforce per-platform (Twitter 280, IG needs image, YT needs video, FB 63K)
- **Publish queue with retry**: Failed publishes go to retry queue with exponential backoff
