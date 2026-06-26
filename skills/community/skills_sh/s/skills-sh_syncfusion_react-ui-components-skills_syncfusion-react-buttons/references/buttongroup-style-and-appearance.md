# Style and Appearance — Syncfusion React ButtonGroup

## CSS Classes Reference

Customize ButtonGroup appearance by overriding its default CSS classes:

| CSS Class | Purpose |
|---|---|
| `.e-btn` | Base button styling within the ButtonGroup |
| `.e-btn:hover` | Button hover state |
| `.e-btn:focus` | Button focus state |
| `.e-btn:active` | Button active/pressed state |
| `.e-primary` | Primary button styling |
| `.e-success` | Success button styling |
| `.e-info` | Informational button styling |
| `.e-warning` | Warning button styling |
| `.e-danger` | Danger button styling |
| `.e-outline` | Outline button styling (transparent background, visible border) |
| `.e-round-corner` | Border-radius styling (rounded group corners) |
| `.e-vertical` | Vertical button arrangement |
| `.e-rtl` | Right-to-left layout |

## Custom CSS Overrides

Override any class in your stylesheet to change colors, borders, padding, or other visual properties. For example, to change the default button background:

```css
.e-btn-group .e-btn {
  background-color: #your-color;
  border-color: #your-border-color;
}
```

## Theme Studio

Generate custom themes for the ButtonGroup using [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material). Theme Studio provides a visual interface to customize all component tokens and export ready-to-use CSS.
