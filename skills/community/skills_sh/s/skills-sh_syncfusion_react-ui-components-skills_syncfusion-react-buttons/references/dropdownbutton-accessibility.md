# Accessibility — Syncfusion React DropDownButton

## Compliance Summary

| Accessibility Criteria | Support |
|------------------------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader | ✅ Full |
| Right-To-Left (RTL) | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device | ✅ Full |
| Keyboard Navigation | ✅ Full |
| accessibility-checker validation | ✅ Full |
| axe-core validation | ✅ Full |

---

## WAI-ARIA Attributes

The DropDownButton component automatically manages the following ARIA attributes:

| Attribute | Purpose |
|-----------|---------|
| `role="button"` | Identifies the trigger element as a button |
| `role="menu"` | Identifies the popup container |
| `role="menuitem"` | Identifies each popup item |
| `aria-haspopup` | Indicates the button controls a popup menu |
| `aria-expanded` | Reflects whether the popup is open (`true`) or closed (`false`) |
| `aria-owns` | Links the button to its popup in the accessibility tree |
| `aria-disabled` | Marks the button as disabled when `disabled={true}` |

No manual ARIA wiring is required — the component handles these automatically.

---

## Keyboard Interaction

| Key | Action |
|-----|--------|
| `Enter` / `Space` | Opens the popup (or activates the highlighted item and closes) |
| `Down Arrow` | Moves focus to the next popup item |
| `Up Arrow` | Moves focus to the previous popup item |
| `Alt + Down Arrow` | Opens the popup |
| `Alt + Up Arrow` | Closes the popup |
| `Escape` | Closes the popup |

---

## RTL Support

Enable right-to-left layout for RTL languages (Arabic, Hebrew, Urdu, etc.):

```tsx
<DropDownButtonComponent
  items={items}
  iconCss="ddb-icons e-message"
  enableRtl={true}
>
  Message
</DropDownButtonComponent>
```

---

## Disabled State

A disabled button is excluded from the tab order and is not interactive:

```tsx
<DropDownButtonComponent items={items} disabled={true}>
  Unavailable
</DropDownButtonComponent>
```

The `aria-disabled="true"` attribute is set automatically.

---

## Best Practices

- Provide meaningful button text or an `aria-label` when using icon-only buttons:
  ```tsx
  <DropDownButtonComponent
    items={items}
    iconCss="e-icons e-menu"
    cssClass="e-caret-hide"
    // Add aria-label via the HTML element
    ref={(scope) => {
      if (scope) scope.element.setAttribute('aria-label', 'Open menu');
    }}
  />
  ```
- Ensure popup item text is descriptive (avoid "Click here" or "Item 1").
- Use separators and grouping to improve navigation for screen reader users.
- Test with assistive tools: [accessibility-checker](https://www.npmjs.com/package/accessibility-checker), [axe-core](https://www.npmjs.com/package/axe-core).
