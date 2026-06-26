# Switch How-To Recipes

Practical recipes for common Switch implementation tasks. Each recipe uses only APIs documented in the official Syncfusion Switch API reference.

## Table of Contents
- [Change Switch Size](#change-switch-size)
- [Set Text Labels on Switch](#set-text-labels-on-switch)
- [Set Disabled State](#set-disabled-state)
- [Prevent State Change](#prevent-state-change)
- [Enable RTL Layout](#enable-rtl-layout)
- [Programmatic Toggle via toggle() Method](#programmatic-toggle-via-toggle-method)
- [Enable Ripple for Switch Label](#enable-ripple-for-switch-label)
- [Submit Name and Value in a Form](#submit-name-and-value-in-a-form)

---

## Change Switch Size

The Switch supports two size variants: **default** and **small**. Use `cssClass="e-small"` to render a compact switch, useful for space-constrained layouts or mobile interfaces.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <table>
      <tbody>
        <tr>
          <td>Small</td>
          <td>
            <SwitchComponent cssClass="e-small" />
          </td>
        </tr>
        <tr>
          <td>Default</td>
          <td>
            <SwitchComponent />
          </td>
        </tr>
      </tbody>
    </table>
  );
}
export default App;
```

**Key API:** `cssClass` property — set to `"e-small"` for compact size.

---

## Set Text Labels on Switch

Display custom text inside the switch track using `onLabel` (checked state) and `offLabel` (unchecked state). This improves clarity when the toggle purpose isn't immediately obvious.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <SwitchComponent onLabel="ON" offLabel="OFF" checked={true} />
  );
}
export default App;
```

> **Gotcha:** Text labels are **not supported in Material themes** and do not support long custom text strings.

---

## Set Disabled State

Use `disabled={true}` to render a non-interactive Switch. The switch appears grayed out and cannot be toggled by users.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <SwitchComponent disabled={true} />
  );
}
export default App;
```

**When to use:** Read-only states, unavailable features, or when another control must be configured before this one can be used.

---

## Prevent State Change

Use the `beforeChange` event to intercept and cancel state transitions. Set `args.cancel = true` within the handler to prevent the change.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { BeforeChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function beforeChange(args: BeforeChangeEventArgs): void {
  // Cancel all state changes — switch is effectively read-only
  args.cancel = true;
}

function App() {
  return (
    <SwitchComponent checked={true} beforeChange={beforeChange} />
  );
}
export default App;
```

**Use cases:**
- Require confirmation before turning a feature off
- Validate conditions before allowing state change
- Block specific transitions (e.g., prevent turning off)

---

## Enable RTL Layout

Set `enableRtl={true}` to mirror the Switch layout for right-to-left languages (Arabic, Hebrew, Persian).

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <SwitchComponent enableRtl={true} checked={true} />
  );
}
export default App;
```

---

## Programmatic Toggle via toggle() Method

Toggle the Switch state from external controls (buttons, keyboard shortcuts, etc.) using the `toggle()` method via a `ref`.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  let switchRef: SwitchComponent;

  function onCreated(): void {
    // Automatically toggle after rendering
    switchRef.toggle();
  }

  return (
    <SwitchComponent
      id="switch"
      ref={(scope) => { switchRef = scope as SwitchComponent; }}
      enableRtl={true}
      checked={true}
      created={onCreated}
    />
  );
}
export default App;
```

> The `change` event fires on every state change triggered by `toggle()`.

---

## Enable Ripple for Switch Label

Add Material Design ripple animations to labels associated with the Switch. This provides visual feedback when users click the label, improving perceived interactivity.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { rippleMouseHandler } from '@syncfusion/ej2-buttons';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  function onCreated(): void {
    const label = document.querySelector('.lSize label') as HTMLElement;
    if (label) {
      label.addEventListener('mouseup', rippleHandler);
      label.addEventListener('mousedown', rippleHandler);
    }

    function rippleHandler(e: MouseEvent): void {
      const rippleSpan = (e.target as HTMLElement)
        .parentElement?.nextElementSibling?.querySelector('.e-ripple-container');
      if (rippleSpan) {
        rippleMouseHandler(e, rippleSpan);
      }
    }
  }

  return (
    <table className="size">
      <tbody>
        <tr>
          <td className="lSize">
            <label htmlFor="switch1">USB Tethering</label>
          </td>
          <td>
            <SwitchComponent id="switch1" created={onCreated} checked={true} />
          </td>
        </tr>
      </tbody>
    </table>
  );
}
export default App;
```

> **TypeScript note:** If you get `'object is possibly null'` errors, disable `strictNullChecks` in `tsconfig.json` or add null checks.

---

## Submit Name and Value in a Form

Use `name` to identify the form field and `value` to set the submitted data. Only **checked and enabled** Switches submit their values.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent, SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <form>
      <div>
        <label htmlFor="switch1">USB</label>
        <SwitchComponent id="switch1" name="Tethering" value="USB" checked={true} />
      </div>
      <div>
        <label htmlFor="switch2">Wi-Fi</label>
        <SwitchComponent id="switch2" name="Hotspot" value="Wi-Fi" checked={true} />
      </div>
      <div>
        <label htmlFor="switch3">Bluetooth</label>
        {/* disabled — excluded from form submission */}
        <SwitchComponent id="switch3" name="Tethering" value="Bluetooth" disabled={true} />
      </div>
      <ButtonComponent isPrimary={true}>Submit</ButtonComponent>
    </form>
  );
}
export default App;
```

In this example, the form submits `Tethering=USB` and `Hotspot=Wi-Fi`. Bluetooth is excluded because it is disabled.
