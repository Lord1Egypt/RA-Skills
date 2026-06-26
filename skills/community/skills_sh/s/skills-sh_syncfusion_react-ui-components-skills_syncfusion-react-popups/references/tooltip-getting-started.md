# Getting Started — Syncfusion React Tooltip

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Tooltip](#basic-tooltip)
- [Tooltip on Multiple Targets](#tooltip-on-multiple-targets)
- [Using title Attribute as Content](#using-title-attribute-as-content)
- [Running the Application](#running-the-application)

---

## Installation

Create a React app with Vite:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-popups --save
npm run dev
```

> For JavaScript projects use `--template react`. The `--save` flag registers the dependency in `package.json`.

---

## CSS Imports

Add Syncfusion theme CSS in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

> Available themes: `material3`, `bootstrap5`, `fluent2`, `tailwind3`. Replace `tailwind3` with your preferred theme across both imports.

---

## Basic Tooltip

The simplest usage wraps any element with `TooltipComponent` and provides a `content` string.

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

function App() {
  const style: React.CSSProperties = {
    display: 'inline-block',
    margin: '60px'
  };
  return (
    <TooltipComponent content="Tooltip Content" style={style}>
      Show Tooltip
    </TooltipComponent>
  );
}
export default App;
```

To place the tooltip on a specific child element rather than the wrapper itself, use the `target` and `position` props:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  return (
    <div id="container">
      <TooltipComponent position="TopCenter" content="Tooltip Content" target="#target">
        <button className="e-btn" id="target">Show Tooltip</button>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

- `target` — CSS selector identifying which child element triggers the tooltip.
- `position` — one of 12 placement values (default `TopCenter`).

---

## Tooltip on Multiple Targets

A single `TooltipComponent` can serve multiple targets within a container. Set `target` to a shared CSS selector and the tooltip reads each element's `title` attribute as its content.

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  return (
    <div id="container">
      <TooltipComponent target=".e-info" position="RightCenter">
        <form>
          <table>
            <tbody>
              <tr>
                <td>User Name</td>
                <td>
                  <input
                    type="text"
                    className="e-info"
                    title="Please enter your name"
                  />
                </td>
              </tr>
              <tr>
                <td>Email Address</td>
                <td>
                  <input
                    type="email"
                    className="e-info"
                    title="Enter a valid email address"
                  />
                </td>
              </tr>
              <tr>
                <td>Password</td>
                <td>
                  <input
                    type="password"
                    className="e-info"
                    title="Be at least 8 characters length"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </form>
      </TooltipComponent>
    </div>
  );
}
export default App;
```

> Each matched `.e-info` element's `title` attribute becomes that element's tooltip content. The `title` attribute is used as fallback when no `content` prop is supplied.

---

## Using title Attribute as Content

If the `content` property is not provided, `TooltipComponent` automatically reads the `title` attribute of the target element.

```tsx
<TooltipComponent target="#myBtn">
  <button id="myBtn" title="This is my tooltip text">Hover Me</button>
</TooltipComponent>
```

> Useful for progressive enhancement — standard HTML `title` attributes become rich Syncfusion tooltips without extra configuration.

---

## Running the Application

```bash
npm run dev
```

The development server starts and opens the app in the browser. The tooltip appears on hover over the target element by default.

---

## See Also
- [Content](content.md) — Templates, dynamic fetch, HTML embedding
- [Position](position.md) — 12 positions, mouse trail, offsets
- [Open Mode](open-mode.md) — Hover, Click, Focus, Custom, Sticky
