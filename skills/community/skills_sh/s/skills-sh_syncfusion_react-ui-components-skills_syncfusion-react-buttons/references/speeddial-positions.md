# Positions and Visibility Control – Syncfusion React Speed Dial

## Table of Contents
- [Position Values](#position-values)
- [Target-Relative Positioning](#target-relative-positioning)
- [Opens on Hover](#opens-on-hover)
- [Programmatic Show and Hide](#programmatic-show-and-hide)
- [Refresh Position](#refresh-position)

---

## Position Values

Use the `position` property to place the Speed Dial button within its target (or the viewport if no target is set).

Available values:

| Value | Placement |
|-------|-----------|
| `TopLeft` | Top-left corner |
| `TopCenter` | Top-center |
| `TopRight` | Top-right corner |
| `MiddleLeft` | Middle of left edge |
| `MiddleCenter` | Center |
| `MiddleRight` | Middle of right edge |
| `BottomLeft` | Bottom-left corner |
| `BottomCenter` | Bottom-center |
| `BottomRight` | Bottom-right corner (default) |

```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' content='Add' position='BottomLeft' target="#targetElement" />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Target-Relative Positioning

When `target` is set, position is relative to that container. Without `target`, position is relative to the browser viewport.

**The target element must have `position: relative`** for correct layout.

```tsx
// Positions relative to #container, not the page
<div id="container" style={{ position: 'relative', minHeight: '400px' }}>
  <SpeedDialComponent id='speeddial' content='Add' position='BottomRight' target="#container" />
</div>
```

---

## Opens on Hover

By default, clicking the button opens the popup. Enable `opensOnHover` to automatically open when the user hovers:

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  return (
    <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
      items={items} opensOnHover={true} target="#targetElement" />
  );
}
export default App;
```

---

## Programmatic Show and Hide

Use `show()` and `hide()` methods to open or close the Speed Dial popup from code. Access the component via a `ref`:

```tsx
import { ButtonComponent, SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  let speeddialObj: SpeedDialComponent;
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  function showClick(): void {
    speeddialObj.show();
  }
  function hideClick(): void {
    speeddialObj.hide();
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '340px', border: '1px solid', padding: '10px' }}>
        <ButtonComponent id="show" cssClass="e-primary" onClick={showClick}>Show</ButtonComponent>
        <ButtonComponent id="hide" cssClass="e-primary" onClick={hideClick}>Hide</ButtonComponent>
      </div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} opensOnHover={true} target="#targetElement"
        ref={(scope) => { speeddialObj = scope; }} />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

---

## Refresh Position

Call `refreshPosition()` after the target container's size or layout changes to ensure correct button placement:

```tsx
import { ButtonComponent, SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  let speeddialObj: SpeedDialComponent;
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  function refresh(): void {
    document.getElementById("targetElement").style.minHeight = "300px";
    speeddialObj.refreshPosition();
  }

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '340px', border: '1px solid', padding: '10px' }}>
        <ButtonComponent id="refresh" cssClass="e-primary" onClick={refresh}>Refresh</ButtonComponent>
      </div>
      <SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' closeIconCss='e-icons e-close'
        items={items} position='MiddleRight' target="#targetElement"
        ref={scope => { speeddialObj = scope; }} />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

> The browser automatically refreshes the position on window resize; call `refreshPosition()` manually only for programmatic layout changes.
