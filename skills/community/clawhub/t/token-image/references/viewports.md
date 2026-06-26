# Viewport Reference

The viewport is a single component wrapping every image. It provides the root container, content alignment, and branding slots.

Save as `.img-gen/src/viewport.tsx`. The `{width}` and `{height}` placeholders are replaced with actual format dimensions when the shared-files agent generates the viewport.

---

## Core Component

Two-layer structure: **outer wrapper** (dimensions, bg, padding, hero pattern) and **inner content area** (alignment, holds children). The agent layers branding elements between or around these two layers.

Props: `{ tokens, children, variant }` where `variant` is `"standard"` (default) or `"hero"`.

The viewport is opinionated about alignment — each variant has its own default. The agent hardcodes the alignment into the inner content div based on guidance below.

```tsx
// @viewport {width}x{height}
import React from "react";

export default function Viewport({
  tokens,
  children,
  variant = "standard",
}: {
  tokens: Record<string, any>;
  children: React.ReactNode;
  variant?: "standard" | "hero";
}) {
  return (
    <div
      style={{
        width: {width},
        height: {height},
        backgroundColor: tokens.color.bg,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        padding: tokens.spacing.xl,
        boxSizing: "border-box",
      }}
    >
      {/* -- branding slots go here (before inner div) -- */}

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          overflow: "hidden",
          gap: tokens.spacing.md,
          overflow: "visible",
          /* paddingTop when branding above, paddingBottom when branding below */
          /* alignment hardcoded here — see guidance below */
        }}
      >
        {children}
      </div>

      {/* -- branding slots go here (after inner div) -- */}
    </div>
  );
}
```

### Inner Wrapper Padding

The inner content div needs padding to create breathing room between content and adjacent branding elements:

- `paddingTop: tokens.spacing.md` — **required** when a branding element sits above the inner div (header bar, four-corners top row)
- `paddingBottom: tokens.spacing.md` — **required** when a branding element sits below the inner div (footer bar, four-corners bottom row)
- No padding needed on a side that has no adjacent branding

### Alignment Guidance

**Standard** — content fills the available space. The inner div uses `alignItems: "stretch"` by default, which lets child elements (grids, stacks, split layouts) expand naturally to fill the width. For centered content, switch to `justifyContent: "center", alignItems: "center"`. For top-anchored content (e.g. a list that shouldn't float), use `justifyContent: "flex-start", alignItems: "stretch"`.

**Hero** — content needs a deliberate position. Pick one:
- `justifyContent: "flex-end", alignItems: "flex-start"` — poster, content bottom-left
- `justifyContent: "flex-end", alignItems: "flex-end"` — cinematic, content bottom-right
- `justifyContent: "center", alignItems: "center"` — billboard, content dead center
- `justifyContent: "center", alignItems: "flex-start"` — editorial, content left-center

Bottom corners work best for dominant headings. Center for short single-line text. Left-center for content-heavy hero layouts that still need room to breathe.

Background patterns for hero variant come from the preset's design guide. Apply them to the outer wrapper's `backgroundImage` + `backgroundSize`.

---

## Branding Snippets

Each snippet is self-contained. Drop them into the outer wrapper before or after the inner content div. Combine as needed — the content brief dictates which ones to use.

### Four Corners (flex)

Two flex rows with `justify-content: space-between`. Place **before** inner div for top row, **after** for bottom row. Adapt to 1-3 corners by leaving slots empty.

**Top pair** (place before inner div):

```tsx
<div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
  <p className="metadata">SERIES NAME</p>
  <p className="metadata">EP 01</p>
</div>
```

**Bottom pair** (place after inner div):

```tsx
<div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
  <p className="metadata">@author</p>
  <p className="metadata">2025</p>
</div>
```

Use 1-3 corners by removing items or replacing with empty spans. The `justify-content: space-between` keeps remaining items pinned to their edges.

---

### Header Bar

Full-width strip at the top. Place **before** inner div. Add a border or separator if the design guide calls for it.

```tsx
<div style={{
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  width: "100%",
  paddingBottom: tokens.spacing.sm,
  borderBottom: `1px solid ${tokens.color.border}`,
  marginBottom: tokens.spacing.md,
}}>
  <p className="metadata">SERIES NAME</p>
  <p className="metadata">EP 01 / 12</p>
</div>
```

---

### Footer Bar

Full-width strip at the bottom. Place **after** inner div. Mirrors header bar structure.

```tsx
<div style={{
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  width: "100%",
  paddingTop: tokens.spacing.sm,
  borderTop: `1px solid ${tokens.color.border}`,
  marginTop: tokens.spacing.md,
}}>
  <p className="metadata">@author</p>
  <p className="metadata">website.com</p>
</div>
```

---

### Edge Label

Thin vertical text running along one edge of the viewport. Uses `position: absolute` on the outer wrapper. Works well for series labels, version numbers, or side metadata.

```tsx
<p
  className="metadata"
  style={{
    position: "absolute",
    left: tokens.spacing.md,
    top: "50%",
    transform: "rotate(-90deg) translateX(-50%)",
    transformOrigin: "left center",
    whiteSpace: "nowrap",
  }}
>
  SERIES NAME · EP 01
</p>
```

Swap `left` for `right` (and use `transformOrigin: "right center"`) for the opposite edge.

---

### Watermark

Centered behind the content, low opacity. Place inside the outer wrapper using `position: absolute` + `inset: 0` with `pointerEvents: "none"`.

```tsx
<div style={{
  position: "absolute",
  inset: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  pointerEvents: "none",
  opacity: tokens.opacity.subtle,
}}>
  <span style={{
    fontFamily: tokens.fontFamily.display,
    fontSize: tokens.fontSize.hero,
    color: tokens.color.border,
    fontWeight: tokens.fontWeight.bold,
  }}>
    BRAND
  </span>
</div>
```

---

## Usage Examples

### Footer Bar (standard + hero)

```tsx
// @viewport {width}x{height}
import React from "react";

export default function Viewport({
  tokens,
  children,
  variant = "standard",
}: {
  tokens: Record<string, any>;
  children: React.ReactNode;
  variant?: "standard" | "hero";
}) {
  const isHero = variant === "hero";
  return (
    <div
      style={{
        width: {width},
        height: {height},
        backgroundColor: tokens.color.bg,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        padding: tokens.spacing.xl,
        boxSizing: "border-box",
        backgroundImage: isHero ? `radial-gradient(circle, ${tokens.color.border} 1px, transparent 1px)` : undefined,
        backgroundSize: isHero ? "24px 24px" : undefined,
      }}
    >
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          overflow: "hidden",
          gap: tokens.spacing.md,
          overflow: "visible",
          paddingBottom: tokens.spacing.md,
          justifyContent: isHero ? "flex-end" : "center",
          alignItems: isHero ? "flex-start" : "stretch",
        }}
      >
        {children}
      </div>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        width: "100%",
        paddingTop: tokens.spacing.sm,
        borderTop: `1px solid ${tokens.color.border}`,
      }}>
        <p className="metadata">REACT SERIES</p>
        <p className="metadata">@author</p>
      </div>
    </div>
  );
}
```

### Four Corners (standard + hero)

```tsx
// @viewport {width}x{height}
import React from "react";

export default function Viewport({
  tokens,
  children,
  variant = "standard",
}: {
  tokens: Record<string, any>;
  children: React.ReactNode;
  variant?: "standard" | "hero";
}) {
  const isHero = variant === "hero";
  return (
    <div
      style={{
        width: {width},
        height: {height},
        backgroundColor: tokens.color.bg,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        padding: tokens.spacing.xl,
        boxSizing: "border-box",
        backgroundImage: isHero ? `radial-gradient(circle, ${tokens.color.border} 1px, transparent 1px)` : undefined,
        backgroundSize: isHero ? "24px 24px" : undefined,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
        <p className="metadata">SERIES NAME</p>
        <p className="metadata">EP 01</p>
      </div>
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          overflow: "hidden",
          gap: tokens.spacing.md,
          overflow: "visible",
          paddingTop: tokens.spacing.md,
          paddingBottom: tokens.spacing.md,
          justifyContent: isHero ? "flex-end" : "center",
          alignItems: isHero ? "flex-start" : "stretch",
        }}
      >
        {children}
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
        <p className="metadata">@author</p>
        <p className="metadata">2025</p>
      </div>
    </div>
  );
}
```

---

## Customization Guide

When creating the viewport for a set:

1. **Set alignment** — hardcode the inner div's `justifyContent` and `alignItems` based on the variant guidance above. No prop — the viewport is opinionated.
2. **Select branding** — pick 1-2 branding patterns from the snippets above based on what the content brief needs. Can combine (e.g., header bar + edge label).
3. **Background pattern** (hero only) — use the pattern from the preset's design guide, applied to the outer wrapper
4. **Inner wrapper padding** — add `paddingTop: tokens.spacing.md` when branding sits above the inner div, `paddingBottom: tokens.spacing.md` when branding sits below. No padding on sides without branding.
5. **Outer padding** — adjust if the preset design guide specifies different safe areas (e.g., `tokens.spacing.2xl` for square formats)
6. **Compose** — the shared-files agent combines core structure + chosen snippets into a single viewport component

### Inner content gap

The inner content div uses `gap: tokens.spacing.md` (16px) to provide consistent vertical spacing between direct children. This is the primary spacing mechanism between top-level content blocks — Writers should not add manual margin/padding between their main sections. Headings get additional bottom margin from the stylesheet (see `default-styles.css`) to create visual hierarchy. Writers can still add `gap` on their own inner flex/grid containers for fine-grained layout spacing.
