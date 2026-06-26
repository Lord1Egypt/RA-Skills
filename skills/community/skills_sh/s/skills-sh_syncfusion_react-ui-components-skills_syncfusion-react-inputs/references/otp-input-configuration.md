# OTP Input Configuration & Appearance

## Table of Contents
- [Input Types](#input-types)
- [Styling Modes](#styling-modes)
- [Placeholder Text](#placeholder-text)
- [Separator Character](#separator-character)
- [Disabled State](#disabled-state)
- [CSS Class Customization](#css-class-customization)
- [Right-to-Left Support](#right-to-left-support)
- [Text Transform](#text-transform)
- [State Persistence](#state-persistence)

---

## Input Types

Use the `type` property to control what characters are accepted in each OTP field.

### Number (default)

Accepts only digits. Best for standard numeric OTP codes.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" type="number" value={1234} />
    </div>
  );
}

export default App;
```

### Text

Accepts letters and digits. Use when OTP codes are alphanumeric.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" type="text" value="e3c7" />
    </div>
  );
}

export default App;
```

### Password

Masks entered characters for security. Use in sensitive authentication flows.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" type="password" value={1234} />
    </div>
  );
}

export default App;
```

> **Decision guide:**
> - User types a numeric PIN → `type="number"`
> - User types an alphanumeric code → `type="text"`
> - Security-sensitive input that should be hidden → `type="password"`

---

## Styling Modes

The `stylingMode` property controls the visual border/fill style of input fields.

### Outlined (default)

Full border around each input field.

```tsx
<OtpInputComponent id="otpinput" stylingMode="outlined" />
```

### Filled

Input fields have a filled background with no visible border.

```tsx
<OtpInputComponent id="otpinput" stylingMode="filled" />
```

### Underlined

Only a bottom border is shown — matches Material Design style forms.

```tsx
<OtpInputComponent id="otpinput" stylingMode="underlined" />
```

> **Decision guide:**
> - Match your form design system — outlined works universally; underlined fits Material Design; filled suits card-based layouts.

---

## Placeholder Text

Use the `placeholder` property to show hint characters in each empty input field.

### Single character placeholder

All input fields display the same placeholder character:

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" placeholder="x" />
    </div>
  );
}

export default App;
```

### Per-field placeholder

Each input field displays a different character from the placeholder string (mapped by position):

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" placeholder="wxyz" />
    </div>
  );
}

export default App;
```

> Placeholder length should match `length` for per-field mapping. If shorter, remaining fields use the last character.

---

## Separator Character

Use the `separator` property to display a character between each OTP input field.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      {/* Slash separator: _ / _ / _ / _ */}
      <OtpInputComponent id="otpinput" separator="/" />
    </div>
  );
}

export default App;
```

Common separator values: `"/"`, `"-"`, `"·"`, `"|"`.

---

## Disabled State

Set `disabled={true}` to prevent user interaction. Combine with `value` to display a read-only OTP.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" value={1234} disabled={true} />
    </div>
  );
}

export default App;
```

> Use the disabled state when: showing an already-submitted OTP, displaying a loading/verification state, or preventing re-entry after submission.

---

## CSS Class Customization

The `cssClass` property applies custom or predefined CSS classes to the component wrapper.

### Predefined state classes

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      {/* Success state - green styling */}
      <OtpInputComponent id="otpinput-success" value={1234} cssClass="e-success" />

      {/* Warning state - yellow/orange styling */}
      <OtpInputComponent id="otpinput-warning" value={1234} cssClass="e-warning" />

      {/* Error state - red styling */}
      <OtpInputComponent id="otpinput-error" value={1234} cssClass="e-error" />
    </div>
  );
}

export default App;
```

### Custom CSS class

Add your own class name to override default styles:

```tsx
<OtpInputComponent id="otpinput" cssClass="my-custom-otp" />
```

```css
/* In your CSS file */
.my-custom-otp .e-otp-input-field {
  border-radius: 8px;
  font-size: 1.5rem;
}
```

> Use `e-success`/`e-warning`/`e-error` to give visual feedback after OTP verification — success for correct, error for incorrect.

---

## Right-to-Left Support

Enable `enableRtl` to render the OTP input in right-to-left layout for Arabic/Hebrew and other RTL languages.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" enableRtl={true} />
    </div>
  );
}

export default App;
```

---

## Text Transform

The `textTransform` property applies automatic case conversion to text typed into OTP fields. Only useful with `type="text"`.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      {/* Always uppercase — useful for code inputs like "AB12" */}
      <OtpInputComponent id="otpinput" type="text" textTransform="uppercase" />
    </div>
  );
}

export default App;
```

| Value | Behavior |
|-------|----------|
| `"none"` | No transformation (default) |
| `"uppercase"` | Converts all typed characters to uppercase |
| `"lowercase"` | Converts all typed characters to lowercase |

---

## State Persistence

Enable `enablePersistence` to save the component state across page reloads using browser localStorage.

```tsx
<OtpInputComponent id="otpinput" enablePersistence={true} />
```

> Use with caution for OTP inputs — OTP codes are time-sensitive and persisting them could be a security concern.
