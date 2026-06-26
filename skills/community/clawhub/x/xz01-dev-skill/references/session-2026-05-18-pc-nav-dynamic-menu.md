# 2026-05-18 xz01 PC Top Navigation Dynamic Menu Rule

## Trigger

The live PC homepage navigation on `https://www.900az.com/` was found to contain guessed hardcoded labels and links such as `热门排行`, `装机必备`, `下载资讯`, `专题合集`, and `https://www.900az.com/zoszx01/` instead of following the `demo_xz01` menu-rendering pattern.

## Correct Pattern

PC top navigation must be rendered from existing navigation/menu data, not from guessed template labels or manually invented routes.

Reference pattern from `demo_xz01`:

```php
<?php
    $nav_list = get_nav_menu(1,0,['list_order'=>'asc'],0,333);
    $current_nav_id=isset($category['id'])?($category['parent_id']==0?$category['id']:$category['parent_id']):(isset($page['id'])?'-1':(isset($keyword)?'-2':0));
    $current_nav_id=$current_nav_id==51?52:$current_nav_id;
?>
{foreach name="$nav_list" id="vo"}
<li class="{if condition='($current_nav_id eq 0&&empty($vo.page_id)) ||(!empty($vo.page_id)&&$current_nav_id eq $vo.page_id)'}active{/if}">
    <a href="{$vo.href}">{$vo.name}</a>
</li>
{/foreach}
```

Adapt the outer DOM/classes to the active template, but keep labels and links data-driven via `$vo.name` / `$vo.href` or an equivalent existing menu source.

## Hard Rule

- Do not invent PC top-navigation column names.
- Do not invent PC top-navigation hrefs.
- Do not map sections by “what seems useful” when a navigation/menu table already exists.
- Do not create new routes to satisfy a navigation design.
- If a helper already returns an absolute href, use it directly and do not prefix it again.

## Validation

For PC homepage/header fixes, test must parse `<nav class="xz-pc-nav">` or the template's equivalent top-navigation block from the rendered page and verify:

1. visible navigation labels match menu data output, not guessed fallback labels;
2. hrefs are from the menu data output;
3. known previous guessed labels/links are absent from the top-navigation block;
4. homepage active state is present where applicable;
5. no backend/controller/route file was changed for this fix.
