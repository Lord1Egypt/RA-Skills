# Session 2026-05-18 — Hermes-native visual-only search handling

## Trigger

User clarified that `https://www.900az.com/` should keep dual-end search-box visual styling, but must not render functional search behavior. The previous interpretation “remove the search box entirely” was wrong.

User also corrected the workflow: when they address Hermes directly, do not invoke OpenClaw sessions, OpenClaw `flow-controller`, or OpenClaw role dispatch. Use Hermes-native tools/workers only.

## Durable lesson

For xz01 live-site/front-end regressions in Hermes:

1. Treat OpenClaw runtime orchestration as reference-only unless the user explicitly asks to use it.
2. Use Hermes-native verification and worker delegation instead of `sessions_send` / `flow-controller`.
3. If the user says dual-end/all front-end pages must not render search functionality, keep search-box visuals when the template design includes them, but disable all behavior:
   - no `/search` link/action
   - no enabled keyword input
   - no enabled submit button
   - no form submission
   - no JS submit binding
   - use visual-only disabled/non-focusable controls such as `disabled`, `tabindex="-1"`, `aria-disabled="true"`, `inert`, and/or `pointer-events:none`.
4. Check both rendered HTML and theme templates/assets for functional residues:
   - `xz-search`
   - `xz-m-search`
   - `xz-m-search-btn`
   - `<form` / `</form>` when it can submit search
   - enabled `placeholder=` search inputs
   - `name="keyword"`
   - `/search`, `Search/index`, `cms/Search/index`, `mobile/Search/index`
   - clickable/enabled labels/buttons such as `搜索`, `查找`, `搜索软件`, `搜索你想下载`
5. The root cause pattern to inspect is common header includes:
   - PC: `common_cms/pc/_header.html`
   - mobile: `common_cms/mobile/_header.html`
   These propagate search boxes and any accidental functionality to homepage/list/detail pages.
6. Clean up or disable coupled frontend behavior as well as markup:
   - PC/mobile header templates
   - PC/mobile JS submit listeners
   - PC/mobile CSS selectors must style visual-only search without enabling pointer interaction
7. Clear `/www/wwwroot/www.900az.com/runtime/` after any theme change before verifying live output.
8. Independently re-verify representative PC/mobile URLs after repair using a rendered HTML scan and, when needed, browser snapshots.

## Boundary

Theme-only repair still applies: modify only `public/themes/<theme>/**` unless the user explicitly authorizes backend work. Do not change PHP controllers/models/config/routes/vendor to make this pass.

## Example verification pattern

Representative URL set:

```text
https://www.900az.com/
https://www.900az.com/azos/
https://www.900az.com/gzos/
https://www.900az.com/zoszx/
https://m.900az.com/
https://m.900az.com/azos/
https://m.900az.com/gzos/
https://m.900az.com/zoszx/
```

Expected result for the visual-only search scan:

```text
visual=True forbidden_function=False disabled_controls=True
```
