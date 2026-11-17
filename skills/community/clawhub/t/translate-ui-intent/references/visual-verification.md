# Visual Verification

Use rendering and interaction evidence to determine whether the implementation
matches the UI Intent Contract and the surrounding product.

## Build the Evidence Matrix

Select representative combinations rather than every possible screenshot:

| Surface | Viewport | State | Interaction | Why material |
|---|---|---|---|---|

Include:

- the primary supported desktop or wide viewport
- the primary narrow or mobile viewport when responsive behavior is in scope
- material loading, empty, error, permission, or success states
- long labels, long values, sparse content, or dense content where they can
  change layout
- hover, focus, selection, disclosure, validation, or destructive confirmation
  when interaction feedback is material

Use repository-supported breakpoints and fixtures when available. Do not invent
device coverage unrelated to the product.

## Execute

1. Discover and run the repository's actual install, build, test, and dev
   commands. Do not guess command names.
2. Check the browser console and failed network requests before trusting the
   rendered result.
3. Capture stable screenshots for the evidence matrix.
4. Exercise material interactions; a static screenshot cannot prove behavior.
5. Compare against the contract and adjacent maintained screens.

If deterministic state setup is unavailable, report the missing state as a
verification gap rather than pretending the happy path covers it.

## Review Criteria

Check:

- **Task hierarchy:** the primary information and action win attention in the
  intended order.
- **Product consistency:** shell, components, icons, tokens, and feedback match
  active repository patterns.
- **Layout integrity:** alignment, spacing rhythm, containment, and fixed-format
  dimensions remain stable.
- **Content resilience:** text wraps or truncates intentionally; content does
  not overlap, clip, or shift controls unexpectedly.
- **Responsive behavior:** regions reflow, collapse, scroll, or reprioritize as
  specified.
- **Interaction clarity:** affordances, focus, selection, progress, success,
  error, and recovery are perceivable.
- **Accessibility:** semantics, keyboard flow, contrast, non-color cues, and
  reduced motion match the contract.

Separate observations from judgments:

```text
Observed: the primary action moves below the fold at the narrow viewport.
Contract: the primary action remains available without scrolling.
Judgment: the implementation does not satisfy the responsive hierarchy.
```

## Iterate

For each mismatch:

1. identify the violated intent or inherited convention
2. choose the smallest design or implementation correction
3. rerun the affected behavioral check
4. recapture the relevant state and viewport
5. retain any unresolved difference as explicit residual uncertainty

Do not claim "pixel perfect" without an authoritative reference and a defined
comparison method. Do not claim visual consistency when rendering was blocked.
