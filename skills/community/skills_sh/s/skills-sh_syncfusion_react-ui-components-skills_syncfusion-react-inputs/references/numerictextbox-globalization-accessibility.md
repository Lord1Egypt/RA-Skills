## Globalization & Accessibility

This reference covers internationalization (number formats, locales), right-to-left (RTL) support, and accessibility best practices for `NumericTextBoxComponent`.

## Table of Contents
- [Number Formatting & Locales](#number-formatting--locales)
- [Currency & Locale-aware Formats](#currency--locale-aware-formats)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Keyboard Interaction](#keyboard-interaction)
- [Screen Reader & ARIA](#screen-reader--aria)
- [Color Contrast & Focus](#color-contrast--focus)
- [Examples](#examples)
- [Edge Cases & Troubleshooting](#edge-cases--troubleshooting)

## Number Formatting & Locales

Use the `format` and `locale` (or globalize/CLDR) settings to control number display. Syncfusion components respect locale-specific grouping separators and decimal markers.

```jsx
<NumericTextBoxComponent value={12345.67} format="n" locale="fr-FR" />
```

In `fr-FR` this will display `12 345,67` (space group separator, comma decimal).

## Currency & Locale-aware Formats

Use `format="c"` or `format="c2"` with appropriate `locale` to display currency symbols in the correct position and format.

```jsx
<NumericTextBoxComponent value={99.99} format="c2" locale="en-US" />
<NumericTextBoxComponent value={99.99} format="c2" locale="de-DE" />
```

## Right-to-Left (RTL) Support

Enable RTL at application or component level depending on your framework setup. Prefer using the component's `enableRtl` property to render the NumericTextBox in RTL mode; alternatively, set `dir="rtl"` on a parent element if your layout requires it.

Example (component-level):

```jsx
<NumericTextBoxComponent value={20} enableRtl={true} />
```

Notes:
- When using `appendTemplate` or `prependTemplate`, verify alignment in RTL and adjust CSS if needed.
- Confirm keyboard navigation order remains logical when switching direction.

## Keyboard Interaction

- `ArrowUp` / `ArrowDown` increase/decrease value by `step`.
- `Home` / `End` may be used to move cursor inside text (component-dependent).
- Focus management: ensure focus styles are visible and keyboard-only users can perceive focus.

## Screen Reader & ARIA

Provide accessible labels and use ARIA attributes where necessary:

```jsx
<label htmlFor="price">Price</label>
<NumericTextBoxComponent id="price" aria-labelledby="price" />
```

Recommendations:
- Use `aria-label` or `aria-labelledby` for unlabeled fields.
- When displaying formatted value with prefix/suffix, expose the raw numeric value via `aria-valuenow` if supported.
- For invalid values, set `aria-invalid="true"` and provide an `aria-describedby` pointing to the error message.

## Color Contrast & Focus

- Ensure the control's text and focus ring meet WCAG contrast ratios (4.5:1 for normal text).
- Provide visible focus outlines for keyboard users. Avoid removing outlines without replacement.

## Examples

1. Locale-aware currency:

```jsx
<NumericTextBoxComponent value={1500} format="c0" locale="ja-JP" />
```

2. RTL with prefix/suffix:

```jsx
<div dir="rtl">
  <NumericTextBoxComponent value={20} prefix="kg " suffix=" units" />
</div>
```

## Edge Cases & Troubleshooting

- Decimal and grouping mismatch: ensure the `locale` matches user's input method (keyboard decimal separator).
- CSS overrides: custom themes can unintentionally hide focus outlines; test with keyboard-only navigation.
- Screen reader verbosity: formatted strings with currency symbols may be read verbosely; use `aria-label` to provide concise support text when appropriate.

---

See `references/formats-and-validation.md` for format patterns and `references/accessibility.md` in the main library for shared accessibility guidance.
