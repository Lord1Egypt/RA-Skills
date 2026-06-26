# React Hooks Integration

Use React Hooks with MaskedTextBox for controlled inputs, auto-focus, and multi-field forms. The `ref` prop enables programmatic access to component methods like `focusIn()`.

## Relevant Hooks

| Hook | Use in MaskedTextBox |
|------|---------------------|
| `useState` | Store and update masked input values |
| `useEffect` | Trigger `focusIn()` on initial render |
| `useRef` | Get a reference to the MaskedTextBox instance |
| `useReducer` | Manage multiple field state updates together |

## Controlled Input with useState

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const [phone, setPhone] = React.useState('');

  return (
    <MaskedTextBoxComponent
      mask="000-000-0000"
      value={phone}
      change={(e) => setPhone(e.value)}
      placeholder="Phone Number"
      floatLabelType="Always"
    />
  );
}

export default App;
```

> `e.value` in the `change` handler returns the raw value without literals or prompt characters.

## Auto-Focus on Mount with useRef + useEffect

Use `useRef` to get the component instance, then call `focusIn()` inside `useEffect` to focus the field when the component mounts.

```tsx
import { useState, useEffect, useRef } from 'react';
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const [productKey, setProductKey] = useState('124-234-765-234');
  const productValueRef = useRef(null);

  useEffect(() => {
    productValueRef.current.focusIn();
  }, []);

  return (
    <MaskedTextBoxComponent
      ref={productValueRef}
      mask="000-000-000-000"
      value={productKey}
      change={(e) => setProductKey(e.value)}
      placeholder="Product key"
      floatLabelType="Always"
    />
  );
}

export default App;
```

## Multi-Field Form with useReducer

When managing multiple masked inputs in a form, `useReducer` keeps state updates predictable.

```tsx
import { useState, useEffect, useRef, useReducer } from 'react';
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

const initialState = { mobileNo: '', postalCode: '' };

function reducer(state, action) {
  switch (action.type) {
    case 'update':
      return { ...state, [action.field]: action.value };
    default:
      return initialState;
  }
}

function App() {
  const [productKey, setProductKey] = useState('124-234-765-234');
  const productValueRef = useRef(null);
  const [state, dispatch] = useReducer(reducer, initialState);

  const update = (field) => (event) => {
    dispatch({ type: 'update', field, value: event.value });
  };

  useEffect(() => {
    productValueRef.current.focusIn();
  }, []);

  return (
    <div>
      <MaskedTextBoxComponent
        ref={productValueRef}
        name="product"
        mask="000-000-000-000"
        value={productKey}
        change={(e) => setProductKey(e.value)}
        placeholder="Product key"
        floatLabelType="Always"
      />
      <MaskedTextBoxComponent
        name="mobile"
        mask="00-0000-0000"
        value={state.mobileNo}
        change={update('mobileNo')}
        placeholder="Mobile Number"
        floatLabelType="Always"
      />
      <MaskedTextBoxComponent
        name="postal"
        mask="000-000"
        value={state.postalCode}
        change={update('postalCode')}
        placeholder="Postal code"
        floatLabelType="Always"
      />
    </div>
  );
}

export default App;
```

## Getting the Masked Value Programmatically

```tsx
const maskRef = React.useRef(null);

// Raw value (no literals, no prompt chars)
const raw = maskRef.current.value;

// Masked value (with literals like dashes)
const masked = maskRef.current.getMaskedValue();

// Example:
// mask="000-000-0000", user typed "1234567890"
// raw     → "1234567890"
// masked  → "123-456-7890"
```
