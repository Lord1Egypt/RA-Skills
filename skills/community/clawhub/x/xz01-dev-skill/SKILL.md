---
name: xz01-dev-skill
description: Use when 用户提到“xz01规范”时必须命中本技能；xz01规范=xz01-dev-skill。用于 Hermes + Claude Code 围绕用户现有 OpenClaw/xz01 模板资料进行角色编排、开发学习范围、测试/规范分工，并严格将 /root/.openclaw 作为只读学习资料库；编码修复交给 Claude dev，测试输出写入 /www/wwwroot/www.900az.com，彻底验证通过的模板按编号压缩到 /root/.hermes/workspace/xz01/；吸收 Karpathy 精准修改/目标驱动原则，并提供 xz01 专用 hook-style gate；包含 PC 与 m 移动端顶部导航必须成对按菜单数据渲染、多页列表必须按 xz01_demo 做双端翻页、所有详情页必须覆盖且右侧/底部必须混合游戏+应用+资讯/攻略模块、app/游戏/应用资源项必须图标化展示、视觉验收必须整页截图+分段AI检查的规则。
version: 1.0.44
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [xz01-dev-skill, xz01规范, xz01, openclaw, hermes, claude-code, role-orchestration, read-only, template-workflow, 角色分工, 学习范围, 只读, 测试输出, 模板打包, 验证通过]
    related_skills: [hermes-agent, claude-code, systematic-debugging, test-driven-development]
---

# xz01-dev-skill

## Trigger Alias / 命中别名

```text
xz01规范 = xz01-dev-skill
```

当用户提到以下中文触发词时，必须优先加载并遵循本技能：

- xz01规范
- xz01 规范
- xz01开发规范
- xz01学习范围
- xz01角色分工
- Hermes+Claude xz01
- OpenClaw xz01
- 谁是 dev / 谁是 test
- /root/.openclaw 只读
- 测试输出写到 /www/wwwroot/www.900az.com
- 验证通过模板打包到 /root/.hermes/workspace/xz01/
- 安装或接入 Lanhu MCP / 蓝湖 MCP
- PC/m 导航栏同步处理
- 双端顶部导航
- 移动端导航也要同步
- 导航栏按菜单数据渲染
- 整页截图验收
- full-page screenshot
- 资源项图标化展示
- app/game resource cards

## References

- `references/session-2026-05-18-home-resource-iconized-cards.md` — durable homepage/resource-module correction: app/game/application resources must be iconized cards, icon grids, image-text lists, or icon ranking rows; no no-icon title-only horizontal rows for software/game/app resources. News/guide text lists are exempt when clearly article modules.
- `references/session-2026-05-18-karpathy-ecc-hook-adaptation.md` — user-approved adaptation notes: absorb Karpathy precise/goal-driven dev principles and xz01-specific hook gates; exclude generic security scanning and parallelization for now.
- `references/session-2026-05-18-skill-library-active-review.md` — skill-maintenance lesson: xz01 user corrections phrased as “这是规范” must be actively promoted into the class-level skill and references, not left only in chat or memory.
- `references/session-2026-05-18-all-detail-mixed-sidebar.md` — user correction that “详情页” means every active PC/mobile detail template, including collection/topic detail when present; PC right sidebars must not be only攻略 and must mix app/software, game, and news/guide modules with real data. Also covers the operational pattern that if a long dev worker times out after making file changes, do not assume failure or success: first inspect modified timestamps/content, then continue with smaller verification/fix tasks.
- `references/session-2026-05-18-dual-end-list-pagination.md` — hard pagination rule: every dual-end list page except ranking/rank-list pages must render pagination like `xz01_demo` when data exceeds one page; PC uses numeric page links, mobile uses `上一页` / `下一页` controls. The scope is route/database-list based, not limited to files named `list_soft/list_game/list_news/list_collection`; examples include `/zoszx/`, image/video/package/kaifu/all-news list templates, and search-result list templates when present.
- `references/session-2026-05-18-rendered-pc-pagination-fallback.md` — correction after a bad pagination repair: do **not** invent a custom fallback pager or page-count algorithm. xz01 list pagination must follow `xz01_demo`'s `getPcPageData` / `getMobilePageData` → `$page_code` → `{$page_code|raw}` pattern; if rendered pagination is absent, fix the data/template chain to match demo rather than designing a new pager.
- `references/session-2026-05-18-pagination-demo-copy-correction.md` — session-specific correction: when user says “造搬/照搬 xz01_demo”, treat it as an implementation-shape constraint, not just a visual/functional goal; revert self-designed pagination code and update the skill/spec immediately.
- `references/session-2026-05-18-pagination-common-data-chain.md` — pagination root-cause correction: `{$page_code|raw}` in the bottom template is not enough; the list template must include the matching `common_data/_list_*_common.html`, and that file must call `getPcPageData` / `getMobilePageData` so `$page_code` is actually generated.
- `references/session-2026-05-18-pagination-data-volume-validation.md` — pagination validation correction: empty rendered `<ul class="pagination"></ul>` is a failure only when the route has more than one page of eligible data; when a non-rank list currently has one page or insufficient data, demo helpers may leave `$page_code` empty and the validator must report it as data-volume-limited rather than asking dev to invent fallback links.
- `references/session-2026-05-18-skill-metadata-sync-audit.md` — publishing-process correction: before `clawhub publish`, audit that `SKILL.md`, `skill.json`, and `_meta.json` all share the same version and that descriptions/changelog match the actual change.
- `references/session-2026-05-18-pagination-rule-template-repair.md` — workflow correction after the user pointed out that only the rule was updated: when a new xz01 rule identifies an active template defect, update the skill/spec and immediately apply the rule to affected deployed/candidate templates, then clear runtime and verify.
- `references/session-2026-05-18-timeout-recovery-partial-work.md` — timeout recovery pattern for xz01 delegate workers: inspect authorized workdirs and partial artifacts after timeout, continue from useful landed work with smaller tasks, and never mark timeout as PASS without independent validation.
- `references/session-2026-05-18-fullpage-visual-qa-correction.md` — user correction after a first-viewport-only PASS missed lower-page layout details: xz01 visual QA must use PC/mobile full-page screenshots, segment/contact-sheet long pages, and inspect lower modules/footer before PASS.
- `references/session-2026-05-18-mobile-domain-validation-correction.md` — mobile QA correction: do not validate mobile by applying a 390px/mobile UA to `www.900az.com`; use the real `m.900az.com` URL plus mobile UA/CDP metrics, and parameterize validation scripts by URL per case.
- `references/session-2026-05-18-openclaw-temp-artifact-boundary.md` — boundary correction after a validation worker created a temporary screenshot script under `/root/.openclaw/workspace`: no temporary scripts, screenshots, reports, manifests, logs, or generated artifacts may be written anywhere under `/root/.openclaw`; use `/tmp`, `/www/wwwroot/www.900az.com/test-artifacts`, or `/root/.hermes/workspace/xz01-artifacts` instead.
- `references/session-2026-05-18-detail-sidebar-bottom-modules.md` — detail-page repair pattern: every active app/game/news/collection detail template must include demo-like right sidebar and bottom data modules using real existing data; validate with source/static checks plus screenshots/AI, require mixed app/software + game + news/guide modules, and watch for PC bottom summary text overflow.
- `references/session-2026-05-18-dual-end-nav-dynamic-menu.md` — user correction and hard rule: PC and m/mobile top navigation are a paired requirement for every xz01 template set; both must render from existing menu/navigation data, never guessed hardcoded labels or invented links.
- `references/session-2026-05-18-mobile-layout-overflow-repair.md` — mobile visual QA/repair pattern: use CDP mobile device emulation plus runtime overflow probes for final validation; fix nav as an internal scroller, two-column modules as shrink-safe grids, and list rows with `min-width:0`/ellipsis.
- `references/session-2026-05-18-pc-nav-dynamic-menu.md` — PC top-navigation repair lesson: render the header nav from existing menu/navigation data (`get_nav_menu` / `$vo.name` / `$vo.href` or equivalent), never from guessed labels or invented links.
- `references/session-2026-05-18-pc-nav-scope-validation.md` — validation-scope lesson: when fixing PC top navigation, parse the actual nav container and do not conflate similar labels in lower shortcut/keyword modules with the header nav.
- `references/session-2026-05-18-hermes-native-title-search-repair.md` — direct Hermes xz01 live-site repair lesson: do not call OpenClaw runtime orchestration when the user addresses Hermes; use Hermes-native dev/test delegation, demo read-only reference, shared-head dynamic title repair, theme-only search template fixes, and multi-keyword title validation.
- `references/session-2026-05-18-hermes-native-no-search-regression.md` — user correction and repair pattern for xz01 live-site regressions when Hermes is addressed directly: do not invoke OpenClaw sessions/flow-controller; use Hermes-native verification/delegation; dual-end search boxes should keep visual styling when shown but must be non-functional by default: no `/search` action/link, no enabled input/submit, and no JS submit binding.
- `references/session-2026-05-18-xz01-skill-autopublish.md` — user correction that xz01 skill edits are incomplete until version metadata is synchronized and `clawhub publish` is executed without asking for confirmation.
- `references/session-2026-05-18-pc-mobile-search-visual-repair.md` — live-site search visual repair lesson: PC search must be right/side-aligned and visually weakened rather than top-center; mobile search must be an obvious compact magnifier-style visual-only entry, not merely the absence of a large input; verify 390px mobile card overflow after search/header changes.
- `references/lanhu-mcp-installation.md` — recommended Docker Compose + HTTP MCP setup for `dsphper/lanhu-mcp`, including Hermes native MCP and Claude Code connection examples.
- `references/demo-xz01-may-2026-source-update.md` — read-only learning notes from the May 2026 `demo_xz01` source update, including the user-confirmed rule that front-end PC/mobile search is canceled/weakened and should not be a default QA failure.
- `references/xz01-template-factory-architecture.md` — architecture notes for upgrading the current main/dev/test/rule loop into a 60-template dual-end xz01 automation factory with corpus ingestion, DB/route learning, planning, rendering, validation, repair loops, rule review, and packaging.
- `references/hermes-native-xz01-first-run.md` — first-run pattern for building a safe Hermes-native xz01 prototype under `/root/.hermes/workspace/xz01-factory`, including minimal output shape, static validation checklist, and prototype-vs-production boundary.
- `references/hermes-native-xz01-live-deploy-validation.md` — live temporary deployment pattern for `/www/wwwroot/www.900az.com/public/themes/default/`, including backup, cache clearing, HTTP/PHP/static/browser/AI validation, fallback data blocks, trace-overlay hiding, and screenshot artifact paths.
- `references/run-0002-visual-repair.md` — session-specific repair notes for making a temporary xz01 homepage more demo-like after AI visual review: PC density/card-count fixes, topic-background cleanup, desktop-vs-mobile-UA validation, true 390px mobile screenshots, right-side alignment/overflow probes, long mobile screenshots for lower modules, and viewport clipping remedies.
- `references/session-2026-05-16-main-role-boundary-correction.md` — user correction that xz01 coding/HTML/CSS/template fixes must be delegated to Claude Code dev even when the fix is small or obvious; main must not directly patch implementation files.
- `references/session-2026-05-16-pc-gap-dev-test-rule-loop.md` — concrete example of handling a small PC quick-topic spacing defect through Claude dev → independent test screenshot/AI review → rule audit, including constrained dev prompt shape and test acceptance criteria.
- `references/session-2026-05-16-right-sidebar-height-balance.md` — follow-up lesson from repeated PC gap corrections: if a lower section is pushed down by a taller right sidebar, reduce right-side content height (e.g. `专题推荐` 4→3) instead of only compressing margins.
- `references/session-2026-05-16-packaging-gate-runtime-list-detail.md` — user correction after an invalid package: every dev change must clear `/www/wwwroot/www.900az.com/runtime/` before validation, and packaging is forbidden until homepage/list/detail rendering, jQuery, trailing-slash links, data images, and dynamic data gates all pass.
- `references/session-2026-05-16-no-php-controller-template-dev.md` — user correction that xz01 template development must never modify PHP/backend/controller/model/config files; dev scope is theme templates/assets only unless the user explicitly authorizes a non-template backend task.
- `references/session-2026-05-16-theme-only-data-links-search.md` — theme-only repair notes after backend restoration: restore data with existing template tags, make slash-ending column links absolute with the correct PC/mobile host, avoid double-prefix domains, keep PC search out of the top center, fix missing detail templates in the theme, and keep test artifacts out of `/root/.openclaw`.
- `references/session-2026-05-16-max-turns-task-splitting-validation-scripts.md` — user correction for repeated `max_turns` and long-running tasks: do not raise max-turns, split work to minimum units, use fixed validation scripts, do not enable the no-re-exploration rule for now, time-box dev/test tasks, use Claude interactive/tmux only as a supervised workbench for a sequence of small tasks, and prioritize stability with a single serial queue unless the user explicitly re-enables concurrency.
- `references/session-2026-05-16-demo-xz01-systematic-validation.md` — user correction that `demo_xz01` must be learned systematically: dual-end list/detail templates must exist and render, pagination variables/data rendering must follow demo patterns, runtime cache must be cleared after every dev change, PC+mobile static/HTTP/browser/screenshot/AI gates are mandatory before packaging, and the validation scripts are part of this skill.
- `references/session-2026-05-16-allpage-visual-qa-and-scanner-fixes.md` — follow-up validation lesson: when the user asks for all-page dual-end screenshots and AI review, capture every crawled URL, create URL→screenshot manifests and contact sheets for AI review, retry screenshot timeouts, and avoid false `0款` scanner matches such as `10款`. Treat DB-backed labels like “手游下载” as wording observations rather than automatic failures when the route and data are valid.
- `references/session-2026-05-16-db-channel-name-display-standard.md` — user correction that xz01 PC/mobile category/list display names must use `cmf_cms_channel.name` from the database row for the current alias; e.g. alias `gzos` must display `手游下载` because the DB channel name is `手游下载`.

## Overview

This skill is for operating a Hermes + Claude Code workflow around the user's existing OpenClaw/xz01 material. The existing OpenClaw tree is a **read-only learning corpus**, not a place to write configs, skills, memory, cron state, sessions, templates, or generated reports unless the user explicitly authorizes a specific write.

Authoritative read-only boundary:

```text
/root/.openclaw/ and every subdirectory = read-only learning material
```

Default runtime division:

```text
Hermes current session = main / dispatcher / final reporter
Claude Code = dev / implementation worker
Hermes independent test role = test / validation worker
Hermes independent rule role = rule / process and standard reviewer
```

Recent correction status:

```text
Dual-end top navigation is mandatory for every xz01 template set: PC and m/mobile nav must be checked and fixed together, using existing menu/navigation data on both ends.
For any dual-end list page where the data volume is greater than one page, pagination is mandatory: PC uses numeric page links; mobile uses 上一页/下一页, matching xz01_demo.
When a new xz01 rule describes a current live/candidate template defect, the response must not stop at updating the skill/spec; apply the rule to the affected templates immediately, then clear runtime and verify.
```

Skill-maintenance lesson from this session:

```text
When the user states a new xz01 rule as “这是规范”, treat it as a durable skill update immediately: add/patch the class-level SKILL.md, create or update a concise references/session-*.md detail file if useful, synchronize skill.json/_meta.json versions, and publish the updated skill. Do not leave the rule only in chat or memory.
```

## When to Use

Use this skill when the user asks about:

- “xz01规范”
- “xz01 规范”
- “xz01-dev-skill”
- “Hermes 和 Claude 怎么分工”
- “谁是 dev，谁是 test”
- “OpenClaw 的学习范围”
- “/root/.openclaw 只读”
- “把这个流程做成 skill”
- “持续优化技能”
- Hermes + Claude role division for OpenClaw/xz01-style work
- what each role should learn from `/root/.openclaw`
- turning OpenClaw process rules into Hermes skills
- coordinating template development, validation, and rule review without modifying OpenClaw's existing files
- preserving dev/test/rule separation while using Claude Code for implementation

Do **not** use this skill to modify `/root/.openclaw` files. Treat them as reference-only.

## Non-Negotiable Boundary

All roles must obey:

```text
Do not write to /root/.openclaw/
Do not create temporary scripts under /root/.openclaw/
Do not create screenshots, reports, manifests, logs, lock files, downloads, or generated artifacts under /root/.openclaw/
Do not patch /root/.openclaw/
Do not update /root/.openclaw/openclaw.json
Do not modify /root/.openclaw/workspace/*
Do not modify /root/.openclaw/agents/*
Do not modify /root/.openclaw/cron/*
Do not modify /root/.openclaw/memory/*
Do not modify /root/.openclaw/flows/*
Do not modify /root/.openclaw/workspace/demo_xz01
```

Allowed operations on `/root/.openclaw`:

- read targeted files
- inventory directories
- summarize rules
- learn conventions
- compare reports against known standards

Template-development backend boundary:

```text
For xz01 template development, NEVER modify PHP/backend/controller/model/config files.
Forbidden paths include: application/**/*.php, config/**/*.php, route/**/*.php, thinkphp/**/*.php, vendor/**/*.php, and any controller/model/service/backend PHP file.
Allowed template scope by default: public/themes/<theme>/** only (HTML templates, CSS, JS, theme assets).
If required data/routes are unavailable through existing backend/template tags, report the limitation; do not patch PHP to make a template pass.
Any package created after PHP/controller/config changes is invalid until those backend changes are reverted and the template is revalidated with theme-only changes.
```

If writes are required, write only to:

- Hermes skill storage (`~/.hermes/skills/...`) when creating/updating Hermes skills
- a user-authorized non-OpenClaw project directory
- `/www/wwwroot/www.900az.com` for all test-side outputs, validation artifacts, screenshots, reports, and website verification outputs unless the user explicitly changes it
- `/root/.hermes/workspace/xz01/` for numbered zip packages of templates that have fully passed verification
- `/tmp/...` for short-lived helper scripts and scratch files; never put temporary helpers under `/root/.openclaw`
- another explicit path the user names

Packaging rule for verified templates:

```text
Only templates that are thoroughly verified as passed may be packed.
Package verified templates as numbered compressed archives under /root/.hermes/workspace/xz01/.
Do not store final verified template packages under /root/.openclaw/.

Hard packaging gate:

- After every add/modify/delete development change, delete all directories/items under `/www/wwwroot/www.900az.com/runtime/` before validation.
- Do not package until PC/mobile homepage, software/game/news/category list pages and detail pages are generated/available and render correctly from existing database routes; list/detail pages must not be merely referenced or assumed. Any dual-end list page with more than one page of data must include pagination: PC numeric page links and mobile `上一页` / `下一页`, matching `xz01_demo`.
- Do not package if rendered pages contain missing header/head jQuery loading, no-slash column URLs, malformed duplicate-host absolute URLs, `cms/page/index/id` / `cms/Page/index` / `mobile/Page/index` errors, prohibited filler SVG data images, mostly `暂无...数据` placeholders, or zero real content/detail links while DB records exist.
- For every rendered column/category URL whose path ends with `/`, output an absolute URL with protocol and the correct host: PC uses `https://www.900az.com/.../`, mobile uses `https://m.900az.com/.../`. Normalize helper output first so an already-absolute URL is not prefixed again.
- PC header/search layout gate: the PC search box must never be placed at the top center of the header. Use a right-side, below-header, or otherwise non-center placement. Mobile is evaluated separately.
- Dual-end top-navigation gate: for every xz01 template set, PC and m/mobile top navigation must be checked/fixed together and rendered from existing menu/navigation data. A header-navigation task is incomplete if either side still uses guessed hardcoded labels or invented links.
```

## Role Map

| Role | Default assignee | Purpose | May write `/root/.openclaw`? |
|---|---|---|---:|
| main | Hermes current session | receive requests, split work, dispatch, supervise, final report | No |
| dev | Claude Code | implement code/template changes in authorized workdir | No |
| test | independent Hermes test role/session | screenshots, AI visual analysis, lint/HTML/CSS/template validation | No |
| rule | independent Hermes rule role/session | process audit, rule review, skill/spec suggestions | No |

## Main Role Learning Scope

Main learns coordination and boundaries, not implementation.

Read-only sources:

- `/root/.openclaw/workspace/IRON_RULES.md`
- `/root/.openclaw/workspace/AGENTS.md`
- `/root/.openclaw/workspace/MEMORY.md`
- `/root/.openclaw/workspace/error.md`
- `/root/.openclaw/workspace/DREAMS.md`
- `/root/.openclaw/workspace/scripts/flow-controller.js`
- `/root/.openclaw/workspace/scripts/check-flow-stuck.js`
- `/root/.openclaw/workspace/scripts/violation-tracker.js`
- `/root/.openclaw/openclaw.json`
- `/root/.openclaw/cron/jobs.json`
- `/root/.openclaw/agents/*/sessions` only when targeted history/debug context is needed
- `/root/.openclaw/memory/*.sqlite` only when targeted memory inspection is explicitly needed

Main must learn:

1. role boundaries
2. flow sequence: main → dev → test → rule → main
3. when to dispatch to each role
4. how to avoid dev/test/rule collapse
5. report format expectations
6. historical violations and user corrections
7. that `/root/.openclaw` is read-only

Main must not:

- write code
- test/screenshot
- modify CSS/templates
- modify PHP/backend/controller/model/config files for template development
- update OpenClaw configs
- silently skip test or rule

## Dev Role Learning Scope

Dev is Claude Code by default. Dev learns implementation standards and writes only in an authorized non-OpenClaw workdir.

Read-only sources:

- `/root/.openclaw/workspace/IRON_RULES.md`
- `/root/.openclaw/workspace/AGENTS.md`
- `/root/.openclaw/workspace/TEMPLATE-SPEC.md`
- `/root/.openclaw/workspace-dev/MEMORY.md`
- `/root/.openclaw/workspace-dev/skills`
- `/root/.openclaw/workspace-dev/memory`
- `/root/.openclaw/workspace/demo_xz01`
- `/root/.openclaw/workspace/memory/team/project` targeted template-development notes

Dev must learn:

1. ThinkPHP template structure
2. PC/mobile dual-template structure
3. common module organization
4. HTML/CSS/JS conventions
5. template tag closure rules (`include`, `foreach`, `if`)
6. data filters such as `is_hide=0` and `status=1`
7. search/navigation/carousel/data rendering conventions, with updated `demo_xz01` nuance and user correction: front-end PC/mobile search should render the search-box visual style when the template design includes that header/search area, but must not render functional search behavior by default. Use disabled/non-submitting visual-only controls: no `/search` link/action, no enabled input, no submit, no JS submit binding. Do not require a working dual-end search feature unless the user explicitly requests functional search. For visual placement, PC search must not sit in the page/header center; keep it right-aligned, side-aligned, below-header, or otherwise clearly non-center and visually weakened. Mobile search must be a compact magnifier/icon-style entry when shown; removing the large input is not enough if no small search entry is visible.
8. Dual-end top-navigation rendering rule (mandatory for every xz01 template set): PC and m/mobile header/top navigation are a paired requirement and must be checked/fixed together. Both ends must come from existing menu/navigation data such as PC `get_nav_menu(1,0,['list_order'=>'asc'],0,333)` and mobile `get_nav_menu(1,0,['list_order'=>'asc'],0,3333)` with `$vo.name` and `$vo.href` (or an equivalent existing menu source); mobile hrefs must use the mobile host, e.g. by replacing `www.` with `m.` when the helper returns PC URLs. Do not hardcode guessed labels like “热门排行/装机必备/专题合集” or mobile shorthand labels like “软件/排行/必备/资讯” unless they are the exact menu data output; do not invent hrefs just because they open. Preserve each active template's outer nav classes while keeping labels/links data-driven.
9. route rule: database routes are authoritative; do not invent routes from template filenames
10. database channel display rule: category/list page labels, headings, breadcrumbs, and related front-end display names must use `cmf_cms_channel.name` for the current database alias on both PC and mobile. The alias/path (e.g. `gzos`) is not the display label; if the DB row has `name='手游下载'`, PC `/gzos/` and mobile `m.900az.com/gzos/` must display `手游下载` consistently. Do not normalize to guessed labels unless explicitly requested.
11. demo_xz01 is a pattern library, not editable and not copy-paste source
12. updated template-structure nuance: some newer templates remove `zyxz_module` entirely or inline sidebar/recommendation blocks instead of using fixed `_side_*.html` partials; preserve the specific template's structure instead of forcing old module inventories
13. demo_xz01 systematic rendering and pagination rules: every xz01 template must implement complete PC+mobile homepage/list/detail coverage for existing DB routes. Except for ranking/rank-list pages, every dual-end database-backed list page whose data volume exceeds one page must render pagination like `xz01_demo`: PC uses numeric page links/page-code style pagination; mobile uses simple `上一页` / `下一页` controls. Scope is based on actual database routes and rendered list pages, not only files named `list_soft/list_game/list_news/list_collection`; include software/game/news/category, collection/topic, image, video, package/gift, kaifu, all-news, and search-result list templates when present. The implementation must copy/align with demo's full pagination chain: the list template includes the matching `common_data/_list_*_common.html`, that common data file calls `getPcPageData` / `getMobilePageData` for the main list, those helpers generate `$page_code`, and templates output `{$page_code|raw}` or an explicitly confirmed demo-equivalent partial. Do not modify PHP/controllers/routes to fake pagination, do not rely on `getAllData()` for the main paginated list, and do not invent custom page-count/request-parameter/fallback pager algorithms in the theme.
14. app/game/application resource-card rule: every app/game/application resource item on homepage, list pages, sidebars, recommendation modules, latest-resource modules, ranking modules, and detail-page related-resource modules must render with an icon/thumbnail/cover plus title and metadata/action in a card, icon grid, or image-text list. It is forbidden to display app/game/application resources as text-only horizontal title rows inside a module. Article/news/guide text lists may remain text-only, but software/game/app resources may not.
15. resource loading rules: do not use `/themes/default/common_cms/common/jquery.min.js`; load jQuery from the correct PC/mobile asset path. Include UIkit and Swiper only when needed, using the correct PC/mobile asset CSS+JS pair.

Dev must not:

- read Feishu group messages
- self-certify final acceptance
- skip test
- write `/root/.openclaw`
- modify `demo_xz01`
- modify PHP/backend/controller/model/config files for template development (`application/**/*.php`, `config/**/*.php`, routes, ThinkPHP core, vendor, backend services). Template tasks are limited to `public/themes/<theme>/**` unless the user explicitly authorizes a non-template backend task.
- perform official screenshot/AI visual validation

Dev output should include:

- changed file list in authorized workdir
- implementation summary
- self-check notes
- items for test to validate

## Test Role Learning Scope

Test is an independent Hermes role/session. It validates; it does not fix.

Read-only sources:

- `/root/.openclaw/workspace/IRON_RULES.md`
- `/root/.openclaw/workspace/AGENTS.md`
- `/root/.openclaw/workspace/TEMPLATE-SPEC.md`
- `/root/.openclaw/workspace-test/MEMORY.md`
- `/root/.openclaw/workspace-test/skills`
- `/root/.openclaw/workspace-test/scripts`
- `/root/.openclaw/workspace-test/skills/template-qa/scripts`
- `/root/.openclaw/workspace/demo_xz01`
- `/root/.openclaw/workspace/memory/team/project` targeted testing/screenshot/AI-vision notes

Test must learn:

1. PC screenshot requirements
2. mobile screenshot requirements
3. AI visual analysis requirement after screenshots
4. layout/overlap/missing-element/color/font/responsive checks
5. HTML tag closure checks
6. CSS path/layout checks
7. ThinkPHP template tag checks
8. search/navigation/carousel/data rendering checks, with updated `demo_xz01` nuance and user correction: a PC/mobile search-box visual shell may be present when required by the template design, but it must be visual-only unless the user explicitly requests functional search. Fail search if it has `/search` links/actions, enabled keyword input, enabled submit buttons, form submission, JS submit binding, or any clickable/searchable behavior; do not fail merely because a disabled visual search box is displayed
9. dual-end list pagination checks: for representative software/app, game, news/guide, category/channel, and equivalent database-backed list routes where data volume exceeds one page, PC must show numeric page links and mobile must show `上一页` / `下一页`; absence of pagination on a multi-page list is a FAIL even when the first page data renders correctly. Static template evidence is only a pre-check: test must verify the full `xz01_demo` pagination chain, not just the bottom output tag: list template includes matching `common_data/_list_*_common.html`, common data calls `getPcPageData` / `getMobilePageData` for the main list, helpers generate `$page_code`, and the template outputs `{$page_code|raw}`. If rendered HTML shows an empty `<ul class="pagination"></ul>`, first determine whether the route has more than one page of eligible data. For multi-page data, fail it as a missing upstream data-chain issue; for one-page/insufficient data, record it as expected demo behavior and do not ask dev to add a self-designed fallback pager.
10. app/game/application resource rendering checks: inspect homepage/list/detail/side/recommend/latest/rank modules and fail any app/game/application resource displayed as a text-only horizontal title row without icon/thumbnail/cover. News/article/guide text lists are exempt only when they are clearly not app/game/application resources.
11. regression testing; do not only check the last fix
12. full issue report format
13. full-page screenshot acceptance rule: for homepage/page visual QA, PC and mobile screenshots must capture the whole page, not only the first viewport. First-viewport screenshots may be used only as supplemental evidence. A visual PASS is forbidden unless the full page has been captured, split/contact-sheeted when long, submitted to AI visual review, and lower modules/footer/detail areas have been checked for layout, spacing, overflow, clipping, and missing/overlapping elements.

Test must not:

- write implementation code
- fix issues directly
- read Feishu group messages
- write `/root/.openclaw`
- claim visual correctness without full-page screenshots + AI visual analysis for homepage/page visual QA

Test output should include:

- PC full-page screenshot paths under `/www/wwwroot/www.900az.com` or mirrored under `/root/.hermes/workspace/...` for WebUI media
- mobile full-page screenshot paths under `/www/wwwroot/www.900az.com` or mirrored under `/root/.hermes/workspace/...` for WebUI media
- long-page segment/contact-sheet paths when a full-page screenshot is too tall for reliable visual review
- AI visual analysis findings saved/reported from the test output area
- structural/lint findings
- functional findings
- pass/fail conclusion
- issue list for dev when failed

All test-side artifacts must be written under `/www/wwwroot/www.900az.com` unless the user explicitly changes the output location.

## Rule Role Learning Scope

Rule is an independent Hermes role/session. It audits workflow and proposes/maintains durable rules. Under the read-only boundary, it must not update OpenClaw files unless explicitly authorized.

Read-only sources:

- `/root/.openclaw/workspace/IRON_RULES.md`
- `/root/.openclaw/workspace/AGENTS.md`
- `/root/.openclaw/workspace/TEMPLATE-SPEC.md`
- `/root/.openclaw/workspace-rule/MEMORY.md`
- `/root/.openclaw/workspace-rule/skills`
- `/root/.openclaw/workspace-rule/memory`
- `/root/.openclaw/workspace/skills`
- `/root/.openclaw/workspace/memory/team/project`
- `/root/.openclaw/workspace/memory/violations`
- `/root/.openclaw/workspace/error.md`

Rule must learn:

1. role-boundary violations to prevent
2. process-completion requirements
3. when a lesson should become a skill
4. when a lesson should remain a report, not memory/skill
5. skill metadata/version/documentation conventions
6. cron-log noise restrictions
7. user-specific hard rules

Rule must not:

- implement code
- test/screenshot
- write `/root/.openclaw`
- publish OpenClaw skills or edit OpenClaw specs without explicit authorization

Rule output should include:

- compliance audit
- whether the flow skipped steps
- whether new durable guidance is needed
- proposed skill/spec text if needed
- where it should be saved, subject to authorization

## Visual Repair Loop for xz01 Homepage Runs

When the user says to “继续” after a first xz01 prototype or says the page is not close enough to `xz01_demo`, do not stop at a functional page. Run an AI-vision-driven repair loop until the visible defects are fixed.

Workflow:

1. Compare against the `demo_xz01` target as a high-density download-station portal, not a sparse landing page.
2. Patch PC/mobile templates and CSS in the authorized run directory and the temporary deployment copy when already deployed.
3. Clear all directories/items under `/www/wwwroot/www.900az.com/runtime/` after every add/modify/delete development change and before any validation. Do this before rendering screenshots or HTTP checks so stale ThinkPHP cache cannot hide template/controller changes.
4. Validate HTTP 200, compiled PHP syntax, mobile no `target="_blank"`, and screenshots.
   - PC validation uses the desktop domain/access path: `https://www.900az.com/` with a desktop UA.
   - Mobile validation must use the mobile domain/access path: `https://m.900az.com/` with a real Android/iPhone Mobile User-Agent. Do not validate `m.900az.com` using the same desktop/PC browser access method as PC.
5. Submit PC and true small-width mobile-UA full-page screenshots to AI vision; if the page is long, also create segment images/contact sheets and ask AI to inspect the whole page. Treat AI findings as actionable repair items.
6. For mobile visual/layout defects, final acceptance must use the real mobile domain (`https://m.900az.com/...`), Chrome DevTools Protocol mobile emulation (`mobile:true`), real iPhone/Android UA, widths such as 360/390/430, and runtime overflow probes (`documentElement.scrollWidth/clientWidth`, `body.scrollWidth`, and bounding boxes). Ordinary headless `--window-size` screenshots are useful for discovery but are not authoritative if they contradict CDP mobile-mode metrics. A 390px/mobile-UA check against `https://www.900az.com/...` is PC-domain responsive testing, not mobile-site validation, unless the user explicitly asks for the PC domain to be phone-responsive. Intentional internal nav scrolling is acceptable only when page-level `scrollWidth` still equals `clientWidth`.
7. If the user reports right-side alignment issues, inspect both PC and mobile with the correct UA/domain pair, run an overflow probe on PC, capture a long mobile screenshot for lower modules, patch the run/deploy CSS, and re-check until AI vision passes.
8. Re-patch and re-check until AI confirms pass.

Common repairs from run-0002:

- PC hot games/apps need enough fallback cards to fill the grid; 3-4 cards create obvious blank areas.
- Topic-card decorative background text should be low-opacity and not compete with foreground titles.
- To match `xz01_demo`, reduce excessive modern-card spacing and increase list/module density.
- Mobile default browser snapshots may hide real phone-width clipping; validate mobile with real Android/iPhone UA against `https://m.900az.com/` and with DevTools mobile emulation at multiple CSS widths such as 390px and 430px.
- If a template includes a mobile back-to-top control, verify it with real Mobile UA + 390px screenshot: the button should be visible when required, must not cover download buttons or core content, and tapping/clicking after scroll should return the page to the top.
- Do not reuse the desktop/PC access method for mobile verification; mobile-domain validation requires a mobile UA header.
- If a 390px screenshot shows left blank strip, right card clipping, or right-side misalignment, fix container/grid width, not just `overflow-x:hidden`.
- For mobile two-column modules such as `每日推荐`, `攻略` category cards, and `精选专辑`, use shrink-safe grids (`repeat(2,minmax(0,1fr))`) and ensure child cards/text use `min-width:0`, `max-width:100%`, and ellipsis where needed.
- For dynamic mobile top navigation with more items than fit the viewport, use an intentional internal horizontal scroller (`overflow-x:auto`, `flex:0 0 auto`, no body-level overflow) rather than squeezing all items into one row or hiding overflow.
- If a mobile back-to-top (`顶`) button visually crowds or overlaps content, prefer a non-intrusive document-flow placement near the page bottom with safe-area spacing over a fixed floating overlay.
- Do not fix mobile containers to `max-width:390px`; it can pass a 390px screenshot but leave a blank strip on wider real phones. Under phone breakpoints prefer `width:100%; max-width:100%` plus safe padding/grid rules, then verify both 390px and 430px.
- For right-side alignment defects, verify PC and mobile separately: PC with desktop UA on `www.900az.com`, mobile with real Android/iPhone UA on `m.900az.com`; do not share access mode.
- For PC right-sidebar drift, probe `documentElement.scrollWidth` and overflowing elements, then unify `.xz-wrap`, hero grid, sidebar, lower sections, and card grids to the same right boundary.
- For homepage/page visual acceptance, never use only a first-viewport screenshot as PASS evidence. Capture full-page PC and mobile screenshots; for long pages, split/contact-sheet them so lower modules such as 热门应用 / 攻略 / 精选专辑 and the footer are explicitly inspected.

Detailed notes: `references/run-0002-visual-repair.md`.

## Lanhu MCP Integration

For xz01 work that needs Lanhu requirements/designs, the Lanhu MCP service is installed and managed outside `/root/.openclaw`:

- Session note: see `references/lanhu-mcp-discovery-notes.md` for the currently exposed tools and the no-account-wide-project-list limitation.

```text
Install path: /root/.hermes/workspace/lanhu-mcp
Docker container: lanhu_mcp_service
HTTP MCP endpoint: http://127.0.0.1:8000/mcp?role=Developer&name=HermesMain
Hermes MCP server name: lanhu
```

Operational rules:

- Use Docker Compose from `/root/.hermes/workspace/lanhu-mcp` to manage the service.
- Keep Lanhu credentials in `/root/.hermes/workspace/lanhu-mcp/.env`; do not write them to `/root/.openclaw`.
- Hermes native MCP connects through `mcp_servers.lanhu` in `/root/.hermes/config.yaml`.
- After MCP config changes, start a fresh Hermes session or restart the relevant Hermes process so discovered MCP tools are loaded.
- If external downloads are needed, use the user's temporary proxy:

```bash
export http_proxy=http://192.168.1.9:1080
export https_proxy=http://192.168.1.9:1080
export all_proxy=socks5://192.168.1.9:1080
```

Verification commands:

```bash
cd /root/.hermes/workspace/lanhu-mcp
docker compose ps
curl -fsS http://127.0.0.1:8000/health
hermes mcp test lanhu
```

Discovered Lanhu tools include page analysis, design analysis, slice extraction, team messages, and member listing.

## Hermes-Native Orchestration Boundary

Do not port OpenClaw-only runtime mechanisms into Hermes workflow design.

When the user directly addresses Hermes for an xz01 live-site/template issue, use Hermes-native execution immediately. Do **not** call OpenClaw `sessions_send`, `flow-controller`, role sessions, or other OpenClaw runtime orchestration unless the user explicitly asks to operate OpenClaw itself. OpenClaw files may still be read as reference material under the read-only boundary.

OpenClaw-specific concepts such as `sessions_send(sessionKey: agent:dev:main, ...)`, `/root/.openclaw/agents/*/sessions`, and the OpenClaw `flow-controller.js` state machine are read-only legacy/reference material for this workflow. They must not be treated as Hermes-native execution primitives.

If the user addresses Hermes directly about an xz01 live-site/front-end regression, do **not** call OpenClaw role sessions, OpenClaw `flow-controller`, or OpenClaw dispatch as the first response. Use Hermes-native tools/workers (`delegate_task`, deterministic scans, browser/curl verification, and theme-only edits where authorized by the task). OpenClaw orchestration may be studied as reference, but it is not the active execution path unless the user explicitly asks for OpenClaw.

Hermes-native replacements:

| OpenClaw concept | Hermes-native replacement | Use case |
|---|---|---|
| `sessions_send` to dev/test/rule sessions | `delegate_task` | Short synchronous subtasks; parent waits for result |
| Persistent role sessions | Hermes profiles + `hermes kanban` | Durable multi-worker queues and role separation |
| `flow-controller.js` single JSON state | Kanban board / factory SQLite queue | Multi-task durable workflow state |
| OpenClaw cron progress monitor | Hermes `cronjob` / `hermes cron` | Scheduled watchdogs and periodic reports |
| Manual subprocess role agents | `terminal(background=True)` or tmux-spawned `hermes` / `claude` | Long-running autonomous workers |
| Feishu-only role routing | Hermes gateway / WebUI / kanban notifications | User-facing delivery and status updates |

For xz01 automation, prefer a Hermes-native design:

```text
Hermes main/orchestrator
  -> xz01-factory queue/SQLite/Kanban task
  -> dev worker: Claude Code or Hermes profile for implementation
  -> renderer/test worker: deterministic scripts + independent Hermes/vision validation
  -> rule worker: Hermes profile or main-side review task
  -> packaging/reporting
```

Rules:

1. Do not claim Hermes supports OpenClaw `sessions_send` unless an explicit OpenClaw compatibility bridge is installed and verified.
2. Do not design new Hermes workflows around `/root/.openclaw` writable state.
3. Use OpenClaw files only as learning/reference material.
4. Use Hermes `delegate_task` for quick isolated checks, `hermes kanban` for durable multi-agent work, and deterministic scripts/SQLite queues for production xz01 factory state.
5. For long-running dev/test agents, spawn explicit `hermes` or `claude` processes via `terminal(background=True)`/tmux, or use Kanban dispatcher profiles.
6. When the user asks whether to keep noting caveats or directly build the first xz01 prototype, choose a safe action: create a Hermes factory run under `/root/.hermes/workspace/xz01-factory`, generate a prototype without touching production, run deterministic static validation, then report remaining production-validation steps. See `references/hermes-native-xz01-first-run.md`.


## Karpathy-Style Dev Execution Principles

The following principles are absorbed from the Andrej Karpathy Claude Code guidance and adapted to xz01. They are subordinate to xz01 hard rules but should be included in dev prompts and reviews:

1. **Think before editing, but do not over-ask.** State the execution assumption only when it affects boundaries such as production writes, backend/PHP changes, or route creation. For normal xz01 defects, proceed through dev → test → rule without asking the user.
2. **Keep implementation simple.** Do not add unrequested abstractions, helpers, framework layers, or broad JavaScript systems for template work.
3. **Make precise edits only.** Every changed line must map to the current xz01 acceptance target. Do not improve neighboring code, reformat unrelated files, remove pre-existing dead code, or change global structure unless required by the task.
4. **Define success criteria before dev starts.** Main's dev prompt should include: target page/component/defect, allowed files, forbidden files, runtime-clear requirement, and test acceptance criteria.
5. **Verify against the goal, not against dev's confidence.** Dev self-check is only a handoff note; official pass requires independent test screenshots + AI visual review + rule review where applicable.

## xz01 Hook-Style Gate Policy

Hooks **can** be part of this skill, but only as xz01-specific guardrails. Do not copy the generic Everything Claude Code hook system into xz01 wholesale.

User-specific exclusions:

```text
No generic security scanning requirement for xz01.
No parallelization/multi-agent expansion unless the user explicitly re-enables it.
No automatic hook that writes to /root/.openclaw.
No hook may replace independent test screenshots + AI visual review.
```

Allowed xz01 hook-style gates:

| Gate | Purpose | Blocking conditions |
|---|---|---|
| pre-dev | stop illegal implementation scope before editing | `/root/.openclaw` write, `demo_xz01` edit, PHP/backend/controller/model/config/route/core/vendor edit |
| post-dev | ensure development handoff is testable | changed files outside theme without explicit authorization; runtime not cleared after add/modify/delete |
| pre-test | prevent stale-cache validation | runtime not cleared |
| post-test | prevent false PASS | missing PC screenshot, missing mobile screenshot, missing AI visual analysis |
| pre-package | prevent invalid packages | static/HTTP/screenshot/AI/rule gates missing, source not an already-validated `public/themes/<theme>` directory |

A reusable script is bundled at:

```bash
/root/.hermes/skills/devops/xz01-dev-skill/scripts/xz01-hook-gate.py
```

Example usage:

```bash
# Before/after dev handoff
python3 scripts/xz01-hook-gate.py pre-dev --changed-files /www/wwwroot/www.900az.com/public/themes/default/pc/index.html
python3 scripts/xz01-hook-gate.py post-dev --changed-files /www/wwwroot/www.900az.com/public/themes/default/pc/index.html --runtime-cleared

# Before/after test
python3 scripts/xz01-hook-gate.py pre-test --runtime-cleared
python3 scripts/xz01-hook-gate.py post-test --pc-screenshot --mobile-screenshot --ai-pass

# Before package
python3 scripts/xz01-hook-gate.py pre-package \
  --theme-dir /www/wwwroot/www.900az.com/public/themes/default \
  --static-pass --http-pass --screenshot-pass --ai-pass --rule-pass
```

These gates may later be wired into Claude Code hooks, Hermes profiles, Kanban workers, or cron watchdogs. Wiring is optional; the policy and script are part of the skill so every xz01 run can use the same guard semantics.

## Execution Time Control and Task Splitting

User-specific rules for xz01 work after repeated `max_turns` interruptions and one task exceeding 50 minutes:

```text
Do not solve this by increasing Claude Code max-turns.
Split all work into the smallest practical units.
Use fixed validation scripts.
Do not enable a hard "禁止重新探索" / no-re-exploration rule for now.
Stability first: do not use concurrency for xz01 template execution unless the user explicitly re-enables it.
Avoid long-running single tasks; time-box dev/test calls and split earlier.
```

Operational rules:

1. Main must split work before dispatch. A dev task should normally cover one page, one component, or one defect class only. If a worker times out, inspect partial outputs first and then split the remaining work into a smaller follow-up; do not simply resend the original large prompt.
2. Execute xz01 template work through a strict serial queue: exactly one active dev task, one active test task, and one active rule review at a time. No parallel dev/test/rule lanes unless the user explicitly changes this rule.
3. Do not bundle development + broad exploration + screenshot/AI visual + full regression + packaging into a single dev task.
3. Dev should not perform official screenshots or full regression; test owns those.
4. Use fixed validation scripts under `/root/.hermes/workspace/xz01-factory/tools/` whenever applicable, or the embedded skill copies under `scripts/` when installing/reusing this skill:
   - `xz01-runtime-clear.sh` — clear `/www/wwwroot/www.900az.com/runtime/` after every add/modify/delete and before validation.
   - `xz01-backend-baseline-check.sh` — verify PHP/backend/controller/model/config scope was not modified for a template task.
   - `xz01-theme-diff-check.sh` — inspect theme-only change boundaries.
   - `xz01-quick-http-gate.py` — quick HTTP checks for key PC/mobile URLs.
   - `xz01-template-static-scan.py` — scan template code for PC/mobile core template completeness, bad jQuery/UI resource paths, pagination-pattern gaps, malformed links, mobile `target="_blank"`, and forbidden filler assets.
   - `xz01-full-url-scan.py` — crawl same-host PC/mobile front-end URLs and fail on 5xx/ThinkPHP errors, malformed links, mobile blank targets, many empty placeholders, and zero-count software/game list pages.
   - `xz01-screenshot-core.sh` — deterministic Chromium headless screenshots for core PC/mobile homepage, software/game list, and news list pages; use before AI visual review and copy artifacts into `/root/.hermes/workspace/...` for WebUI media.
   - `xz01-hook-gate.py` — xz01-specific hook-style guard script for manual use or future Claude Code/Hermes hook wiring; blocks `/root/.openclaw` writes, demo edits, backend/PHP/config/route/core/vendor edits, missing runtime-clear, missing screenshot+AI test closure, and incomplete package gates.
5. Keep `--max-turns` task-appropriate, but do not raise it as the mitigation. If a task cannot complete without raising turns, it is too large and must be split.
6. Time-box tool calls. If a run risks becoming long, stop and split the remaining work rather than allowing 50+ minute single runs.
7. For a batch of many related minimum-unit fixes, use Claude interactive session / tmux as a supervised workbench to reduce repeated startup/resume overhead and preserve local context. Each tmux instruction must still be one small task with an explicit stop/checkpoint; tmux is not permission to run one large task.
8. The proposed no-re-exploration rule is not active; do not insert it as a hard prompt constraint unless the user later enables it.

## Dispatch Rules

Main routes tasks by type:

| User request type | Route to |
|---|---|
| code/template development or repair | dev |
| screenshot, validation, visual QA, lint, functional checking | test |
| rule changes, process audit, durable lessons | rule |
| final synthesis and user-facing status | main |

When in doubt:

- development goes to dev
- validation goes to test
- durable process/spec review goes to rule
- main does not collapse roles
- use a serial queue for stability: no concurrent xz01 dev/test/rule execution unless explicitly re-enabled by the user
- split every assignment to the smallest practical unit before dispatch; do not use a larger `--max-turns` setting as the fix for long tasks
- prefer fixed validation scripts over ad-hoc validation commands
- do not enable a hard no-re-exploration prompt rule for now; the user explicitly paused that recommendation
- if a live xz01 page has a visible defect and the fix appears obvious, main still does not patch HTML/CSS/templates directly; main creates/dispatches the dev task and lets the dev→test→rule loop close it
- if a dev/test worker times out, do not treat timeout as either failure or success. First inspect the authorized workdir for changed timestamps, changed content, runtime state, and partial artifacts; if useful work landed, continue from that state with a smaller follow-up task, otherwise re-dispatch a narrower task. This avoids losing partial implementation work while still preserving independent validation.
- for small visual spacing defects, main should still use a constrained dev prompt with exact text anchors, allowed files/run dirs, and boundaries; after dev self-check, route to independent test for screenshot + AI review before reporting pass; if the user names a remaining sliver (e.g. above `游戏活动`), treat it as a new visible defect and repeat the loop rather than relying on the previous PASS
- if the user states a new hard xz01 rule that also describes an existing deployed/candidate template defect, do not perform a documentation-only update. Split it into (1) durable skill/spec update and (2) immediate template remediation in the authorized theme scope, followed by runtime clear and verification. The user explicitly corrected this after the pagination rule: “你只更新了规范, 没有处理模版!!!”

## Flow

Default flow:

```text
user → Hermes main → Claude dev → Hermes test
                              ↘ fail → dev fixes → test repeats
                               pass → Hermes rule → Hermes main → user
```

Main should preserve role separation even if a task is small.

## Reporting Format for This User

For Hermes-native xz01 workflow reports, do **not** use the old OpenClaw 10-column table unless the user explicitly asks for it. Use a concise xz01 report format instead:

```markdown
## xz01 执行报告｜<阶段/任务名>

**结论**：✅/⚠️/❌ 一句话状态

### 已完成
- ...

### 发现问题与处理
- 问题：...
- 处理：...

### 验证结果
- PC：...
- 移动端：...
- 静态检查：...
- AI视觉：...

### 产物
- 模板目录：...
- 报告：...
- 截图：MEDIA:/root/.hermes/...  （不要用 /www 的媒体路径直接给 WebUI）

### 下一步
- ...
```

Media artifact rule:
- Test artifacts may still be saved under `/www/wwwroot/www.900az.com` for website-side records.
- When sharing screenshots/files in Hermes WebUI, also copy them under `/root/.hermes/workspace/...` or another Hermes-allowed media location and reference that path with `MEDIA:/absolute/path`.
- Avoid sending `/www/...` paths as WebUI media links because the WebUI media API may return `403 Path not in allowed location`.

## Continuous Skill Improvement

Hermes should continuously improve this skill when actual workflow reveals gaps, but only within Hermes skill storage or another user-authorized non-OpenClaw location.

Patch this skill when:

- the user corrects role division
- a new hard boundary is stated
- a role's learning scope is missing material
- a recurring mistake appears
- a command/path/tool pattern is proven useful
- a previous instruction is stale or unsafe

Do not patch this skill for:

- one-off task progress
- temporary file paths
- transient PR/issue/session IDs
- anything likely to be stale within a week

### Mandatory publish-after-edit workflow

For this user's xz01 skill, editing local skill files is not complete. After any substantive xz01 skill update:

1. Update `SKILL.md` frontmatter `version` with a semver bump.
2. Synchronize `skill.json` `version` and `description` with the actual change.
3. Synchronize `_meta.json` `version`, `description`, and changelog/updated fields.
4. Audit that `SKILL.md`, `skill.json`, and `_meta.json` now contain the **same version** and that metadata descriptions/changelog describe the actual change; version drift is a blocking error.
5. Check that stale contradictory wording was removed from `SKILL.md` and relevant `references/*.md`.
6. Run `clawhub publish <skill-dir> --version <new-version> --changelog "<actual change>"` immediately; do not ask the user whether to publish.
7. Report the published version and returned publish ID.

Before finishing a complex task that changed the workflow, check whether this skill needs a patch and publish if it was changed.

## Common Pitfalls

1. **Treating `/root/.openclaw` as a writable config home.** It is read-only for this workflow unless explicitly authorized.
2. **Modifying PHP/controllers/config during template development.** This is forbidden. Do not patch `application/**/*.php`, `config/**/*.php`, routes, ThinkPHP core, models, services, or backend PHP to make a theme render. Use existing routes/template tags/data variables; otherwise report the limitation and keep work theme-only.
3. **Double-prefixing absolute URLs.** Helpers such as `cmf_url()` may already return an absolute URL. Normalize before prefixing; do not produce `https://www.900az.comhttps://...` or `https://m.900az.comhttps//...`.
4. **Putting the PC search box at the top center or making mobile search disappear.** The user explicitly forbids a PC top-center/header-center search box. Keep PC search in a right-side, below-header, or otherwise non-center placement and visually weaken it if needed. On mobile, the accepted replacement for a top full-width input is an obvious compact magnifier/icon-style visual entry; merely hiding/removing the big input without a visible small search affordance is only a partial fix.
5. **Letting Claude be both dev and test.** Dev/test must stay separate; if Claude is used for test, it must be a separate test instance.
6. **Only reading Markdown.** Scripts, JSON metadata, cron state, SQLite flow state, skill support files, and test tooling also encode rules.
7. **Skipping AI visual analysis.** Test screenshots are incomplete without AI visual review.
8. **Copying demo templates.** `demo_xz01` is a sample corpus, not an editable/copy target.
9. **Writing test artifacts under `/root/.openclaw`.** Treat `/root/.openclaw` as read-only; screenshots/reports should go under `/root/.hermes/workspace/...` for Hermes media or `/www/wwwroot/www.900az.com` for site-side records.
10. **Main doing hands-on QA or fixes.** Main supervises and reports; it does not implement or test. User explicitly corrected this after a PC homepage visual repair: even small/urgent HTML/CSS/ThinkPHP fixes must be delegated to Claude Code dev, then verified by an independent test role. Do not let speed become a reason for main to patch templates directly.
11. **Under-scoped Claude Code delegation.** When delegating implementation in print mode, include `Grep`/`Glob` if the task requires locating selectors/files; otherwise permission denials can burn turns and trigger `error_max_turns`. If that happens, resume the same Claude session with the missing tools allowed, or ask for a no-edit completion summary before moving to test.
12. **Starting direct Hermes xz01 work by calling OpenClaw runtime orchestration.** If the user is addressing Hermes and asks for xz01 live-site/template repair, do not call OpenClaw `sessions_send`, `flow-controller`, or OpenClaw role dispatch. Use Hermes-native `delegate_task`/Claude Code for dev and a separate Hermes-native test task. See `references/session-2026-05-18-hermes-native-title-search-repair.md`.
13. **Accepting a search title after testing only one keyword.** A title such as `王者荣耀_站点名` can be a hardcoded fallback or stale `$keyword`. Test multiple different keywords (for example `王者荣耀`, `和平精英`, `原神`) and ensure the title changes.
14. **Writing OpenClaw memories/skills/configs.** Durable updates for this Hermes workflow belong in Hermes skills/memory unless user authorizes otherwise.
15. **Fixing only one side of top navigation.** PC and m/mobile header nav are a paired xz01 requirement for every template set. Do not fix PC while leaving mobile hardcoded, or fix mobile while leaving PC hardcoded. Both rendered nav blocks must be parsed and verified from live PC and mobile domains.
16. **Hardcoding top navigation from guesses.** PC and mobile header nav must be rendered from existing menu/navigation data (`get_nav_menu` / `$vo.name` / `$vo.href` or equivalent). Do not invent labels or links such as PC “热门排行/装机必备/专题合集” or mobile “软件/排行/必备/资讯” because they look plausible or open successfully; parse the rendered top-nav block during validation to ensure it matches data-driven output. Use exact item matching, not broad substring checks, so valid labels like “应用软件” and “手游排行榜” are not mistaken for old guessed standalone labels. If similar labels remain in lower shortcut/keyword/sidebar modules, report them separately instead of treating them as header-nav failures.
17. **Under-scoping pagination to a few template filenames, static checks, missing common_data, or self-designed pagers.** The pagination rule applies to every dual-end, database-backed list page except ranking/rank-list pages, not just the first visible `list_soft/list_game/list_news/list_collection` files. Determine scope from `cmf_cms_channel` routes/list templates and rendered URLs. Non-ranking examples include `/zoszx/`, image/video/package/kaifu/all-news/search lists. PC must use numeric page links/page-code style output; mobile must use `上一页` / `下一页`. Rendering only page-one items is not acceptable when data exceeds one page. Seeing `$page_code|raw` or a pagination class in template source is not a complete PASS: if the bottom renders as empty `<ul class="pagination"></ul>`, check whether the template is missing the demo `common_data/_list_*_common.html` include or whether the main list uses `getAllData()` instead of `getPcPageData` / `getMobilePageData`. The repair is to restore the demo data chain, not to write a custom `request()->param`, `page_count`, `pager_i`, `ellipsis`, or disabled-prev/next pager in the theme. When the user explicitly says “照搬/造搬 xz01_demo”, do not reinterpret it as “make an equivalent feature”; preserve the demo's implementation shape unless a backend limitation is explicitly reported and approved.
18. **Rendering app/game/application resources as text-only rows.** For software, games, apps, rankings, latest resources, recommended resources, related resources, and sidebar resource modules, every item must include an icon/thumbnail/cover and be laid out as a card, icon grid, or image-text list. Do not use no-icon horizontal title-only rows for app/game/application resources. Text-only lists are acceptable only for news/articles/guides.
19. **Updating only the rule when the template is also wrong.** When the user says a new xz01 rule as “这是规范” and it points at a current template defect, do not stop after skill/spec/memory updates. Inspect and repair the affected template files in the authorized theme scope, clear runtime, and verify. The pagination correction is the reference example.
20. **Importing external Claude/agent frameworks wholesale.** When borrowing ideas from repositories such as Karpathy-style Claude guidelines or Everything Claude Code, adapt only the class-level principle that improves xz01 execution. Do not add generic security scanning, parallelization, or broad hook systems unless the user explicitly asks; encode useful hook ideas as xz01-specific gates that preserve dev/test/rule separation.
19. **Testing the wrong domain for mobile QA.** Mobile viewport emulation on `www.900az.com` can expose PC fixed-width containers such as `.xz-wrap` and produce false mobile failures. For xz01 mobile acceptance, navigate to `https://m.900az.com/...` with a real mobile UA and CDP mobile metrics. Validation scripts must carry separate URLs per test case; do not use one global PC URL for both PC and mobile cases. See `references/session-2026-05-18-mobile-domain-validation-correction.md`.
11. **Misreading visual-only search as deleting the search box.** When the user says dual-end/all front-end pages should not render search functionality, keep the search-box visual styling if the template design includes it, but disable behavior: no `/search` action/link, no enabled keyword input, no enabled submit button, no form submission, and no JS submit binding. Scan both PC and mobile for functional residues; then clear runtime and verify live PC/mobile URLs.
12. **Importing external Claude/agent frameworks wholesale.** When borrowing ideas from repositories such as Karpathy-style Claude guidelines or Everything Claude Code, adapt only the class-level principle that improves xz01 execution. Do not add generic security scanning, parallelization, or broad hook systems unless the user explicitly asks; encode useful hook ideas as xz01-specific gates that preserve dev/test/rule separation.

## Verification Checklist

Before reporting role orchestration status:

- [ ] `/root/.openclaw` treated as read-only
- [ ] main/dev/test/rule are distinct
- [ ] dev assigned to Claude Code by default
- [ ] test assigned to independent Hermes test role/session
- [ ] rule assigned to independent Hermes rule role/session
- [ ] each role has a clear learning scope
- [ ] no write/patch to OpenClaw directories occurred
- [ ] no PHP/backend/controller/model/config files were modified for a template-development task; allowed changes stayed within `public/themes/<theme>/**` unless the user explicitly authorized backend work
- [ ] task was split to the smallest practical unit; max-turns was not increased as the mitigation for long-running work
- [ ] xz01 execution used a strict serial queue with no concurrent dev/test/rule lanes unless the user explicitly re-enabled concurrency
- [ ] fixed validation scripts were used where applicable instead of ad-hoc repeated checks
- [ ] no hard no-re-exploration rule was added to prompts unless explicitly re-enabled by the user
- [ ] if this session introduced a new xz01 hard rule and the rule describes a current template defect, affected deployed/candidate templates were repaired in the authorized theme scope; the response did not stop at updating skill/spec documentation only
- [ ] every add/modify/delete development change was followed by clearing `/www/wwwroot/www.900az.com/runtime/` before validation
- [ ] static template validation was run with `xz01-template-static-scan.py` against the deployed/default theme or candidate theme
- [ ] PC/mobile URL crawl validation was run with `xz01-full-url-scan.py` or equivalent browser/curl scan before packaging; no existing DB route checked returns 500/ThinkPHP error
- [ ] PC/mobile homepage plus required software/game/news/category list pages and detail pages are generated/available and render correctly from existing DB routes before any package is created
- [ ] PC and m/mobile top navigation are both rendered from existing menu/navigation data (`get_nav_menu` / `$vo.name` / `$vo.href` or equivalent), not hardcoded guessed labels/links; rendered labels/hrefs are parsed from the actual top-nav containers on both live domains (for example `<nav class="xz-pc-nav">` and `<nav class="xz-m-nav">`) rather than from unrelated lower homepage shortcut/keyword modules; mobile hrefs use the `m.` host when appropriate
- [ ] category/list page display names match `cmf_cms_channel.name` for the current DB alias on both PC and mobile; e.g. alias `gzos` must display `手游下载` when the DB channel name is `手游下载`
- [ ] every dual-end database-backed list page except ranking/rank-list pages whose data volume exceeds one page renders pagination like `xz01_demo`: PC numeric page links/page-code output, mobile `上一页` / `下一页`; scope was derived from actual DB routes/list templates, not only `list_soft/list_game/list_news/list_collection`. Missing pagination on non-rank multi-page lists such as `/zoszx/`, image/video/package/kaifu/all-news/search lists is a validation failure even if page-one items render. Static source checks are insufficient, but implementation must remain demo-aligned: list templates include matching `common_data/_list_*_common.html`, common data calls `getPcPageData`/`getMobilePageData`, helpers generate `$page_code`, and templates output `{$page_code|raw}` or a verified demo-equivalent partial. Empty `<ul class="pagination"></ul>` is a data-chain failure only when the route has more than one page of eligible data; if the route currently has one page or insufficient data, report the empty output as expected demo behavior. No custom request-param/page-count/fallback pager algorithms are allowed.
- [ ] app/game/application resources on homepage/list/detail/sidebar/recommend/latest/rank modules are iconized: each item has an icon/thumbnail/cover plus title and metadata/action in a card, icon grid, or image-text list; no app/game/application resource appears as a no-icon text-only horizontal title row. News/article/guide text lists are checked separately and are not false positives.
- [ ] mobile visual/layout validation uses the real mobile domain (`https://m.900az.com/...`) with mobile UA/CDP metrics; testing `www.900az.com` at 390px is not accepted as mobile-site evidence unless explicitly requested
- [ ] rendered output passes xz01 hard gates: header/head jQuery loading present and not using `/common_cms/common/jquery.min.js`; UIkit and Swiper assets are included only when needed using the correct PC/mobile asset paths; column URLs that end with `/` are absolute with the correct PC/mobile host and are not double-prefixed; PC search is not top-center or visually dominant; mobile search, when shown, is an obvious compact magnifier/icon-style visual entry rather than a full-width top input or an invisible affordance; no `cms/page/index/id` links; no prohibited filler SVG data images; mobile no `target="_blank"`; and real data/detail links are present when DB records exist
- [ ] before packaging, PC+mobile relevant pages have static scan, curl/browser access, screenshots, and AI visual review results recorded
- [ ] when the requirement is “全部页面截图/AI复检”, every URL from the crawl result has a screenshot manifest entry, timeout pages are retried, contact sheets are generated for the full screenshot set, and every contact sheet is AI-reviewed
- [ ] if an xz01 skill/spec update was made, `SKILL.md`, `skill.json`, and `_meta.json` versions/descriptions/changelog were audited for sync before `clawhub publish`, and the publish ID was reported
- [ ] user-facing reply starts with the required 10-column table when applicable
