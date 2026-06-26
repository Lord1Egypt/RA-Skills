# How-To Patterns — Syncfusion React Button

## Table of Contents
1. [Create a Block (Full-Width) Button](#create-a-block-full-width-button)
2. [Create a Rounded-Corner Button](#create-a-rounded-corner-button)
3. [Add a Navigation Link to a Button](#add-a-navigation-link-to-a-button)
4. [Customize Button Appearance with CSS](#customize-button-appearance-with-css)
5. [Style Native Input and Anchor Elements as Buttons](#style-native-input-and-anchor-elements-as-buttons)
6. [Set the Disabled State](#set-the-disabled-state)
7. [Enable Right-to-Left (RTL) Support](#enable-right-to-left-rtl-support)
8. [Add a Tooltip on Hover](#add-a-tooltip-on-hover)
9. [Implement a Repeat Button](#implement-a-repeat-button)

---

## Create a Block (Full-Width) Button

A block button expands to fill the full width of its parent container. Set `cssClass='e-block'`.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      {/* Default block button */}
      <ButtonComponent cssClass='e-block'>Block Button</ButtonComponent>

      {/* Primary block button */}
      <ButtonComponent cssClass='e-block' isPrimary={true}>Block Button</ButtonComponent>

      {/* Success block button — combine e-block with a color style */}
      <ButtonComponent cssClass='e-block e-success'>Block Button</ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Create a Rounded-Corner Button

Apply the `e-round-corner` CSS class (or a custom class with `border-radius`) via `cssClass`. The built-in class uses `5px` border radius.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ButtonComponent cssClass='e-round-corner'>Button</ButtonComponent>
  );
}
export default App;
```

For a custom radius, define a CSS class:

```css
/* styles.css */
.e-custom-radius {
  border-radius: 20px;
}
```

```tsx
<ButtonComponent cssClass='e-custom-radius'>Pill Button</ButtonComponent>
```

---

## Add a Navigation Link to a Button

Style a button as a hyperlink using `cssClass='e-link'` and open the URL in the click handler using `window.open()`.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  function btnClick(): void {
    window.open('https://www.syncfusion.com');
  }

  return (
    <div>
      <ButtonComponent cssClass='e-link' onClick={btnClick}>Go to Syncfusion</ButtonComponent>
    </div>
  );
}
export default App;
```

> Use `window.open(url, '_blank')` to open in a new tab.

---

## Customize Button Appearance with CSS

Define a custom CSS class and assign it via `cssClass`. You can target all button states (default, hover, focus, active).

```css
/* styles.css */
.e-custom {
  background-color: #6c5ce7;
  color: #ffffff;
  height: 40px;
  border-radius: 8px;
  border: none;
}

.e-custom:hover {
  background-color: #a29bfe;
}

.e-custom:focus {
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.4);
}

.e-custom:active {
  background-color: #4834d4;
}
```

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './styles.css';

enableRipple(true);

function App() {
  return (
    <ButtonComponent cssClass='e-custom'>Custom</ButtonComponent>
  );
}
export default App;
```

> For systematic theme customization, use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material).

---

## Style Native Input and Anchor Elements as Buttons

Apply the Syncfusion button CSS classes (`e-btn`) directly on native HTML `<input>` and `<a>` elements — no `ButtonComponent` required:

```html
<!-- Input styled as a link button -->
<input type="button" value="Input Button" class="e-btn e-link" />

<!-- Anchor styled as a primary button -->
<a href="https://www.syncfusion.com" class="e-btn e-primary">Anchor Button</a>
```

This is useful when you need standard HTML elements to match the Syncfusion button appearance without using the React component.

---

## Set the Disabled State

Set `disabled={true}` to prevent interaction. A disabled button cannot receive focus or trigger click events.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      <ButtonComponent disabled={true}>Disabled</ButtonComponent>
      <ButtonComponent disabled={true} cssClass='e-primary'>Disabled Primary</ButtonComponent>
    </div>
  );
}
export default App;
```

To toggle `disabled` dynamically, use React state:

```tsx
const [isDisabled, setIsDisabled] = React.useState(false);

<ButtonComponent disabled={isDisabled}>Submit</ButtonComponent>
<ButtonComponent onClick={() => setIsDisabled(true)}>Disable Submit</ButtonComponent>
```

---

## Enable Right-to-Left (RTL) Support

Set `enableRtl={true}` to flip the layout for RTL languages such as Arabic or Hebrew. This mirrors the text and icon directions.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div>
      <ButtonComponent enableRtl={true} iconCss='e-btn-icons e-setting-icon'>
        Settings
      </ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Add a Tooltip on Hover

Set the `title` attribute on the button's underlying DOM element after rendering. Access the element via the `created` event and a `ref`.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let btnRef: ButtonComponent | null = null;

  function onCreated(): void {
    if (btnRef && btnRef.element) {
      (btnRef.element as HTMLElement).setAttribute('title', 'Click to save changes');
    }
  }

  return (
    <div>
      <ButtonComponent
        id='btn'
        ref={(scope) => { btnRef = scope; }}
        created={onCreated}
        isPrimary={true}
      >
        Save
      </ButtonComponent>
    </div>
  );
}
export default App;
```

> For rich tooltip UIs, consider the Syncfusion `TooltipComponent` — the `title` attribute renders a native browser tooltip only.

---

## Implement a Repeat Button

A repeat button continuously fires its action while held down, useful for incrementing values or controlling media.

The pattern uses `mousedown`/`mouseup` (and `touchstart`/`touchend`) events combined with `setInterval`:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let btnRef: ButtonComponent | null = null;
  let timeout: ReturnType<typeof setInterval> | null = null;
  let count = 0;

  function onCreated(): void {
    if (!btnRef || !btnRef.element) return;
    const elem = btnRef.element as HTMLElement;
    elem.addEventListener('mousedown', startRepeat);
    elem.addEventListener('mouseup', stopRepeat);
    elem.addEventListener('touchstart', startRepeat);
    elem.addEventListener('touchend', stopRepeat);
  }

  function startRepeat(): void {
    timeout = setInterval(() => {
      count++;
      console.log(`Repeat action triggered: ${count}`);
    }, 200);
  }

  function stopRepeat(): void {
    if (timeout) {
      clearInterval(timeout);
      timeout = null;
    }
  }

  return (
    <ButtonComponent
      id='repeat-btn'
      ref={(scope) => { btnRef = scope; }}
      created={onCreated}
      content='Hold Me'
    />
  );
}
export default App;
```

> Always clear the interval in `mouseup`/`touchend` to avoid memory leaks. Also handle `mouseleave` if the button should stop when the cursor leaves its bounds.
