# PC Navigation Scope Validation Lesson

## Why this exists

A live PC homepage repair changed the top `<nav class="xz-pc-nav">` to render from `get_nav_menu`, but the rendered page still contained words such as `软件下载`, `热门排行`, `装机必备`, and `下载资讯` in lower homepage shortcut/keyword blocks. Those lower blocks are content modules, not the top navigation bar.

## Durable lesson

When the user reports a `PC导航栏` problem, scope validation to the actual top navigation container first. Do not treat same/similar labels elsewhere in the homepage as proof the header nav is still wrong.

## Validation pattern

1. Identify the top-nav container in the template and rendered HTML, e.g. `<nav class="xz-pc-nav">`.
2. Parse only that block for labels and hrefs.
3. Confirm the block is data-driven (`get_nav_menu` / `$vo.name` / `$vo.href` or equivalent existing menu source).
4. Separately note if similar labels remain in non-nav content modules, but do not conflate them with the top-nav bug.
5. If the user asks to also fix shortcut/keyword modules, split that into a separate small xz01 task.
