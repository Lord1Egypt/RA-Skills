# 2026-05-18 xz01 Dual-End Top Navigation Dynamic Menu Rule

## Trigger

After fixing PC header navigation on `https://www.900az.com/`, the mobile domain `https://m.900az.com/` was found to have the same class of error: the mobile top nav was hardcoded as `首页 / 软件 / 排行 / 必备 / 资讯` with guessed links such as `https://m.900az.com/zoszx01/`, instead of using the same menu/navigation source as the PC header.

User correction: **m 的导航栏也是同步处理的，必须加入 xz01 技能规范，强制严格每套模板都执行。**

## Mandatory Rule

For every xz01 template set, **PC and mobile top navigation are a paired requirement**:

1. If PC header/top navigation is implemented or repaired, mobile header/top navigation must be checked and repaired in the same task scope.
2. If mobile header/top navigation is implemented or repaired, PC header/top navigation must be checked and kept aligned.
3. Both ends must render labels and links from existing menu/navigation data, not guessed hardcoded labels or invented hrefs.
4. This applies to every xz01 template set, not only the current `900az` live theme.
5. A task is incomplete if only one end is fixed while the other end still contains guessed hardcoded nav items.

## Reference Patterns

PC-style pattern:

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

Mobile-style pattern:

```php
<?php
    $nav_list = get_nav_menu(1,0,['list_order'=>'asc'],0,3333);
    $current_nav_id=isset($category['id'])?($category['parent_id']==0?$category['id']:$category['parent_id']):(isset($page['id'])?'-1':(isset($keyword)?'-2':0));
    $current_nav_id=$current_nav_id==51?52:$current_nav_id;
?>
{foreach name="$nav_list" id="vo"}
<?php $vo['href'] = str_replace("www.", "m.", $vo['href']); ?>
<a {if condition='($current_nav_id eq 0&&empty($vo.page_id)) ||(!empty($vo.page_id)&&$current_nav_id eq $vo.page_id)'}class="active"{/if} href="{$vo.href}">{$vo.name}</a>
{/foreach}
```

The exact DOM (`ul/li/a`, `nav/a`, class names) may be adapted to the active template design. The invariant is that `$vo.name` / `$vo.href` or an equivalent existing menu source provides the labels and links.

## Forbidden

- Do not hardcode PC-only nav fixes and leave mobile hardcoded.
- Do not use guessed mobile labels like `软件`, `排行`, `必备`, `资讯` unless they are the exact menu data output.
- Do not invent mobile hrefs like `/zoszx01/`, `/zoszx02/`, `/zoszx03/` because they open or appear plausible.
- Do not create backend routes or columns to satisfy a header design.
- Do not verify by substring only; `应用软件` and `手游排行榜` are valid menu labels and must not be confused with old guessed standalone labels `软件` / `排行`.

## Validation

For any xz01 template header/navigation task, test must parse the rendered top-navigation containers on both domains:

- PC: `https://www.<domain>/` with desktop UA, e.g. `<nav class="xz-pc-nav">` or equivalent.
- Mobile: `https://m.<domain>/` with real mobile UA, e.g. `<nav class="xz-m-nav">` or equivalent.

The validation report must include:

1. PC nav item list: label, href, active state.
2. Mobile nav item list: label, href, active state.
3. Explicit confirmation that labels/hrefs are data-driven from existing menu/navigation data.
4. Exact-item checks for known guessed labels; do not rely on broad substring matching.
5. Checks that known guessed links are absent from the nav block.
6. Confirmation that no PHP/backend/controller/model/config/route/vendor/thinkphp files were changed for a template navigation fix.
