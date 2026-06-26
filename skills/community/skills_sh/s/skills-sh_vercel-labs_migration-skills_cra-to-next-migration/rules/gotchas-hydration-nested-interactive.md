---
title: Avoid Nested Interactive Elements
impact: HIGH
impactDescription: Button inside Link or anchor causes hydration errors
tags: gotchas, hydration, accessibility, html
---

## Avoid Nested Interactive Elements

Nesting interactive elements (button inside a link, link inside a button) causes hydration errors in Next.js. The browser's HTML parser corrects invalid nesting, creating a mismatch between server-rendered and client-rendered HTML.

**Problem: Button inside Link**

```tsx
// BAD - Causes hydration error
<Link href="/page">
  <button onClick={handleClick}>Click me</button>
</Link>
```

Error: `Hydration failed because the initial UI does not match what was rendered on the server`

This happens because `<a>` cannot contain `<button>` per HTML spec. The browser "fixes" the HTML differently than React expects.

**Solution 1: Style the Link as a button**

```tsx
// GOOD - Link styled to look like a button
<Link href="/page" className="btn btn-primary">
  Click me
</Link>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 500;
  cursor: pointer;
}
```

**Solution 2: Use asChild prop (Radix UI / Shadcn)**

If using Radix UI or Shadcn components:

```tsx
// GOOD - Button passes props to Link child
<Button asChild>
  <Link href="/page">Click me</Link>
</Button>
```

**Solution 3: Separate the actions**

If you need both navigation AND a click handler:

```tsx
// GOOD - Card is clickable, button is separate
function Card() {
  const router = useRouter();

  return (
    <div
      onClick={() => router.push('/page')}
      className="cursor-pointer"
      role="link"
      tabIndex={0}
    >
      <h3>Card Title</h3>
      <button
        onClick={(e) => {
          e.stopPropagation(); // Prevent card navigation
          handleAction();
        }}
      >
        Action
      </button>
    </div>
  );
}
```

**Solution 4: Use div with onClick for navigation**

```tsx
// GOOD - No nested interactive elements
function NavigableCard() {
  const router = useRouter();

  const handleClick = () => {
    router.push('/page');
  };

  const handleButtonClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    doSomething();
  };

  return (
    <div onClick={handleClick} className="card clickable">
      <span>Card content</span>
      <button onClick={handleButtonClick}>Action</button>
    </div>
  );
}
```

**Other invalid nesting patterns:**

```tsx
// BAD - All of these cause hydration errors
<a href="/page"><a href="/other">Nested link</a></a>
<button><button>Nested button</button></button>
<a href="/page"><button>Button in link</button></a>
<button><a href="/page">Link in button</a></button>

// Also invalid (form controls)
<label><label>Nested label</label></label>
<button><input type="text" /></button>
```

**Why this matters more in Next.js:**

In pure client-side React (CRA), the browser's HTML correction happens before React attaches. In Next.js with SSR, the server sends valid-looking HTML that the browser then "corrects," causing a mismatch when React hydrates.
