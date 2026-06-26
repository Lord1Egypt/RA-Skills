# xz01 dual-end list pagination rule

User correction on 2026-05-18:

```text
所有双端、列表页、数据量大于1页的，没有使用翻页，PC端用页码，手机端用上一页下一页表示，和xz01_demo一致，这是规范。
```

Follow-up correction after an under-scoped template repair:

```text
不是这8个,是除排行榜以外的,都要应用这个规则
https://www.900az.com/zoszx/
```

Durable rule:

- Every dual-end xz01 database-backed list page whose underlying data volume exceeds one page must render pagination.
- Ranking/rank-list pages are explicitly excluded from this pagination repair scope unless the user separately requests them.
- Scope is determined from actual database routes/list templates and rendered URLs, not just files named `list_soft.html`, `list_game.html`, `list_news.html`, or `list_collection.html`.
- PC list pages must use numeric page links/page-code style pagination, matching `xz01_demo` semantics.
- Mobile list pages must use simple `上一页` / `下一页` controls, matching `xz01_demo` semantics.
- A non-ranking list page with more than one page of data but no visible/usable pagination is a validation failure.
- This applies to software/app lists, game lists, news/guide lists, category/channel lists, collection/topic lists, image lists, video lists, package/gift lists, kaifu lists, all-news lists, and search-result list templates when present.
- If a project uses an equivalent confirmed pagination helper instead of the literal demo variables, it is acceptable only when the rendered output still follows PC numeric pages and mobile previous/next controls.

Operational implications:

- Before declaring the rule applied, query or otherwise inventory active DB list routes such as `cmf_cms_channel`, exclude rank/ranking routes, and verify every remaining list template/route pair.
- Dev must implement pagination in theme templates using existing backend/template pagination data; do not modify PHP/controllers/routes to fake pagination.
- Test must check representative and high-risk non-ranking multi-page routes on both domains, including `/zoszx/`.
- Static scans should flag list templates that render repeated database list items but have no pagination output/control.
