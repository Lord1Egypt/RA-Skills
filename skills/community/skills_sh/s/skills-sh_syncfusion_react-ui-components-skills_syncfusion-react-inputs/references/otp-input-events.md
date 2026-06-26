# OTP Input Events

## Table of Contents
- [Overview](#overview)
- [created](#created)
- [focus](#focus)
- [blur](#blur)
- [input](#input)
- [valueChanged](#valuechanged)
- [Programmatic Focus Control](#programmatic-focus-control)
- [Common Patterns](#common-patterns)

---

## Overview

The OTP Input provides five events covering the full lifecycle of user interaction:

| Event | When it fires |
|-------|---------------|
| `created` | Once, after the component finishes rendering |
| `focus` | Each time an input field receives focus |
| `blur` | Each time an input field loses focus |
| `input` | Each time the value of any individual field changes |
| `valueChanged` | When all fields are filled and the input loses focus |

Import event argument types as needed:

```tsx
import {
  OtpInputComponent,
  OtpFocusEventArgs,
  OtpInputEventArgs,
  OtpChangedEventArgs
} from '@syncfusion/ej2-react-inputs';
```

---

## created

Fires once after the OTP Input finishes rendering. Use for post-render initialization (e.g., logging, analytics, additional DOM setup).

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleCreated = () => {
    console.log('OTP Input is ready');
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" created={handleCreated} />
    </div>
  );
}

export default App;
```

---

## focus

Fires when any OTP input field receives focus. The `OtpFocusEventArgs` argument provides the native event and the index of the focused field.

```tsx
import { OtpInputComponent, OtpFocusEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleFocus = (args: OtpFocusEventArgs) => {
    console.log('Focused input index:', args.index);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" focus={handleFocus} />
    </div>
  );
}

export default App;
```

---

## blur

Fires when any OTP input field loses focus. Same argument type as `focus`.

```tsx
import { OtpInputComponent, OtpFocusEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleBlur = (args: OtpFocusEventArgs) => {
    console.log('Blurred from input index:', args.index);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" blur={handleBlur} />
    </div>
  );
}

export default App;
```

---

## input

Fires each time the value of any individual OTP input field changes. The `OtpInputEventArgs` argument includes the current full OTP value string.

Use `input` for real-time feedback as the user types (e.g., showing a progress indicator, disabling a submit button until all fields are filled).

```tsx
import { OtpInputComponent, OtpInputEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleInput = (args: OtpInputEventArgs) => {
    console.log('Current OTP value:', args.value);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" input={handleInput} />
    </div>
  );
}

export default App;
```

---

## valueChanged

Fires when the OTP is complete (all fields filled) **and** the component loses focus. The `OtpChangedEventArgs` argument provides the final value and the previous value.

This is the primary event to use for OTP verification/submission logic.

```tsx
import { OtpInputComponent, OtpChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleValueChanged = (args: OtpChangedEventArgs) => {
    console.log('Submitted OTP:', args.value);
    console.log('Previous OTP:', args.previousValue);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" valueChanged={handleValueChanged} />
    </div>
  );
}

export default App;
```

**With alert for demonstration:**

```tsx
import { OtpInputComponent, OtpChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleValueChanged = (args: OtpChangedEventArgs) => {
    alert('Entered OTP value: ' + args.value);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" valueChanged={handleValueChanged} />
    </div>
  );
}

export default App;
```

> **`input` vs `valueChanged`:**
> - Use `input` to track partial progress (e.g., show how many digits have been entered).
> - Use `valueChanged` to trigger verification when the user has finished entering the full OTP.

---

## Programmatic Focus Control

Use `ref` to access the component instance and call focus methods programmatically.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const otpRef = React.useRef<OtpInputComponent>(null);

  const handleFocusIn = () => {
    otpRef.current?.focusIn();
  };

  const handleFocusOut = () => {
    otpRef.current?.focusOut();
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" ref={otpRef} />
      <button onClick={handleFocusIn}>Focus OTP</button>
      <button onClick={handleFocusOut}>Blur OTP</button>
    </div>
  );
}

export default App;
```

---

## Common Patterns

### Show submit button only when OTP is complete

```tsx
import { OtpInputComponent, OtpInputEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const [otpValue, setOtpValue] = React.useState('');
  const OTP_LENGTH = 4;

  const handleInput = (args: OtpInputEventArgs) => {
    setOtpValue(args.value ?? '');
  };

  const handleSubmit = () => {
    alert('Verifying OTP: ' + otpValue);
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" length={OTP_LENGTH} input={handleInput} />
      <button
        onClick={handleSubmit}
        disabled={otpValue.length < OTP_LENGTH}
      >
        Verify
      </button>
    </div>
  );
}

export default App;
```

### Visual feedback after verification

```tsx
import { OtpInputComponent, OtpChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

const CORRECT_OTP = '1234';

function App() {
  const [status, setStatus] = React.useState<'idle' | 'success' | 'error'>('idle');

  const cssClassMap = {
    idle: '',
    success: 'e-success',
    error: 'e-error',
  };

  const handleValueChanged = (args: OtpChangedEventArgs) => {
    if (args.value === CORRECT_OTP) {
      setStatus('success');
    } else {
      setStatus('error');
    }
  };

  return (
    <div id="container">
      <OtpInputComponent
        id="otpinput"
        cssClass={cssClassMap[status]}
        valueChanged={handleValueChanged}
      />
      {status === 'success' && <p>OTP verified successfully!</p>}
      {status === 'error' && <p>Incorrect OTP. Please try again.</p>}
    </div>
  );
}

export default App;
```
