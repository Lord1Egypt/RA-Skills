# Accessibility, Styling, and Localization in Syncfusion React MultiSelect

## Table of Contents
- [Accessibility Overview](#accessibility-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [CSS Customization](#css-customization)
- [RTL Support](#rtl-support)
- [Localization](#localization)

---

## Accessibility Overview

The MultiSelect component meets the following accessibility standards out of the box:

| Standard | Support |
|----------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader | ✅ Full |
| RTL | ✅ Full |
| Keyboard Navigation | ✅ Full |
| Mobile Device | ✅ Full |
| Color Contrast | ✅ Full |
| Axe-core Validation | ✅ Full |

No extra configuration is required to meet these standards — the component ships with the necessary ARIA roles, keyboard support, and focus management.

---

## WAI-ARIA Attributes

The MultiSelect follows [WAI-ARIA combobox patterns](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). The following ARIA attributes are applied automatically:

| Attribute | Purpose |
|-----------|---------|
| `aria-haspopup` | Indicates the input has an associated popup list |
| `aria-expanded` | Reflects whether the popup is open or closed |
| `aria-selected` | Marks the currently selected option |
| `aria-readonly` | Reflects the readonly state of the component |
| `aria-disabled` | Reflects the disabled state of the component |
| `aria-activedescendant` | Points to the active list item for screen reader focus |
| `aria-owns` | Associates the popup list as a child element of the input |

These are managed internally — you do not need to set them manually.

---

## Keyboard Navigation

Users can fully operate the MultiSelect without a mouse:

| Key | Action |
|-----|--------|
| `Arrow Down` | Focus first item (if none selected) or move to next item |
| `Arrow Up` | Move focus to previous item |
| `Page Down` | Scroll down one page in the popup |
| `Page Up` | Scroll up one page in the popup |
| `Enter` | Select focused item; close popup if open |
| `Tab` | Close popup and move focus to next element on page |
| `Shift + Tab` | Close popup and move focus to previous element on page |
| `Alt + Down` | Open the popup list |
| `Alt + Up` | Close the popup list |
| `Esc` | Close popup; keep current selections |
| `Home` | Move focus to the first item |
| `End` | Move focus to the last item |

To set an access key for keyboard focus to the component, use the `htmlAttributes` prop:

```tsx
<MultiSelectComponent
  id="mtselement"
  dataSource={sportsData}
  htmlAttributes={{ accesskey: 't' }}
  placeholder="Focus with Alt+T"
/>
```

---

## CSS Customization

Override built-in CSS classes to match your design system. All selectors target the component's DOM elements:

### Wrapper Background Color

```css
.e-multiselect.e-input-group .e-multi-select-wrapper {
  background-color: #f0f7ff;
}
```

### Chip (Tag) Appearance

```css
/* Chip content (text) */
.e-multiselect .e-multi-select-wrapper .e-chips .e-chipcontent {
  font-family: 'Segoe UI', sans-serif;
  font-size: 13px;
  color: #1a1a2e;
}

/* Chip container */
.e-multi-select-wrapper .e-chips {
  background-color: #dbeafe;
  height: 26px;
  border-radius: 4px;
}
```

### Dropdown Icon Color and Size

```css
.e-multiselect.e-input-group .e-input-group-icon,
.e-multiselect.e-input-group.e-control-wrapper .e-input-group-icon:hover {
  color: #3b82f6;
  font-size: 14px;
}
```

### Delimiter Text Styling

Applies when `mode="Delimiter"` (comma-separated selected values):

```css
.e-multiselect .e-delim-values {
  color: #1d4ed8;
  font-size: 14px;
}
```

### Popup Background

```css
.e-multiselect .e-popup .e-dropdownbase {
  background-color: #fafafa;
}
```

### Focused State Border

```css
.e-multiselect.e-input-group.e-input-focus .e-multi-select-wrapper {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
```

> **Theme Studio:** For systematic design token overrides across all Syncfusion components, use Syncfusion's [Theme Studio](https://ej2.syncfusion.com/themestudio/) to generate a custom CSS file.

---

## RTL Support

Enable right-to-left text direction for Arabic, Hebrew, or other RTL languages:

```tsx
<MultiSelectComponent
  id="mtselement"
  dataSource={sportsData}
  enableRtl={true}
  placeholder="اختر رياضة"
/>
```

RTL flips the layout: dropdown icon appears on the left, chips flow right-to-left, popup aligns to the right.

---

## Localization

Translate the default static text strings (`noRecordsTemplate`, `actionFailureTemplate`) using the `L10n` class:

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

// Register translations before rendering the component
L10n.load({
  'fr-BE': {
    'multi-select': {
      'noRecordsTemplate': 'Aucun enregistrement trouvé',
      'actionFailureTemplate': "Modèle d'échec d'action",
    },
  },
});

export default function App() {
  const customerData = new DataManager({
    adaptor: new ODataV4Adaptor(),
    crossDomain: true,
    url: 'url',
  });
  const fields = { text: 'ContactName', value: 'CustomerID' };
  // Take 0 results to show noRecordsTemplate
  const query = new Query().select(['ContactName', 'CustomerID']).take(0);

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={customerData}
      fields={fields}
      query={query}
      locale="fr-BE"
      placeholder="Sélectionner un client"
    />
  );
}
```

### Supported Locale Keys

| Key | Default (en-US) |
|-----|-----------------|
| `noRecordsTemplate` | `No records found` |
| `actionFailureTemplate` | `Request failed` |

> **When to use `L10n` vs. template props:**
> - For simple translated strings → use `L10n` with `locale` prop
> - For rich JSX content (icons, links, custom markup) → use `noRecordsTemplate` / `actionFailureTemplate` props directly

## See Also

- [Templates](templates.md) — custom JSX no-records and action-failure templates
- [Selection and Features](selection-and-features.md) — chip customization via `tagging` event
- [Data Binding](data-binding.md) — remote data that may trigger action failure
