# Customization — React Spinner

## Table of Contents
- [Overview](#overview)
- [CSS Class Customization (cssClass)](#css-class-customization-cssclass)
- [Custom Size via width](#custom-size-via-width)
- [Custom Template](#custom-template)
- [Global Customization with setSpinner](#global-customization-with-setspinner)
- [Spinner Color via CSS](#spinner-color-via-css)
- [Positioning the Spinner Label](#positioning-the-spinner-label)
- [Overlay Backdrop Customization](#overlay-backdrop-customization)
- [Theme-Specific Customization](#theme-specific-customization)
- [Responsive Spinner](#responsive-spinner)

---

## Overview

The Spinner supports customization through:
1. `cssClass` — adds CSS class(es) to the spinner root for styling hooks
2. `width` — controls the size of the spinner icon
3. `template` — replaces the default animation with custom HTML
4. `setSpinner` — applies customizations globally across all spinners

---

## CSS Class Customization (cssClass)

Add custom class names to the spinner wrapper element:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function CustomClassSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        cssClass: 'dark-bg-spinner'
      });
      showSpinner(ref.current);
    }
  }, []);

  return <div ref={ref} style={{ height: '200px', background: '#1e1e2e' }} />;
}
```

**CSS (App.css):**

```css
/* Style the spinner overlay when dark-bg-spinner class is present */
.dark-bg-spinner .e-spinner-pane {
  background-color: rgba(0, 0, 0, 0.6);
}

.dark-bg-spinner .e-spinner-inner .e-spin-material {
  stroke: #ffffff;
}
```

**Multiple classes:**

```tsx
createSpinner({
  target: el,
  cssClass: 'overlay-dark compact-spinner'
});
```

---

## Custom Size via width

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function SizedSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        width: '56px'    // string with units
        // width: 56     // number (treated as px)
      });
      showSpinner(ref.current);
    }
  }, []);

  return <div ref={ref} style={{ height: '200px' }} />;
}
```

**Size recommendations:**

| Context | Suggested width |
|---|---|
| Inline / button | `'20px'` – `'24px'` |
| Card / panel | `'34px'` (default) |
| Full-page overlay | `'48px'` – `'64px'` |

---

## Custom Template

Replace the built-in spinner animation with your own HTML:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function PulseSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        template: `
          <div class="pulse-ring"></div>
        `
      });
      showSpinner(ref.current);
    }
  }, []);

  return <div ref={ref} style={{ height: '200px', position: 'relative' }} />;
}
```

**App.css:**

```css
.pulse-ring {
  width: 40px;
  height: 40px;
  border: 4px solid #007bff;
  border-radius: 50%;
  animation: pulse 1s ease-out infinite;
}

@keyframes pulse {
  0%   { transform: scale(0.8); opacity: 1; }
  100% { transform: scale(1.8); opacity: 0; }
}
```

**Image-based template:**

```tsx
createSpinner({
  target: el,
  template: '<img src="/spinner.gif" alt="Loading" width="40" />'
});
```

**SVG template:**

```tsx
createSpinner({
  target: el,
  template: `
    <svg width="40" height="40" viewBox="0 0 40 40">
      <circle cx="20" cy="20" r="16" fill="none" stroke="#007bff" stroke-width="4"
        stroke-dasharray="80" stroke-dashoffset="60">
        <animateTransform attributeName="transform" type="rotate"
          from="0 20 20" to="360 20 20" dur="1s" repeatCount="indefinite"/>
      </circle>
    </svg>
  `
});
```

---

## Global Customization with setSpinner

Apply customizations to all spinners created after the call:

```tsx
import { setSpinner, createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';

// ⚠️ Call BEFORE any createSpinner calls
setSpinner({
  type: 'Bootstrap5',
  cssClass: 'app-global-spinner'
});

// CSS for the global class
// .app-global-spinner .e-spinner-pane { ... }
```

**Global custom template:**

```tsx
setSpinner({
  template: '<div class="brand-loader"><span>Loading</span></div>'
});
```

**Combining type + cssClass globally:**

```tsx
setSpinner({
  type: 'Fluent2',
  cssClass: 'large-spinner'
});
```

> ⚠️ `setSpinner` affects spinners created **after** it is called. Spinners already created are not affected.

---

## Spinner Color via CSS

Override the spinner stroke/fill color using CSS targeting the spinner's internal classes:

```css
/* Material spinner color override */
.e-spinner-pane .e-spin-material {
  stroke: #e91e63;
}

/* Bootstrap spinner color override */
.e-spinner-pane .e-spin-bootstrap {
  background-color: #17a2b8;
}

/* Fluent spinner color override */
.e-spinner-pane .e-spin-fluent2 {
  stroke: #0078d4;
}
```

**Scoped to a specific container:**

```tsx
createSpinner({
  target: el,
  cssClass: 'pink-spinner'
});
```

```css
.pink-spinner .e-spin-material {
  stroke: #e91e63;
}
```

---

## Positioning the Spinner Label

The `label` appears below the spinner by default. Override with CSS:

```tsx
createSpinner({
  target: el,
  label: 'Please wait...',
  cssClass: 'inline-label-spinner'
});
```

```css
/* Position label to the right of the spinner (inline layout) */
.inline-label-spinner .e-spinner-inner {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

/* Style the label text */
.inline-label-spinner .e-spin-label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-top: 0;
}
```

---

## Overlay Backdrop Customization

Customize the semi-transparent overlay that covers the target element:

```css
/* Default: semi-transparent white — override to dark */
.e-spinner-pane {
  background-color: rgba(0, 0, 0, 0.4) !important;
}

/* Completely transparent (spinner only, no backdrop) */
.transparent-overlay .e-spinner-pane {
  background-color: transparent;
}

/* Blurred backdrop */
.blur-overlay .e-spinner-pane {
  backdrop-filter: blur(4px);
  background-color: rgba(255, 255, 255, 0.5);
}
```

```tsx
// Apply scoped overlay
createSpinner({ target: el, cssClass: 'blur-overlay' });
```

---

## Theme-Specific Customization

Match the spinner type to your app's CSS theme for automatic correct styling:

```tsx
// For apps using Material theme CSS
createSpinner({ target: el, type: 'Material' });

// For apps using Bootstrap 5 theme CSS
createSpinner({ target: el, type: 'Bootstrap5' });

// For apps using Fluent 2 theme CSS
createSpinner({ target: el, type: 'Fluent2' });

// For apps using Tailwind 3 theme CSS
createSpinner({ target: el, type: 'Tailwind3' });

// For high-contrast accessibility mode
createSpinner({ target: el, type: 'HighContrast' });
```

**Auto-detection via setSpinner at app entry:**

```tsx
// In src/main.tsx or src/index.tsx — before React root render
import { setSpinner } from '@syncfusion/ej2-react-popups';

setSpinner({ type: 'Fluent2' }); // match your app's theme
```

---

## Responsive Spinner

Adjust spinner size based on viewport:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function ResponsiveSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const isMobile = window.innerWidth < 768;
    createSpinner({
      target: ref.current,
      width: isMobile ? '28px' : '44px',
      label: isMobile ? '' : 'Loading...'
    });
    showSpinner(ref.current);
  }, []);

  return <div ref={ref} style={{ height: '200px' }} />;
}
```

**CSS-based responsiveness:**

```css
/* Smaller spinner on mobile */
@media (max-width: 768px) {
  .e-spinner-pane .e-spin-material {
    width: 28px !important;
    height: 28px !important;
  }
}
```
