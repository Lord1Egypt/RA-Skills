# Session note: theme-only repair, absolute column links, PC search placement

## Context

After PHP/controller/config files were restored and the user permanently forbade backend changes for template development, a theme-only repair was needed for these issues:

1. PC homepage data disappeared after backend restoration.
2. Column links ending with `/` needed full protocol + host, with PC using `https://www.900az.com` and mobile using `https://m.900az.com`.
3. PC search box must never be placed at the top center.
4. A PC topic/detail URL and a mobile software detail URL errored.
5. A later regression discovered missing `cms/show_news.html` for a news detail URL.

## Durable rules

For xz01 template development:

1. Keep fixes theme-only: no PHP/controllers/models/config/routes/ThinkPHP/vendor changes.
2. If homepage/list/detail data disappears after backend restoration, repair templates using existing ThinkCMF template tags and variables (for example existing `getAllData` patterns), not backend code.
3. Every rendered column/category link whose path ends with `/` must be absolute with protocol and the correct host:
   - PC: `https://www.900az.com/.../`
   - Mobile: `https://m.900az.com/.../`
4. Avoid double-prefixing hosts. Before adding a host, account for template helpers such as `cmf_url()` possibly already returning an absolute URL.
   - Bad: `https://www.900az.comhttps://www.900az.com/yyalzos001/`
   - Bad: `https://m.900az.comhttps//m.900az.com/azos08/`
   - Good: `https://www.900az.com/yyalzos001/`
   - Good: `https://m.900az.com/azos08/`
5. PC search boxes must never be placed in the top-center/header-center position. Put them in a right-side header area, below-header area, or another non-center location appropriate to the design.
6. Detail rich text must render as HTML in templates; visible escaped tags such as `<p>`, `<h3>`, `<span ...>` or `&lt;p&gt;` are validation failures.
7. Missing detail templates such as `cms/show_news.html` should be fixed by adding/adapting the theme template, not by changing controllers.
8. Test artifacts must not be written under `/root/.openclaw`; use `/root/.hermes/workspace/...` or `/www/wwwroot/www.900az.com` as appropriate.

## Verification pattern

Before packaging or reporting pass:

- Run a backend PHP baseline check if one exists (`sha256sum -c guards/php-backend-baseline-before-theme-repair.sha256`) and require all OK.
- Compare live theme and generated theme directories for no drift.
- Clear `/www/wwwroot/www.900az.com/runtime` after each theme change before validation.
- Check representative PC and mobile pages for:
  - HTTP 200 and no `系统发生错误`, trace, or `TemplateNotFound`.
  - Homepage/list/detail real data and real images.
  - No duplicate-host malformed links.
  - PC absolute slash-ending category links use `https://www.900az.com`.
  - Mobile absolute slash-ending category links use `https://m.900az.com`.
  - PC search is not top-center.
  - Mobile has no `target="_blank"` and no horizontal overflow.
  - Rich text does not expose HTML tags as text.
