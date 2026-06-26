# Accessibility — Syncfusion React RadioButton

The Syncfusion React RadioButton is fully accessible and compliant with major accessibility standards.

---

## Compliance Summary

| Accessibility Criteria | Compliance |
|------------------------|-----------|
| WCAG 2.2 | ✅ Full support |
| Section 508 | ✅ Full support |
| Screen Reader Support | ✅ Full support |
| Right-To-Left Support | ✅ Full support |
| Color Contrast | ✅ Meets WCAG contrast ratios |
| Mobile Device Support | ✅ Full support |
| Keyboard Navigation | ✅ Full support |
| Accessibility Checker Validation | ✅ Passes |
| axe-core Validation | ✅ Passes |

---

## WAI-ARIA Attributes

The RadioButton follows the [WAI-ARIA radio button pattern](https://www.w3.org/WAI/ARIA/apg/patterns/radio/). These ARIA attributes are applied automatically:

| Attribute | Purpose |
|-----------|---------|
| `role="radio"` | Identifies the element as a radio button for assistive technologies |
| `aria-checked` | Communicates the checked (`true`) or unchecked (`false`) state to screen readers |
| `aria-disabled` | Indicates when the button is disabled and cannot be interacted with |
| `aria-label` | Provides an accessible name when no visible label is present |

These attributes are managed by Syncfusion automatically — no manual ARIA attributes needed when using the `label` property.

---

## Keyboard Interaction

The RadioButton implements [W3C keyboard interaction guidelines](https://www.w3.org/WAI/ARIA/apg/patterns/radio/#keyboardinteraction):

| Key | Action |
|-----|--------|
| `Tab` | Moves focus to the next RadioButton group or focusable element |
| `Shift + Tab` | Moves focus to the previous focusable element |
| `Up Arrow` / `Left Arrow` | Selects the **previous** RadioButton in the group |
| `Down Arrow` / `Right Arrow` | Selects the **next** RadioButton in the group |

> **Note:** Arrow keys move selection **within** a named group. `Tab` moves focus **between** groups and other focusable elements.

---

## Accessible Usage Example

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <fieldset>
      <legend>Choose your preferred contact method</legend>
      <ul>
        <li><RadioButtonComponent label="Email"  name="contact" value="email"  checked={true} /></li>
        <li><RadioButtonComponent label="Phone"  name="contact" value="phone" /></li>
        <li><RadioButtonComponent label="SMS"    name="contact" value="sms" /></li>
      </ul>
    </fieldset>
  );
}
export default App;
```

> **Best practice:** Wrap radio groups in a `<fieldset>` with a `<legend>` to give screen readers context about what the group represents.

---

## RTL Accessibility

Right-to-left support is built in. Enabling `enableRtl` flips the layout for RTL languages while maintaining all ARIA attributes and keyboard navigation:

```tsx
<RadioButtonComponent label="العربية" name="lang" enableRtl={true} />
```

---

## Testing Accessibility

The RadioButton's accessibility is validated with:
- [`accessibility-checker`](https://www.npmjs.com/package/accessibility-checker) — automated accessibility testing
- [`axe-core`](https://www.npmjs.com/package/axe-core) — industry-standard accessibility engine

You can test a live sample at: [https://ej2.syncfusion.com/accessibility/radiobutton.html](https://ej2.syncfusion.com/accessibility/radiobutton.html)

---

## See Also

- [features-and-state.md](features-and-state.md) — `disabled` and `enableRtl` usage
- [api.md](api.md) — `htmlAttributes` for additional ARIA overrides
