# Source modes and upstream boundaries

| Mode | Direct route | Required semantic proof | Bounded coverage |
|---|---|---|---|
| `youtube-transcript` | `youtube-transcript-api==1.2.4`, `GenericProxyConfig(http_url=..., https_url=...)` | Matching video id, nonempty timed segments, returned language/generated flag | Up to limit segments; missing/disabled/age-restricted captions are `no_data` |
| `youtube-comments` | Existing yt-dlp, private explicit config containing `--proxy`, skip-download and write-comments | Matching requested id and title; each comment id and nonempty text | Ranked top/new sample; extractor limit; empty comments are ambiguous |
| `google-citations` | Playwright browser using supplied HTTP proxy, fresh Google query | Exactly one visible reviewed AI root/answer with marker; citation links inside answer | Visible anchors only; no expanded source panels; region unverified |
| `xiaohongshu` | Existing upstream MCP with server-side `XHS_PROXY` | Positively confirmed login; discovered tools; same id/xsecToken pair; matching noteId/title/desc | One selected note, bounded top-level comments, no replies or OCR |
| `price` | Playwright browser, known Amazon desktop fields or strict Product/Offer JSON-LD | Exact ASIN/SKU, title, price/availability and supplied variant where available | One product page; no checkout, delivery-country, tax or full multistore guarantee |

The library/CLI proxy option changes the caller's network route. It is not a content parser, browser fingerprint, login provider or site authorization. The YouTube caption library's cookie auth is currently disabled; a proxy does not restore missing captions or an age-restricted account. SOCKS proxy support would also require its library-specific dependencies and is not implemented here.

The comments adapter covers YouTube directly. Instagram/TikTok comments are **not** implemented by this raw-proxy collector. ScrapeCreators documents managed `/v2/instagram/post/comments`, `/v1/tiktok/video/comments` and `/v1/youtube/video/comments` endpoints with API-key authentication, cursors and provider limits. Those endpoints do not expose a checked BYO-proxy parameter: using ProxyLane to call their API would not configure their API-to-social egress. Do not describe that as ProxyLane coverage. A managed adapter would need separate user authority, API key, cost/limit contract and upstream-specific raw-response tests. No automatic paid fallback exists in this release.

Price mode `amazon` supports only listed Amazon markets and product `/dp/ASIN` or `/gp/product/ASIN` URLs. The exact selectors are recorded in raw evidence; selectors are volatile and may fail on another marketplace layout. `jsonld` works only on pages exposing one matching Product and one explicit Offer with complete fields. AggregateOffer low/high ranges and ambiguous multi-variant offers fail instead of producing a guessed price. Do not advertise universal Amazon or multistore coverage from a fixture or one site.

Primary sources checked for the adapter design:

- [youtube-transcript-api generic proxies](https://github.com/jdepoix/youtube-transcript-api#using-other-proxy-solutions), [current API implementation](https://github.com/jdepoix/youtube-transcript-api/blob/master/youtube_transcript_api/_api.py), [proxy implementation](https://github.com/jdepoix/youtube-transcript-api/blob/master/youtube_transcript_api/proxies.py)
- [yt-dlp network options](https://github.com/yt-dlp/yt-dlp#network-options), [YouTube extractor comments](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youtube/_video.py), [current YouTube requirements](https://github.com/yt-dlp/yt-dlp/wiki/EJS)
- [XHS server proxy setup](https://github.com/xpzouying/xiaohongshu-mcp/blob/main/README_EN.md), [MCP argument mapping](https://github.com/xpzouying/xiaohongshu-mcp/blob/main/mcp_server.go), [source data types](https://github.com/xpzouying/xiaohongshu-mcp/blob/main/xiaohongshu/types.go)
- [Google Search AI features](https://developers.google.com/search/docs/appearance/ai-features), [Google location/language relevance](https://developers.google.com/search/docs/fundamentals/how-search-works)
- [Playwright HTTP proxy configuration](https://playwright.dev/python/docs/network#http-proxy), [schema.org Product](https://schema.org/Product), [schema.org Offer](https://schema.org/Offer)
- [ScrapeCreators API schema](https://docs.scrapecreators.com/openapi.json), [Instagram comments](https://docs.scrapecreators.com/v2/instagram/post/comments), [TikTok comments](https://docs.scrapecreators.com/v1/tiktok/video/comments)

Official API/CLI references support configuration and argument shapes. The Google DOM and Amazon CSS contracts are collector compatibility choices requiring current rendered-page verification, not official stable APIs. Their execution boundary is listed separately in verification receipts.
