# API Reference – Syncfusion React Floating Action Button

Source: [https://ej2.syncfusion.com/react/documentation/api/floating-action-button/index-default](https://ej2.syncfusion.com/react/documentation/api/floating-action-button/index-default)

## Table of Contents
- [Component Import](#component-import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)

---

## Component Import

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
```

---

## Properties

### content `string`
Defines the text content of the FAB button element.

- **Default:** `""`
- **Use:** Display a text label on the FAB, either alone or alongside an icon.

```tsx
<FabComponent id="fab" content="Add" />
```

---

### cssClass `string`
Defines one or more CSS classes (space-separated) applied to the FAB element. Used to apply predefined styles or custom styles.

**Predefined values:** `e-primary`, `e-outline`, `e-info`, `e-success`, `e-warning`, `e-danger`

- **Default:** `""`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" cssClass="e-danger" />
```

---

### disabled `boolean`
Specifies whether the FAB is disabled. When `true`, the FAB is non-interactive and `aria-disabled` is set automatically.

- **Default:** `false`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" disabled={true} />
```

---

### enableHtmlSanitizer `boolean`
When `true`, the component sanitizes any suspected untrusted HTML strings in `content` before rendering. Keep this enabled (default) to prevent XSS.

- **Default:** `true`

```tsx
<FabComponent id="fab" content="<b>Add</b>" enableHtmlSanitizer={true} />
```

---

### enablePersistence `boolean`
When `true`, persists the component state (e.g., `visible`) between page reloads using browser storage.

- **Default:** `false`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" enablePersistence={true} />
```

---

### enableRtl `boolean`
Renders the FAB in right-to-left direction when `true`. Use for RTL language support.

- **Default:** `false`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" content="تحرير" enableRtl={true} />
```

---

### iconCss `string`
Defines one or more CSS classes (space-separated) for the FAB icon. Supports Syncfusion built-in icon classes (`e-icons e-*`) and custom icon fonts.

- **Default:** `""`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" />
```

---

### iconPosition `string | IconPosition`
Positions the icon relative to the text content.

| Value | Description |
|-------|-------------|
| `'Left'` | Icon to the left of text (default) |
| `'Right'` | Icon to the right of text |

- **Default:** `IconPosition.Left` (`"Left"`)

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" content="Edit" iconPosition="Right" />
```

---

### isPrimary `boolean`
Applies primary styling to the FAB. This is enabled by default, giving the FAB its characteristic filled primary color.

- **Default:** `true`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" isPrimary={false} />
```

---

### isToggle `boolean`
Makes the FAB a toggle button. When `true`, clicking the FAB alternates between normal and active states.

- **Default:** `false`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" isToggle={true} />
```

---

### position `string | FabPosition`
Defines the position of the FAB relative to the `target` element or browser viewport.

| Value | Description |
|-------|-------------|
| `'TopLeft'` | Top-left corner |
| `'TopCenter'` | Top-center |
| `'TopRight'` | Top-right corner |
| `'MiddleLeft'` | Middle-left |
| `'MiddleCenter'` | Center |
| `'MiddleRight'` | Middle-right |
| `'BottomLeft'` | Bottom-left corner |
| `'BottomCenter'` | Bottom-center |
| `'BottomRight'` | Bottom-right corner (default) |

- **Default:** `FabPosition.BottomRight` (`"BottomRight"`)

```tsx
<FabComponent id="fab" content="Add" position="BottomLeft" target="#container" />
```

---

### target `string | HTMLElement`
Defines the selector or element reference that the FAB positions itself within. Without a `target`, the FAB positions relative to the browser viewport.

> The target element must have `position: relative` in its CSS.

- **Default:** `""`

```tsx
<FabComponent id="fab" content="Add" target="#targetElement" />
```

---

### visible `boolean`
Controls FAB visibility. Set to `false` to hide the FAB without destroying it.

- **Default:** `true`

```tsx
<FabComponent id="fab" iconCss="e-icons e-edit" visible={false} />
```

---

## Methods

### click()
Programmatically clicks the FAB element (native click method).

- **Returns:** `void`

```tsx
fabRef.current?.click();
```

---

### destroy()
Destroys the FAB component instance and cleans up all event listeners and DOM changes.

- **Returns:** `void`

```tsx
fabRef.current?.destroy();
```

---

### focusIn()
Sets focus to the FAB button element (native focus method).

- **Returns:** `void`

```tsx
fabRef.current?.focusIn();
```

---

### getPersistData()
Returns a JSON string of the properties that are maintained in the persisted state (relevant when `enablePersistence={true}`).

- **Returns:** `string`

```tsx
const persistedData = fabRef.current?.getPersistData();
console.log(persistedData);
```

---

### refreshPosition()
Recalculates and reapplies the FAB's position. Call this method when the `target` container is resized dynamically.

- **Returns:** `void`

```tsx
fabRef.current?.refreshPosition();
```

---

## Events

### created `EmitType<Event>`
Triggers once the FAB component has fully rendered and is ready for interaction.

```tsx
function onCreate(): void {
  console.log('FAB is ready');
}

<FabComponent id="fab" iconCss="e-icons e-edit" created={onCreate} />
```

---

### onClick `EmitType<Event>`
Triggers when the FAB is clicked by the user (mouse click or keyboard activation via Enter/Space).

```tsx
function handleClick(): void {
  console.log('FAB clicked');
}

<FabComponent id="fab" iconCss="e-icons e-edit" onClick={handleClick} />
```

---

## Complete Usage Example

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  const fabRef = React.useRef<FabComponent>(null);

  function onCreate(): void {
    console.log('FAB ready');
  }

  function handleClick(): void {
    console.log('FAB clicked');
  }

  function handleRefresh(): void {
    fabRef.current?.refreshPosition();
  }

  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <button onClick={handleRefresh}>Refresh Position</button>
      <FabComponent
        ref={fabRef}
        id="fab"
        iconCss="e-icons e-edit"
        content="Edit"
        iconPosition="Left"
        position="BottomRight"
        cssClass="e-primary"
        target="#target"
        visible={true}
        disabled={false}
        isPrimary={true}
        enableRtl={false}
        enableHtmlSanitizer={true}
        enablePersistence={false}
        created={onCreate}
        onClick={handleClick}
      />
    </div>
  );
}
export default App;
```
