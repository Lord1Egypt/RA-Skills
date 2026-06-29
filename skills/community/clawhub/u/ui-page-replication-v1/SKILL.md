---
name: ui-page-replication-v1
description: High-fidelity UI page replication workflow for backend/admin systems. Use when Codex is asked to replicate, restore, clone, or second-develop an existing UI page with Playwright/browser collection, including prompts such as 复刻页面, 页面还原, UI还原, 后台系统复刻, playwright采集页面, 二开页面开发, 100%还原页面, and when all tabs, modals, forms, tables, mock data, API layer, TypeScript interfaces, and styling must be preserved or recreated.
---

# UI Page Replication V1

Use this skill for high-fidelity admin/backend UI replication from an existing browser page.

## Core Rules

- Replicate structure, layout, visual style, and behavior as completely as practical.
- Do not simplify visible UI elements, table columns, search fields, tabs, toolbars, modals, nested modals, upload controls, selectors, or linked interactions.
- Traverse every visible tab, dropdown path, modal, secondary modal, drawer, and collapsible area until no new UI nodes appear.
- Capture page snapshots, screenshots, console/network clues, colors, spacing, table fields, form fields, button states, pagination, and modal dimensions.
- Store Playwright artifacts under the project cache directory, preferably .playwright-mcp/artifacts/.
- Generate TypeScript interfaces for the replicated page data.
- Use mock data first, but preserve an API layer even when backed by mock implementations. Include semantic operations such as getList, getDetail, create, update, delete, submit, and audit when relevant.
- Match the host project framework and routing. When the source page uses Ant Design and high visual fidelity is required, prefer Ant Design components for the cloned page while keeping the host layout unchanged.

## Required Workflow

1. Inspect the host project framework, router, UI libraries, styling system, and existing page patterns.
2. Open the source page with Playwright/browser tooling. Capture a full-page screenshot and DOM/accessibility snapshot.
3. Map page regions: search/filter area, toolbar, stats, table/list, pagination, tabs, detail areas, forms, drawers, and other sections.
4. Traverse all tabs and interaction branches.
5. Open every modal/drawer/popover from toolbar and row actions. Recursively inspect nested interactions.
6. Extract form fields, validation requirements, disabled/read-only fields, units/suffixes, default values, and layout columns.
7. Extract table columns, widths when visible, row actions, selection behavior, pagination text, and empty/loading states.
8. Design TypeScript data models and mock data that reflect the source page.
9. Implement the page using the host project's route conventions and code style.
10. Add or preserve API-shaped functions for list/detail/create/update/delete/submit/audit semantics, even if they return mock data.
11. Recreate styles, spacing, colors, typography, control height, modal size, and responsive behavior.
12. Build and, when feasible, verify with Playwright screenshots.
13. Report implementation files, captured artifacts, behavior covered, and any known fidelity gaps.

## Reference Source

The original imported TypeScript skill files are preserved in references/source/. Read them only if you need the original config, prompt, schema, or utility code.

Important files:

- references/source/config.ts: trigger phrases and strict-mode flags.
- references/source/prompt.ts: original mandatory replication prompt.
- references/source/types.ts: page schema interfaces.
- references/source/pipeline.ts and index.ts: original lightweight execution wrapper.
