# Events – Syncfusion React Floating Action Button

## Table of Contents
- [created](#created)
- [onClick](#onclick)
- [Combined Example](#combined-example)

---

## created

The `created` event fires once the FAB component has fully initialized and rendered. Use it to perform post-render setup, access component properties, or trigger dependent logic.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  function onCreate(): void {
    // Perform initialization logic after FAB creation
    console.log('FAB component is ready');
  }

  return (
    <FabComponent id="fab" iconCss="e-icons e-edit" content="Edit" created={onCreate} />
  );
}
export default App;
```

**When to use `created`:**
- Initialize data or fetch content that the FAB depends on
- Log analytics when the FAB becomes visible
- Set focus or perform DOM operations after the FAB renders

---

## onClick

The `onClick` event fires when the FAB is activated by a mouse click or keyboard press (Enter/Space). Use this event to trigger the primary action associated with the FAB.

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  function handleClick(): void {
    // Execute action when FAB is clicked
    console.log('FAB clicked');
  }

  return (
    <FabComponent id="fab" iconCss="e-icons e-edit" content="Edit" onClick={handleClick} />
  );
}
export default App;
```

Full example with a target container:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  function onClick(): void {
    alert('Edit is clicked!');
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-edit"
        content="Edit"
        onClick={onClick}
        target="#targetElement"
      />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

**When to use `onClick`:**
- Open a dialog or modal
- Add a new item to a list
- Trigger a navigation action
- Submit a quick form

---

## Combined Example

Using both `created` and `onClick` together:

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const [clickCount, setClickCount] = React.useState(0);

  function onCreate(): void {
    console.log('FAB initialized and ready');
  }

  function handleClick(): void {
    setClickCount((prev) => prev + 1);
    console.log(`FAB clicked ${clickCount + 1} time(s)`);
  }

  return (
    <div>
      <p>Click count: {clickCount}</p>
      <div id="target" style={{ position: 'relative', minHeight: '300px', border: '1px solid' }}></div>
      <FabComponent
        id="fab"
        iconCss="e-icons e-edit"
        content="Edit"
        created={onCreate}
        onClick={handleClick}
        target="#target"
      />
    </div>
  );
}
export default App;
```
