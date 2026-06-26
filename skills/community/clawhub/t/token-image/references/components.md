# Component & Layout Reference

Layout patterns and component snippets for social/marketing images. Each pattern shows the **CSS class** (what the shared agent adds to `styles.css`) and the **TSX usage** (what the writer writes).

The shared agent reads this file alongside the content plan to determine which CSS classes to create. Writers read this file to understand pattern conventions, then use the actual classes from `styles.css`.

All CSS values reference token vars (e.g., `var(--spacing-md)`, `var(--color-surface)`). The `tokens` prop provides CSS var references in TSX (e.g., `tokens.spacing.md` → `var(--spacing-md)`).

**Heading spacing:** All headings have `margin: 0`. Spacing between elements is handled by flex/grid `gap` (viewport inner div, `.content-stack`, `.numbered-list`, etc.). Do not add `margin-top` or `margin-bottom` to headings — let the gap handle it.

**Viewport children:** The viewport's inner container is a flex column with `gap`. Pass **multiple direct children** (heading, layout block, metadata) so the gap works. Do NOT wrap everything in a single div — that collapses the gap to zero. If a single wrapper is truly needed, replicate the viewport's flex related props: `flex`, `flexDirection`, `justifyContent`, `alignItems` and etc.

---

## Layout Patterns

### Hero / Full Canvas

Title-only or title + tagline. No body content. Uses viewport hero variant for positioning.

No special CSS class needed — the viewport hero variant handles layout.

```tsx
<Viewport tokens={tokens} variant="hero">
  <h1 className="display">{TITLE}</h1>
  <h3>{TAGLINE}</h3>
</Viewport>
```

Use when: single bold statement, set title card, brand splash.

---

### Single Column

Title, optional subtitle, body text. Simple informational layout.

No special CSS class needed — semantic HTML + base stylesheet handles it.

```tsx
<Viewport tokens={tokens} variant="standard">
  <h1>{TITLE}</h1>
  <h3>{SUBTITLE}</h3>
  <p>{BODY}</p>
  <p className="metadata">{METADATA}</p>
</Viewport>
```

Use when: announcements, quotes, simple info. Add `maxWidth` via inline style if lines get too wide.

---

### Split (Equal)

Two equal columns. Content on either or both sides.

**CSS:**

```css
.split {
  display: flex;
  gap: var(--spacing-xl);
}
.split > * {
  flex: 1;
}
```

**TSX:**

```tsx
<div className="split">
  <div>
    <h2>{TITLE}</h2>
    <h3>{SUBTITLE}</h3>
    <p style={{ marginTop: tokens.spacing.md }}>{BODY}</p>
  </div>
  <div>
    {/* right panel content */}
  </div>
</div>
```

Use when: content naturally divides into two zones. Both sides should have real content — avoid leaving one side empty.

---

### Split (Asymmetric)

Two columns with unequal widths. Heavier content gets more space.

**CSS:**

```css
.split-60-40 {
  display: flex;
  gap: var(--spacing-xl);
}
.split-60-40 > :first-child {
  flex: 3;
}
.split-60-40 > :last-child {
  flex: 2;
}

.split-40-60 {
  display: flex;
  gap: var(--spacing-xl);
}
.split-40-60 > :first-child {
  flex: 2;
}
.split-40-60 > :last-child {
  flex: 3;
}
```

**TSX:**

```tsx
<div className="split-60-40">
  <div>
    <h2>{TITLE}</h2>
    <p style={{ marginTop: tokens.spacing.md }}>{BODY}</p>
  </div>
  <div className="grid-2">
    {/* 2x2 card grid in the narrower panel */}
    <div className="card">...</div>
    <div className="card">...</div>
    <div className="card">...</div>
    <div className="card">...</div>
  </div>
</div>
```

Use when: one side has significantly more content than the other, or you want visual weight difference.

---

### Title Above Content

Title spanning full width at top, content below. Content can be a grid, list, split, or any layout.

**CSS:**

```css
.content-stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}
```

**TSX with grid:**

```tsx
<div className="content-stack">
  <h1>{TITLE}</h1>
  <div className="grid-2">
    <div className="card">
      <span className="card-label">LABEL</span>
      <p className="card-content">Content text</p>
    </div>
    {/* more cards... */}
  </div>
</div>
```

**TSX with split below:**

```tsx
<div className="content-stack">
  <h1>{TITLE}</h1>
  <div className="split">
    <div>
      <h3>{SUBTITLE}</h3>
      <p style={{ marginTop: tokens.spacing.sm }}>{BODY}</p>
    </div>
    <div className="grid-2">
      {/* cards */}
    </div>
  </div>
</div>
```

Use when: title needs to span the full width but content below is two-column or gridded. This is the most common pattern for mixing layouts.

---

### Numbered List

Numbered steps or items with visual numbering. Good for processes, top-N lists, how-tos.

**CSS:**

```css
.numbered-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}
.numbered-item {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-start;
}
.numbered-num {
  font-family: var(--font-family-mono);
  color: var(--color-accent);
  font-size: var(--font-size-h3);
  flex-shrink: 0;
}
```

**TSX:**

```tsx
<h2>{TITLE}</h2>
<div className="numbered-list">
  <div className="numbered-item">
    <span className="numbered-num">01</span>
    <div>
      <span className="card-label">LABEL</span>
      <p className="card-content" style={{ marginTop: tokens.spacing.xs }}>Description text</p>
    </div>
  </div>
  {/* more items... */}
</div>
```

Use when: sequential steps, ranked items, process descriptions.

---

### Content Row

Horizontal strip of items. Good for stats, feature highlights, compact info.

**CSS:**

```css
.content-row {
  display: flex;
  gap: var(--spacing-md);
}
.content-row > * {
  flex: 1;
}
```

**TSX:**

```tsx
<div className="content-row">
  <div className="card">
    <span className="card-label">METRIC</span>
    <p className="display" style={{ fontSize: tokens.fontSize.h2 }}>99%</p>
  </div>
  <div className="card">
    <span className="card-label">USERS</span>
    <p className="display" style={{ fontSize: tokens.fontSize.h2 }}>10K</p>
  </div>
  <div className="card">
    <span className="card-label">UPTIME</span>
    <p className="display" style={{ fontSize: tokens.fontSize.h2 }}>24/7</p>
  </div>
</div>
```

Use when: 3-5 parallel items that should read left-to-right.

---

### Freeform

Custom layout not covered by other patterns. Uses inline styles for unique positioning.

No CSS class — inline styles only.

```tsx
<Viewport tokens={tokens} variant="standard">
  <div style={{
    display: "grid",
    gridTemplateColumns: "1fr 2fr 1fr",
    gridTemplateRows: "1fr 1fr",
    gap: tokens.spacing.md,
    flex: 1,
  }}>
    <div className="card" style={{ gridColumn: "1 / 3" }}>...</div>
    <div className="card">...</div>
    <div className="card">...</div>
    <div className="card">...</div>
  </div>
</Viewport>
```

Use when: nothing else fits. The layout description in the brief will specify what's needed.

---

## Component Patterns

### Card (basic)

```tsx
<div className="card">
  <p>Card content text here</p>
</div>
```

### Card with label + content

```tsx
<div className="card" style={{ display: "flex", flexDirection: "column", gap: tokens.spacing.xs }}>
  <span className="card-label">LABEL</span>
  <p className="card-content">Description text</p>
</div>
```

### Grid (2-column, 3-column)

```tsx
<div className="grid-2">
  {/* 2, 3, or 4 cards — uneven last row is fine */}
</div>

<div className="grid-3">
  {/* 3, 4, 5, or 6 cards — uneven last row is fine */}
</div>
```

Grid classes (`.grid-2`, `.grid-3`) are in the base stylesheet. Uneven last rows are fine.

### Code Block

```tsx
<pre><code>{`const [state, setState] = useState(initialValue)`}</code></pre>
```

### Metadata Bar

```tsx
<p className="metadata">SERIES NAME · PART 1</p>
```

### Dot-grid Background Pattern

Apply to a container div. NOT a standalone element.

```tsx
<div style={{
  backgroundImage: `radial-gradient(circle, ${tokens.color.border} 1px, transparent 1px)`,
  backgroundSize: "16px 16px",
  opacity: tokens.opacity.subtle,
}} />
```

---

## Full Component Example

```tsx
// @size 1200x600
import React from "react";
import Viewport from "./viewport";
import "./styles.css";

const TITLE = "React Hooks";
const SUBTITLE = "Understanding the fundamentals";
const METADATA = "REACT SERIES · PART 1";

export default function Component({ tokens }: { tokens: Record<string, any> }) {
  return (
    <Viewport tokens={tokens} variant="standard">
      <div className="content-stack">
        <h1 className="display">{TITLE}</h1>
        <div className="split-60-40">
          <div>
            <h3>{SUBTITLE}</h3>
            <p style={{ marginTop: tokens.spacing.md }}>
              Hooks let you use state and other features in function components.
            </p>
          </div>
          <div className="grid-2">
            <div className="card">
              <span className="card-label">STATE</span>
              <p className="card-content">useState for local state</p>
            </div>
            <div className="card">
              <span className="card-label">EFFECT</span>
              <p className="card-content">useEffect for side effects</p>
            </div>
            <div className="card">
              <span className="card-label">CONTEXT</span>
              <p className="card-content">useContext for shared data</p>
            </div>
            <div className="card">
              <span className="card-label">CUSTOM</span>
              <p className="card-content">Build reusable logic</p>
            </div>
          </div>
        </div>
      </div>
      <p className="metadata">{METADATA}</p>
    </Viewport>
  );
}
```
