# Types and Styles — Syncfusion React Button

## Table of Contents
1. [Button Styles (Color Variants)](#button-styles-color-variants)
2. [Flat Button](#flat-button)
3. [Outline Button](#outline-button)
4. [Round Button](#round-button)
5. [Toggle Button](#toggle-button)
6. [Basic HTML Button Types](#basic-html-button-types)
7. [Icons](#icons)
   - [Font Icons](#font-icons)
   - [SVG Icons](#svg-icons)
   - [Icon Position](#icon-position)
8. [Button Sizes](#button-sizes)

---

## Button Styles (Color Variants)

Apply predefined semantic color styles using the `cssClass` prop. These convey intent visually but do not alter functional behavior — always use meaningful button text for assistive technology users.

| `cssClass` value | Visual meaning |
|---|---|
| `e-primary` | Primary action |
| `e-success` | Positive / confirmatory action |
| `e-info` | Informative action |
| `e-warning` | Cautionary action |
| `e-danger` | Destructive / negative action |
| `e-link` | Hyperlink appearance |

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      <ButtonComponent cssClass='e-primary'>Primary</ButtonComponent>
      <ButtonComponent cssClass='e-success'>Success</ButtonComponent>
      <ButtonComponent cssClass='e-info'>Info</ButtonComponent>
      <ButtonComponent cssClass='e-warning'>Warning</ButtonComponent>
      <ButtonComponent cssClass='e-danger'>Danger</ButtonComponent>
      <ButtonComponent cssClass='e-link'>Link</ButtonComponent>
    </div>
  );
}
export default App;
```

Multiple classes can be combined (space-separated):

```tsx
<ButtonComponent cssClass='e-small e-primary'>Small Primary</ButtonComponent>
```

---

## Flat Button

A flat button has no background color — useful for secondary or low-emphasis actions.

```tsx
<ButtonComponent cssClass='e-flat'>Flat</ButtonComponent>
```

---

## Outline Button

An outline button has a visible border with a transparent background.

```tsx
<ButtonComponent cssClass='e-outline'>Outline</ButtonComponent>
```

---

## Round Button

A round (circular) button typically contains only an icon. Set `cssClass='e-round'` and supply an icon via `iconCss`.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    // isPrimary enhances the visual appearance
    <ButtonComponent cssClass='e-round' iconCss='e-icons e-plus-icon' isPrimary={true} />
  );
}
export default App;
```

> Use `isPrimary={true}` with round buttons to apply enhanced visual styling.

---

## Toggle Button

A toggle button switches between two states (normal ↔ active). Set `isToggle={true}`. When active, the `e-active` CSS class is applied automatically.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { useState } from 'react';
import * as React from 'react';

enableRipple(true);

function App() {
  const [state, setState] = useState({ content: 'Play', iconCss: 'e-btn-sb-icon e-play-icon' });

  function btnClick(): void {
    if (state.content === 'Play') {
      setState({ content: 'Pause', iconCss: 'e-btn-sb-icon e-pause-icon' });
    } else {
      setState({ content: 'Play', iconCss: 'e-btn-sb-icon e-play-icon' });
    }
  }

  return (
    <ButtonComponent
      cssClass='e-flat'
      iconCss={state.iconCss}
      content={state.content}
      isToggle={true}
      onClick={btnClick}
    />
  );
}
export default App;
```

> The `e-active` class is applied by Syncfusion when the button is in the toggled state. Update your own React state independently if you need to track the toggle state for logic purposes.

---

## Basic HTML Button Types

Use the native HTML `type` attribute to control form submission behavior:

| Type | Description |
|---|---|
| `button` (default) | Standard click button, no form action |
| `submit` | Submits the parent `<form>` to the server |
| `reset` | Resets all controls in the parent `<form>` to their initial values |

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <form>
      <ButtonComponent type='submit'>Submit</ButtonComponent>
      <ButtonComponent type='reset'>Reset</ButtonComponent>
    </form>
  );
}
export default App;
```

---

## Icons

### Font Icons

Add an icon using the `iconCss` prop. Syncfusion's built-in icon set uses the `e-icons` base class.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      {/* Icon on the left (default) */}
      <ButtonComponent iconCss='e-btn-sb-icon e-prev-icon'>Previous</ButtonComponent>

      {/* Icon on the right */}
      <ButtonComponent iconCss='e-btn-sb-icon e-stop-icon' iconPosition='Right'>Stop</ButtonComponent>
    </div>
  );
}
export default App;
```

> The `e-icons` class loads Syncfusion's Essential JS 2 built-in icon font. Third-party icon libraries (e.g., Font Awesome) can also be used by supplying the appropriate CSS class.

### SVG Icons

SVG images can also be loaded via `iconCss` by referencing a custom CSS class that defines the SVG as a background or mask image:

```tsx
<ButtonComponent iconCss='e-search-icon' />
```

Define `.e-search-icon` in your CSS with the desired `height`, `width`, and SVG `background-image`.

### Icon Position

Control icon placement with `iconPosition`. Accepted values: `'Left'` (default) and `'Right'`.

```tsx
<ButtonComponent iconCss='e-icons e-save' iconPosition='Left'>Save</ButtonComponent>
<ButtonComponent iconCss='e-icons e-delete' iconPosition='Right'>Delete</ButtonComponent>
```

---

## Button Sizes

Two sizes are available — **normal** (default) and **small**. Use `cssClass='e-small'` to render a compact button.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      <ButtonComponent cssClass='e-small'>Small</ButtonComponent>
      <ButtonComponent>Normal</ButtonComponent>
    </div>
  );
}
export default App;
```
