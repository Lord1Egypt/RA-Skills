# Syncfusion React NumericTextBox API Reference

Complete API reference for the `NumericTextBoxComponent` from `@syncfusion/ej2-react-inputs`.

**Import:**

```tsx
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';
```

---

## Properties

### allowMouseWheel

`boolean`

Gets or sets a value indicating whether the mouse wheel interaction is enabled for incrementing or decrementing the value in the NumericTextBox component.

**Default:** `true`

```tsx
<NumericTextBoxComponent value={10} allowMouseWheel={false} />
```

---

### appendTemplate

`string | function | JSX.Element`

Specifies the HTML template string for custom elements to append to the NumericTextBox input. Supports icons, buttons, or any valid HTML. Updates dynamically on property change.

**Default:** `null`

**Function Signature:** `() => JSX.Element`

```tsx
function appendTemplate(): JSX.Element {
  return (
    <>
      <span className="e-input-separator"></span>
      <span className="e-icons e-eye"></span>
    </>
  );
}

<NumericTextBoxComponent value={10} appendTemplate={appendTemplate} />
```

---

### cssClass

`string`

Gets or Sets the CSS classes to root element of the NumericTextBox which helps to customize the complete UI styles for the NumericTextBox component.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={10} cssClass="e-small" placeholder="Small" />
<NumericTextBoxComponent value={10} cssClass="e-bigger" placeholder="Large" />
<NumericTextBoxComponent value={10} cssClass="e-error" placeholder="Error State" />
<NumericTextBoxComponent value={10} cssClass="e-warning" placeholder="Warning State" />
<NumericTextBoxComponent value={10} cssClass="e-success" placeholder="Success State" />
```

---

### currency

`string`

Specifies the currency code to use in currency formatting. Possible values are the ISO 4217 currency codes, such as `'USD'` for the US dollar, `'EUR'` for the euro.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={99.99} format="c2" currency="EUR" placeholder="Amount" />
```

---

### decimals

`number`

Specifies the number precision applied to the textbox value when the NumericTextBox is focused.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={10.5} decimals={2} placeholder="Enter value" />
```

---

### enablePersistence

`boolean`

Enable or disable persisting NumericTextBox state between page reloads. If enabled, the `value` state will be persisted.

**Default:** `false`

```tsx
<NumericTextBoxComponent value={10} enablePersistence={true} placeholder="Persisted" />
```

---

### enableRtl

`boolean`

Enable or disable rendering component in right to left direction.

**Default:** `false`

```tsx
<NumericTextBoxComponent value={10} enableRtl={true} placeholder="RTL Input" />
```

---

### enabled

`boolean`

Sets a value that enables or disables the NumericTextBox control.

**Default:** `true`

```tsx
<NumericTextBoxComponent value={10} enabled={false} placeholder="Disabled" />
```

---

### floatLabelType

`FloatLabelType`

The placeholder acts as a label and floats above the NumericTextBox based on the below values.

**Possible values:**
- `'Never'` – Never floats the label in the NumericTextBox when the placeholder is available (default)
- `'Always'` – The floating label always floats above the NumericTextBox
- `'Auto'` – The floating label floats above the NumericTextBox after focusing it or when a value is entered

**Default:** `'Never'`

```tsx
<NumericTextBoxComponent value={10} placeholder="Enter Number" floatLabelType="Auto" />
<NumericTextBoxComponent value={10} placeholder="Enter Number" floatLabelType="Always" />
<NumericTextBoxComponent value={10} placeholder="Enter Number" floatLabelType="Never" />
```

---

### format

`string`

Specifies the number format that indicates the display format for the value of the NumericTextBox.

**Common format specifiers:**
- `'n2'` – Number with 2 decimal places (default)
- `'c2'` – Currency with 2 decimal places
- `'p2'` – Percentage with 2 decimal places
- `'e2'` – Scientific notation with 2 decimal places

**Default:** `'n2'`

```tsx
<NumericTextBoxComponent value={99.99} format="c2" placeholder="Currency" />
<NumericTextBoxComponent value={0.5} format="p2" placeholder="Percentage" />
<NumericTextBoxComponent value={12345} format="n0" placeholder="Integer" />
<NumericTextBoxComponent value={0.00012} format="e2" placeholder="Scientific" />
```

---

### htmlAttributes

`{ [key: string]: string }`

You can add additional HTML attributes such as `disabled`, `value`, `name`, `min`, `max`, etc. to the element. If both property and equivalent HTML attribute are configured, the component considers the property value.

**Default:** `{}`

```tsx
import * as React from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

class App extends React.Component {
  public htmlAttributes = { name: "quantity", min: "0", max: "100" };
  public render() {
    return (<NumericTextBoxComponent htmlAttributes={this.htmlAttributes} />);
  }
}

export default App;
```

---

### locale

`string`

Overrides the global culture and localization value for this component. Default global culture is `'en-US'`.

**Default:** `''`

```tsx
<NumericTextBoxComponent value={1234.56} locale="de" format="n2" placeholder="German Format" />
<NumericTextBoxComponent value={1234.56} locale="fr-FR" format="c2" placeholder="French Currency" />
```

---

### max

`number`

Specifies a maximum value that a user can enter.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={50} max={100} placeholder="Max: 100" />
```

---

### min

`number`

Specifies a minimum value that a user can enter.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={10} min={0} placeholder="Min: 0" />
```

---

### placeholder

`string`

Gets or sets the string shown as a hint/placeholder when the NumericTextBox is empty. It acts as a label and floats above the NumericTextBox based on the `floatLabelType`.

**Default:** `null`

```tsx
<NumericTextBoxComponent placeholder="Enter a number" floatLabelType="Auto" />
```

---

### prependTemplate

`string | function | JSX.Element`

Specifies the HTML template string for custom elements to prepend to the NumericTextBox input. Supports icons, buttons, or any valid HTML. Updates dynamically on property change.

**Default:** `null`

**Function Signature:** `() => JSX.Element`

```tsx
function prependTemplate(): JSX.Element {
  return (
    <>
      <span className="e-input-group-icon e-icons e-dollar"></span>
      <span className="e-input-separator"></span>
    </>
  );
}

<NumericTextBoxComponent value={99.99} prependTemplate={prependTemplate} placeholder="Amount" />
```

---

### readonly

`boolean`

Sets a value that enables or disables the readonly state on the NumericTextBox. If it is `true`, the NumericTextBox will not allow user input.

**Default:** `false`

```tsx
<NumericTextBoxComponent value={42} readonly={true} placeholder="Read-only" floatLabelType="Auto" />
```

---

### showClearButton

`boolean`

Specifies whether to show or hide the clear icon.

**Default:** `false`

```tsx
<NumericTextBoxComponent value={10} showClearButton={true} placeholder="Enter value" floatLabelType="Auto" />
```

---

### showSpinButton

`boolean`

Specifies whether the up and down spin buttons should be displayed in the NumericTextBox.

**Default:** `true`

```tsx
<NumericTextBoxComponent value={10} showSpinButton={false} placeholder="No Spinner" />
```

---

### step

`number`

Specifies the incremental or decremental step size for the NumericTextBox.

**Default:** `1`

```tsx
<NumericTextBoxComponent value={0} step={5} min={0} max={100} placeholder="Step: 5" />
<NumericTextBoxComponent value={0} step={0.5} decimals={1} placeholder="Step: 0.5" />
```

---

### strictMode

`boolean`

Specifies a value that indicates whether the NumericTextBox control allows the value for the specified range.

- If `true`, the input value will be restricted between the `min` and `max` range. The typed value gets modified to fit the range on focused-out state.
- If `false`, it allows any value even out of range. When a wrong value is entered, the error class will be added to the component to highlight the error.

**Default:** `true`

```tsx
import * as React from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

class App extends React.Component {
  public render() {
    return (<NumericTextBoxComponent strictMode={false} min={10} max={20} value={25} />);
  }
}

export default App;
```

---

### validateDecimalOnType

`boolean`

Specifies whether the decimal length should be restricted during typing.

**Default:** `false`

```tsx
<NumericTextBoxComponent value={10.5} decimals={2} validateDecimalOnType={true} placeholder="Max 2 decimals" />
```

---

### value

`number`

Sets the value of the NumericTextBox.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={42} placeholder="Enter number" floatLabelType="Auto" />
```

---

### width

`number | string`

Specifies the width of the NumericTextBox.

**Default:** `null`

```tsx
<NumericTextBoxComponent value={10} width="300px" placeholder="Enter number" />
<NumericTextBoxComponent value={10} width={400} placeholder="Enter number" />
```

---

## Methods

### decrement

Decrements the NumericTextBox value with the specified step value.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` (optional) | `number` | Specifies the value used to decrement the NumericTextBox value. If not given, the numeric value will be decremented based on the `step` property value. |

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const handleDecrement = () => {
    numericRef.current?.decrement(5);
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={50} min={0} max={100} />
      <button onClick={handleDecrement}>Decrement by 5</button>
    </>
  );
}
```

---

### destroy

Removes the component from the DOM and detaches all its related event handlers. Also maintains the initial input element from the DOM.

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const handleDestroy = () => {
    numericRef.current?.destroy();
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={10} placeholder="Enter number" />
      <button onClick={handleDestroy}>Destroy</button>
    </>
  );
}
```

---

### focusIn

Sets the focus to the widget for interaction.

**Returns:** `void`

```tsx
import { useRef, useEffect } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  useEffect(() => {
    numericRef.current?.focusIn();
  }, []);

  return (
    <NumericTextBoxComponent ref={numericRef} value={10} placeholder="Auto-focused" floatLabelType="Auto" />
  );
}
```

---

### focusOut

Removes the focus from the widget if the widget is in a focused state.

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const handleBlur = () => {
    numericRef.current?.focusOut();
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={10} placeholder="Enter number" />
      <button onClick={handleBlur}>Remove Focus</button>
    </>
  );
}
```

---

### getPersistData

Gets the properties to be maintained in the persisted state.

**Returns:** `string`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const logPersistData = () => {
    const data = numericRef.current?.getPersistData();
    console.log('Persist data:', data);
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={10} enablePersistence={true} placeholder="Persisted" />
      <button onClick={logPersistData}>Get Persist Data</button>
    </>
  );
}
```

---

### getText

Returns the value of the NumericTextBox with the format applied to the NumericTextBox.

**Returns:** `string`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const showFormattedText = () => {
    const text = numericRef.current?.getText();
    console.log('Formatted value:', text); // e.g., "$1,234.56"
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={1234.56} format="c2" placeholder="Amount" />
      <button onClick={showFormattedText}>Get Formatted Text</button>
    </>
  );
}
```

---

### increment

Increments the NumericTextBox value with the specified step value.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` (optional) | `number` | Specifies the value used to increment the NumericTextBox value. If not given, the numeric value will be incremented based on the `step` property value. |

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const handleIncrement = () => {
    numericRef.current?.increment(10);
  };

  return (
    <>
      <NumericTextBoxComponent ref={numericRef} value={0} min={0} max={100} />
      <button onClick={handleIncrement}>Increment by 10</button>
    </>
  );
}
```

---

## Events

### blur

`EmitType<NumericBlurEventArgs>`

Triggers when the NumericTextBox got focus out.

**Event Arguments (`NumericBlurEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `container` | `HTMLElement` | Returns the NumericTextBox container element. |
| `event` | `MouseEvent \| FocusEvent \| TouchEvent \| KeyboardEvent` | Returns the original event arguments. |
| `name` | `string` | Specifies the name of the event. |
| `value` | `number` | Returns the value of the NumericTextBox. |

```tsx
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleBlur = (args: any) => {
    console.log('Blurred, value:', args.value);
    console.log('Container:', args.container);
  };

  return (
    <NumericTextBoxComponent
      value={10}
      placeholder="Enter number"
      floatLabelType="Auto"
      blur={handleBlur}
    />
  );
}
```

---

### change

`EmitType<ChangeEventArgs>`

Triggers when the value of the NumericTextBox changes. The change event is triggered in the following scenarios:
- Changing the previous value using keyboard interaction and then focusing out of the component.
- Focusing on the component and scrolling within the input.
- Changing the value using the spin buttons.
- Programmatically changing the value using the `value` property.

**Event Arguments (`ChangeEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `event` | `Event` | Returns the event parameters from the NumericTextBox. |
| `isInteracted` | `boolean` | Returns `true` when the value of the NumericTextBox is changed by user interaction. Otherwise, returns `false`. |
| `name` | `string` | Specifies the name of the event. |
| `previousValue` | `number` | Returns the previously entered value of the NumericTextBox. |
| `value` | `number` | Returns the entered value of the NumericTextBox. |

```tsx
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleChange = (args: any) => {
    console.log('New value:', args.value);
    console.log('Previous value:', args.previousValue);
    console.log('User interaction:', args.isInteracted);
  };

  return (
    <NumericTextBoxComponent
      value={10}
      min={0}
      max={100}
      placeholder="Enter number"
      floatLabelType="Auto"
      change={handleChange}
    />
  );
}
```

---

### created

`EmitType<Object>`

Triggers when the NumericTextBox component is created.

```tsx
import { useRef } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const numericRef = useRef<NumericTextBoxComponent>(null);

  const handleCreated = () => {
    console.log('NumericTextBox created');
    console.log('Initial value:', numericRef.current?.value);
  };

  return (
    <NumericTextBoxComponent
      ref={numericRef}
      value={10}
      placeholder="Enter number"
      floatLabelType="Auto"
      created={handleCreated}
    />
  );
}
```

---

### destroyed

`EmitType<Object>`

Triggers when the NumericTextBox component is destroyed.

```tsx
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleDestroyed = () => {
    console.log('NumericTextBox destroyed');
  };

  return (
    <NumericTextBoxComponent
      value={10}
      placeholder="Enter number"
      destroyed={handleDestroyed}
    />
  );
}
```

---

### focus

`EmitType<NumericFocusEventArgs>`

Triggers when the NumericTextBox got focus in.

**Event Arguments (`NumericFocusEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `container` | `HTMLElement` | Returns the NumericTextBox container element. |
| `event` | `MouseEvent \| FocusEvent \| TouchEvent \| KeyboardEvent` | Returns the original event arguments. |
| `name` | `string` | Specifies the name of the event. |
| `value` | `number` | Returns the value of the NumericTextBox. |

```tsx
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleFocus = (args: any) => {
    console.log('Focused, value:', args.value);
    console.log('Container:', args.container);
  };

  return (
    <NumericTextBoxComponent
      value={10}
      placeholder="Enter number"
      floatLabelType="Auto"
      focus={handleFocus}
    />
  );
}
```
