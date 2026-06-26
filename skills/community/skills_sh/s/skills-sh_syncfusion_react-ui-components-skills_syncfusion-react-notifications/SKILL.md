---
name: syncfusion-react-notifications
description: Comprehensive guide for implementing Syncfusion React Notification components including Badge, Message, Skeleton, Toast, and Spinner. Use this when applying status indicators and badges with color variants and shapes; showing informational, success, warning, or error messages; configuring severity levels and display variants (Text, Outlined, Filled); handling message dismissal; toast positioning, toast templates, toast animations; displaying skeleton loading placeholders with shimmer animations (Wave, Pulse, Fade) and shapes (Circle, Rectangle, Text); or customizing notification appearance and accessibility.
metadata:
  author: "Syncfusion Inc"
  category: "Notifications"
  version: "33.1.44"
---

# Implementing Syncfusion React Notifications

## Toast

The Syncfusion React Toast component displays brief, non-intrusive notifications that auto-dismiss after a configurable timeout. Toasts support rich content through templates, action buttons, animated entry/exit, precise positioning, and programmatic control via `ToastUtility`.

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

### Package and Setup

📄 **Read:** [references/getting-started.md](references/toast-getting-started.md)
- Installing `@syncfusion/ej2-react-notifications` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-notifications@33.x.x --save`. Verify with `npm audit`*
- CSS imports for all required themes
- Basic `ToastComponent` usage (class and functional patterns)
- Rendering toast in a custom target container
- Triggering show in the `created` event

### Documentation and Navigation Guide

#### Configuration and Layout

📄 **Read:** [references/configuration.md](references/toast-configuration.md)
- Setting `title` and `content` (plain text, HTML, elements)
- Custom `target` container for scoped notifications
- `showCloseButton` for manual dismissal
- `showProgressBar` and `progressDirection` (Ltr / Rtl)
- `newestOnTop` stacking order
- `width` and `height` dimensions (px, %, auto)

#### Positioning

📄 **Read:** [references/position.md](references/toast-position.md)
- Nine predefined X/Y positions (Left, Center, Right / Top, Bottom)
- Custom pixel and percentage coordinates
- Targeting a container element for relative positioning
- Multiple Toast instances at different screen positions

#### Timeout and Dismissal

📄 **Read:** [references/timeout-and-dismissal.md](references/toast-timeout-and-dismissal.md)
- `timeOut` property (default 5000 ms)
- `extendedTimeout` on hover (default 1000 ms)
- Static persistent toasts with `timeOut: 0`
- Click-to-close via `clickToClose` in the `click` event
- Preventing mobile swipe dismissal with `beforeClose`

#### Templates and Styling

📄 **Read:** [references/templates-and-styling.md](references/toast-templates-and-styling.md)
- `template` property with HTML strings and DOM selectors
- Dynamic templates passed at `show()` call time
- Semantic CSS classes: `e-toast-success`, `e-toast-info`, `e-toast-warning`, `e-toast-danger`
- CSS selectors for title, content, icon, and background customization

#### Animation

📄 **Read:** [references/animation.md](references/toast-animation.md)
- `animation` property with `show` and `hide` effect settings
- Available effects: FadeIn, FadeZoomIn, SlideBottomIn, ZoomIn, FlipLeftUpIn, and more
- Default: FadeIn / FadeOut
- Accessibility: reduced-motion considerations

#### Toast Services and Advanced Patterns

📄 **Read:** [references/toast-services.md](references/toast-services.md)
- `ToastUtility.show()` for quick toasts without component instantiation
- Four predefined types: `Information`, `Success`, `Error`, `Warning`
- Passing a full `ToastModel` to `ToastUtility.show()`
- Playing audio on `beforeOpen`
- Restricting maximum simultaneous toasts with `beforeOpen`
- Preventing duplicate toasts using `beforeOpen` + `close`

#### Accessibility

📄 **Read:** [references/accessibility.md](references/toast-accessibility.md)
- WAI-ARIA: `role="alert"`, `aria-live="assertive"`, `aria-label`
- WCAG 2.2, Section 508, ADA compliance
- Screen reader support (JAWS, NVDA, VoiceOver)
- RTL support via `enableRtl`
- Mobile and accessibility checker validation

#### API Reference

📄 **Read:** [references/api.md](references/toast-api.md)
- All properties with types, defaults, and descriptions
- `show()` and `hide()` method signatures
- All events: `beforeOpen`, `open`, `click`, `beforeClose`, `close`, `created`, `destroyed`, `beforeSanitizeHtml`

### Quick Start Example

> 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev` after setup.*

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-notifications/styles/tailwind3.css';
import { useRef } from 'react';

function App() {
  const toastRef = useRef<ToastComponent>(null);

  return (
    <>
      <button onClick={() => toastRef.current?.show()}>Show Toast</button>
      <ToastComponent
        ref={toastRef}
        title="Success!"
        content="Your changes have been saved."
        cssClass="e-toast-success"
        position={{ X: 'Right', Y: 'Bottom' }}
        timeOut={4000}
        showProgressBar={true}
        showCloseButton={true}
      />
    </>
  );
}
```

### Quick Utility Toast (No Component Needed)

```tsx
import { ToastUtility } from '@syncfusion/ej2-react-notifications';

// Show a success toast instantly
ToastUtility.show('File saved successfully', 'Success', 3000);

// Show an error toast
ToastUtility.show('Connection failed', 'Error', 5000);
```

### Common Patterns

#### Semantic type toasts
Use `cssClass` with `e-toast-success`, `e-toast-info`, `e-toast-warning`, `e-toast-danger` for visual differentiation — see [references/templates-and-styling.md](references/toast-templates-and-styling.md).

#### Static/persistent toasts  
Set `timeOut: 0` with `showCloseButton: true` for notifications users must explicitly dismiss — see [references/timeout-and-dismissal.md](references/toast-timeout-and-dismissal.md).

#### Action-required toasts  
Use the `buttons` property to add Ignore/Confirm/Undo buttons — see [references/configuration.md](references/toast-configuration.md).

#### Prevent duplicates  
Use the `beforeOpen` event to cancel duplicate toasts already on screen — see [references/toast-services.md](references/toast-services.md).

#### Limit max visible toasts  
Cap simultaneous toasts at N using `beforeOpen` and `element.childElementCount` — see [references/toast-services.md](references/toast-services.md).

## Message

The Syncfusion `MessageComponent` displays contextual messages with visual severity indicators—icons and colors—to communicate importance and context to end users. It supports five severity levels, three visual variants, close-icon dismissal, custom templates, and full accessibility compliance.

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

### Navigation Guide

#### Getting Started
📄 **Read:** [references/message-getting-started.md](references/message-getting-started.md)
- Installation of `@syncfusion/ej2-react-notifications` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-notifications@33.x.x --save`. Verify with `npm audit`*
- CSS imports and theme configuration
- Rendering the first `MessageComponent`
- Content via `content` prop or JSX children
- Running the Vite development server

#### Severity Levels
📄 **Read:** [references/message-severities.md](references/message-severities.md)
- Five severity levels: Normal, Success, Info, Warning, Error
- `severity` prop usage and valid values
- Visual distinctions (icons and colors per severity)
- Choosing the right severity for your use case

#### Display Variants
📄 **Read:** [references/message-variants.md](references/message-variants.md)
- Three variants: Text (default), Outlined, Filled
- `variant` prop usage
- Combining variant with severity
- Visual trade-offs and when to use each

#### Icons and Close Icon
📄 **Read:** [references/message-icons-and-close.md](references/message-icons-and-close.md)
- Severity icon visibility: `showIcon` prop (default `true`)
- Disabling severity icons
- Custom severity icons via `cssClass` CSS overrides
- Close icon: `showCloseIcon` prop (default `false`)
- `closed` event handler for dismiss callbacks
- Toggling visibility with the `visible` prop

#### Customization and Templates
📄 **Read:** [references/message-customization.md](references/message-customization.md)
- Content alignment: left (default), center (`e-content-center`), right (`e-content-right`)
- Custom appearance with `cssClass`
- CSS-only message rendering (no JS, pure HTML + CSS)
- Content templates: JSX element or render function via `content` prop
- RTL support via `enableRtl`
- Persistence with `enablePersistence`

#### Accessibility
📄 **Read:** [references/message-accessibility.md](references/message-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes (`role=alert`, `aria-label`)
- Keyboard navigation (Tab, Enter/Space)
- Screen reader support

#### API Reference
📄 **Read:** [references/message-api.md](references/message-api.md)
- All properties with types, defaults, and descriptions
- Methods: `destroy`, `getPersistData`
- Events: `closed`, `created`, `destroyed`
- `MessageCloseEventArgs` interface
- `Severity` and `Variant` enum values

---

### Quick Start

> 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev` after setup.*

```bash
npm install @syncfusion/ej2-react-notifications@33.x.x --save
npm audit
```

```css
/* src/App.css */
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-notifications/styles/tailwind3.css';
```

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
import './App.css';

function App() {
  return (
    <MessageComponent content="Please read the comments carefully" />
  );
}
export default App;
```

---

### Common Patterns

#### Severity Messages
```tsx
<MessageComponent content="Editing is restricted" />
<MessageComponent content="Operation completed" severity="Success" />
<MessageComponent content="Read these notes" severity="Info" />
<MessageComponent content="Check your connection" severity="Warning" />
<MessageComponent content="Submission failed" severity="Error" />
```

#### Variant + Severity Combo
```tsx
<MessageComponent content="Editing is restricted" variant="Filled" />
<MessageComponent content="Operation completed" severity="Success" variant="Outlined" />
<MessageComponent content="Submission failed" severity="Error" variant="Filled" />
```

#### Dismissible Message
```tsx
import { useState } from 'react';

function App() {
  const [visible, setVisible] = useState(true);
  return (
    <MessageComponent
      content="Your session will expire soon"
      severity="Warning"
      showCloseIcon={true}
      visible={visible}
      closed={() => setVisible(false)}
    />
  );
}
```

#### Content Template
```tsx
const contentTemplate = () => (
  <div>
    <h4>Build succeeded</h4>
    <p>All 42 tests passed.</p>
  </div>
);

<MessageComponent content={contentTemplate} severity="Success" />
```

---

## Skeleton

The Syncfusion React `SkeletonComponent` renders animated placeholder shapes that mimic the layout of loading content. It reduces perceived load time and communicates progress to users with configurable shapes, shimmer animations, and full accessibility support.

**Package:** `@syncfusion/ej2-react-notifications`

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/skeleton-getting-started.md](references/skeleton-getting-started.md)
- Installing `@syncfusion/ej2-react-notifications` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-notifications@33.x.x --save`. Verify with `npm audit`*
- CSS theme imports (tailwind3)
- Minimal `SkeletonComponent` setup with `height` and `width`
- Running the Vite/React app

#### Shapes
📄 **Read:** [references/skeleton-shapes.md](references/skeleton-shapes.md)
- `shape` prop: `"Circle"`, `"Square"`, `"Rectangle"`, `"Text"` (default)
- Dimension rules: width required for Circle/Square; width + height for Rectangle/Text
- Building multi-shape card skeleton layouts
- Choosing the right shape for avatar, image, text, and icon placeholders

#### Shimmer Effects
📄 **Read:** [references/skeleton-shimmer-effect.md](references/skeleton-shimmer-effect.md)
- `shimmerEffect` prop: `"Wave"` (default), `"Pulse"`, `"Fade"`
- Visual behavior of each effect type
- List skeleton example with Pulse effect
- Selecting an effect to match UI context

#### Styles and Visibility
📄 **Read:** [references/skeleton-styles.md](references/skeleton-styles.md)
- `cssClass` prop for custom CSS overrides (wave color, background, animation speed)
- `visible` prop to toggle skeleton on/off based on loading state
- Transition pattern: skeleton → actual content
- CSS variable customization

#### Accessibility
📄 **Read:** [references/skeleton-accessibility.md](references/skeleton-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes: `role="status"`, `aria-label`, `aria-live`, `aria-busy`
- `label` prop for accessible skeleton names
- RTL support via `enableRtl`
- `prefers-reduced-motion` respect

#### API Reference
📄 **Read:** [references/skeleton-api.md](references/skeleton-api.md)
- All properties: `cssClass`, `enablePersistence`, `enableRtl`, `height`, `label`, `locale`, `shape`, `shimmerEffect`, `visible`, `width`
- Methods: `destroy()`
- `SkeletonType` and `ShimmerEffect` enum values

---

### Quick Start

> 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev` after setup.*

```bash
npm install @syncfusion/ej2-react-notifications@33.x.x --save
npm audit
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css";
```

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <SkeletonComponent height="15px" width="100%" />
  );
}
export default App;
```

---

### Common Patterns

#### Profile Card Skeleton
```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function ProfileCardSkeleton() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px' }}>
      {/* Avatar placeholder */}
      <SkeletonComponent shape="Circle" width="48px" />
      {/* Name and subtitle placeholders */}
      <div style={{ flex: 1 }}>
        <SkeletonComponent width="60%" height="15px" />
        <br />
        <SkeletonComponent width="40%" height="12px" />
      </div>
    </div>
  );
}
export default ProfileCardSkeleton;
```

#### Toggle Skeleton on Data Load
```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function DataCard() {
  const [loading, setLoading] = React.useState(true);
  const [content, setContent] = React.useState('');

  React.useEffect(() => {
    setTimeout(() => {
      setContent('Data loaded successfully');
      setLoading(false);
    }, 2000);
  }, []);

  return (
    <div>
      {loading ? (
        <SkeletonComponent width="80%" height="20px" />
      ) : (
        <p>{content}</p>
      )}
    </div>
  );
}
export default DataCard;
```

#### Shimmer List with Pulse Effect
```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function ListSkeleton() {
  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {[1, 2, 3].map((i) => (
        <li key={i} style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
          <SkeletonComponent shape="Circle" width="40px" shimmerEffect="Pulse" />
          <div style={{ flex: 1 }}>
            <SkeletonComponent width="70%" height="14px" shimmerEffect="Pulse" />
            <br />
            <SkeletonComponent width="45%" height="12px" shimmerEffect="Pulse" />
          </div>
        </li>
      ))}
    </ul>
  );
}
export default ListSkeleton;
```

---

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `shape` | `'Text' \| 'Circle' \| 'Square' \| 'Rectangle'` | `'Text'` | Skeleton shape variant |
| `width` | `string \| number` | `''` | Width; required for Circle/Square |
| `height` | `string \| number` | `''` | Height; used for Rectangle/Text |
| `shimmerEffect` | `'Wave' \| 'Pulse' \| 'Fade'` | `'Wave'` | Animation style |
| `visible` | `boolean` | `true` | Show/hide skeleton |
| `cssClass` | `string` | `''` | Custom CSS class(es) |
| `label` | `string` | `'Loading…'` | ARIA label for accessibility |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enablePersistence` | `boolean` | `false` | Persist state across reloads |

---

## Spinner

A skill for implementing the Syncfusion React Spinner — a load indicator that blocks user interaction with a target element while an operation is in progress.

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

### Documentation

#### Getting Started
📄 **Read:** [references/spinner-getting-started.md](references/spinner-getting-started.md)
- Installation: 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-popups@33.x.x --save`. Verify with `npm audit`*
- CSS theme imports (ej2-base + ej2-react-popups)
- Basic functional and class component patterns
- `createSpinner` → `showSpinner` workflow
- Show/hide control
- Full-page overlay spinner
- Troubleshooting missing styles and TypeScript errors

#### Spinner Features
📄 **Read:** [references/spinner-features.md](references/spinner-features.md)
- Global spinner configuration with `setSpinner`
- All `SpinnerType` values (Material, Bootstrap5, Fluent2, etc.)
- Spinner size via `width` property
- Label text alongside spinner
- Custom HTML template support
- Show/hide toggle patterns
- Multiple spinners on one page
- Async data fetching with `finally` cleanup
- React state + spinner synchronization
- Spinner inside cards and modals

#### API Reference
📄 **Read:** [references/spinner-api.md](references/spinner-api.md)
- `createSpinner(args: SpinnerArgs)` — full signature and params
- `showSpinner(container: HTMLElement)` — signature
- `hideSpinner(container: HTMLElement)` — signature
- `setSpinner(args: SetSpinnerArgs)` — signature
- `SpinnerArgs` interface (target, width, label, cssClass, template, type)
- `SetSpinnerArgs` interface (template, cssClass, type)
- All 11 `SpinnerType` values
- CSS import paths per theme
- Common invalid API gotchas

#### Customization
📄 **Read:** [references/spinner-customization.md](references/spinner-customization.md)
- `cssClass` for CSS hook customization
- `width` for spinner icon sizing
- `template` for custom HTML animations
- `setSpinner` for global defaults
- Overriding spinner colors via CSS
- Label positioning with CSS
- Overlay backdrop customization
- Theme-specific type mapping
- Responsive spinner patterns

#### Accessibility
📄 **Read:** [references/spinner-accessibility.md](references/spinner-accessibility.md)
- `aria-busy` on the loading region
- `aria-live` region for screen reader announcements
- `type: 'HighContrast'` for high contrast displays
- Keyboard accessibility (trigger focus, return focus)
- Focus management patterns
- Complete accessible spinner pattern
- WCAG 2.1 compliance checklist

### Quick Start

#### Minimal Spinner (Functional Component)

> 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev` after setup.*

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';
import './App.css';

function App() {
  useEffect(() => {
    createSpinner({
      target: document.getElementById('container') as HTMLElement
    });
    showSpinner(document.getElementById('container') as HTMLElement);
  }, []);

  return (
    <div id="container" style={{ height: '200px' }} />
  );
}

export default App;
```

#### Spinner with Show/Hide Toggle

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef, useState } from 'react';

function DataLoader() {
  const ref = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (ref.current) {
      createSpinner({ target: ref.current, label: 'Loading...' });
    }
  }, []);

  const load = async () => {
    setLoading(true);
    showSpinner(ref.current as HTMLElement);
    try {
      await fetchData();
    } finally {
      hideSpinner(ref.current as HTMLElement);
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={load} disabled={loading}>Load Data</button>
      <div ref={ref} style={{ height: '200px', position: 'relative' }} />
    </div>
  );
}
```

#### Global Spinner Type

```tsx
import { setSpinner } from '@syncfusion/ej2-react-popups';

// Call BEFORE any createSpinner — sets global default type
setSpinner({ type: 'Bootstrap5' });
```

### Common Patterns

#### Pattern 1: Async Fetch with Cleanup

```tsx
const fetchWithSpinner = async (container: HTMLElement) => {
  showSpinner(container);
  try {
    const data = await fetch('/api/data').then(r => r.json());
    return data;
  } finally {
    hideSpinner(container); // Always hide, even on error
  }
};
```

#### Pattern 2: React State Sync

```tsx
useEffect(() => {
  if (!ref.current) return;
  if (isLoading) {
    showSpinner(ref.current);
  } else {
    hideSpinner(ref.current);
  }
}, [isLoading]);
```

#### Pattern 3: Full-Page Loading

```tsx
useEffect(() => {
  createSpinner({ target: document.body, label: 'Initializing...' });
  showSpinner(document.body);

  initializeApp().finally(() => hideSpinner(document.body));
}, []);
```

#### Pattern 4: Spinner with Custom Type

```tsx
createSpinner({
  target: el,
  type: 'Fluent2',
  width: '40px',
  label: 'Processing...',
  cssClass: 'my-overlay'
});
```

### Key API Quick Reference

| Function | Signature | Purpose |
|---|---|---|
| `createSpinner` | `(args: SpinnerArgs) => void` | Initialize spinner on DOM element |
| `showSpinner` | `(el: HTMLElement) => void` | Show an existing spinner |
| `hideSpinner` | `(el: HTMLElement) => void` | Hide a visible spinner |
| `setSpinner` | `(args: SetSpinnerArgs) => void` | Set global defaults for all spinners |

**SpinnerArgs properties:** `target` (required), `width`, `label`, `cssClass`, `template`, `type`

**SpinnerType values:** `'Material'` | `'Material3'` | `'Fabric'` | `'Bootstrap'` | `'Bootstrap4'` | `'Bootstrap5'` | `'HighContrast'` | `'Tailwind'` | `'Tailwind3'` | `'Fluent'` | `'Fluent2'`

### Critical Rules

- ❌ **No `SpinnerComponent` class** — `import { SpinnerComponent }` does NOT exist
- ✅ **Only use:** `createSpinner`, `showSpinner`, `hideSpinner`, `setSpinner`
- ❌ **Do NOT use:** `color`, `size`, `visible`, `isLoading` as SpinnerArgs — they don't exist
- ✅ **Valid SpinnerArgs:** `target`, `width`, `label`, `cssClass`, `template`, `type`
- ⚠️ **Call `createSpinner` BEFORE `showSpinner`** — order matters
- ⚠️ **Put spinner logic in `useEffect`** — the DOM element must exist before calling createSpinner
- ✅ **Always call `hideSpinner` in `finally`** — prevents stuck loading states

### Troubleshooting

| Issue | Solution |
|---|---|
| Spinner not showing | Ensure `createSpinner` is called before `showSpinner`; check DOM element exists |
| Spinner stays visible | Call `hideSpinner` in `finally` block; check for unhandled promise rejections |
| No animation | Verify both `ej2-base` and `ej2-react-popups` CSS imported; `ej2-base` must come first |
| TypeScript error | Cast: `document.getElementById('id') as HTMLElement` or use `useRef<HTMLDivElement>` |
| Spinner outside bounds | Add `position: relative` to target element |
| Wrong theme | Set `type` to match your app's CSS theme (e.g., `'Fluent2'` for Fluent 2 CSS) |

### Related Components

- **Progress Bar** — For determinate progress with a percentage
- **Skeleton** — For content placeholder/shimmer loading patterns
- **Toast** — For non-blocking loading notifications
- **Dialog** — For modal loading states that require user acknowledgment

### Resources

- **Official Docs:** [https://ej2.syncfusion.com/react/documentation/spinner/](https://ej2.syncfusion.com/react/documentation/spinner/)
- **Getting Started:** [https://ej2.syncfusion.com/react/documentation/spinner/getting-started](https://ej2.syncfusion.com/react/documentation/spinner/getting-started)
- **npm Package:** [@syncfusion/ej2-react-popups](https://www.npmjs.com/package/@syncfusion/ej2-react-popups)

## Badge

The Syncfusion React Badge is a pure CSS component — no React component class to import. Badges are applied by adding CSS modifier classes to a `<span>` (or `<a>`) element nested inside the target UI element.

**Package:** `@syncfusion/ej2-react-notifications`

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

### Key Features

- **8 color variants** — primary, secondary, success, danger, warning, info, light, dark
- **Shape types** — circle, pill, link, notification, dot, overlap
- **Positioning** — top (default) and bottom placement on parent elements
- **Customization** — custom colors, sizes, and arbitrary positions via CSS
- **ListView integration** — embed badges in list items with dynamic content

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/badge-getting-started.md)
- Package installation: 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-notifications@33.x.x --save`. Verify with `npm audit`*
- Adding the first badge to a React component
- Minimal working example
- Running the application

#### Badge Types and Shapes
📄 **Read:** [references/types-and-shapes.md](references/badge-types-and-shapes.md)
- 8 predefined color variants and their semantic purpose
- Circle, pill, link, notification, dot, overlap shape types
- Badge positioning (top vs bottom)
- When to combine modifier classes (e.g., overlap + notification + circle)

#### Customization
📄 **Read:** [references/customization.md](references/badge-customization.md)
- Custom color overrides with CSS classes
- Adjusting badge size via `font-size`
- Custom positioning (left-top, left-bottom) with CSS overrides
- When to use custom CSS vs built-in modifier classes

#### How-To Guides
📄 **Read:** [references/how-to.md](references/badge-how-to.md)
- Integrate badges into a ListView component
- Update badge content dynamically (increment counts)
- React pattern for badge state management using DOM updates

### Quick Start

**1. Install the package:**
```bash
npm install @syncfusion/ej2-react-notifications@33.x.x --save
npm audit
```

**2. Add CSS to `src/App.css`:**
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css";
```

**3. Add a badge in your component:**
```tsx
import * as React from 'react';
import './App.css';

function App() {
  return (
    <h1>Badge Component <span className="e-badge e-badge-primary">New</span></h1>
  );
}
export default App;
```

### Common Patterns

#### Notification badge on an icon
```tsx
// Parent must have position: relative
<div className="badge-block">
  <div className="skype svg_icons"></div>
  <span className="e-badge e-badge-success e-badge-overlap e-badge-notification">99+</span>
</div>
```

#### Dot status indicator (bottom position)
```tsx
<div className="badge-block">
  <div className="firefox svg_icons"></div>
  <span className="e-badge e-badge-success e-badge-overlap e-badge-dot e-badge-bottom"></span>
</div>
```

#### Pill-shaped label
```tsx
<h1>Messages <span className="e-badge e-badge-primary e-badge-pill">New</span></h1>
```

### CSS Class Reference

| Class | Purpose |
|---|---|
| `e-badge` | Required base class for all badges |
| `e-badge-primary` / `e-badge-{color}` | Color variant |
| `e-badge-pill` | Pill (rounded rectangle) shape |
| `e-badge-circle` | Circle shape |
| `e-badge-notification` | Notification counter badge |
| `e-badge-dot` | Minimalist dot badge (no text) |
| `e-badge-overlap` | Overlaps the parent element edge |
| `e-badge-bottom` | Positions badge at bottom instead of top |
