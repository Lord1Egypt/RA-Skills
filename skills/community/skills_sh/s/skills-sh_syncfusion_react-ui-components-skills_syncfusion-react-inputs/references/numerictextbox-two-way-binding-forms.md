## Two-Way Binding & Forms

This reference explains how to use `NumericTextBoxComponent` as a controlled form field in React, integrate it with popular form libraries, and handle common validation patterns.

## Table of Contents
- [Overview](#overview)
- [Controlled Component Pattern](#controlled-component-pattern)
- [Using with React Hook Form](#using-with-react-hook-form)
- [Uncontrolled Patterns](#uncontrolled-patterns)
- [Validation Patterns](#validation-patterns)
- [Examples](#examples)
- [Edge Cases & Troubleshooting](#edge-cases--troubleshooting)

## Overview

There are two common ways to use `NumericTextBoxComponent` in React apps:

- Controlled: React state owns the value via `value` and `onChange`.
- Uncontrolled: Use a ref and read the value when needed.

Controlled components are recommended for forms where validation and immediate UI feedback are required.

## Controlled Component Pattern

Use `useState` (or form state) to hold the value and update on `onChange`.

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ControlledExample() {
  const [value, setValue] = useState(0);

  return (
    <NumericTextBoxComponent
      value={value}
      onChange={(e) => setValue(e.value)}
      min={0}
      max={100}
      step={1}
    />
  );
}
```

Key notes:
- Always pass `value` when you want React to own the input.
- Use `onChange` to sync component updates into React state.
- Use `decimals` to restrict fraction digits when needed.

## Using with React Hook Form

React Hook Form (RHF) expects uncontrolled inputs by default, but works with controlled components using `Controller`.

```jsx
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RHFExample() {
  const { control, handleSubmit } = useForm({ defaultValues: { amount: 0 } });

  const onSubmit = (data) => console.log('submit', data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="amount"
        control={control}
        rules={{ required: true, min: 0 }}
        render={({ field }) => (
          <NumericTextBoxComponent
            {...field}
            value={field.value}
            change={(e) => field.onChange(e.value)}
            format="c2"
          />
        )}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

Tips:
- Pass `field.value` into `value` to keep RHF state in sync.
- Call `field.onChange(e.value)` inside `onChange` handler.

## Uncontrolled Patterns

If you prefer an uncontrolled approach, use a `ref` and call component methods or read its value when needed.

```jsx
import React, { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

function Uncontrolled() {
  const numRef = useRef(null);

  const readValue = () => {
    // numRef.current.value may contain formatted string; prefer API method if available
    console.log('value', numRef.current.value);
  };

  return (
    <div>
      <NumericTextBoxComponent ref={numRef} value={5} />
      <button onClick={readValue}>Read</button>
    </div>
  );
}
```

Note: uncontrolled patterns are simpler but make validation and immediate UI feedback harder to manage.

## Validation Patterns

- Use component props `min`, `max`, and `strictMode` for edge validation.
- For custom validation, validate React state or form library values before submit.
- Provide user feedback with inline messages and ARIA `aria-invalid` when invalid.

Example using local validation:

```jsx
function FormWithValidation() {
  const [value, setValue] = React.useState('');
  const [error, setError] = React.useState(null);

  const validate = (val) => {
    if (val === null || val === undefined || val === '') return 'Value required';
    if (val < 0) return 'Value cannot be negative';
    return null;
  };

  return (
    <div>
      <NumericTextBoxComponent
        value={value}
        onChange={(e) => {
          setValue(e.value);
          setError(validate(e.value));
        }}
      />
      {error && <div role="alert" style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}
```

## Examples

- Simple controlled input
- RHF controlled input with `Controller`
- Combined validation example (above)

## Edge Cases & Troubleshooting

- Formatting vs raw value: the displayed string may include currency symbols; prefer using `value` from events for numeric operations.
- Trailing zeros: use `decimals` and `validateDecimalOnType` to control behavior.
- When integrating with RHF, ensure the component value is synchronous with RHF state to avoid stale values.

---

For additional examples, see `references/getting-started.md` and `references/precision-decimals.md`.
