# Session 2026-05-18 — Hermes-native xz01 title/search repair

## Trigger

User reported that `https://www.900az.com/` dual-end titles were not following `xz01_demo`, then explicitly corrected the assistant: **“你是 hermes, 不要去调用 openclaw”**.

## Durable workflow lesson

For direct Hermes xz01 live-site/template tasks, do **not** start with OpenClaw `sessions_send`, `flow-controller`, or OpenClaw role dispatch. Use Hermes-native execution instead:

1. Load `xz01-dev-skill`.
2. Treat `/root/.openclaw/**` and `demo_xz01` as read-only reference only.
3. Use Hermes-native role separation:
   - dev: `delegate_task` or Claude Code, limited to theme files.
   - test: independent `delegate_task`, no code edits.
4. Keep writes within `/www/wwwroot/www.900az.com/public/themes/default/**` for live theme repair unless the user authorizes another path.
5. Never modify backend/PHP/controller/model/config/route/vendor/thinkphp for template tasks.
6. Clear `/www/wwwroot/www.900az.com/runtime/` after every theme change.
7. Re-test via HTTP/title/static checks before reporting completion.

## Concrete title repair pattern

Problem: production common head only used `$seo_title`/`site_name`, so many pages collapsed to the same site title.

Effective fix class:

- Put title construction in the shared head include used by both PC and mobile.
- Follow demo-style dynamic precedence:
  - detail: `article.seo_title` first, otherwise article/download title + site name.
  - category/list: `category.seo_title` first, otherwise category name + site name.
  - search: request keyword + site name; no keyword should be a neutral search title, not a hardcoded game name.
  - tag/page/home: appropriate tag/page/site SEO fallback.
- Output a single `<title>{$title}</title>` from the common head.

## Search route repair pattern

During testing, `/search` was an existing visible route but returned 500 `TemplateNotFoundException` because the theme lacked search templates. Since the route already existed, this was not route creation and was valid theme-only repair.

Effective fix class:

- Add/fix only theme templates such as:
  - `public/themes/default/cms/search.html`
  - `public/themes/default/mobile/search.html`
- Include the existing PC/mobile header so the shared head/title logic is used.
- Prepare `$keyword` before including the header/head.
- Read common request parameter aliases in theme scope: `keyword`, `keywords`, `key`, `wd`, `q`.
- If no keyword is supplied, use a neutral display/title such as `搜索_站点名`; do not hardcode `王者荣耀` or any other sample query.

## Validation pattern

A good final test for this class does not require screenshots; it should verify titles and HTTP status:

- PC and mobile `/search` return 200 and are not `系统发生错误`.
- PC and mobile `/search?keyword=王者荣耀`, `/search?keyword=和平精英`, `/search?keyword=原神` produce distinct keyword-specific titles.
- Sample at least 8 PC and 8 mobile URLs across home, category/list, detail, article, and search.
- Fail if any title is empty, all titles collapse to the same value, template variables remain unresolved, or ThinkPHP/Fatal/Exception text appears.

## Pitfall

Do not treat a search page title that happens to show `王者荣耀_站点名` as valid unless a different keyword changes the title. Test at least two different keywords to catch hardcoded or stale `$keyword` values.
