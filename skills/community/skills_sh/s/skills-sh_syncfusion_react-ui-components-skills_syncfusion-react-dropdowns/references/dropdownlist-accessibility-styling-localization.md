# Accessibility, Styling & Localization

## Table of Contents
- [Accessibility Compliance](#accessibility-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [cssClass Prop](#cssclass-prop)
- [CSS Customization](#css-customization)
  - [Wrapper Element](#wrapper-element)
  - [Dropdown Icon](#dropdown-icon)
  - [Popup List Container](#popup-list-container)
  - [List Items](#list-items)
  - [Placeholder Text](#placeholder-text)
- [Theming](#theming)
- [Localization](#localization)
- [RTL Layout](#rtl-layout)
- [Gotchas](#gotchas)

---

## Accessibility Compliance

The DropDownList meets the following standards:

| Criteria | Support |
|---|---|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader | ✅ Full |
| RTL Support | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Accessibility Checker | ✅ Full |
| Axe-core Validation | ✅ Full |

---

## WAI-ARIA Attributes

The DropDownList follows the [WAI-ARIA combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/):

| Attribute | Purpose |
|---|---|
| `aria-haspopup` | Indicates the input has an associated popup list |
| `aria-expanded` | Reflects whether the popup is open |
| `aria-selected` | Marks the currently selected option |
| `aria-readonly` | Reflects the readonly state |
| `aria-disabled` | Reflects the disabled state |
| `aria-activedescendent` | Points to the active item inside the popup for screen readers |
| `aria-owns` | Associates the popup list as a child of the input |

These attributes are managed automatically — no manual configuration needed.

---

## Keyboard Navigation

| Key | Action |
|---|---|
| `Arrow Down` | Selects the first item (if none selected), or the next item |
| `Arrow Up` | Selects the previous item |
| `Page Down` | Scrolls down one page and selects the first item |
| `Page Up` | Scrolls up one page and selects the first item |
| `Enter` | Confirms selection and closes popup; or opens popup if closed |
| `Tab` | Closes popup and moves focus to the next tab stop |
| `Shift + Tab` | Closes popup and moves focus to the previous tab stop |
| `Alt + Down` | Opens the popup |
| `Alt + Up` | Closes the popup |
| `Escape` | Closes the popup, retaining the current selection |
| `Home` | Selects the first item |
| `End` | Selects the last item |

---

## cssClass Prop

| Detail | Value |
|---|---|
| **Prop** | `cssClass` |
| **Type** | `string` |
| **Default** | `null` |

The `cssClass` prop adds one or more custom CSS class names to the **root element** of the DropDownList component (the `.e-ddl` wrapper). Use it to scope all style overrides to a specific instance without affecting other DropDownList components on the page.

### Basic Usage

```tsx
<DropDownListComponent
  dataSource={sportsData}
  cssClass="my-custom-ddl"
  placeholder="Select a game"
/>
```

This renders as:
```html
<span class="e-control-wrapper e-ddl e-lib e-keyboard my-custom-ddl ...">
```

### Scoped Style Overrides with cssClass

Because `cssClass` is applied to the root wrapper, you can scope all your CSS rules to that class and avoid conflicts with other components:

```tsx
// Component
<DropDownListComponent
  dataSource={countryData}
  fields={fields}
  cssClass="country-picker"
  placeholder="Select a country"
/>
```

```css
/* Scoped to only this instance */
.country-picker .e-input {
  font-size: 14px;
  color: #1a1a2e;
  background-color: #f0f4ff;
}

.country-picker .e-ddl-icon::before {
  color: #4361ee;
}

/* Popup inherits the cssClass too — target it like this */
.country-picker.e-popup .e-list-item.e-hover {
  background-color: #e8edff;
  color: #4361ee;
}

.country-picker.e-popup .e-list-item.e-active {
  background-color: #4361ee;
  color: #ffffff;
}
```

> **Important:** The popup element also receives the `cssClass` value. You can target it using `.your-class.e-popup` or `.your-class .e-list-item`.

### Multiple CSS Classes

Pass a space-separated string to apply multiple classes simultaneously:

```tsx
<DropDownListComponent
  dataSource={data}
  cssClass="compact-ddl dark-theme"
  placeholder="Select"
/>
```

```css
.compact-ddl .e-input { padding: 4px 8px; height: 28px; }
.dark-theme .e-input   { background: #1e1e2e; color: #cdd6f4; }
```

### Applying cssClass Conditionally (React State)

```tsx
import { useState } from 'react';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const [hasError, setHasError] = useState(false);

  return (
    <DropDownListComponent
      dataSource={['Option A', 'Option B', 'Option C']}
      cssClass={hasError ? 'e-error' : ''}
      placeholder="Select an option"
      change={(e) => setHasError(e.value === null)}
    />
  );
}
```

Syncfusion ships a built-in `e-error` CSS class that renders the component with a red border to indicate validation errors.

### Built-in Utility Classes

| Class | Effect |
|---|---|
| `e-error` | Red border — validation error state |
| `e-success` | Green border — validation success state |
| `e-outline` | Outlined input style (Material-like) |
| `e-filled` | Filled input style |

---

## CSS Customization

Target Syncfusion CSS class selectors to override default styles. Always scope to `.e-ddl` to avoid affecting other components.

### Wrapper Element

```css
.e-ddl.e-input-group.e-control-wrapper .e-input {
  font-size: 16px;
  font-family: 'Inter', sans-serif;
  color: #333;
  background: #f9f9f9;
}
```

### Dropdown Icon

```css
/* Change the dropdown arrow icon color */
.e-ddl .e-input-group-icon.e-ddl-icon::before {
  color: #6200ea;
}
```

### Popup List Container

```css
/* Style the popup container */
.e-dropdownbase .e-list-parent.e-ul {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
}
```

### List Items

```css
/* Hover state */
.e-dropdownbase .e-list-item.e-hover {
  background-color: #f3e5f5;
  color: #6200ea;
}

/* Selected state */
.e-dropdownbase .e-list-item.e-active {
  background-color: #6200ea;
  color: #ffffff;
}
```

### Placeholder Text

```css
.e-ddl.e-input-group input::placeholder {
  color: #9e9e9e;
  font-style: italic;
}
```

---

## Theming

Syncfusion provides built-in themes. Switch by changing the CSS import in `App.css`:

```css
/* Tailwind 3 (current default — recommended) */
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";

/* Material 3 */
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/material3.css";

/* Bootstrap 5 */
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/bootstrap5.css";

/* Fluent 2 */
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/fluent2.css";
```

> Always import the base and inputs CSS alongside the dropdowns CSS:
> ```css
> @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
> @import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
> @import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
> ```

For a custom theme, use [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/).

---

## Localization

Override the default English text for no-records and request failure messages using `L10n`:

| Locale key | Default (en-US) |
|---|---|
| `noRecordsTemplate` | `No records found` |
| `actionFailureTemplate` | `The request failed` |

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

// Load French translations before rendering
L10n.load({
  'fr-BE': {
    'dropdowns': {
      noRecordsTemplate: 'Aucun enregistrement trouvé',
      actionFailureTemplate: 'La requête a échoué',
    }
  }
});

export default function App() {
  return (
    <DropDownListComponent
      dataSource={[]}
      locale="fr-BE"
      placeholder="Sélectionnez un élément"
    />
  );
}
```

> `L10n.load()` must be called before the component renders. Do this at app initialization level.

---

## RTL Layout

```tsx
<DropDownListComponent
  dataSource={sportsData}
  enableRtl={true}
  placeholder="Select a game"
/>
```

RTL flips the popup and icon direction for right-to-left languages (Arabic, Hebrew, Urdu, etc.). Combine with `locale` for full internationalization.

---

## Gotchas

- **`cssClass` scopes to the root wrapper AND the popup** — use `.your-class.e-popup` to target popup-level styles; the popup is teleported outside the component's DOM tree but still receives the class.
- **`cssClass` replaces, not merges, on re-render** — when passing a dynamic value, always include all needed classes in the string (e.g., `cssClass={[base, error].filter(Boolean).join(' ')}`).
- **CSS specificity** — Syncfusion styles use specific selectors. If overrides don't work, increase specificity or use `!important` sparingly.
- **Theme consistency** — all three CSS imports (`ej2-base`, `ej2-inputs`, `ej2-react-dropdowns`) must use the same theme name. Mixing themes causes visual glitches.
- **`L10n.load()` timing** — must run before the component first renders; placing it inside a component's render function causes a race condition.
- **Screen reader testing** — ARIA attributes are managed automatically but verify with an actual screen reader (NVDA, VoiceOver) in your specific browser environment.

## See Also

- [Getting Started](getting-started.md) — CSS import setup
- [Grouping & Templates](grouping-and-templates.md) — `noRecordsTemplate` and `actionFailureTemplate` as JSX
- [Features & Configuration](features-and-configuration.md) — `enableRtl`, `readonly`, `enabled`
