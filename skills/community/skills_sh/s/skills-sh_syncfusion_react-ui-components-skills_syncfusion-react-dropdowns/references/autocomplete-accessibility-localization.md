# Accessibility and Localization – Syncfusion React AutoComplete

## Table of Contents
- [Accessibility Compliance](#accessibility-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [RTL Support](#rtl-support)
- [Localization](#localization)

---

## Accessibility Compliance

The AutoComplete is designed against WAI-ARIA specifications and meets the following standards:

| Criteria | Support |
|---|---|
| WCAG 2.2 | Partial |
| Section 508 | Partial |
| Screen Reader | Full |
| Right-To-Left | Full |
| Color Contrast | Full |
| Mobile Device | Full |
| Keyboard Navigation | Full |
| Accessibility Checker Validation | Full |
| Axe-core Validation | Full |

---

## WAI-ARIA Attributes

The AutoComplete applies the following ARIA attributes automatically:

| Attribute | Purpose |
|---|---|
| `aria-haspopup` | Indicates whether the input has an associated suggestion list |
| `aria-expanded` | Indicates whether the suggestion popup is open |
| `aria-selected` | Indicates the currently selected item in the list |
| `aria-readonly` | Indicates the read-only state of the input |
| `aria-disabled` | Indicates whether the component is disabled |
| `aria-activedescendant` | Holds the ID of the focused list item |
| `aria-owns` | References the popup element as a child |
| `aria-autocomplete` | Set to `'both'` — indicates inline suggestion and list |

---

## Keyboard Navigation

| Key | Action |
|---|---|
| `Arrow Down` | Opens popup (if closed); selects first item or next item (if open) |
| `Arrow Up` | Opens popup (if closed); selects last item or previous item (if open) |
| `Page Down` | Scrolls to next page; selects first item on that page |
| `Page Up` | Scrolls to previous page; selects first item on that page |
| `Enter` | Confirms the focused suggestion and sets it as the value |
| `Tab` | Closes popup and moves focus to next element |
| `Shift + Tab` | Closes popup and moves focus to previous element |
| `Alt + Down Arrow` | Opens the suggestion popup |
| `Alt + Up Arrow` | Opens popup (if closed); closes popup (if open) |
| `Escape` | Closes popup and clears the current selection |
| `Home` | Moves cursor to beginning of the input |
| `End` | Moves cursor to end of the input |

---

## RTL Support

Enable right-to-left rendering with `enableRtl`:

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={sportsData}
  enableRtl={true}
  placeholder="Find a game"
/>
```

---

## Localization

Use the `L10n` class from `@syncfusion/ej2-base` to localize the component's built-in strings:

| Locale Key | Default (en-US) |
|---|---|
| `noRecordsTemplate` | No Records Found |
| `actionFailureTemplate` | The Request Failed |

### Example: French localization

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const customerData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });
  const fields: object = { value: 'ContactName' };
  // take(0) to trigger noRecordsTemplate
  const query: Query = new Query().select(['ContactName', 'CustomerID']).take(0);

  React.useEffect(() => {
    L10n.load({
      'fr-BE': {
        dropdowns: {
          noRecordsTemplate: 'Aucun enregistrement trouvé',
          actionFailureTemplate: "Modèle d'échec d'action",
        }
      }
    });
  }, []);

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={customerData}
      fields={fields}
      query={query}
      locale="fr-BE"
      placeholder="Trouver un client"
    />
  );
}
```

> Call `L10n.load()` before the component renders (e.g., inside `useEffect` or `componentWillMount`). The `locale` prop on the component then activates the loaded culture.
