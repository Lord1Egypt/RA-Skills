# Switch Features and Configuration

This file covers all configurable properties of the Syncfusion React Switch component. Every property listed here maps directly to the official API at `https://ej2.syncfusion.com/react/documentation/api/switch/`.

## Table of Contents
- [Text Labels (onLabel / offLabel)](#text-labels-onlabel--offlabel)
- [Disabled State](#disabled-state)
- [Name and Value (Form Submission)](#name-and-value-form-submission)
- [Custom CSS Class](#custom-css-class)
- [Right-to-Left (RTL)](#right-to-left-rtl)
- [Persist State Across Reloads](#persist-state-across-reloads)
- [HTML Attributes Passthrough](#html-attributes-passthrough)
- [Localization](#localization)

---

## Text Labels (onLabel / offLabel)

Use `onLabel` and `offLabel` to display custom text inside the Switch track for the on and off states respectively. This clarifies the switch's purpose when the toggle alone is not self-explanatory.

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <SwitchComponent onLabel="ON" offLabel="OFF" checked={true} />
  );
}
```

> **Note:** Text labels are **not supported** in Material themes. Do not use long custom text — labels have limited width inside the track.

---

## Disabled State

Set `disabled={true}` to prevent user interaction. A disabled Switch appears grayed out and cannot be toggled. Use this for read-only states or when a feature is temporarily unavailable.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <SwitchComponent disabled={true} />
  );
}
```

> Disabled Switches are excluded from HTML form submission data — only enabled, checked Switches send values.

---

## Name and Value (Form Submission)

Use `name` to group Switches for form submission and `value` to define the data sent to the server. Only **checked and enabled** Switches submit their values when a form is submitted.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent, SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <form>
      <label htmlFor="switch1">USB</label>
      <SwitchComponent id="switch1" name="Tethering" value="USB" checked={true} />

      <label htmlFor="switch2">Wi-Fi</label>
      <SwitchComponent id="switch2" name="Hotspot" value="Wi-Fi" checked={true} />

      <label htmlFor="switch3">Bluetooth</label>
      <SwitchComponent id="switch3" name="Tethering" value="Bluetooth" disabled={true} />

      <ButtonComponent isPrimary={true}>Submit</ButtonComponent>
    </form>
  );
}
```

In this example, `USB` and `Wi-Fi` values are submitted; `Bluetooth` is excluded because it is disabled.

---

## Custom CSS Class

Use `cssClass` to apply custom styling classes to the Switch component. This is the primary mechanism for resizing, recoloring, and reshaping the Switch.

```tsx
// Small size variant
<SwitchComponent cssClass="e-small" />

// Custom class for your own CSS
<SwitchComponent cssClass="my-custom-switch" />
```

Multiple classes can be space-separated:
```tsx
<SwitchComponent cssClass="e-small my-custom-switch" />
```

> See [style-and-appearance.md](style-and-appearance.md) for CSS class details and customization examples.

---

## Right-to-Left (RTL)

Set `enableRtl={true}` to mirror the Switch layout for right-to-left languages such as Arabic, Hebrew, and Persian.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <SwitchComponent enableRtl={true} checked={true} />
  );
}
```

---

## Persist State Across Reloads

Set `enablePersistence={true}` to save the Switch's checked state in browser storage. The Switch will restore its last state when the page reloads.

```tsx
<SwitchComponent enablePersistence={true} checked={false} />
```

---

## HTML Attributes Passthrough

Use `htmlAttributes` to pass additional HTML attributes to the underlying `<input>` element. If you configure both a property and an equivalent HTML attribute, the **property value takes precedence**.

```tsx
<SwitchComponent
  htmlAttributes={{ 'aria-label': 'Toggle dark mode', 'data-testid': 'theme-switch' }}
/>
```

---

## Localization

Override the global culture/locale for the Switch component using the `locale` property. The default global culture is `'en-US'`.

```tsx
<SwitchComponent locale="fr-FR" />
```

> For full localization setup (loading locale data, L10n configuration), refer to the Syncfusion globalization documentation.
