# Getting Started with Syncfusion React Toast

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Toast Component](#basic-toast-component)
- [Functional Component Pattern](#functional-component-pattern)
- [Class Component Pattern](#class-component-pattern)
- [Toast with Custom Target](#toast-with-custom-target)

---

## Installation

Install the Syncfusion notifications package, which contains the Toast component:

```bash
npm install @syncfusion/ej2-react-notifications --save
```

Toast depends on buttons and popups packages (installed automatically as peers):
```bash
npm install @syncfusion/ej2-react-buttons @syncfusion/ej2-popups --save
```

---

## CSS Imports

Add all required CSS files in `src/App.css` (or your global stylesheet):

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-notifications/styles/tailwind3.css';
```

Other available themes: `material.css`, `bootstrap5.css`, `fluent.css`, `fabric.css`

---

## Basic Toast Component

Import `ToastComponent` from the notifications package:

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';
```

The Toast renders hidden by default. Call `toastInstance.show()` to display it — the `created` event fires once the component mounts, making it the standard place to trigger the initial show.

---

## Functional Component Pattern

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';
import './App.css';

function App() {
  let toastInstance: ToastComponent;

  function toastCreated(): void {
    toastInstance.show();
  }

  return (
    <ToastComponent
      ref={toast => toastInstance = toast!}
      title="Matt sent you a friend request"
      content="Hey, wanna dress up as wizards and ride our hoverboards?"
      created={toastCreated.bind(this)}
    />
  );
}

export default App;
```

**Key points:**
- Use a `ref` callback to capture the component instance
- `created` fires after the component mounts — call `show()` here for auto-display
- `title` renders as the toast headline; `content` as the body

---

## Class Component Pattern

```tsx
import { ToastComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';
import './App.css';

class App extends React.Component<{}, {}> {
  public toastInstance: ToastComponent;

  public toastCreated(): void {
    this.toastInstance.show();
  }

  public render() {
    return (
      <ToastComponent
        ref={toast => this.toastInstance = toast!}
        title="Matt sent you a friend request"
        content="Hey, wanna dress up as wizards and ride our hoverboards?"
        created={this.toastCreated = this.toastCreated.bind(this)}
      />
    );
  }
}

export default App;
```

---

## Toast with Custom Target

By default, Toast renders in `document.body`. Render inside a specific container element using the `target` property — useful for modals, panels, and scoped notification areas:

```tsx
function App() {
  let toastInstance: ToastComponent;

  function toastCreated(): void {
    toastInstance.show();
  }

  return (
    <div>
      <div id="toast_target" />
      <ToastComponent
        id="toast_target"
        ref={toast => toastInstance = toast!}
        title="Sample Toast"
        content="Rendered inside a custom container"
        target="#toast_target"
        created={toastCreated.bind(this)}
      />
    </div>
  );
}
```

> **Note:** When `target` is set, toast `position` is calculated relative to that container rather than the viewport.

---

## Triggering Toast from a Button

```tsx
function App() {
  let toastInstance: ToastComponent;

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Notification"
        content="This is a toast message"
        position={{ X: 'Right', Y: 'Bottom' }}
      />
    </div>
  );
}
```

## See Also

- [Configuration options](./configuration.md)
- [Positioning](./position.md)
- [Toast services (ToastUtility)](./toast-services.md)
