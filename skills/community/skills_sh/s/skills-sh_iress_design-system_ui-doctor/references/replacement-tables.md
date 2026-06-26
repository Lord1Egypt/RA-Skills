# IDS Component Replacement Tables

Use these tables when scanning for raw HTML, third-party components, or custom implementations that should be replaced with IDS equivalents.

## Third-Party UI Library Detection

Check for imports from third-party UI libraries that overlap with IDS. Common libraries to flag:

| Third-Party Library                 | Common Imports to Flag                                    | IDS Replacement                |
| ----------------------------------- | --------------------------------------------------------- | ------------------------------ |
| Material UI (`@mui/*`)              | `Button`, `TextField`, `Select`, `Modal`, `Table`, `Tabs` | Equivalent `Iress*` components |
| Ant Design (`antd`)                 | `Button`, `Input`, `Select`, `Modal`, `Table`, `Tabs`     | Equivalent `Iress*` components |
| Chakra UI (`@chakra-ui/*`)          | `Button`, `Input`, `Select`, `Modal`, `Table`             | Equivalent `Iress*` components |
| React Bootstrap (`react-bootstrap`) | `Button`, `Form`, `Modal`, `Table`, `Nav`                 | Equivalent `Iress*` components |
| Radix UI (`@radix-ui/*`)            | `Dialog`, `Popover`, `Tooltip`, `Tabs`, `Select`          | Equivalent `Iress*` components |
| Headless UI (`@headlessui/react`)   | `Dialog`, `Popover`, `Menu`, `Tab`, `Switch`              | Equivalent `Iress*` components |

**How to detect:** Search for import statements matching these package names. Any UI component imported from a third-party library that has an IDS equivalent should be flagged as a **High** priority replacement.

```typescript
// ❌ Third-party UI component — should use IDS
import { Button } from '@mui/material';
import { Modal } from 'antd';
import { Dialog } from '@radix-ui/react-dialog';

// ✅ IDS components
import { IressButton, IressModal } from '@iress-oss/ids-components';
```

## HTML Element → IDS Component Replacement Map

| Raw HTML / Custom Code                  | IDS Replacement                                       | Priority |
| --------------------------------------- | ----------------------------------------------------- | -------- |
| `<button>`                              | `IressButton`                                         | High     |
| `<a>` (navigation link)                 | `IressLink`                                           | High     |
| `<input type="text">`                   | `IressField` + `IressInput`                           | High     |
| `<input type="checkbox">`               | `IressCheckbox`                                       | High     |
| `<input type="radio">`                  | `IressRadio` + `IressRadioGroup`                      | High     |
| `<select>`                              | `IressField` + `IressSelect`                          | High     |
| `<textarea>`                            | `IressField` + `IressInput`                           | High     |
| `<table>`                               | `IressTable`                                          | High     |
| `<label>`                               | `IressField` (wraps input with label)                 | High     |
| `<h1>`–`<h6>`, `<p>`, `<span>` (styled) | `IressText`                                           | Medium   |
| `<img>`                                 | `IressImage`                                          | Medium   |
| `<hr>`                                  | `IressDivider`                                        | Medium   |
| `<dialog>` / custom modal               | `IressModal`                                          | High     |
| Custom confirmation / danger dialog     | `IressModal status="danger"` (or `success`/`warning`) | High     |
| Custom drawer / slideout                | `IressSlideout`                                       | High     |
| Custom tooltip                          | `IressTooltip`                                        | Medium   |
| Custom popover                          | `IressPopover`                                        | Medium   |
| Custom tabs                             | `IressTabSet` + `IressTab`                            | High     |
| Custom spinner / loader                 | `IressSpinner`                                        | Medium   |
| Custom skeleton loader                  | `IressSkeleton`                                       | Low      |
| Custom progress bar                     | `IressProgress`                                       | Low      |
| Custom alert / toast                    | `IressAlert` / `IressToaster`                         | High     |
| Custom card / panel                     | `IressCard` / `IressPanel`                            | Medium   |
| Custom toggle / switch                  | `IressToggle`                                         | High     |
| Custom badge / tag                      | `IressTag` / `IressPill`                              | Low      |
| Custom breadcrumbs                      | `IressBreadcrumbs`                                    | Medium   |
| Custom side navigation                  | `IressSideNav`                                        | Medium   |
| Custom context menu                     | `IressMenu` + `IressMenuItem`                         | Medium   |
| Custom icon (SVG inline)                | `IressIcon`                                           | Medium   |
| `<div>` with flex column styles         | `IressStack`                                          | Medium   |
| `<div>` with flex row styles            | `IressInline`                                         | Medium   |
| `<div>` with grid styles                | `IressRow` + `IressCol`                               | Medium   |
| `<div>` with max-width container        | `IressContainer`                                      | Low      |
| `<form>`                                | `IressForm` + `IressFormField`                        | High     |
| `<input type="range">`                  | `IressSlider`                                         | Medium   |
| `<input type="number">` (currency)      | `IressField` + `IressInputCurrency`                   | Medium   |
| `<details>` / custom accordion          | `IressExpander`                                       | Medium   |
| Custom autocomplete / typeahead         | `IressAutocomplete`                                   | High     |
| Custom select with search               | `IressField` + `IressSelect`                          | High     |
| Custom read-only display                | `IressReadonly`                                       | Medium   |
| Custom segmented control / button group | `IressButtonGroup`                                    | Medium   |
| Custom validation messages              | `IressValidationMessage` / `IressValidationSummary`   | High     |
| Custom styled wrapper `<div>`           | `IressStyled`                                         | Low      |

## What to Look For

```typescript
// ❌ Raw HTML — should use IDS components
<button onClick={handleClick}>Submit</button>
<input type="text" placeholder="Name" />
<select>
  <option>Option 1</option>
</select>
<div className="modal-overlay">...</div>
<div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>...</div>

// ✅ IDS components
<IressButton mode="primary" onClick={handleClick}>Submit</IressButton>
<IressField label="Name" htmlFor="name">
  <IressInput id="name" placeholder="Name" />
</IressField>
<IressField label="Options" htmlFor="options">
  <IressSelect id="options">
    <option>Option 1</option>
  </IressSelect>
</IressField>
<IressModal open={isOpen} onClose={handleClose}>...</IressModal>
<IressStack gap="4">...</IressStack>
```

## Acceptable Exceptions

Not every raw HTML element is a violation. The following are **acceptable exceptions** that should NOT be flagged:

| Pattern                                                      | Why It's Acceptable                                                                                                                     |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `<a>` inside markdown/MDX renderers                          | Content-driven, not application UI                                                                                                      |
| `<button>` inside third-party widgets the app cannot control | External dependency constraint                                                                                                          |
| `<table>` in email templates                                 | Email clients don't support custom components                                                                                           |
| `<img>` in SVG sprites or `<picture>` elements               | IressImage doesn't cover these use cases                                                                                                |
| `<div>` for ref targets, portals, or measurement containers  | Technical necessity, not layout                                                                                                         |
| Raw elements in test files / stories for demonstration       | Not shipped to users                                                                                                                    |
| `<form>` wrapping a single action (e.g., search bar)         | `IressForm` is best for multi-field forms; standalone search inputs may use `IressAutocomplete` or `IressField` + `IressInput` directly |
| `<input type="hidden">`                                      | Not user-facing UI                                                                                                                      |
| Custom components wrapping IDS components internally         | App-level abstraction is valid as long as IDS components are used underneath                                                            |

**When reporting:** If a potential violation falls into an exception category, note it as "Reviewed — Acceptable Exception" rather than a finding. This prevents false positives and keeps reports actionable.
