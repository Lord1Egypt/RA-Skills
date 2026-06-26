# OTP Input API Reference

## Table of Contents
- [Component](#component)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Type Enumerations](#type-enumerations)
- [Event Argument Types](#event-argument-types)

---

## Component

**Import:**
```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
```

**Basic usage:**
```tsx
<OtpInputComponent id="otpinput" value={value} />
```

---

## Properties

### ariaLabels `string[]`
Defines the ARIA-label attribute for each input field. Each string in the array corresponds to one input field's ARIA-label.

- **Default:** `[]`

```tsx
const ariaLabels = ['First digit', 'Second digit', 'Third digit', 'Fourth digit'];
<OtpInputComponent id="otpinput" ariaLabels={ariaLabels} />
```

---

### autoFocus `boolean`
Specifies whether the OTP input field should automatically receive focus when the component is rendered.

- **Default:** `false`

```tsx
<OtpInputComponent id="otpinput" autoFocus={true} />
```

---

### cssClass `string`
Defines one or more CSS classes to customize the appearance of the OTP Input component.

Predefined CSS classes:

| Class | Description |
|-------|-------------|
| `e-success` | Positive/success state styling |
| `e-warning` | Caution/warning state styling |
| `e-error` | Negative/error state styling |

- **Default:** `''`

```tsx
<OtpInputComponent id="otpinput" cssClass="e-success" />
```

---

### disabled `boolean`
Specifies whether the OTP Input component is disabled. When `true`, user input is not allowed.

- **Default:** `false`

```tsx
<OtpInputComponent id="otpinput" value={1234} disabled={true} />
```

---

### enablePersistence `boolean`
Enable or disable persisting the component's state between page reloads.

- **Default:** `false`

```tsx
<OtpInputComponent id="otpinput" enablePersistence={true} />
```

---

### enableRtl `boolean`
Enable or disable rendering the component in right-to-left direction.

- **Default:** `false`

```tsx
<OtpInputComponent id="otpinput" enableRtl={true} />
```

---

### htmlAttributes `{ [key: string]: string }`
Specifies additional HTML attributes to be applied to the OTP Input component as key-value pairs.

- **Default:** `{}`

```tsx
const htmlAttributes = { title: 'One-Time Password', 'data-testid': 'otp-input' };
<OtpInputComponent id="otpinput" htmlAttributes={htmlAttributes} />
```

---

### length `number`
Specifies the number of OTP input fields (i.e., the OTP code length).

- **Default:** `4`

```tsx
<OtpInputComponent id="otpinput" length={6} />
```

---

### locale `string`
Overrides the global culture and localization value for this component.

- **Default:** `''` (uses global culture `'en-US'`)

---

### placeholder `string`
Specifies hint text shown in each input field until the user enters a value.

- Single character: same character shown in all input fields.
- Multiple characters: each character maps to a corresponding input field sequentially.
- **Default:** `''`

```tsx
// Single character placeholder
<OtpInputComponent id="otpinput" placeholder="x" />

// Per-field placeholder
<OtpInputComponent id="otpinput" placeholder="wxyz" />
```

---

### separator `string`
Specifies the separator character displayed between each OTP input field.

- **Default:** `''`

```tsx
<OtpInputComponent id="otpinput" separator="/" />
```

---

### stylingMode `string | OtpInputStyle`
Specifies the visual style variant for the OTP input fields.

| Value | Description |
|-------|-------------|
| `'outlined'` | Outlined border style (default) |
| `'filled'` | Filled background style |
| `'underlined'` | Bottom border only style |

- **Default:** `OtpInputStyle.Outlined` (`'outlined'`)

```tsx
<OtpInputComponent id="otpinput" stylingMode="filled" />
```

---

### textTransform `string | TextTransform`
Specifies case transformation applied to the OTP input text.

| Value | Description |
|-------|-------------|
| `'none'` | No transformation (default) |
| `'uppercase'` | Converts input to uppercase |
| `'lowercase'` | Converts input to lowercase |

- **Default:** `TextTransform.None`

```tsx
<OtpInputComponent id="otpinput" type="text" textTransform="uppercase" />
```

---

### type `string | OtpInputType`
Specifies the input type for each OTP field.

| Value | Description |
|-------|-------------|
| `'number'` | Numeric digits only (default) |
| `'text'` | Alphanumeric characters |
| `'password'` | Masked input for security |

- **Default:** `OtpInputType.Number` (`'number'`)

```tsx
<OtpInputComponent id="otpinput" type="password" />
```

---

### value `string | number`
Specifies the current value of the OTP input. Can be a string or number.

- **Default:** `''`

```tsx
<OtpInputComponent id="otpinput" value={1234} />
<OtpInputComponent id="otpinput" value="AB12" type="text" />
```

---

## Methods

### destroy()
Destroys the OTP Input component and releases associated resources.

```tsx
import { useRef } from 'react';
const otpRef = useRef<OtpInputComponent>(null);
otpRef.current?.destroy();
```

---

### focusIn()
Sets focus to the OTP input for user interaction.

```tsx
otpRef.current?.focusIn();
```

---

### focusOut()
Removes focus from the OTP input if it is currently focused.

```tsx
otpRef.current?.focusOut();
```

---

## Events

### blur `EmitType<OtpFocusEventArgs>`
Triggered when the OTP input loses focus.

```tsx
const handleBlur = (args: OtpFocusEventArgs) => {
  console.log('Blurred from index:', args.index);
};
<OtpInputComponent id="otpinput" blur={handleBlur} />
```

---

### created `EmitType<Event>`
Triggered after the OTP Input component finishes rendering.

```tsx
const handleCreated = () => {
  console.log('OTP Input rendered');
};
<OtpInputComponent id="otpinput" created={handleCreated} />
```

---

### focus `EmitType<OtpFocusEventArgs>`
Triggered when the OTP input receives focus.

```tsx
const handleFocus = (args: OtpFocusEventArgs) => {
  console.log('Focused on index:', args.index);
};
<OtpInputComponent id="otpinput" focus={handleFocus} />
```

---

### input `EmitType<OtpInputEventArgs>`
Triggered each time the value of any individual OTP input field changes.

```tsx
const handleInput = (args: OtpInputEventArgs) => {
  console.log('Current value:', args.value);
};
<OtpInputComponent id="otpinput" input={handleInput} />
```

---

### valueChanged `EmitType<OtpChangedEventArgs>`
Triggered when the OTP value is complete (all fields filled) and the input loses focus.

```tsx
const handleValueChanged = (args: OtpChangedEventArgs) => {
  console.log('Complete OTP:', args.value);
};
<OtpInputComponent id="otpinput" valueChanged={handleValueChanged} />
```

---

## Type Enumerations

### OtpInputType
```tsx
import { OtpInputType } from '@syncfusion/ej2-react-inputs';
// Values: 'number' | 'text' | 'password'
```

### OtpInputStyle
```tsx
import { OtpInputStyle } from '@syncfusion/ej2-react-inputs';
// Values: 'outlined' | 'filled' | 'underlined'
```

### TextTransform
```tsx
import { TextTransform } from '@syncfusion/ej2-react-inputs';
// Values: 'none' | 'uppercase' | 'lowercase'
```

---

## Event Argument Types

### OtpFocusEventArgs
Used by `focus` and `blur` events.

| Property | Type | Description |
|----------|------|-------------|
| `event` | `FocusEvent` | The native DOM focus/blur event |
| `index` | `number` | The index of the focused/blurred input field |

### OtpInputEventArgs
Used by the `input` event.

| Property | Type | Description |
|----------|------|-------------|
| `event` | `InputEvent` | The native DOM input event |
| `value` | `string` | The current complete OTP value |

### OtpChangedEventArgs
Used by the `valueChanged` event.

| Property | Type | Description |
|----------|------|-------------|
| `value` | `string` | The final complete OTP value |
| `previousValue` | `string` | The previous OTP value before the change |
