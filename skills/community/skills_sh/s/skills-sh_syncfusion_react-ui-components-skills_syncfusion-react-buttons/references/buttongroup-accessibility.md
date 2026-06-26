# Accessibility — Syncfusion React ButtonGroup

## Compliance Summary

The ButtonGroup component meets the following accessibility standards:

| Accessibility Criteria | Support |
|---|---|
| WCAG 2.2 | Full |
| Section 508 | Full |
| Screen Reader Support | Full |
| Right-To-Left Support | Full |
| Color Contrast | Full |
| Mobile Device Support | Full |
| Keyboard Navigation | Full |
| Accessibility Checker Validation | Full |
| Axe-core Accessibility Validation | Full |

## Keyboard Interaction

### Normal (Button) Behavior

| Key | Action |
|---|---|
| `Tab` | Moves focus to the next button in the ButtonGroup |
| `Enter` / `Space` | Activates the focused button |

### Checkbox Behavior

| Key | Action |
|---|---|
| `Tab` | Moves focus to the next button |
| `Space` | Toggles the focused button's checked state |

### Radio Button Behavior

| Key | Action |
|---|---|
| `Tab` | Focuses the currently active (checked) button |
| `Right Arrow` / `Left Arrow` | Moves selection to the next or previous button |

## ARIA Role

Add `role="group"` to the ButtonGroup container for proper semantic grouping. This helps screen readers announce the component as a group of related controls:

```tsx
<div className='e-btn-group' role='group'>
  <ButtonComponent>HTML</ButtonComponent>
  <ButtonComponent>CSS</ButtonComponent>
  <ButtonComponent>Javascript</ButtonComponent>
</div>
```

## Validation Tools

The ButtonGroup's accessibility is validated using:
- [accessibility-checker](https://www.npmjs.com/package/accessibility-checker)
- [axe-core](https://www.npmjs.com/package/axe-core)
