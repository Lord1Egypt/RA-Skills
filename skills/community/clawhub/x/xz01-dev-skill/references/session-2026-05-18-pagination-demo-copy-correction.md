# Session note: user correction to copy xz01_demo pagination exactly

## Trigger

During a live-site xz01 pagination repair, the assistant first implemented a custom PC pagination fallback shell to make pagination visible. The user corrected this:

```text
你搞错了,不要按你自己的意思去开发 翻页功能 造搬xz01_demo的,就可以了. 处理下,并更新规范
```

## Durable lesson

For xz01 tasks, “照搬/造搬 xz01_demo” is an implementation-shape requirement, not merely a functional or visual target.

If pagination is the topic, do not satisfy the requirement by creating an equivalent new pager. The correct action is to align with the demo chain:

```text
getPcPageData / getMobilePageData
→ $page_code
→ {$page_code|raw}
```

## What to avoid

Do not add or keep theme-side custom pagination algorithms such as:

- `request()->param(...)` for current page / URL construction
- `page_count`, `total_page`, or `total_pages` local variables
- hand-written `pager_i` loops
- custom `ellipsis` handling
- custom `disabled prev` / `disabled next` shells
- forced one-page output such as `上一页 1 下一页` unless it is produced by the demo pagination renderer itself

## Correct repair flow

1. Read the relevant `demo_xz01` list/common-data templates first.
2. Identify where demo calls `getPcPageData` or `getMobilePageData`.
3. Identify where demo outputs `{$page_code|raw}` or temporarily preserves `$page_code` through `$new_page`.
4. Revert any self-designed pagination code in the target theme.
5. Use the demo-compatible `$page_code` output in PC and mobile templates.
6. Clear runtime cache.
7. Test source for no custom-pager residue and sanity-check live 200 routes.
8. If the demo chain cannot produce pagination because a data/helper/backend assumption is missing, report the limitation instead of inventing a new front-end pager.

## Skill-library implication

When a correction says a prior approach was “your own idea” instead of demo-aligned, update the governing class-level xz01 skill immediately. Do not leave the correction only in chat or memory.
