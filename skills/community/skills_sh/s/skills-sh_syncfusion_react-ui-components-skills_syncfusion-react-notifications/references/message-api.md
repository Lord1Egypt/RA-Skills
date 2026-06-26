# API Reference — Syncfusion React MessageComponent

Source: [https://ej2.syncfusion.com/react/documentation/api/message/index-default](https://ej2.syncfusion.com/react/documentation/api/message/index-default)

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Types and Enums](#types-and-enums)

---

## Import

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
```

---

## Properties

### content
**Type:** `string | function | JSX.Element`  
**Default:** `null`

Specifies the content to be displayed in the Message component. Accepts a plain string, a render function that returns JSX, or a JSX element directly.

```tsx
{/* String */}
<MessageComponent content="Please read the comments carefully" />

{/* Render function */}
const template = () => <div><strong>Note:</strong> Action cannot be undone.</div>;
<MessageComponent content={template} />
```

---

### cssClass
**Type:** `string`  
**Default:** `''`

Specifies one or more CSS classes (space-separated) to append to the root element of the Message component. Use for custom styling, content alignment, or appearance overrides.

```tsx
<MessageComponent content="Warning" cssClass="e-content-center rounded" severity="Warning" />
```

Built-in alignment classes: `e-content-center`, `e-content-right`.

---

### enablePersistence
**Type:** `boolean`  
**Default:** `false`

When `true`, the component's state (including `visible`) is persisted across page reloads using browser storage.

```tsx
<MessageComponent content="Persistent message" enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`

Enables right-to-left rendering for RTL language support (Arabic, Hebrew, etc.).

```tsx
<MessageComponent content="مرحبا" enableRtl={true} />
```

---

### locale
**Type:** `string`  
**Default:** `''`

Overrides the global culture and localization value for this component. Defaults to `'en-US'` when empty.

```tsx
<MessageComponent content="Message" locale="fr-FR" />
```

---

### severity
**Type:** `string | Severity`  
**Default:** `Severity.Normal`

Specifies the severity of the message, which controls the icon and color scheme. Valid values:

| Value | Description |
|-------|-------------|
| `"Normal"` | Default — neutral/general message |
| `"Success"` | Positive outcome or confirmation |
| `"Info"` | Informational content |
| `"Warning"` | Caution or potential issue |
| `"Error"` | Critical failure or error |

```tsx
<MessageComponent content="Operation failed" severity="Error" />
```

---

### showCloseIcon
**Type:** `boolean`  
**Default:** `false`

Shows a close icon that allows users to dismiss the message. When clicked (or activated via keyboard), the `closed` event fires.

```tsx
<MessageComponent content="Session expiring" showCloseIcon={true} closed={() => setVisible(false)} />
```

---

### showIcon
**Type:** `boolean`  
**Default:** `true`

Shows or hides the severity icon displayed at the left edge of the message. Set to `false` for text-only appearance.

```tsx
<MessageComponent content="No icon" showIcon={false} />
```

---

### variant
**Type:** `string | Variant`  
**Default:** `Variant.Text`

Specifies the visual presentation variant. Valid values:

| Value | Description |
|-------|-------------|
| `"Text"` | Subtle styling — light background with colored text (default) |
| `"Outlined"` | Colored border with transparent background |
| `"Filled"` | Bold — dark background with contrasting text |

```tsx
<MessageComponent content="Critical error" severity="Error" variant="Filled" />
```

---

### visible
**Type:** `boolean`  
**Default:** `true`

Controls the visibility of the Message component. When `false`, the message is hidden but remains mounted in the DOM.

```tsx
<MessageComponent content="Done" severity="Success" visible={isComplete} />
```

---

## Methods

### destroy()
**Returns:** `void`

Destroys the Message component instance — removes it from the DOM and detaches all bound events, attributes, and classes.

```tsx
const msgRef = useRef<MessageComponent>(null);

// Call to clean up
msgRef.current?.destroy();
```

---

### getPersistData()
**Returns:** `string`

Returns a JSON string of the component's persisted state properties. Useful for debugging or manually saving state.

```tsx
const data = msgRef.current?.getPersistData();
console.log(data);
```

---

## Events

### closed
**Type:** `EmitType<MessageCloseEventArgs>`

Fires when the Message component is closed (dismissed) by the user via the close icon.

```tsx
<MessageComponent
  content="Dismissible message"
  showCloseIcon={true}
  closed={(args: MessageCloseEventArgs) => {
    console.log('Message closed', args);
    setVisible(false);
  }}
/>
```

---

### created
**Type:** `EmitType<Object>`

Fires when the Message component has been successfully created and mounted.

```tsx
<MessageComponent
  content="Hello"
  created={() => console.log('Message created')}
/>
```

---

### destroyed
**Type:** `EmitType<Event>`

Fires when the Message component is destroyed via the `destroy()` method.

```tsx
<MessageComponent
  content="Hello"
  destroyed={() => console.log('Message destroyed')}
/>
```

---

## Types and Enums

### Severity Enum

```ts
enum Severity {
  Normal  = 'Normal',
  Success = 'Success',
  Info    = 'Info',
  Warning = 'Warning',
  Error   = 'Error'
}
```

### Variant Enum

```ts
enum Variant {
  Text     = 'Text',
  Outlined = 'Outlined',
  Filled   = 'Filled'
}
```

### MessageCloseEventArgs

The argument object passed to the `closed` event handler:

| Property | Type | Description |
|----------|------|-------------|
| (event args from closed event) | `object` | Standard event arguments provided when the message is closed |
