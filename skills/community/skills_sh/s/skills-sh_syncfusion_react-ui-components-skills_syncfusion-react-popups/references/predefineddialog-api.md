# Predefined Dialogs — API Reference (React)

> Source: [Syncfusion React Predefined Dialogs documentation](https://ej2.syncfusion.com/react/documentation/predefined-dialogs/)
>
> All code examples in the skill must use **only** the APIs listed here.
> Do NOT use `<ejs-dialog>` component syntax — predefined dialogs are utility-based.

---

## Import

```ts
import { DialogUtility } from '@syncfusion/ej2-react-popups';
```

---

## DialogUtility Methods

### `DialogUtility.alert(options: AlertDialogArgs): Dialog`

Opens an alert dialog with an OK button.

### `DialogUtility.confirm(options: ConfirmDialogArgs): Dialog`

Opens a confirm dialog with OK and Cancel buttons.
Also used for **prompt** dialogs by embedding an `<input>` in the `content` field.

---

## Shared Options (AlertDialogArgs / ConfirmDialogArgs)

| Property | Type | Default | Description |
|---|---|---|---|
| `title` | `string` | `''` | Dialog header title |
| `content` | `string \| HTMLElement` | `''` | Dialog body content; supports HTML strings |
| `width` | `string \| number` | `'100%'` | Dialog width (e.g. `'300px'`) |
| `height` | `string \| number` | `'auto'` | Dialog height (e.g. `'200px'`) |
| `cssClass` | `string` | `''` | CSS class(es) added to the dialog root element |
| `position` | `PositionDataModel` | `{ X: 'center', Y: 'center' }` | Dialog position: `X` = `left\|center\|right\|offset`, `Y` = `top\|center\|bottom\|offset` |
| `animationSettings` | `{ effect?: string; duration?: number; delay?: number }` | `{ effect: 'Fade', duration: 400, delay: 0 }` | Open/close animation settings |
| `isDraggable` | `boolean` | `false` | Allow users to drag the dialog by its header |
| `showCloseIcon` | `boolean` | `false` | Show × close icon in the header |
| `closeOnEscape` | `boolean` | `false` | Close dialog when Escape key is pressed |
| `okButton` | `ButtonArgs` | — | Customize the OK button |
| `cancelButton` | `ButtonArgs` | — | Customize the Cancel button (confirm/prompt only) |

---

## ButtonArgs

| Property | Type | Description |
|---|---|---|
| `text` | `string` | Button label text |
| `icon` | `string` | CSS icon class (e.g. `'e-icons e-check'`) |
| `click` | `() => void` | Callback when button is clicked |

---

## Dialog Instance (return value)

The return value of `DialogUtility.alert()` and `DialogUtility.confirm()` is a **Dialog instance** with the following method:

| Method | Signature | Description |
|---|---|---|
| `hide` | `hide(event?: Event): void` | Programmatically closes the dialog |

---

## PositionDataModel

| Property | Type | Values |
|---|---|---|
| `X` | `string \| number` | `'left'`, `'center'`, `'right'`, or numeric pixel offset |
| `Y` | `string \| number` | `'top'`, `'center'`, `'bottom'`, or numeric pixel offset |

---

## animationSettings Effects

Common effect values (from Syncfusion animation library):
`'Fade'`, `'FadeZoom'`, `'Zoom'`, `'FlipXDown'`, `'FlipXUp'`, `'FlipYLeft'`, `'FlipYRight'`, `'SlideBottom'`, `'SlideLeft'`, `'SlideRight'`, `'SlideTop'`, `'None'`

---

## Notes

- **`DialogUtility.alert()`** — shows only an OK button.
- **`DialogUtility.confirm()`** — shows both OK and Cancel buttons; also used to build prompt dialogs by placing an `<input>` in the `content` HTML string.
- Dialogs are **modal by default** when created with `DialogUtility`.
- Call `.hide()` on the returned instance inside button `click` handlers to close the dialog.
- Use `cssClass` + CSS rules to apply `max-width`, `min-width`, `max-height`, `min-height` constraints.
