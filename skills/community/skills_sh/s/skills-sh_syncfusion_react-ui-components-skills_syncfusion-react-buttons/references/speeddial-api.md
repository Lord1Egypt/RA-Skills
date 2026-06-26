# API Reference – Syncfusion React Speed Dial

## Table of Contents
- [SpeedDialComponent](#speeddialcomponent)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [SpeedDialItemModel](#speeddialitemmodel)
- [SpeedDialAnimationSettingsModel](#speeddialanimationsettingsmodel)
- [RadialSettingsModel](#radialsettingsmodel)
- [Event Argument Types](#event-argument-types)

---

## SpeedDialComponent

**Import:**
```tsx
import { SpeedDialComponent } from '@syncfusion/ej2-react-buttons';
```

**Basic usage:**
```tsx
<SpeedDialComponent content='Edit'></SpeedDialComponent>
```

---

## Properties

### animation
**Type:** `SpeedDialAnimationSettingsModel`  
**Default:** `{ effect: 'Fade', duration: 400, delay: 0 }`  
Options to customize the animation when opening and closing the popup.

```tsx
const animation: SpeedDialAnimationSettingsModel = { effect: 'Zoom' };
<SpeedDialComponent items={items} animation={animation} />
```

---

### closeIconCss
**Type:** `string`  
**Default:** `''`  
CSS class(es) to display an icon when the Speed Dial is open (popup visible).

```tsx
<SpeedDialComponent openIconCss='e-icons e-edit' closeIconCss='e-icons e-close' items={items} />
```

---

### content
**Type:** `string`  
**Default:** `''`  
Text content displayed on the Speed Dial button.

```tsx
<SpeedDialComponent content='Edit' items={items} />
```

---

### cssClass
**Type:** `string`  
**Default:** `''`  
One or more CSS classes to customize the Speed Dial's appearance. Predefined values: `e-primary`, `e-outline`, `e-info`, `e-success`, `e-warning`, `e-danger`.

```tsx
<SpeedDialComponent content='Edit' cssClass='e-warning' items={items} />
```

---

### direction
**Type:** `string | LinearDirection`  
**Default:** `LinearDirection.Auto`  
Direction for item display in Linear mode. Values: `Up`, `Down`, `Left`, `Right`, `Auto`.

```tsx
<SpeedDialComponent items={items} mode='Linear' direction='Up' />
```

---

### disabled
**Type:** `boolean`  
**Default:** `false`  
Disables the Speed Dial button, preventing all user interaction.

```tsx
<SpeedDialComponent content='Edit' disabled={true} items={items} />
```

---

### enablePersistence
**Type:** `boolean`  
**Default:** `false`  
Persists the component's state between page reloads.

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`  
Renders the component in right-to-left direction for RTL language support.

```tsx
<SpeedDialComponent content='Edit' enableRtl={true} items={items} />
```

---

### iconPosition
**Type:** `string | IconPosition`  
**Default:** `IconPosition.Left`  
Position of the icon relative to text in the button. Values: `Left`, `Right`.

```tsx
<SpeedDialComponent content='Edit' openIconCss='e-icons e-edit' iconPosition='Right' items={items} />
```

---

### isPrimary
**Type:** `boolean`  
**Default:** `true`  
Specifies whether the Speed Dial acts as the primary action button.

---

### itemTemplate
**Type:** `string | function | JSX.Element`  
**Default:** `''`  
Template for customizing the content of each Speed Dial action item.

```tsx
function itemTemplate(props: any): JSX.Element {
  return <div>{props.properties.text}</div>;
}
<SpeedDialComponent items={items} itemTemplate={itemTemplate} />
```

---

### items
**Type:** `SpeedDialItemModel[]`  
**Default:** `[]`  
Array of action items to display in the Speed Dial popup.

```tsx
const items: SpeedDialItemModel[] = [
  { text: 'Cut', iconCss: 'e-icons e-cut' }
];
<SpeedDialComponent items={items} />
```

---

### locale
**Type:** `string`  
**Default:** `''`  
Overrides the global culture/localization value. Default is `'en-US'`.

---

### modal
**Type:** `boolean`  
**Default:** `false`  
When `true`, displays a semi-transparent overlay behind the popup and blocks interaction with other page elements. Clicking the overlay closes the popup.

```tsx
<SpeedDialComponent items={items} openIconCss='e-icons e-edit' modal={true} />
```

---

### mode
**Type:** `string | SpeedDialMode`  
**Default:** `SpeedDialMode.Linear`  
Display mode of the action items. Values: `Linear`, `Radial`.

```tsx
<SpeedDialComponent items={items} mode='Radial' />
```

---

### openIconCss
**Type:** `string`  
**Default:** `''`  
CSS class(es) to display an icon when the Speed Dial is closed (button state).

```tsx
<SpeedDialComponent openIconCss='e-icons e-edit' items={items} />
```

---

### opensOnHover
**Type:** `boolean`  
**Default:** `false`  
When `true`, opens the popup when the user hovers over the button instead of clicking.

```tsx
<SpeedDialComponent items={items} openIconCss='e-icons e-edit' opensOnHover={true} />
```

---

### popupTemplate
**Type:** `string | function | JSX.Element`  
**Default:** `''`  
Template for the entire popup container. When set, replaces the items list entirely.

```tsx
function popupTemplate(): JSX.Element {
  return <div className="custom-popup">Custom content</div>;
}
<SpeedDialComponent content='Edit' popupTemplate={popupTemplate} />
```

---

### position
**Type:** `string | FabPosition`  
**Default:** `FabPosition.BottomRight`  
Position of the Speed Dial button relative to the `target` element (or viewport if no target). Values: `TopLeft`, `TopCenter`, `TopRight`, `MiddleLeft`, `MiddleCenter`, `MiddleRight`, `BottomLeft`, `BottomCenter`, `BottomRight`.

```tsx
<SpeedDialComponent content='Add' position='BottomLeft' target="#targetElement" />
```

---

### radialSettings
**Type:** `RadialSettingsModel`  
**Default:** `{ startAngle: null, endAngle: null, direction: 'Auto' }`  
Customizes action item layout when `mode='Radial'`. See [RadialSettingsModel](#radialsettingsmodel).

```tsx
const radialSettings: RadialSettingsModel = { offset: '80px', direction: 'AntiClockwise' };
<SpeedDialComponent items={items} mode='Radial' radialSettings={radialSettings} />
```

---

### target
**Type:** `string | HTMLElement`  
**Default:** `''`  
CSS selector or element reference that the Speed Dial button is positioned within. The target element must have `position: relative`.

```tsx
<SpeedDialComponent items={items} target="#targetElement" />
```

---

### visible
**Type:** `boolean`  
**Default:** `true`  
Controls whether the Speed Dial button is visible. Set to `false` to hide it.

```tsx
<SpeedDialComponent content='Edit' visible={false} items={items} />
```

---

## Methods

### show()
**Returns:** `void`  
Opens the Speed Dial popup programmatically.

```tsx
let speeddialRef: SpeedDialComponent;
// ...
speeddialRef.show();
```

---

### hide()
**Returns:** `void`  
Closes the Speed Dial popup programmatically.

```tsx
speeddialRef.hide();
```

---

### refreshPosition()
**Returns:** `void`  
Recalculates and updates the button's position relative to its target. Call this after the target element's size or layout changes programmatically.

```tsx
speeddialRef.refreshPosition();
```

> The browser automatically refreshes position on window resize; this method is for manual layout changes only.

---

## Events

### beforeClose
**Type:** `EmitType<SpeedDialBeforeOpenCloseEventArgs>`  
Fires before the Speed Dial popup closes. Set `args.cancel = true` to prevent closing.

### beforeItemRender
**Type:** `EmitType<SpeedDialItemEventArgs>`  
Fires before each action item is rendered. Use to modify item data dynamically.

### beforeOpen
**Type:** `EmitType<SpeedDialBeforeOpenCloseEventArgs>`  
Fires before the Speed Dial popup opens. Set `args.cancel = true` to prevent opening.

### clicked
**Type:** `EmitType<SpeedDialItemEventArgs>`  
Fires when the user clicks an action item. `args.item` contains item details.

### created
**Type:** `EmitType<Event>`  
Fires after the Speed Dial component finishes rendering.

### onClose
**Type:** `EmitType<SpeedDialOpenCloseEventArgs>`  
Fires after the Speed Dial popup closes.

### onOpen
**Type:** `EmitType<SpeedDialOpenCloseEventArgs>`  
Fires after the Speed Dial popup opens.

---

## SpeedDialItemModel

**Import:** `import { SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';`

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | `string` | — | Text label for the item |
| `iconCss` | `string` | — | CSS class(es) for the item icon |
| `id` | `string` | — | Unique identifier for the item (available in event args) |
| `title` | `string` | — | Tooltip text shown on hover |
| `disabled` | `boolean` | `false` | Disables the item when `true` |

---

## SpeedDialAnimationSettingsModel

**Import:** `import { SpeedDialAnimationSettingsModel } from '@syncfusion/ej2-react-buttons';`

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `effect` | `SpeedDialAnimationEffect` | `'Fade'` | Animation effect type (e.g., `'Fade'`, `'Zoom'`, `'None'`) |
| `duration` | `number` | `400` | Duration of the animation in milliseconds |
| `delay` | `number` | `0` | Delay before animation starts (ms) |

---

## RadialSettingsModel

**Import:** `import { RadialSettingsModel } from '@syncfusion/ej2-react-buttons';`

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `direction` | `RadialDirection` | `'Auto'` | Item arrangement direction: `'Clockwise'`, `'AntiClockwise'`, `'Auto'` |
| `startAngle` | `number` | `null` | Starting angle of the radial arc (0–360 degrees) |
| `endAngle` | `number` | `null` | Ending angle of the radial arc (0–360 degrees) |
| `offset` | `string` | — | Distance between items and the button (e.g., `'80px'`) |

---

## Event Argument Types

### SpeedDialItemEventArgs
Used by `clicked` and `beforeItemRender`.

| Property | Type | Description |
|----------|------|-------------|
| `item` | `SpeedDialItemModel` | The action item that triggered the event |
| `element` | `HTMLElement` | The DOM element of the item |

### SpeedDialBeforeOpenCloseEventArgs
Used by `beforeOpen` and `beforeClose`.

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | `boolean` | Set to `true` to cancel the open/close action |
| `element` | `HTMLElement` | The popup DOM element |

### SpeedDialOpenCloseEventArgs
Used by `onOpen` and `onClose`.

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | The popup DOM element |
