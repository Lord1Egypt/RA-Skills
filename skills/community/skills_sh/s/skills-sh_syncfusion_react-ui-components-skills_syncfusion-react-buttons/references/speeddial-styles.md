# Styles and Appearance – Syncfusion React Speed Dial

## Table of Contents
- [Button Icons](#button-icons)
- [Button Text](#button-text)
- [Icon with Text Button](#icon-with-text-button)
- [Predefined CSS Classes (cssClass)](#predefined-css-classes-cssclass)
- [Disabled State](#disabled-state)
- [Visible Property](#visible-property)
- [Tooltip on Button](#tooltip-on-button)
- [Opens on Hover](#opens-on-hover)
- [Custom CSS Styling](#custom-css-styling)
- [Icon Position](#icon-position)

---

## Button Icons

Use `openIconCss` to set the icon shown when the popup is closed, and `closeIconCss` for the icon shown when it's open:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Button Text

Use the `content` property to show text in the button instead of (or alongside) icons:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Edit' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Icon with Text Button

Combine `openIconCss` (or `closeIconCss`) and `content` for an icon-and-text button:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Edit' openIconCss='e-icons e-edit' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

Use `iconPosition` to place the icon on the `'Left'` (default) or `'Right'` side of the text.

---

## Predefined CSS Classes (cssClass)

Apply semantic color styles using the `cssClass` property:

| CSS Class | Style | Use Case |
|-----------|-------|----------|
| `e-primary` | Primary (default look) | Main user actions |
| `e-outline` | Outlined, no fill | Secondary actions |
| `e-info` | Informative blue | Help or info actions |
| `e-success` | Green success | Confirm or complete actions |
| `e-warning` | Orange/yellow warning | Caution actions |
| `e-danger` | Red destructive | Delete or irreversible actions |

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Edit' cssClass='e-warning' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Disabled State

Set `disabled={true}` to prevent all user interaction with the Speed Dial button:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <SpeedDialComponent id='speeddial' content='Edit' disabled={true} target="#targetElement" />
  );
}
export default App;
```

---

## Visible Property

Control whether the Speed Dial button is rendered and visible using `visible`. Set to `false` to hide it:

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <SpeedDialComponent id='speeddial' content='Edit' visible={false} target="#targetElement" />
  );
}
export default App;
```

---

## Tooltip on Button

Add a `title` attribute to the wrapping element or use item-level `title` on `SpeedDialItemModel` to show tooltips. Button-level tooltip is applied via a standard HTML `title` attribute:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut', title: 'Cut' },
    { iconCss: 'e-icons e-copy', title: 'Copy' },
    { iconCss: 'e-icons e-paste', title: 'Paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' items={items} openIconCss='e-icons e-edit' target='#targetElement' />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Opens on Hover

Set `opensOnHover={true}` to open the Speed Dial on mouse hover instead of click:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} opensOnHover={true} target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Custom CSS Styling

Apply a custom CSS class via `cssClass` and define your own styles to override default appearance:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} target="#targetElement" cssClass='custom-css' />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

```css
/* Example custom styles */
.custom-css .e-fab-btn {
  background-color: #6200ea;
  border-color: #6200ea;
}
```
