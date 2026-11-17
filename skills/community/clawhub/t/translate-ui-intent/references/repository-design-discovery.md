# Repository Design Discovery

Use this reference in existing-product mode. Recover the active product language
before asking the user to redescribe it.

## Evidence Order

Inspect evidence in this order:

1. repository and module instructions
2. frontend manifests, framework configuration, and app entry points
3. documented design system, tokens, themes, and public component APIs
4. stories, examples, tests, and current component consumers
5. current screens with the closest user task and information structure
6. agent judgment only where repository evidence is silent

A screenshot reveals appearance but not necessarily component ownership,
semantics, responsive behavior, or accessibility. Confirm those in source when
possible.

## Discovery Map

Inspect only the surfaces relevant to the requested change:

| Surface | Evidence to find |
|---|---|
| App shell | navigation, page frame, content width, breadcrumbs, headers |
| Layout | grid, flex patterns, breakpoints, spacing scale, density |
| Typography | font family, type scale, weights, line height, truncation |
| Color and surfaces | semantic tokens, backgrounds, borders, elevation |
| Components | public APIs, variants, composition patterns, ownership |
| Inputs and actions | forms, validation, button hierarchy, destructive actions |
| Feedback | loading, empty, error, success, toast, inline status |
| Data display | tables, lists, cards, charts, filters, pagination |
| Icons and media | installed icon set, sizing, image treatment |
| Interaction | focus, hover, selection, disclosure, keyboard behavior, motion |
| Responsive behavior | supported viewports, reflow, collapse, overflow |
| Accessibility | labels, landmarks, contrast, focus order, reduced motion |
| Verification | stories, visual tests, component tests, E2E, dev commands |

Record files, components, routes, or rendered screens as evidence. Avoid vague
claims such as "the project seems to use cards."

## Identify the Active Convention

Do not copy the first matching implementation. Prefer a pattern when several of
these signals agree:

- it appears in the relevant product area
- it uses current public components and semantic tokens
- it is documented, tested, or represented in stories
- it is used by multiple maintained screens
- it fits the same user task and content shape
- it is not marked deprecated or bypassing the current system

When the repository is inconsistent, state the conflict and recommend the best
supported pattern. Do not silently average incompatible conventions.

## Reuse Decision

Use this table for material UI needs:

| UI need | Evidence | Existing candidate | Reuse action | Confidence | Deviation |
|---|---|---|---|---|---|

Apply these rules:

- Reuse semantics and behavior, not just visual similarity.
- Compose existing primitives before widening a shared API.
- Extend a shared component only when the new capability belongs to its contract
  and existing consumers remain compatible.
- Keep a one-off need local when making it shared would create speculative API.
- Use existing tokens even when a new local component is justified.
- Treat a new dependency or parallel design system as a last resort.
- Verify routes, action handlers, permissions, data contracts, and workflows
  separately; visual similarity is not evidence that business behavior exists.

## Greenfield Threshold

Enter greenfield mode only when no applicable repository or supplied-artifact
evidence exists. A missing exact component does not make the product greenfield
if its tokens, primitives, layouts, and interaction patterns are reusable.
