# Features and State — Syncfusion React RadioButton

## Table of Contents
- [Checked and Unchecked State](#checked-and-unchecked-state)
- [Disabled State](#disabled-state)
- [Form Submission: Name and Value](#form-submission-name-and-value)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Change Event](#change-event)
- [Created Event](#created-event)
- [State Persistence](#state-persistence)
- [Getting Selected Value Programmatically](#getting-selected-value-programmatically)

---

## Checked and Unchecked State

The RadioButton has two visual states:
- **Checked** — inner circle visible; button is selected
- **Unchecked** — button appears empty; not selected

Use the `checked` property to set the initial state. Setting `checked={true}` pre-selects the button when rendered.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <ul>
      {/* Pre-selected */}
      <li><RadioButtonComponent label="Option 1" name="state" checked={true} /></li>

      {/* Not selected */}
      <li><RadioButtonComponent label="Option 2" name="state" /></li>
    </ul>
  );
}
export default App;
```

> **Note:** Within a `name` group, only one button can be `checked={true}` at a time. If multiple are set, the last one in the DOM wins.

---

## Disabled State

Use `disabled={true}` to prevent user interaction. A disabled RadioButton appears grayed out and cannot be clicked, but remains visible.

Disabled buttons are excluded from form submissions (their `value` is not sent).

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  let radioInstance1: RadioButtonComponent;
  let radioInstance2: RadioButtonComponent;
  let radioInstance3: RadioButtonComponent;

  function changeOption1(): void {
    (document.getElementById('text') as HTMLElement).innerText =
      'Selected : ' + radioInstance1.label;
  }

  function changeOption2(): void {
    (document.getElementById('text') as HTMLElement).innerText =
      'Selected : ' + radioInstance2.label;
  }

  function changeOption3(): void {
    (document.getElementById('text') as HTMLElement).innerText =
      'Selected : ' + radioInstance3.label;
  }

  return (
    <ul>
      <li><div id="text">Selected : Option 1</div></li>
      <li>
        <RadioButtonComponent
          label="Option 1"
          name="default"
          checked={true}
          change={changeOption1}
          ref={r => radioInstance1 = r as RadioButtonComponent}
        />
      </li>
      <li>
        <RadioButtonComponent
          label="Option 2 (Disabled)"
          name="default"
          disabled={true}
          change={changeOption2}
          ref={r => radioInstance2 = r as RadioButtonComponent}
        />
      </li>
      <li>
        <RadioButtonComponent
          label="Option 3"
          name="default"
          change={changeOption3}
          ref={r => radioInstance3 = r as RadioButtonComponent}
        />
      </li>
    </ul>
  );
}
export default App;
```

---

## Form Submission: Name and Value

Use `name` to group radio buttons and `value` to specify what gets submitted to the server. When a form is submitted, only the `value` of the **checked** button in each `name` group is sent.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent, ButtonComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <form>
      <ul>
        <li>
          <RadioButtonComponent
            name="payment"
            value="credit/debit"
            label="Credit / Debit Card"
            checked={true}
          />
        </li>
        <li>
          <RadioButtonComponent
            name="payment"
            value="netbanking"
            label="Net Banking"
          />
        </li>
        <li>
          <RadioButtonComponent
            name="payment"
            value="cashondelivery"
            label="Cash On Delivery"
          />
        </li>
        <li>
          <RadioButtonComponent
            name="payment"
            value="others"
            label="Others"
          />
        </li>
        <li><ButtonComponent isPrimary={true}>Submit</ButtonComponent></li>
      </ul>
    </form>
  );
}
export default App;
```

> **Rules:**
> - `name` groups the buttons — only one per group is submitted
> - `value` is what the server receives
> - Disabled or unchecked buttons do NOT submit their values

---

## Right-to-Left (RTL) Support

Enable RTL layout for Arabic, Hebrew, Persian, or any right-to-left language by setting `enableRtl={true}`. This flips the component layout and text direction.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><RadioButtonComponent label="الخيار 1" name="rtl" enableRtl={true} /></li>
      <li><RadioButtonComponent label="الخيار 2" name="rtl" enableRtl={true} /></li>
    </ul>
  );
}
export default App;
```

> **Tip:** You can also enable RTL globally via `L10n` or the component's `locale` property to avoid setting it on each instance.

---

## Change Event

The `change` event fires when the user selects a RadioButton. The event argument is `ChangeArgs`, which includes:

| Property | Type | Description |
|----------|------|-------------|
| `value` | string | The `value` prop of the newly selected button |
| `event` | Event | The native DOM event |
| `name` | string | The name of the event |

```tsx
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';
import { useState } from 'react';

function App() {
  const [selected, setSelected] = useState<string>('');

  const handleChange = (args: ChangeArgs) => {
    setSelected(args.value);
    console.log('Selected value:', args.value);
  };

  return (
    <div>
      <p>Selected: {selected}</p>
      <ul>
        <li>
          <RadioButtonComponent
            label="Small"
            name="size-plan"
            value="small"
            change={handleChange}
          />
        </li>
        <li>
          <RadioButtonComponent
            label="Medium"
            name="size-plan"
            value="medium"
            checked={true}
            change={handleChange}
          />
        </li>
        <li>
          <RadioButtonComponent
            label="Large"
            name="size-plan"
            value="large"
            change={handleChange}
          />
        </li>
      </ul>
    </div>
  );
}
export default App;
```

---

## Created Event

The `created` event fires once after the component has fully rendered. Use it for post-render logic like focusing or reading the initial state.

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const handleCreated = () => {
    console.log('RadioButton rendered and ready');
  };

  return (
    <RadioButtonComponent
      label="Notify on Ready"
      name="lifecycle"
      created={handleCreated}
    />
  );
}
export default App;
```

---

## State Persistence

Use `enablePersistence={true}` to automatically save and restore the RadioButton's state across page reloads using browser storage.

```tsx
<RadioButtonComponent
  label="Persist My State"
  name="persist"
  enablePersistence={true}
/>
```

> **When to use:** Useful in multi-step wizards or preference settings where the user's choice should survive a page refresh.

---

## Getting Selected Value Programmatically

Use the `getSelectedValue()` method on a RadioButton instance to retrieve the currently selected value from the group at any time — without relying on the `change` event.

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';
import { useRef } from 'react';

function App() {
  const radioRef = useRef<RadioButtonComponent>(null);

  const readValue = () => {
    if (radioRef.current) {
      const val = radioRef.current.getSelectedValue();
      alert('Currently selected: ' + val);
    }
  };

  return (
    <div>
      <RadioButtonComponent label="Option A" name="prog" value="a" checked={true} ref={radioRef} />
      <RadioButtonComponent label="Option B" name="prog" value="b" />
      <button onClick={readValue}>Read Selected</button>
    </div>
  );
}
export default App;
```

---

## See Also

- [label-and-size.md](label-and-size.md) — label and size configuration
- [style-and-appearance.md](style-and-appearance.md) — CSS customization
- [accessibility.md](accessibility.md) — WCAG, ARIA, keyboard support
- [api.md](api.md) — full API reference
