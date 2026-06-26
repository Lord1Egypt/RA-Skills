# MaskedTextBox API Reference

Source: https://ej2.syncfusion.com/react/documentation/api/maskedtextbox/index-default

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Event Argument Types](#event-argument-types)
- [Accessibility & WAI-ARIA](#accessibility--wai-aria)

## Import

```tsx
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
```

---

## Properties

### `mask` · string · Default: `null`

Sets the input mask to enforce input format. Accepts standard mask elements, custom characters, and regular expressions. When empty, behaves as a plain text input.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" />
```

---

### `value` · string · Default: `null`

Gets or sets the raw value of the MaskedTextBox — without literals and prompt characters. Use `getMaskedValue()` to retrieve the value in masked format.

```tsx
<MaskedTextBoxComponent mask="(999) 9999-999" value="8674321756" />
```

---

### `placeholder` · string · Default: `null`

Sets the hint text shown when the MaskedTextBox is empty. Acts as a floating label when used with `floatLabelType`.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" placeholder="Enter phone number" />
```

---

### `floatLabelType` · FloatLabelType · Default: `"Never"`

Controls floating label behavior. Options:
- `"Never"` — label does not float
- `"Always"` — label always floats above the input
- `"Auto"` — label floats when input is focused or has a value

```tsx
<MaskedTextBoxComponent mask="000-000-0000" placeholder="Phone" floatLabelType="Auto" />
```

---

### `promptChar` · string · Default: `"_"`

Sets the prompt symbol displayed at unfilled mask positions.

```tsx
<MaskedTextBoxComponent mask="999-999-9999" promptChar="#" />
```

---

### `customCharacters` · `{ [x: string]: Object }` · Default: `null`

Maps non-mask literal characters in the mask to their accepted input values. Each key is a mask character and the value is a comma-separated string of accepted characters.

```tsx
const chars = { P: 'P,A,p,a', M: 'M,m' };
<MaskedTextBoxComponent mask="00:00 >PM" customCharacters={chars} />
```

---

### `cssClass` · string · Default: `null`

Applies additional CSS classes to the root element for custom styling.

```tsx
<MaskedTextBoxComponent mask="00000" cssClass="e-style" />
```

---

### `enabled` · boolean · Default: `true`

Enables or disables the MaskedTextBox component.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" enabled={false} />
```

---

### `readonly` · boolean · Default: `false`

When `true`, the user cannot change the input value.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" value="123-456-7890" readonly={true} />
```

---

### `showClearButton` · boolean · Default: `false`

When `true`, displays a clear (×) icon inside the input to reset the value.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" showClearButton={true} />
```

---

### `enableRtl` · boolean · Default: `false`

Renders the component in right-to-left direction.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" enableRtl={true} />
```

---

### `enablePersistence` · boolean · Default: `false`

When `true`, persists the `value` state in browser storage and restores it after page reload.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" enablePersistence={true} />
```

---

### `htmlAttributes` · `{ [key: string]: string }` · Default: `{}`

Passes additional HTML attributes to the underlying input element. If a property is also set directly, the property value takes precedence.

```tsx
// Add name, tabindex, and readonly via HTML attributes
const attrs = { name: 'phonenumber', tabindex: '-1' };
<MaskedTextBoxComponent mask="000000" htmlAttributes={attrs} value="6000021" />

// Show numeric keypad on mobile devices
<MaskedTextBoxComponent mask="999-99999" htmlAttributes={{ type: 'tel' }} />
```

---

### `locale` · string · Default: `""`

Overrides the global culture/localization for this component. Default is `'en-US'`.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" locale="en-US" />
```

---

### `width` · number | string · Default: `null`

Sets the width of the MaskedTextBox.

```tsx
<MaskedTextBoxComponent mask="000-000-0000" width="300px" />
<MaskedTextBoxComponent mask="000-000-0000" width={300} />
```

---

### `prependTemplate` · string | function | JSX.Element · Default: `null`

Renders custom content (icons, buttons, HTML) **before** the masked input. Updates dynamically.

```tsx
const prepend = () => <span className="e-icons e-user" />;
<MaskedTextBoxComponent mask="000-000-0000" prependTemplate={prepend} />
```

---

### `appendTemplate` · string | function | JSX.Element · Default: `null`

Renders custom content (icons, buttons, HTML) **after** the masked input. Updates dynamically.

```tsx
const append = () => <span className="e-icons e-send" />;
<MaskedTextBoxComponent mask="000-000-0000" appendTemplate={append} />
```

---

## Methods

Methods are accessed via a component `ref`.

```tsx
const maskRef = React.useRef(null);
<MaskedTextBoxComponent ref={maskRef} mask="000-000-0000" />

// Call methods:
maskRef.current.focusIn();
```

### `focusIn()` → void

Programmatically sets focus to the MaskedTextBox.

```tsx
// Auto-focus on mount
useEffect(() => {
  maskRef.current.focusIn();
}, []);
```

---

### `focusOut()` → void

Removes focus from the MaskedTextBox if it is currently focused.

```tsx
maskRef.current.focusOut();
```

---

### `getMaskedValue()` → string

Returns the current value in masked format (including literals like dashes). Use `value` property for the raw value without literals.

```tsx
// mask="000-000-0000", user typed "1234567890"
const raw    = maskRef.current.value;            // "1234567890"
const masked = maskRef.current.getMaskedValue(); // "123-456-7890"
```

---

### `destroy()` → void

Removes the component from the DOM and detaches all event handlers. Restores the original input element.

```tsx
maskRef.current.destroy();
```

---

### `getPersistData()` → string

Returns the properties that are maintained in the persisted state (used internally for `enablePersistence`).

```tsx
const persisted = maskRef.current.getPersistData();
```

---

## Events

### `change` · EmitType\<MaskChangeEventArgs\>

Fires when the value of the MaskedTextBox changes.

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  change={(args) => {
    console.log(args.value);       // raw value
    console.log(args.maskedValue); // value with mask literals
  }}
/>
```

---

### `focus` · EmitType\<MaskFocusEventArgs\>

Fires when the MaskedTextBox receives focus. Use `selectionStart` and `selectionEnd` from the event args to control cursor position.

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  focus={(args) => {
    // Position cursor at the beginning
    args.selectionEnd = args.selectionStart = 0;
  }}
/>
```

---

### `blur` · EmitType\<MaskBlurEventArgs\>

Fires when the MaskedTextBox loses focus.

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  blur={(args) => {
    console.log('Blurred. Value:', args.value);
  }}
/>
```

---

### `created` · EmitType\<Object\>

Fires when the MaskedTextBox component is created and rendered.

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  created={() => console.log('MaskedTextBox created')}
/>
```

---

### `destroyed` · EmitType\<Object\>

Fires when the MaskedTextBox component is destroyed.

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  destroyed={() => console.log('MaskedTextBox destroyed')}
/>
```

---

## Event Argument Types

### MaskChangeEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `value` | string | Raw value without literals and prompt characters |
| `maskedValue` | string | Value including mask literals |
| `isInteracted` | boolean | Whether the change was triggered by user interaction |

### MaskFocusEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `selectionStart` | number | Cursor start position (writable — set to control cursor) |
| `selectionEnd` | number | Cursor end position (writable — set to control cursor) |
| `maskedValue` | string | Full masked string including literals |
| `value` | string | Raw value |
| `container` | HTMLElement | The wrapper container element |
| `event` | FocusEvent | Native browser focus event |

### MaskBlurEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `value` | string | Raw value at the time of blur |
| `maskedValue` | string | Masked value at the time of blur |
| `container` | HTMLElement | The wrapper container element |
| `event` | FocusEvent | Native browser blur event |

---

## Accessibility & WAI-ARIA

The MaskedTextBox fully supports WCAG 2.2, Section 508, and WAI-ARIA standards. It uses the `textbox` role.

| ARIA Attribute | Usage |
|----------------|-------|
| `aria-live` | Indicates priority of live region updates |
| `aria-disabled` | Reflects the `enabled` property state |
| `aria-valuenow` | Reflects the current value |
| `aria-invalid` | Marks input as invalid when validation fails |
| `aria-placeholder` | Short hint when no value is entered |
| `aria-labelledby` | Points to the floating label element |

**Compliance summary:**
- WCAG 2.2 ✅
- Section 508 ✅
- Screen Reader Support ✅
- Right-To-Left (`enableRtl`) ✅
- Color Contrast ✅
- Mobile Device Support ✅
- Keyboard Navigation ✅
