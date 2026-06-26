# Source Reference — Spotify News Digest

This document lists all news sources, their RSS URLs, reliability notes, and category mappings.

## Official Spotify Sources

| Name | URL | Category | Notes |
|------|-----|----------|-------|
| Spotify Engineering Blog | https://engineering.atspotify.com/feed/ | official | Covers backend, ML, infra, data eng |
| Spotify Newsroom | https://newsroom.spotify.com/feed/ | official | Product launches, partnerships, culture |
| Spotify Research | https://research.atspotify.com/feed/ | research | Academic/ML papers by Spotify researchers |
| Spotify Design | https://spotify.design/feed | design | UX/product design articles |

## Media Sources

| Name | URL | Category | Filter |
|------|-----|----------|--------|
| TechCrunch Spotify | https://techcrunch.com/tag/spotify/feed/ | media | Pre-filtered by tag |
| The Verge | https://www.theverge.com/rss/index.xml | media | keyword_filter: "spotify" |
| Music Business Worldwide | https://www.musicbusinessworldwide.com/feed/ | industry | Disabled (slow) — via DDG |
| Billboard | https://www.billboard.com/feed/ | industry | Disabled (slow) — via DDG |

## Community Sources

| Name | URL | Category | Notes |
|------|-----|----------|-------|
| Hacker News | https://hn.algolia.com/api/v1/search?query=spotify&tags=story | community | Returns by recent; keyword_filter in code |

## DDG News Search Queries

Used as fallback when RSS is restricted or for broader coverage:

1. `spotify new feature product`
2. `spotify engineering algorithm`
3. `spotify music streaming news`
4. `spotify podcast update`
5. `spotify business revenue`

**timelimit:** `d` (24h) or `w` (7 days), controlled by `--hours` arg.

## Category → Display Label Mapping

```
official  → 🎵 官方动态
research  → 🔬 技术研究
design    → 🎨 产品设计
media     → 📰 媒体报道
community → 💬 社区讨论
industry  → 🏭 行业资讯
```

## Source Authority Weights (for scoring)

```python
source_weight = {
    'Spotify Engineering Blog': 90,
    'Spotify Research':         85,
    'Spotify Newsroom':         80,
    'Spotify Design':           75,
    'TechCrunch':               60,
    'TechCrunch Spotify':       60,
    'The Verge':                55,
    'The Verge Spotify':        55,
    'Hacker News Spotify':      50,
    'Music Business Worldwide': 40,
    'Billboard':                35,
    # Fallback for unknown sources
    default:                    30,
}
```

Higher weight = higher probability of appearing in final top-N output.
