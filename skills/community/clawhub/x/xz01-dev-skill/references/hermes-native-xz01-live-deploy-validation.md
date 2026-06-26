# Hermes native xz01 live deployment and validation notes

Use this when the user asks to deploy a temporary xz01 template for live validation via:

- `https://www.900az.com/`
- `https://m.900az.com/`

## Key correction from the first live run

The prototype directory under `/root/.hermes/workspace/xz01-factory/runs/<run>/generated/` is safe for staging, but the user may explicitly want temporary template development to live under:

```text
/www/wwwroot/www.900az.com/public/themes/default/
```

When this happens, proceed directly but first make a timestamped backup of the current `default` theme.

## Safe live deployment sequence

1. Ensure generated source exists under the run directory.
2. Create backup:

```bash
BACKUP_DIR=/root/.hermes/workspace/xz01-factory/backups
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/default-before-<run_id>-$(date +%Y%m%d-%H%M%S).tar.gz" \
  -C /www/wwwroot/www.900az.com/public/themes default
```

3. Replace default theme:

```bash
rm -rf /www/wwwroot/www.900az.com/public/themes/default
mkdir -p /www/wwwroot/www.900az.com/public/themes/default
cp -a /root/.hermes/workspace/xz01-factory/runs/<run_id>/generated/public/themes/default/. \
  /www/wwwroot/www.900az.com/public/themes/default/
rm -rf /www/wwwroot/www.900az.com/runtime/*
```

4. Verify PC and mobile return HTTP 200.
5. Run PHP syntax checks on compiled runtime templates under `/www/wwwroot/www.900az.com/runtime/temp/*.php` after first render.
6. Run static checks:
   - mobile contains no `target="_blank"`
   - source templates contain no raw PHP tags
   - no `href="#"`
   - no `uk-cover`
   - no `limit="0"` / `getAllData({limit:0})`
   - CSS brace counts balanced
7. Use browser screenshots and AI vision on both URLs.
8. Save artifacts under:

```text
/www/wwwroot/www.900az.com/xz01-runs/screenshots/<run_id>/
/www/wwwroot/www.900az.com/xz01-runs/reports/
```

## Pitfalls found in run-0001

### Undefined template variables can cause 500

If the controller does not provide variables such as `$recommend_list`, `$latest_list`, `$rank_list`, `$category_list`, `$news_list`, or `$topic_list`, ThinkPHP may throw `未定义变量` during template compilation/rendering.

For live prototypes, wrap optional data blocks with `isset(...)` and provide static fallback content so the page can render before real DB binding exists:

```html
{if condition="isset($recommend_list)"}
  {foreach name="recommend_list" item="vo" key="key"}
  ...
  {/foreach}
{else/}
  <!-- static fallback cards for visual validation -->
{/if}
```

### Some `|default` forms may compile badly

Avoid complex `|default` expressions in live xz01 prototypes, especially inside `{:...}` expressions. Prefer explicit `isset(...) ? ... : ...` or static fallback blocks.

### ThinkPHP trace overlay can pollute screenshots

If debug trace is enabled, screenshots can show `#think_page_trace_open` with a small runtime number such as `0.070867s`. Hide it in temporary template CSS before visual validation:

```css
#think_page_trace,
#think_page_trace_open {
  display: none !important;
  visibility: hidden !important;
}
```

### Broken images are caught by AI vision

Static prototype references need actual files. If using fallback cards, create local placeholder assets under both PC and mobile `assets/images/` rather than relying on missing image paths. SVG placeholders are acceptable for temporary validation.

## First-run validated output shape

The first run successfully used:

```text
public/themes/default/
├── cms/index.html
├── mobile/index.html
└── common_cms/
    ├── common/_head.html
    ├── pc/_header.html
    ├── pc/_footer.html
    ├── pc/assets/css/style.css
    ├── pc/assets/js/style.js
    ├── pc/assets/images/*.svg
    ├── mobile/_header.html
    ├── mobile/_footer.html
    ├── mobile/assets/css/style.css
    ├── mobile/assets/js/style.js
    └── mobile/assets/images/*.svg
```

## Acceptance bar for a temporary homepage run

Minimum pass condition before reporting success:

- PC URL returns 200.
- Mobile URL returns 200.
- Compiled runtime PHP has no syntax errors.
- Browser console has no JS errors.
- PC screenshot AI check says no obvious layout overlap/missing content.
- Mobile screenshot AI check says no obvious layout overlap/missing content.
- AI confirms images display normally and trace overlay is not visible.
