# Switch API Reference

Complete API reference for the Syncfusion React `SwitchComponent`. All properties, methods, and events listed here are sourced directly from the official documentation at:
- https://ej2.syncfusion.com/react/documentation/api/switch/
- https://ej2.syncfusion.com/react/documentation/api/switch/changeeventargs
- https://ej2.syncfusion.com/react/documentation/api/switch/beforechangeeventargs

> **Critical rule:** Only use APIs explicitly listed in this file. Do not use undocumented or assumed properties.

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [ChangeEventArgs Interface](#changeeventargs-interface)
- [BeforeChangeEventArgs Interface](#beforechangeeventargs-interface)

---

## Import

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

// For event types:
import { ChangeEventArgs, BeforeChangeEventArgs } from '@syncfusion/ej2-react-buttons';

// For ripple utility (optional):
import { enableRipple } from '@syncfusion/ej2-base';
import { rippleMouseHandler } from '@syncfusion/ej2-buttons';
```

---

## Properties

All properties are passed as JSX props to `<SwitchComponent>`.

### checked
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether the Switch is in the checked (on) state. When `true`, the Switch renders in its checked state.

```tsx
<SwitchComponent checked={true} />
```

---

### cssClass
- **Type:** `string`
- **Default:** `''`
- **Description:** Adds custom CSS classes to the Switch component. Use `"e-small"` for the compact size variant. Multiple classes can be space-separated.

```tsx
<SwitchComponent cssClass="e-small my-custom-class" />
```

---

### disabled
- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, the Switch is rendered in a disabled state — it cannot be toggled and is excluded from form submissions.

```tsx
<SwitchComponent disabled={true} />
```

---

### enablePersistence
- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, the component's state (checked value) is persisted in browser storage and restored on page reload.

```tsx
<SwitchComponent enablePersistence={true} />
```

---

### enableRtl
- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, renders the component in right-to-left direction. Used for RTL languages such as Arabic, Hebrew, and Persian.

```tsx
<SwitchComponent enableRtl={true} />
```

---

### htmlAttributes
- **Type:** `{ [key: string]: string }`
- **Default:** `{}`
- **Description:** Passes additional HTML attributes to the underlying element. If both property and equivalent HTML attribute are configured, the **property value takes precedence**.

```tsx
<SwitchComponent htmlAttributes={{ 'aria-label': 'Toggle notifications', 'data-testid': 'notif-switch' }} />
```

---

### locale
- **Type:** `string`
- **Default:** `''` (uses global culture `'en-US'`)
- **Description:** Overrides the global culture and localization value for this specific component instance.

```tsx
<SwitchComponent locale="fr-FR" />
```

---

### name
- **Type:** `string`
- **Default:** `''`
- **Description:** Defines the `name` attribute for the Switch. Used to reference form data after a form is submitted.

```tsx
<SwitchComponent name="wifi-toggle" />
```

---

### offLabel
- **Type:** `string`
- **Default:** `''`
- **Description:** Specifies the text displayed inside the Switch track when it is in the unchecked (off) state.

> **Note:** Not supported in Material themes. Does not support long text strings.

```tsx
<SwitchComponent offLabel="OFF" />
```

---

### onLabel
- **Type:** `string`
- **Default:** `''`
- **Description:** Specifies the text displayed inside the Switch track when it is in the checked (on) state.

> **Note:** Not supported in Material themes. Does not support long text strings.

```tsx
<SwitchComponent onLabel="ON" />
```

---

### value
- **Type:** `string`
- **Default:** `''`
- **Description:** Defines the `value` attribute for the Switch. This is the form data value submitted to the server. Only submitted when the Switch is checked and enabled.

```tsx
<SwitchComponent name="connection" value="wifi" checked={true} />
```

---

## Methods

Call methods via a component `ref`.

```tsx
let switchInstance: SwitchComponent;
<SwitchComponent ref={(scope) => { switchInstance = scope as SwitchComponent; }} />
```

### toggle()
- **Returns:** `void`
- **Description:** Toggles the Switch component state between checked and unchecked. Fires the `change` event after toggling.

```tsx
switchInstance.toggle();
```

---

### click()
- **Returns:** `void`
- **Description:** Triggers the Switch element's native click behavior programmatically.

```tsx
switchInstance.click();
```

---

### focusIn()
- **Returns:** `void`
- **Description:** Sets focus to the Switch element programmatically using its native method.

```tsx
switchInstance.focusIn();
```

---

### destroy()
- **Returns:** `void`
- **Description:** Destroys the Switch widget, releasing all event listeners and DOM references.

```tsx
switchInstance.destroy();
```

---

## Events

Attach event handlers as JSX props on `<SwitchComponent>`.

### change
- **Type:** `EmitType<ChangeEventArgs>`
- **Description:** Triggers when the Switch state has been changed by user interaction. See [`ChangeEventArgs`](#changeeventargs-interface) for argument details.

```tsx
<SwitchComponent change={(args: ChangeEventArgs) => console.log(args.checked)} />
```

---

### beforeChange
- **Type:** `EmitType<BeforeChangeEventArgs>`
- **Description:** Triggers **before** the state of the Switch changes. Set `args.cancel = true` to cancel the state transition. See [`BeforeChangeEventArgs`](#beforechangeeventargs-interface) for argument details.

```tsx
<SwitchComponent beforeChange={(args: BeforeChangeEventArgs) => { args.cancel = true; }} />
```

---

### created
- **Type:** `EmitType<Event>`
- **Description:** Triggers once after the component rendering is completed.

```tsx
<SwitchComponent created={() => console.log('Switch rendered')} />
```

---

## ChangeEventArgs Interface

**Import:** `import { ChangeEventArgs } from '@syncfusion/ej2-react-buttons';`

Represents the argument object passed to the `change` event handler.

| Property | Type | Description |
|----------|------|-------------|
| `checked` | `boolean` | The new checked state of the Switch after the change |
| `event` | `Event` | The original DOM event that triggered the state change |
| `name` | `string` | The name of the event (`"change"`) |

```tsx
import { ChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';

function onChange(args: ChangeEventArgs): void {
  console.log('New state:', args.checked);
  console.log('Event name:', args.name);
  console.log('Original event:', args.event);
}

<SwitchComponent change={onChange} />
```

---

## BeforeChangeEventArgs Interface

**Import:** `import { BeforeChangeEventArgs } from '@syncfusion/ej2-react-buttons';`

Represents the argument object passed to the `beforeChange` event handler.

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | `boolean` | Set to `true` to cancel the state change before it is finalized |
| `checked` | `boolean` | The **current** checked state of the Switch (before the change) |
| `event` | `Event` | The original DOM event that initiated the state change |

```tsx
import { BeforeChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';

function beforeChange(args: BeforeChangeEventArgs): void {
  console.log('Current state before change:', args.checked);

  // Cancel the change if needed
  if (someCondition) {
    args.cancel = true;
  }
}

<SwitchComponent beforeChange={beforeChange} checked={true} />
```

---

## Full Example Using All Key APIs

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import {
  ChangeEventArgs,
  BeforeChangeEventArgs,
  SwitchComponent
} from '@syncfusion/ej2-react-buttons';
import { useRef } from 'react';

enableRipple(true);

function App() {
  const switchRef = useRef<SwitchComponent>(null);

  function onChange(args: ChangeEventArgs): void {
    console.log('Switch changed to:', args.checked);
  }

  function beforeChange(args: BeforeChangeEventArgs): void {
    // Allow the change (remove this line to cancel)
    // args.cancel = true;
  }

  function onCreated(): void {
    console.log('Switch is ready');
  }

  function handleToggle(): void {
    switchRef.current?.toggle();
  }

  return (
    <div>
      <SwitchComponent
        ref={switchRef}
        checked={false}
        disabled={false}
        cssClass="e-small"
        onLabel="ON"
        offLabel="OFF"
        name="feature-toggle"
        value="enabled"
        enableRtl={false}
        enablePersistence={false}
        htmlAttributes={{ 'aria-label': 'Feature toggle' }}
        change={onChange}
        beforeChange={beforeChange}
        created={onCreated}
      />
      <button onClick={handleToggle}>Toggle Programmatically</button>
    </div>
  );
}
export default App;
```
