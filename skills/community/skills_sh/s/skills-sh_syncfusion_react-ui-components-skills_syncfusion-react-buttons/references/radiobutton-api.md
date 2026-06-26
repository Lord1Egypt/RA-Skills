# API Reference — Syncfusion React RadioButton

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [ChangeArgs Interface](#changeargs-interface)
- [RadioLabelPosition Type](#radiolabelposition-type)

---

## Import

```tsx
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';
```

---

## Properties

### checked
**Type:** `boolean` | **Default:** `false`

Specifies whether the RadioButton is in the checked (selected) state. When `true`, the inner circle indicator is displayed.

```tsx
<RadioButtonComponent label="Selected" name="group" checked={true} />
```

---

### cssClass
**Type:** `string` | **Default:** `''`

Defines one or more CSS class names (space-separated) applied to the RadioButton element. Use this to add custom styles or apply built-in size/variant classes like `e-small`.

```tsx
<RadioButtonComponent label="Custom" name="group" cssClass="e-small my-custom-class" />
```

---

### disabled
**Type:** `boolean` | **Default:** `false`

When `true`, the RadioButton is rendered in a disabled state — grayed out and non-interactive. Disabled buttons are excluded from form submissions.

```tsx
<RadioButtonComponent label="Unavailable" name="group" disabled={true} />
```

---

### enableHtmlSanitizer
**Type:** `boolean` | **Default:** `true`

When `true`, the component sanitizes any suspected untrusted HTML strings before rendering them. Disable only if you have full control over the `label` content and need to render raw HTML.

```tsx
<RadioButtonComponent label="Safe Label" name="group" enableHtmlSanitizer={true} />
```

---

### enablePersistence
**Type:** `boolean` | **Default:** `false`

When `true`, the component's checked state is persisted in browser storage and restored on page reload.

```tsx
<RadioButtonComponent label="Remember Me" name="persist" enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean` | **Default:** `false`

Enables right-to-left (RTL) rendering. The layout and text direction are flipped for RTL languages (Arabic, Hebrew, Persian, etc.).

```tsx
<RadioButtonComponent label="خيار" name="rtl" enableRtl={true} />
```

---

### htmlAttributes
**Type:** `{ [key: string]: string }` | **Default:** `{}`

Additional HTML attributes to apply to the underlying `<input>` element. If a property and its equivalent HTML attribute are both set, the component property value takes precedence.

```tsx
<RadioButtonComponent
  label="Required Option"
  name="form"
  htmlAttributes={{ required: 'required', 'data-id': 'option-1' }}
/>
```

---

### label
**Type:** `string` | **Default:** `''`

Caption text displayed alongside the RadioButton. Describes its purpose to the user. Internally handled for accessibility (proper `for`/`id` binding).

```tsx
<RadioButtonComponent label="Accept Terms and Conditions" name="terms" />
```

---

### labelPosition
**Type:** `RadioLabelPosition` (`'Before'` | `'After'`) | **Default:** `'After'`

Controls where the label text appears relative to the radio indicator:
- `'After'` (default) — label is to the **right**
- `'Before'` — label is to the **left**

```tsx
<RadioButtonComponent label="Left Label" name="pos" labelPosition="Before" />
<RadioButtonComponent label="Right Label" name="pos" labelPosition="After" />
```

---

### locale
**Type:** `string` | **Default:** `''`

Overrides the global culture/localization for this specific component instance. Default global culture is `'en-US'`.

```tsx
<RadioButtonComponent label="Option" name="group" locale="ar" />
```

---

### name
**Type:** `string` | **Default:** `''`

Groups RadioButton components as mutually exclusive options. All buttons sharing the same `name` value form a selection group — selecting one deselects all others. Also used as the form field name during submission.

```tsx
<RadioButtonComponent label="Option A" name="payment" value="a" />
<RadioButtonComponent label="Option B" name="payment" value="b" />
```

---

### value
**Type:** `string` | **Default:** `''`

The value submitted to the server when this RadioButton is checked and the form is submitted. Retrieved server-side using the `name` attribute.

```tsx
<RadioButtonComponent label="Credit Card" name="payment" value="credit" />
```

---

## Methods

### click()
**Returns:** `void`

Programmatically clicks the RadioButton (native browser click). This selects the button and triggers the `change` event.

```tsx
const radioRef = useRef<RadioButtonComponent>(null);

// Trigger a click programmatically
radioRef.current?.click();
```

---

### destroy()
**Returns:** `void`

Destroys the RadioButton component and releases all associated resources. Use during component unmount in class components or cleanup in hooks.

```tsx
const radioRef = useRef<RadioButtonComponent>(null);

useEffect(() => {
  return () => {
    radioRef.current?.destroy();
  };
}, []);
```

---

### focusIn()
**Returns:** `void`

Sets focus on the RadioButton element programmatically (native browser focus behavior).

```tsx
const radioRef = useRef<RadioButtonComponent>(null);

const focusButton = () => {
  radioRef.current?.focusIn();
};
```

---

### getSelectedValue()
**Returns:** `string`

Returns the `value` of the currently selected (checked) RadioButton within the same `name` group. Call on any button in the group to get the group's current selection.

```tsx
const radioRef = useRef<RadioButtonComponent>(null);

const logSelected = () => {
  const selected = radioRef.current?.getSelectedValue();
  console.log('Selected value:', selected);
};

return (
  <div>
    <RadioButtonComponent label="A" name="group" value="a" checked={true} ref={radioRef} />
    <RadioButtonComponent label="B" name="group" value="b" />
    <button onClick={logSelected}>Get Selected</button>
  </div>
);
```

---

## Events

### change
**Type:** `EmitType<ChangeArgs>`

Fires when the user changes the RadioButton state (selects a different option). Receives a `ChangeArgs` object.

```tsx
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';

function App() {
  const handleChange = (args: ChangeArgs) => {
    console.log('New value:', args.value);
    console.log('Event:', args.event);
  };

  return (
    <RadioButtonComponent
      label="Option"
      name="group"
      value="option1"
      change={handleChange}
    />
  );
}
```

> **Note:** The `change` event fires only on **user interaction**, not when `checked` is set programmatically via props.

---

### created
**Type:** `EmitType<Event>`

Fires once after the component has finished rendering. Use for post-render initialization or logging.

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const onCreated = () => {
    console.log('RadioButton is ready');
  };

  return (
    <RadioButtonComponent
      label="Option"
      name="group"
      created={onCreated}
    />
  );
}
```

---

## ChangeArgs Interface

Argument object passed to the `change` event handler.

| Property | Type | Description |
|----------|------|-------------|
| `value` | `string` | The `value` prop of the newly selected RadioButton |
| `event` | `Event` | The native DOM event that triggered the change |
| `name` | `string` | The name of the event (`'change'`) |

```tsx
const handleChange = (args: ChangeArgs) => {
  console.log(args.value);  // e.g., "credit"
  console.log(args.event);  // MouseEvent or KeyboardEvent
  console.log(args.name);   // "change"
};
```

---

## RadioLabelPosition Type

```ts
type RadioLabelPosition = 'Before' | 'After';
```

| Value | Effect |
|-------|--------|
| `'Before'` | Label appears to the left of the radio indicator |
| `'After'` | Label appears to the right of the radio indicator (default) |

---

## Full Example

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';
import { useState, useRef } from 'react';

enableRipple(true);

function App() {
  const [selected, setSelected] = useState<string>('monthly');
  const radioRef = useRef<RadioButtonComponent>(null);

  const handleChange = (args: ChangeArgs) => {
    setSelected(args.value);
  };

  const readCurrent = () => {
    alert('Selected: ' + radioRef.current?.getSelectedValue());
  };

  return (
    <div>
      <p>Plan: {selected}</p>
      <ul>
        <li>
          <RadioButtonComponent
            label="Monthly"
            name="plan"
            value="monthly"
            checked={selected === 'monthly'}
            change={handleChange}
            ref={radioRef}
          />
        </li>
        <li>
          <RadioButtonComponent
            label="Yearly (Save 20%)"
            name="plan"
            value="yearly"
            checked={selected === 'yearly'}
            change={handleChange}
          />
        </li>
        <li>
          <RadioButtonComponent
            label="Enterprise (Contact us)"
            name="plan"
            value="enterprise"
            disabled={true}
          />
        </li>
      </ul>
      <button onClick={readCurrent}>Check Selected via Method</button>
    </div>
  );
}
export default App;
```

---

## Official Documentation

- [API Reference](https://ej2.syncfusion.com/react/documentation/api/radio-button/index-default)
- [Component Overview](https://ej2.syncfusion.com/react/documentation/radio-button/)
- [ChangeArgs](https://ej2.syncfusion.com/react/documentation/api/radio-button/changeargs)
