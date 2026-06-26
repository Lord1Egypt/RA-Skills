# Accessibility — Syncfusion React ColorPicker

## Table of Contents
- [Compliance Overview](#compliance-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Ensuring Accessibility in Your App](#ensuring-accessibility-in-your-app)

---

## Compliance Overview

The Syncfusion React ColorPicker component is built to meet major accessibility standards:

| Accessibility Criteria | Support |
|----------------------|---------|
| WCAG 2.2 | ✅ Full |
| Section 508 | ✅ Full |
| Screen Reader Support | ✅ Full |
| Right-To-Left Support | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device Support | ✅ Full |
| Keyboard Navigation Support | ✅ Full |
| Accessibility Checker Validation | ✅ Full |
| Axe-core Validation | ✅ Full |

---

## WAI-ARIA Attributes

The ColorPicker follows [WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/) patterns and applies the following ARIA attributes automatically:

| Attribute | Purpose |
|-----------|---------|
| `role="color"` | Identifies the ColorPicker as a color input component |
| `role="gridcell"` | Applied to each palette tile |
| `aria-label` | Accessible name for each palette tile (color value as label) |
| `aria-selected` | Indicates which tile is currently selected |
| `aria-haspopup` | Indicates a popup is available (on the SplitButton trigger) |
| `aria-expanded` | Reflects whether the popup is currently open |
| `aria-owns` | Links the trigger button to the popup it controls |
| `aria-disabled` | Marks the component as non-interactive when `disabled={true}` |

No extra ARIA configuration is needed — all attributes are managed automatically.

---

## Keyboard Navigation

Full keyboard support is provided for both the picker gradient area and the palette grid:

| Key | Action |
|-----|--------|
| `Up Arrow` | Moves the picker handle / palette selection upward |
| `Down Arrow` | Moves the picker handle / palette selection downward |
| `Left Arrow` | Moves the picker handle / palette selection left |
| `Right Arrow` | Moves the picker handle / palette selection right |
| `Enter` | Applies the currently selected color value |
| `Tab` | Moves focus to the next focusable element inside the ColorPicker popup |

Arrow key behavior:
- **In Picker mode:** moves the gradient selection handle to adjust hue/saturation
- **In Palette mode:** navigates between palette tiles

---

## Ensuring Accessibility in Your App

When integrating the ColorPicker, follow these guidelines to maintain full accessibility:

**1. Always provide a visible label:**
```tsx
<label htmlFor="theme-color">Theme Color</label>
<ColorPickerComponent id="theme-color" />
```

**2. Use sufficient color contrast** in your surrounding UI — the ColorPicker itself meets contrast requirements, but preview areas you build should also meet WCAG AA (4.5:1) contrast ratios.

**3. Test with screen readers** (NVDA, JAWS, VoiceOver). The component announces color names and selection state automatically.

**4. Validate with tools:**
- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- [axe-core](https://www.npmjs.com/package/axe-core)
- Live demo: https://ej2.syncfusion.com/accessibility/color-picker.html

**5. Avoid relying solely on color** to convey information in your app — pair color selections with text labels or values (the `change` event's `args.currentValue.hex` can be displayed alongside the picker).
