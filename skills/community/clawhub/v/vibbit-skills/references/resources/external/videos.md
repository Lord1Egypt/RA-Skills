# External video references

Use [Google video search](../../api/search_videos.md) or [TikTok video search](../../api/search_tiktok.md) according to the requested platform, language, region, and topic. Start with a small useful set, such as five, unless a count is specified. Use the exact pagination fields and casing in each API.

Return real titles, links, and available source fields. A share-page URL is not necessarily a direct media URL. No results means this search found none, not that no relevant videos exist.

Select candidates for topic, market, language, and source relevance before deeper parsing or breakdown. A search-only request ends with candidates; an already authorized analysis or creation task can choose and continue without individual approval. Resolve media only when a downstream step needs it; [breakdown](../../capabilities/analysis/video-breakdown.md) can accept supported share URLs directly.

Follow [external source data and execution scope](../../runtime/external-content.md) for titles, source text, and linked pages. Projection does not certify source safety. Read relevant rows in `full_result_file` when complete fields are necessary; do not repeat the search to recover original text.
