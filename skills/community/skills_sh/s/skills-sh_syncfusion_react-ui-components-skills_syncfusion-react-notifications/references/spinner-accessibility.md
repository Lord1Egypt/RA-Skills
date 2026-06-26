# Accessibility — React Spinner

## Table of Contents
- [Overview](#overview)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Announcements](#screen-reader-announcements)
- [High Contrast Mode](#high-contrast-mode)
- [Keyboard Accessibility](#keyboard-accessibility)
- [Focus Management](#focus-management)
- [Accessible Spinner Pattern](#accessible-spinner-pattern)
- [WCAG 2.1 Compliance Notes](#wcag-21-compliance-notes)

---

## Overview

The Syncfusion Spinner is a visual loading indicator. Because it blocks user interaction during loading, accessibility considerations focus on:

- Communicating loading state to screen readers via ARIA live regions
- Providing meaningful labels
- Supporting high contrast mode via the `'HighContrast'` spinner type
- Managing focus appropriately when spinner appears/disappears

---

## ARIA Attributes

The Spinner renders with the following ARIA roles and attributes by default:

| Attribute | Value | Purpose |
|---|---|---|
| `role` | `"progressbar"` or not set (varies by version) | Indicates it is an indeterminate progress indicator |
| `aria-label` | Derived from the `label` property | Announces the loading message |
| `aria-busy` | Set on parent container | Signals that the region is loading |

**Best practice: manage `aria-busy` yourself:**

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function AccessibleSpinner() {
  const ref = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        label: 'Loading content, please wait'
      });
    }
  }, []);

  const startLoad = async () => {
    setLoading(true);
    showSpinner(ref.current as HTMLElement);

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
    } finally {
      hideSpinner(ref.current as HTMLElement);
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={startLoad} disabled={loading}>Load Data</button>
      <div
        ref={ref}
        aria-busy={loading}        // ✅ Tell screen readers region is loading
        aria-label="Content area"
        style={{ minHeight: '120px', position: 'relative' }}
      />
    </div>
  );
}
```

---

## Screen Reader Announcements

Use an ARIA live region to announce loading state changes to screen reader users:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function ScreenReaderFriendlySpinner() {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    if (spinnerRef.current) {
      createSpinner({
        target: spinnerRef.current,
        label: 'Loading...'
      });
    }
  }, []);

  const fetchData = async () => {
    // Announce start
    setAnnouncement('Loading data, please wait.');
    showSpinner(spinnerRef.current as HTMLElement);

    try {
      await new Promise(resolve => setTimeout(resolve, 2500));
      setAnnouncement('Data loaded successfully.');
    } catch {
      setAnnouncement('Failed to load data. Please try again.');
    } finally {
      hideSpinner(spinnerRef.current as HTMLElement);
    }
  };

  return (
    <div>
      {/* Visually hidden live region for screen readers */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: 'absolute',
          width: '1px',
          height: '1px',
          overflow: 'hidden',
          clip: 'rect(0,0,0,0)',
          whiteSpace: 'nowrap'
        }}
      >
        {announcement}
      </div>

      <button onClick={fetchData}>Fetch Data</button>
      <div
        ref={spinnerRef}
        style={{ height: '200px', position: 'relative' }}
      />
    </div>
  );
}

export default ScreenReaderFriendlySpinner;
```

**Key patterns:**
- `role="status"` + `aria-live="polite"` — announces changes without interrupting current speech
- `aria-live="assertive"` — use for urgent messages that should interrupt (e.g., errors)
- `aria-atomic="true"` — reads the entire region content, not just changed parts

---

## High Contrast Mode

Use `type: 'HighContrast'` for users with high contrast display settings:

```tsx
import { createSpinner, showSpinner, setSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function HighContrastSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        type: 'HighContrast',
        label: 'Loading...'
      });
      showSpinner(ref.current);
    }
  }, []);

  return <div ref={ref} style={{ height: '200px', background: '#000' }} />;
}
```

**Detect and apply high contrast automatically:**

```tsx
import { setSpinner } from '@syncfusion/ej2-react-popups';

// Detect Windows high contrast mode (forced-colors media query)
const prefersHighContrast = window.matchMedia('(forced-colors: active)').matches;

setSpinner({
  type: prefersHighContrast ? 'HighContrast' : 'Fluent2'
});
```

Import high contrast CSS:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/highcontrast.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/highcontrast.css";
```

---

## Keyboard Accessibility

The Spinner itself is **not keyboard-operable** (it's a visual overlay). However, ensure that:

1. **Focus is not trapped** inside the spinner overlay
2. **Controls that trigger the spinner** are keyboard-accessible (use `<button>`, not `<div onClick>`)
3. **Focus returns** to the triggering element after the spinner hides

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function KeyboardFriendlySpinner() {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (spinnerRef.current) {
      createSpinner({ target: spinnerRef.current });
    }
  }, []);

  const handleAction = async () => {
    setLoading(true);
    showSpinner(spinnerRef.current as HTMLElement);

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
    } finally {
      hideSpinner(spinnerRef.current as HTMLElement);
      setLoading(false);
      // Return focus to the trigger button after loading
      buttonRef.current?.focus();
    }
  };

  return (
    <div>
      {/* ✅ Use native <button> for keyboard accessibility */}
      <button
        ref={buttonRef}
        onClick={handleAction}
        disabled={loading}
        aria-busy={loading}
        aria-label={loading ? 'Loading, please wait' : 'Load content'}
      >
        {loading ? 'Loading...' : 'Load Content'}
      </button>

      <div
        ref={spinnerRef}
        aria-hidden={!loading}
        style={{ height: '150px', position: 'relative' }}
      />
    </div>
  );
}

export default KeyboardFriendlySpinner;
```

---

## Focus Management

When the spinner blocks a region, prevent focus from entering it:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function FocusManagedSpinner() {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (spinnerRef.current) {
      createSpinner({ target: spinnerRef.current });
    }
  }, []);

  const load = async () => {
    setLoading(true);
    showSpinner(spinnerRef.current as HTMLElement);
    await new Promise(resolve => setTimeout(resolve, 2000));
    hideSpinner(spinnerRef.current as HTMLElement);
    setLoading(false);
  };

  return (
    <div>
      <button onClick={load} disabled={loading}>Start</button>

      {/* aria-hidden hides the loading region from assistive tech while loading */}
      <div
        ref={spinnerRef}
        aria-hidden={loading}
        style={{ height: '200px', position: 'relative' }}
      >
        {!loading && (
          <div>
            <button>Interactive Button 1</button>
            <button>Interactive Button 2</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default FocusManagedSpinner;
```

---

## Accessible Spinner Pattern

A complete, production-ready accessible spinner implementation:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useCallback, useEffect, useRef, useState } from 'react';

interface AccessibleSpinnerProps {
  loadingLabel?: string;
  onLoad: () => Promise<void>;
  children: React.ReactNode;
}

function AccessibleSpinnerRegion({
  loadingLabel = 'Loading, please wait',
  onLoad,
  children
}: AccessibleSpinnerProps) {
  const regionRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const [loading, setLoading] = useState(false);
  const [liveMessage, setLiveMessage] = useState('');

  useEffect(() => {
    if (regionRef.current) {
      createSpinner({
        target: regionRef.current,
        label: loadingLabel,
        width: '36px'
      });
    }
  }, [loadingLabel]);

  const handleLoad = useCallback(async () => {
    setLoading(true);
    setLiveMessage(loadingLabel);
    showSpinner(regionRef.current as HTMLElement);

    try {
      await onLoad();
      setLiveMessage('Content loaded.');
    } catch {
      setLiveMessage('Failed to load content.');
    } finally {
      hideSpinner(regionRef.current as HTMLElement);
      setLoading(false);
      triggerRef.current?.focus();
    }
  }, [onLoad, loadingLabel]);

  return (
    <div>
      {/* Screen reader live announcement */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0,0,0,0)' }}
      >
        {liveMessage}
      </div>

      <button
        ref={triggerRef}
        onClick={handleLoad}
        disabled={loading}
        aria-busy={loading}
      >
        {loading ? 'Loading...' : 'Refresh'}
      </button>

      <div
        ref={regionRef}
        aria-busy={loading}
        aria-label="Content region"
        style={{ minHeight: '200px', position: 'relative' }}
      >
        {!loading && children}
      </div>
    </div>
  );
}

export default AccessibleSpinnerRegion;
```

---

## WCAG 2.1 Compliance Notes

| WCAG Criterion | Guidance |
|---|---|
| **1.4.3 Contrast** | Use `type: 'HighContrast'` for high contrast environments; ensure label text has sufficient contrast |
| **2.1.1 Keyboard** | Ensure the trigger element (button) is keyboard-operable; spinner itself needs no keyboard interaction |
| **2.4.3 Focus Order** | Return focus to trigger element after spinner hides |
| **4.1.2 Name, Role, Value** | Use `aria-busy` on the loading region; use `aria-live` region for announcements |
| **1.3.1 Info and Relationships** | The `label` property provides a programmatic name for the spinner |

**Checklist:**
- [ ] Use `<button>` (not `<div>`) for spinner triggers
- [ ] Set `aria-busy="true"` on the loading region while spinner is shown
- [ ] Provide an `aria-live` region to announce loading start/end
- [ ] Return focus to the trigger after loading completes
- [ ] Use `type: 'HighContrast'` or detect `forced-colors` media query
- [ ] Provide a meaningful `label` in `createSpinner` for context
- [ ] Set `aria-hidden="true"` on the spinner container to avoid double-announcing
