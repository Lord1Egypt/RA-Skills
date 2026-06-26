# Session note: pagination must follow xz01_demo, not a custom fallback

## Trigger

User corrected a bad pagination repair after list-page pagination was reported missing on `https://www.900az.com/`:

```text
你搞错了,不要按你自己的意思去开发 翻页功能 造搬xz01_demo的,就可以了. 处理下,并更新规范
```

## What went wrong

A previous repair treated missing rendered PC pagination as permission to build a custom theme-level pager. That introduced self-designed logic such as request-parameter/page-count handling, disabled prev/next states, ellipses, and a stable one-page shell.

This was wrong for xz01 work. The user does not want a newly designed pagination feature. The required behavior is to copy/align with `xz01_demo`.

## Correct xz01_demo pattern

The demo pagination chain is:

1. Data common/list logic calls `getPcPageData(...)` for PC or `getMobilePageData(...)` for mobile.
2. Those helpers set global/template `$page_code` through ThinkPHP pagination render logic.
3. PC and mobile templates output the pagination with:

```html
{$page_code|raw}
```

Some demo files temporarily assign `$new_page = $page_code` and restore it later, but they still preserve the same `page_code` chain.

## Durable rule

For xz01 list pages, implement pagination by copying/aliging with `xz01_demo`'s `getPcPageData` / `getMobilePageData` → `$page_code` → `{$page_code|raw}` pattern.

Do **not** invent a custom pager in the theme. In particular, do not add template-side algorithms based on:

- `request()->param(...)` for current page construction
- custom `page_count` / `total_page` / `total_pages` variables
- hand-written `pager_i` loops
- custom `ellipsis` generation
- custom `disabled prev` / `disabled next` pager shells
- forced one-page shells like `上一页 1 下一页` unless that exact behavior is produced by the demo pagination chain

## Repair pattern

When pagination is missing or static code does not match rendered output:

1. Read the corresponding `demo_xz01` list/common_data templates.
2. Identify the demo data helper chain (`getPcPageData` / `getMobilePageData`) and the output location for `{$page_code|raw}`.
3. Align the current template to that chain, using existing backend helpers and existing route data.
4. Do not modify routes/controllers/backend PHP to fake pagination unless the user explicitly authorizes backend work.
5. Clear `/www/wwwroot/www.900az.com/runtime/` after template changes.
6. Validate both source and rendered 200 routes, but if rendered pagination is absent, report/fix it as a demo-chain mismatch rather than adding a self-designed pager.

## Validation

A PASS requires:

- target list/search templates contain demo-compatible `{$page_code|raw}` or a verified demo-equivalent pagination partial;
- no self-designed pager keywords remain (`request()->param`, `page_count`, `total_pages`, `total_page`, `pager_i`, `ellipsis`, `disabled prev`, `disabled next`);
- relevant real PC and mobile routes return HTTP 200 without ThinkPHP/PHP errors;
- non-existent database routes are not treated as failures and must not be created from template filenames.
