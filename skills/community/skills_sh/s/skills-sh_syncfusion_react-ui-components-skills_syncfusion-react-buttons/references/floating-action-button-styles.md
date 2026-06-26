# Styles and Appearance – Syncfusion React Floating Action Button

## Table of Contents
- [Predefined Styles](#predefined-styles)
- [Applying a Style](#applying-a-style)
- [CSS Class Override Reference](#css-class-override-reference)
- [Show Text on Hover](#show-text-on-hover)
- [Outline Color Customization](#outline-color-customization)
- [Theme Studio](#theme-studio)

---

## Predefined Styles

Apply visual variants using the `cssClass` property. These are semantic styles intended to communicate action priority or type:

| `cssClass` value | Description | Recommended Use |
|------------------|-------------|-----------------|
| `e-primary` | Primary action style (default appearance) | Main user actions |
| `e-outline` | Button with an outline border | Secondary actions |
| `e-info` | Informative blue styling | Help or information actions |
| `e-success` | Positive green styling | Confirm or success actions |
| `e-warning` | Cautionary amber/orange styling | Warning or alert actions |
| `e-danger` | Negative red styling | Delete or destructive actions |

> **Accessibility note:** Predefined styles are visual indicators only. Use the `content` property to provide meaningful text for assistive technologies such as screen readers.

---

## Applying a Style

Pass the desired CSS class string to the `cssClass` prop:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      {/* Warning style FAB */}
      <FabComponent id="fab" iconCss="e-icons e-edit" cssClass="e-warning" target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

Applying danger style for a delete action:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '300px' }}></div>
      <FabComponent id="fab" iconCss="e-icons e-delete" cssClass="e-danger" target="#target" />
    </div>
  );
}
export default App;
```

---

## CSS Class Override Reference

Override default FAB styles by targeting these CSS classes in your stylesheet:

| CSS Class | Purpose |
|-----------|---------|
| `.e-fab` | Container for the FAB component |
| `.e-fab.e-btn` | Base FAB button styling |
| `.e-fab.e-btn:hover` | FAB styling on mouse hover |
| `.e-fab.e-btn:focus` | FAB styling when focused via keyboard |
| `.e-fab.e-btn:active` | FAB styling when pressed or active |
| `.e-fab.e-btn-icon` | Icon styling within the FAB |
| `.e-fab.e-btn-content` | Text/content styling within the FAB |
| `.e-fab.e-primary` | Primary style variant |
| `.e-fab.e-outline` | Outline style variant |
| `.e-fab.e-info` | Info style variant |
| `.e-fab.e-success` | Success style variant |
| `.e-fab.e-warning` | Warning style variant |
| `.e-fab.e-danger` | Danger style variant |
| `.e-fab:disabled` | Styling for disabled FAB state |
| `.e-fab-overlay` | Overlay styling when FAB has focus |

---

## Show Text on Hover

Use `cssClass` with a custom CSS class to reveal a text label when the user hovers over an icon-only FAB. The `content` accepts HTML; when `enableHtmlSanitizer` is enabled (default `true`), valid HTML tags are preserved.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-edit"
        content='<span class="text-container"><span class="textEle">Edit</span></span>'
        cssClass="fab-hover"
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

Example CSS for the hover reveal effect:

```css
/* Initially hide the text */
.fab-hover .text-container {
  display: inline-block;
  overflow: hidden;
  max-width: 0;
  transition: max-width 0.3s ease;
  white-space: nowrap;
}

/* Reveal text on hover */
.fab-hover:hover .text-container {
  max-width: 100px;
}
```

---

## Outline Color Customization

Customize the outline FAB color by combining `e-outline` with a custom CSS class:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-people"
        content="Contact"
        cssClass="custom-css"
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

```css
/* Custom outline color overrides */
.custom-css.e-fab.e-btn {
  border-color: #6200ea;
  color: #6200ea;
}

.custom-css.e-fab.e-btn:hover {
  background-color: #6200ea;
  color: #fff;
}
```

---

## Theme Studio

For consistent brand-wide theming, use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=fluent) to generate a custom CSS theme. Export the generated CSS and replace the default Tailwind3 imports with your custom theme file.
