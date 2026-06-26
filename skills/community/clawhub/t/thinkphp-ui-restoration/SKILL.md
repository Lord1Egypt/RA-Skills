---
name: thinkphp-ui-restoration
description: Generate and restore ThinkPHP UI components using this project's existing conventions. Use when the user asks to create or restore `.tpl` components, adapt screenshots/designs into existing ThinkPHP pages, or add matching CSS/mock data/controller bindings for this codebase.
---

# ThinkPHP UI Restoration

## Use When

- The user wants a new ThinkPHP `.tpl` component or page section.
- The user provides a screenshot, DOM, or reference UI to restore in this project.
- The task also needs matching CSS, mock data, or controller `View::assign` structure.

## Rules

1. Reuse existing project structure first: `view/@components`, `view/@pages`, `public/__base/css/common.css`, and current class naming patterns.
2. Follow ThinkPHP template syntax and safe field access, such as `{$e.xxx|default=''}` and `isset(...)` checks, to avoid undefined index errors.
3. When adding a component, also add the required CSS, mock fields, and controller/template wiring so it can render directly.
4. Prefer updating existing `xqbj-` components over creating a new pattern when the UI is only a variation of an existing block.
5. Put shared styles in `public/__base/css/common.css`; only use page-level CSS when the style is truly page-specific.
6. If the component depends on list data, also update the matching mock data in `app/BaseController.php` or the relevant controller.

## Workflow

1. Inspect nearby components and styles before creating new structure.
2. Decide whether to reuse, extend, or add a new component.
3. Implement the `.tpl` first, then matching CSS, then any mock/controller data needed.
4. Keep output visually consistent with the existing project, including spacing, truncation, image handling, and mobile behavior.

## Project Conventions

- Components usually live in `view/@components/` and are included from page templates.
- Page templates usually live in `view/@pages/`.
- Shared UI styles usually belong in `public/__base/css/common.css`.
- Mock lists and fallback fields are commonly assigned from `app/BaseController.php`.
- Use existing class prefixes such as `xqbj-component-`, `xqbj-list-`, and page-level wrappers already present nearby.

## Delivery Checklist

- `.tpl` structure matches nearby component style.
- CSS is added in the correct file and follows existing naming.
- Missing fields are guarded with `default` or conditional rendering.
- Long text has truncation rules when needed.
- Mobile layout is considered if the block appears in responsive pages.
- Required mock data or controller `View::assign` data is updated.

## Output Standard

- Prefer minimal edits over introducing new abstractions.
- Keep naming consistent with existing `xqbj-` / page-level patterns.
- If a field may be absent, provide a default or conditional render path.
- When restoring from a screenshot, match the existing project style rather than inventing a new design system.
