# SuperDoc Reference

This file contains key information from the superdoc repository's CLAUDE.md/AGENTS.md for future reference.

**Source:** https://github.com/superdoc-dev/superdoc
**Installation:** `npm install superdoc` (for projects) or `npm install @superdoc-dev/react` (for React)
**Version installed:** 1.17.0

## Key Architecture Points

### Rendering Pipeline

SuperDoc uses its own rendering pipeline — **ProseMirror is NOT used for visual output**.

```
PM Doc (hidden) → pm-adapter → FlowBlock[] → layout-engine → Layout[] → DomPainter → DOM
```

- `PresentationEditor` wraps a hidden ProseMirror `Editor` instance for document state and editing commands
- The hidden Editor's contenteditable DOM is never shown to the user
- **DomPainter** (`layout-engine/painters/dom/`) owns all visual rendering
- Style-resolved properties must flow through `pm-adapter` → DomPainter, not through PM decorations

### Where Visual Changes Go

| Change | Where |
|--------|-------|
| How something looks | `pm-adapter/` (data) + `painters/dom/` (rendering) |
| Style resolution | `style-engine/` |
| Editing behavior | `super-editor/src/extensions/` |

**Important:** Do NOT add ProseMirror decoration plugins for visual styling — DomPainter handles rendering.

## Project Structure

```
packages/
  superdoc/          Main entry point (npm: superdoc)
  react/             React wrapper (@superdoc-dev/react)
  super-editor/      ProseMirror editor (@superdoc/super-editor)
  layout-engine/     Layout & pagination pipeline
    contracts/       - Shared type definitions
    pm-adapter/      - ProseMirror → Layout bridge
    layout-engine/   - Pagination algorithms
    layout-bridge/   - Pipeline orchestration
    painters/dom/    - DOM rendering
    style-engine/    - OOXML style resolution
  ai/                AI integration
  collaboration-yjs/ Collaboration server
```

## Where to Look for Common Tasks

| Task | Location |
|------|----------|
| React integration | `packages/react/src/SuperDocEditor.tsx` |
| Editing features | `super-editor/src/extensions/` |
| Presentation mode visuals | `layout-engine/painters/dom/src/renderer.ts` |
| DOCX import/export | `super-editor/src/core/super-converter/` |
| Style resolution | `layout-engine/style-engine/` |
| Main entry point (Vue) | `superdoc/src/SuperDoc.vue` |
| Document API contract | `packages/document-api/src/contract/operation-definitions.ts` |

## Style Resolution Boundary

**The importer stores raw OOXML properties. The style-engine resolves them at render time.**

- The converter should only parse and store what is explicitly in the XML
- The style-engine is the single source of truth for cascade logic
- Both rendering systems call the style-engine to compute final visual properties

**Why**: Resolving styles during import bakes them into node attributes. On export, these get written as direct formatting instead of style references, losing the original document intent.

## Document API Contract

The `packages/document-api/` package uses a contract-first pattern:

- **`operation-definitions.ts`** — canonical object defining every operation
- **`operation-registry.ts`** — type-level registry mapping operations to types
- **`invoke.ts`** — `TypedDispatchTable` validates dispatch wiring at compile time

Do NOT hand-edit derived maps — they are generated from `OPERATION_DEFINITIONS`.

## JSDoc Types

Many packages use `.js` files with JSDoc `@typedef` for type definitions. These typedefs ARE the published type declarations.

- Keep JSDoc typedefs in sync with code
- Verify types after adding parameters
- Workspace packages don't publish types

## Commands

- `pnpm build` - Build all packages
- `pnpm test` - Run tests
- `pnpm dev` - Start dev server
- `pnpm run generate:all` - Generate all derived artifacts

## Testing

| What to verify | Command | Speed |
|---|---|---|
| Logic works? | `pnpm test` | seconds |
| Editing works? | `pnpm test:behavior` | minutes |
| Layout regressed? | `pnpm test:layout` | ~10 min |
| Pixel diff? | `pnpm test:visual` | ~5 min |

### Test Types

1. **Unit Tests (Vitest)** - Co-located with source code, test pure logic
2. **Behavior Tests (Playwright)** - End-to-end editing features through browser
3. **Layout Comparison** - Compares layout engine output across ~382 test documents
4. **Visual Comparison** - Pixel-level before/after comparison

## Brand & Design System

- Brand guidelines in `brand/`
- Token values in `packages/superdoc/src/assets/styles/tokens.css`
- Use `--sd-*` CSS custom properties, never hardcode hex values
- Product name is always **SuperDoc** (capital S, capital D)

## Installation Notes

- **Browser-first library**: Primarily designed for browser use
- **Headless usage**: Requires additional setup (see examples/headless/)
- **React wrapper**: Available as `@superdoc-dev/react`
- **License**: AGPLv3 for community use, commercial license available

## Verification

Installed successfully at:
- Global: `/usr/local/lib/node_modules/superdoc@1.17.0`
- Local test: `/tmp/superdoc-test/node_modules/superdoc@1.17.0`

Package structure verified with proper dist/ directory and package.json exports.
