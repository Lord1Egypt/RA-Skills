# API Reference — Syncfusion React ButtonComponent

## Table of Contents
1. [Import](#import)
2. [Properties](#properties)
3. [Methods](#methods)
4. [Events](#events)
5. [Usage Examples](#usage-examples)

---

## Import

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
```

JSX usage:

```tsx
<ButtonComponent>Button</ButtonComponent>
```

---

## Properties

### `content` — `string`

Defines the text content rendered inside the button element.

- **Default:** `""`
- **Note:** Text can also be supplied as JSX children (`<ButtonComponent>Text</ButtonComponent>`). When both are used, `content` takes precedence.

```tsx
<ButtonComponent content="Save" cssClass="e-primary" />
```

---

### `cssClass` — `string`

Defines one or more CSS classes (space-separated) to apply to the button element. Used to control button types, color styles, size, and custom appearance.

- **Default:** `""`
- **Common values:** `e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`, `e-link`, `e-flat`, `e-outline`, `e-round`, `e-small`, `e-block`, `e-round-corner`

```tsx
<ButtonComponent cssClass="e-primary">Primary</ButtonComponent>
<ButtonComponent cssClass="e-small e-outline">Small Outline</ButtonComponent>
```

---

### `disabled` — `boolean`

Specifies whether the button is disabled. A disabled button is not interactive, cannot receive focus, and does not trigger click events.

- **Default:** `false`

```tsx
<ButtonComponent disabled={true}>Disabled</ButtonComponent>
```

---

### `enableHtmlSanitizer` — `boolean`

When `true`, the component sanitizes untrusted HTML strings and scripts in the `content` property before rendering, preventing XSS vulnerabilities.

- **Default:** `true`

> Keep this as `true` (default) unless you explicitly need to render trusted HTML markup in the button label. Disabling it without proper validation creates a security risk.

```tsx
<ButtonComponent enableHtmlSanitizer={false} content="<b>Bold</b>" />
```

---

### `enablePersistence` — `boolean`

When `true`, the component's state is persisted across page reloads using browser local storage.

- **Default:** `false`

```tsx
<ButtonComponent enablePersistence={true} isToggle={true}>Toggle</ButtonComponent>
```

---

### `enableRtl` — `boolean`

When `true`, renders the component in right-to-left (RTL) direction. Useful for Arabic, Hebrew, and other RTL scripts.

- **Default:** `false`

```tsx
<ButtonComponent enableRtl={true} iconCss="e-btn-icons e-setting-icon">Settings</ButtonComponent>
```

---

### `iconCss` — `string`

Defines one or more CSS classes for an icon to display within the button. Supports Syncfusion built-in icons (`e-icons`) and third-party icon libraries.

- **Default:** `""`

```tsx
<ButtonComponent iconCss="e-icons e-save">Save</ButtonComponent>
```

---

### `iconPosition` — `string | IconPosition`

Controls where the icon appears relative to the button text.

- **Default:** `IconPosition.Left` (`"Left"`)
- **Accepted values:** `"Left"` | `"Right"`

```tsx
<ButtonComponent iconCss="e-icons e-send" iconPosition="Right">Send</ButtonComponent>
```

---

### `isPrimary` — `boolean`

Enhances the visual appearance of the button with an emphasized primary style when set to `true`.

- **Default:** `false`

> `isPrimary={true}` is functionally similar to `cssClass='e-primary'` but uses a boolean prop. Prefer `cssClass='e-primary'` for consistency with other color styles.

```tsx
<ButtonComponent isPrimary={true}>Primary</ButtonComponent>
```

---

### `isToggle` — `boolean`

Makes the button a toggle button. When clicked, it transitions between a normal and active state. In the active state, Syncfusion applies the `e-active` CSS class to the element.

- **Default:** `false`

```tsx
<ButtonComponent isToggle={true} cssClass="e-flat">Toggle Me</ButtonComponent>
```

---

## Methods

Methods are called on the component instance obtained via `ref`.

### `click()` — `void`

Programmatically triggers the button's native click action.

```tsx
let btnRef: ButtonComponent | null = null;

function triggerClick(): void {
  if (btnRef) btnRef.click();
}

<ButtonComponent ref={(scope) => { btnRef = scope; }}>Action</ButtonComponent>
<button onClick={triggerClick}>Trigger via code</button>
```

---

### `focusIn()` — `void`

Programmatically sets focus to the button element (native focus method).

```tsx
let btnRef: ButtonComponent | null = null;

function focusButton(): void {
  if (btnRef) btnRef.focusIn();
}

<ButtonComponent ref={(scope) => { btnRef = scope; }}>Focusable</ButtonComponent>
<button onClick={focusButton}>Focus the button</button>
```

---

### `destroy()` — `void`

Destroys the `ButtonComponent` instance and cleans up event listeners and DOM modifications. Call this before unmounting if managing the component lifecycle manually.

```tsx
let btnRef: ButtonComponent | null = null;

function cleanup(): void {
  if (btnRef) btnRef.destroy();
}
```

> In React, `destroy()` is typically not needed — React's unmounting handles cleanup. Use it only in advanced scenarios where you manually control the component lifecycle outside the React tree.

---

## Events

### `created` — `EmitType<Event>`

Fires once after the component has fully rendered. Use it for post-render DOM operations such as setting `title` attributes or programmatic focus.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  let btnRef: ButtonComponent | null = null;

  function onCreated(): void {
    if (btnRef && btnRef.element) {
      (btnRef.element as HTMLElement).setAttribute('title', 'Click to submit');
    }
  }

  return (
    <ButtonComponent
      ref={(scope) => { btnRef = scope; }}
      created={onCreated}
      isPrimary={true}
    >
      Submit
    </ButtonComponent>
  );
}
export default App;
```

---

## Usage Examples

### All properties in one component

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let btnRef: ButtonComponent | null = null;

  function onCreated(): void {
    if (btnRef && btnRef.element) {
      (btnRef.element as HTMLElement).setAttribute('title', 'Save your changes');
    }
  }

  return (
    <ButtonComponent
      content="Save"
      cssClass="e-primary"
      disabled={false}
      enableHtmlSanitizer={true}
      enablePersistence={false}
      enableRtl={false}
      iconCss="e-icons e-save"
      iconPosition="Left"
      isPrimary={false}
      isToggle={false}
      created={onCreated}
      ref={(scope) => { btnRef = scope; }}
    />
  );
}
export default App;
```

### Toggle button with state tracking

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import { useState } from 'react';

enableRipple(true);

function App() {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <ButtonComponent
      isToggle={true}
      cssClass="e-flat"
      iconCss={isPlaying ? 'e-btn-sb-icon e-pause-icon' : 'e-btn-sb-icon e-play-icon'}
      content={isPlaying ? 'Pause' : 'Play'}
      onClick={() => setIsPlaying(!isPlaying)}
    />
  );
}
export default App;
```
