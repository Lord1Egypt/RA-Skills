# Spinner Features — React Spinner

## Table of Contents
- [Global Spinner Configuration (setSpinner)](#global-spinner-configuration-setspinner)
- [Spinner Types and Themes](#spinner-types-and-themes)
- [Spinner Size (width)](#spinner-size-width)
- [Spinner Label](#spinner-label)
- [Custom Template](#custom-template)
- [Show and Hide Control](#show-and-hide-control)
- [Multiple Spinners on a Page](#multiple-spinners-on-a-page)
- [Spinner with Async Data Fetching](#spinner-with-async-data-fetching)
- [Spinner with React State](#spinner-with-react-state)
- [Spinner Inside a Card or Modal](#spinner-inside-a-card-or-modal)

---

## Global Spinner Configuration (setSpinner)

Use `setSpinner` to apply a default theme or CSS class to **all** spinners on the page. Call it **before** any `createSpinner` call.

```tsx
import { setSpinner, createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';

// Set global spinner type before component creation
setSpinner({ type: 'Bootstrap5' });

function App() {
  useEffect(() => {
    // This spinner inherits the Bootstrap5 type set globally
    createSpinner({
      target: document.getElementById('container') as HTMLElement
    });
    showSpinner(document.getElementById('container') as HTMLElement);
  }, []);

  return <div id="container" style={{ height: '200px' }} />;
}

export default App;
```

**When to use `setSpinner`:**
- Your app has a theme that doesn't match the default spinner style
- You want consistent spinner appearance without specifying `type` on every `createSpinner` call
- You want to inject a custom template across all spinners

```tsx
// Global custom CSS class for all spinners
setSpinner({ cssClass: 'app-spinner' });

// Global custom template for all spinners
setSpinner({ template: '<div class="my-custom-loader"></div>' });
```

---

## Spinner Types and Themes

Set the visual theme of the spinner using the `type` property on `createSpinner` or globally via `setSpinner`.

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function SpinnerTypes() {
  const targets = ['material', 'material3', 'bootstrap5', 'fluent2', 'tailwind3'];

  useEffect(() => {
    const typeMap: Record<string, 'Material' | 'Material3' | 'Bootstrap5' | 'Fluent2' | 'Tailwind3'> = {
      material: 'Material',
      material3: 'Material3',
      bootstrap5: 'Bootstrap5',
      fluent2: 'Fluent2',
      tailwind3: 'Tailwind3'
    };

    targets.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        createSpinner({ target: el, type: typeMap[id] });
        showSpinner(el);
      }
    });
  }, []);

  return (
    <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
      {targets.map(id => (
        <div key={id}>
          <p>{id}</p>
          <div id={id} style={{ width: '80px', height: '80px' }} />
        </div>
      ))}
    </div>
  );
}
```

**All supported `type` values:**

| Value | Description |
|---|---|
| `'Material'` | Google Material Design |
| `'Material3'` | Material Design 3 |
| `'Fabric'` | Microsoft Fabric / Office |
| `'Bootstrap'` | Bootstrap 3 |
| `'Bootstrap4'` | Bootstrap 4 |
| `'Bootstrap5'` | Bootstrap 5 |
| `'HighContrast'` | Accessibility high contrast |
| `'Tailwind'` | Tailwind CSS |
| `'Tailwind3'` | Tailwind CSS v3 |
| `'Fluent'` | Microsoft Fluent |
| `'Fluent2'` | Microsoft Fluent 2 |

---

## Spinner Size (width)

Control the size of the spinner icon via the `width` property:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function SpinnerSizes() {
  const smallRef = useRef<HTMLDivElement>(null);
  const mediumRef = useRef<HTMLDivElement>(null);
  const largeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (smallRef.current) {
      createSpinner({ target: smallRef.current, width: '20px' });
      showSpinner(smallRef.current);
    }
    if (mediumRef.current) {
      createSpinner({ target: mediumRef.current, width: '34px' });
      showSpinner(mediumRef.current);
    }
    if (largeRef.current) {
      createSpinner({ target: largeRef.current, width: '56px' });
      showSpinner(largeRef.current);
    }
  }, []);

  return (
    <div style={{ display: 'flex', gap: '40px', alignItems: 'center' }}>
      <div>
        <p>Small (20px)</p>
        <div ref={smallRef} style={{ height: '60px', width: '60px' }} />
      </div>
      <div>
        <p>Medium (34px)</p>
        <div ref={mediumRef} style={{ height: '80px', width: '80px' }} />
      </div>
      <div>
        <p>Large (56px)</p>
        <div ref={largeRef} style={{ height: '120px', width: '120px' }} />
      </div>
    </div>
  );
}
```

> `width` accepts a string with units (`'34px'`, `'2rem'`) or a number (interpreted as pixels).

---

## Spinner Label

Display a text message alongside the spinner using the `label` property:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function LabeledSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        label: 'Loading data, please wait...',
        width: '40px'
      });
      showSpinner(ref.current);
    }
  }, []);

  return (
    <div
      ref={ref}
      style={{ height: '200px', position: 'relative' }}
    />
  );
}
```

**Label placement:** The label appears below the spinner icon by default. Use `cssClass` with custom CSS to adjust positioning.

---

## Custom Template

Replace the default spinner animation with a custom HTML template:

```tsx
import { createSpinner, showSpinner } from '@syncfusion/ej2-react-popups';
import { useEffect, useRef } from 'react';

function CustomTemplateSpinner() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      createSpinner({
        target: ref.current,
        // Custom HTML replaces the default spinner SVG
        template: '<div class="custom-loader"><div class="loader-dot"></div><div class="loader-dot"></div><div class="loader-dot"></div></div>'
      });
      showSpinner(ref.current);
    }
  }, []);

  return (
    <div
      ref={ref}
      style={{ height: '200px', position: 'relative' }}
    />
  );
}
```

**CSS for the custom template (in App.css):**

```css
.custom-loader {
  display: flex;
  gap: 8px;
  align-items: center;
}

.loader-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #007bff;
  animation: bounce 1.2s infinite ease-in-out;
}

.loader-dot:nth-child(2) { animation-delay: 0.2s; }
.loader-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
```

> Use `setSpinner({ template: '...' })` to apply a custom template globally to all spinners.

---

## Show and Hide Control

Control spinner visibility dynamically:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function ToggleSpinner() {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (ref.current) {
      // Create once, toggle visibility
      createSpinner({ target: ref.current });
    }
  }, []);

  const toggle = () => {
    if (!ref.current) return;
    if (visible) {
      hideSpinner(ref.current);
      setVisible(false);
    } else {
      showSpinner(ref.current);
      setVisible(true);
    }
  };

  return (
    <div>
      <button onClick={toggle}>
        {visible ? 'Hide Spinner' : 'Show Spinner'}
      </button>
      <div ref={ref} style={{ height: '200px', marginTop: '20px' }} />
    </div>
  );
}

export default ToggleSpinner;
```

---

## Multiple Spinners on a Page

Each spinner is independent. Create multiple by targeting different elements:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect } from 'react';

function MultipleSpinners() {
  useEffect(() => {
    const ids = ['spinner1', 'spinner2', 'spinner3'];
    ids.forEach(id => {
      const el = document.getElementById(id) as HTMLElement;
      if (el) {
        createSpinner({ target: el });
        showSpinner(el);
      }
    });

    // Hide individual spinners independently
    setTimeout(() => hideSpinner(document.getElementById('spinner1') as HTMLElement), 1000);
    setTimeout(() => hideSpinner(document.getElementById('spinner2') as HTMLElement), 2000);
    setTimeout(() => hideSpinner(document.getElementById('spinner3') as HTMLElement), 3000);
  }, []);

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div id="spinner1" style={{ width: '100px', height: '100px' }} />
      <div id="spinner2" style={{ width: '100px', height: '100px' }} />
      <div id="spinner3" style={{ width: '100px', height: '100px' }} />
    </div>
  );
}

export default MultipleSpinners;
```

---

## Spinner with Async Data Fetching

Show spinner during async operations and hide when complete:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

interface User { id: number; name: string; email: string; }

function DataFetcher() {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (spinnerRef.current) {
      createSpinner({ target: spinnerRef.current, label: 'Fetching users...' });
    }
  }, []);

  const fetchUsers = async () => {
    if (!spinnerRef.current) return;

    showSpinner(spinnerRef.current);
    setError(null);

    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/users');
      const data: User[] = await response.json();
      setUsers(data);
    } catch (err) {
      setError('Failed to fetch users.');
    } finally {
      // Always hide spinner, even on error
      hideSpinner(spinnerRef.current);
    }
  };

  return (
    <div>
      <button onClick={fetchUsers}>Load Users</button>
      <div ref={spinnerRef} style={{ minHeight: '100px', position: 'relative' }} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {users.map(u => <li key={u.id}>{u.name} — {u.email}</li>)}
      </ul>
    </div>
  );
}

export default DataFetcher;
```

> ✅ Always call `hideSpinner` in a `finally` block to prevent stuck spinners.

---

## Spinner with React State

Combine React state with spinner for clean UI control:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useCallback, useEffect, useRef, useState } from 'react';

function FormWithSpinner() {
  const spinnerRef = useRef<HTMLDivElement>(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (spinnerRef.current) {
      createSpinner({
        target: spinnerRef.current,
        label: 'Submitting form...',
        width: '30px'
      });
    }
  }, []);

  useEffect(() => {
    if (!spinnerRef.current) return;
    if (submitting) {
      showSpinner(spinnerRef.current);
    } else {
      hideSpinner(spinnerRef.current);
    }
  }, [submitting]);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setSuccess(false);

    try {
      // Simulate form submission
      await new Promise(resolve => setTimeout(resolve, 2000));
      setSuccess(true);
    } finally {
      setSubmitting(false);
    }
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Your name" required />
      <button type="submit" disabled={submitting}>
        {submitting ? 'Submitting...' : 'Submit'}
      </button>
      <div ref={spinnerRef} style={{ height: '80px' }} />
      {success && <p style={{ color: 'green' }}>Form submitted successfully!</p>}
    </form>
  );
}

export default FormWithSpinner;
```

---

## Spinner Inside a Card or Modal

Use relative positioning so the spinner overlays only the card:

```tsx
import { createSpinner, showSpinner, hideSpinner } from '@syncfusion/ej2-react-popups';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';

function CardWithSpinner() {
  const cardRef = useRef<HTMLDivElement>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (cardRef.current) {
      createSpinner({ target: cardRef.current });
      showSpinner(cardRef.current);

      // Simulate content loading
      setTimeout(() => {
        hideSpinner(cardRef.current as HTMLElement);
        setLoaded(true);
      }, 2500);
    }
  }, []);

  return (
    <div
      ref={cardRef}
      style={{
        width: '320px',
        height: '200px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '16px',
        position: 'relative'  // Required for spinner to overlay within bounds
      }}
    >
      {loaded && (
        <div>
          <h3>Card Title</h3>
          <p>Content loaded successfully!</p>
        </div>
      )}
    </div>
  );
}

export default CardWithSpinner;
```

> ⚠️ The target element needs `position: relative` (or `absolute`/`fixed`) for the spinner overlay to work correctly inside it.
