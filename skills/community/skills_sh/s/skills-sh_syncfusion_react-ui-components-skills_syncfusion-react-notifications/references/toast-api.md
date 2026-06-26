# Toast API Reference

**Source:** https://ej2.syncfusion.com/react/documentation/api/toast/index-default  
**Component:** `ToastComponent` from `@syncfusion/ej2-react-notifications`

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Supporting Interfaces](#supporting-interfaces)

---

## Properties

### animation
**Type:** `ToastAnimationSettingsModel`  
**Default:** `{ show: { effect: 'FadeIn', duration: 600, easing: 'linear' }, hide: { effect: 'FadeOut', duration: 600, easing: 'linear' } }`

Specifies the animation configuration settings for showing and hiding the toast.

```tsx
<ToastComponent
  animation={{
    show: { effect: 'SlideBottomIn', duration: 400, easing: 'ease-out' },
    hide: { effect: 'FadeOut', duration: 300, easing: 'ease-in' }
  }}
/>
```

---

### buttons
**Type:** `ButtonModelPropsModel[]`  
**Default:** `[{}]`

Collection of action buttons rendered inside the toast. Each entry uses a `model` (ButtonModel props) and optional `click` handler.

```tsx
<ToastComponent
  buttons={[
    { model: { content: 'Undo' }, click: () => console.log('Undo') },
    { model: { content: 'Dismiss' } }
  ]}
/>
```

---

### content
**Type:** `string | HTMLElement | Function`  
**Default:** `null`

Content displayed in the toast body. Accepts plain text, HTML strings, DOM elements, or JSX-returning functions.

```tsx
<ToastComponent content="File saved successfully" />
<ToastComponent content={() => <p>File <strong>saved</strong></p>} />
```

---

### cssClass
**Type:** `string`  
**Default:** `null`

One or more CSS classes (space-separated) for customizing toast appearance. Built-in semantic classes: `e-toast-success`, `e-toast-info`, `e-toast-warning`, `e-toast-danger`.

```tsx
<ToastComponent cssClass="e-toast-success" />
```

---

### enableHtmlSanitizer
**Type:** `boolean`  
**Default:** `true`

When `true`, sanitizes HTML content in `title` and `content` to prevent XSS. Set to `false` only when rendering trusted HTML content.

---

### enablePersistence
**Type:** `boolean`  
**Default:** `false`

Persists component state between page reloads.

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`

Renders the component in right-to-left direction for RTL language support.

```tsx
<ToastComponent enableRtl={true} />
```

---

### extendedTimeout
**Type:** `number`  
**Default:** `1000`

Additional milliseconds the toast remains visible after user interaction (hover/focus). Extends display time to prevent accidental dismissal while reading.

```tsx
<ToastComponent timeOut={3000} extendedTimeout={5000} />
```

---

### height
**Type:** `string | number`  
**Default:** `'auto'`

Height of the toast in pixels, numbers, or percentages. Number values are treated as pixels.

```tsx
<ToastComponent height={250} />
<ToastComponent height="auto" />
```

---

### icon
**Type:** `string`  
**Default:** `null`

CSS class for an icon displayed at the top-left corner of the toast. Use Syncfusion icon classes (e.g., `e-icons e-check-circle`) or any icon font class.

```tsx
<ToastComponent icon="e-icons e-check-circle" />
```

---

### locale
**Type:** `string`  
**Default:** `''`

Overrides the global culture/localization value for this component. Defaults to the application's global culture (`'en-US'`).

---

### newestOnTop
**Type:** `boolean`  
**Default:** `true`

Controls stacking order of multiple toasts. When `true`, newer toasts appear above older ones. When `false`, new toasts append below the existing stack.

```tsx
<ToastComponent newestOnTop={false} />
```

---

### position
**Type:** `ToastPositionModel`  
**Default:** `{ X: 'Left', Y: 'Top' }`

Position of the toast within the target container. X accepts `'Left'`, `'Center'`, `'Right'`, or numeric/percentage values. Y accepts `'Top'`, `'Bottom'`, or numeric/percentage values.

```tsx
<ToastComponent position={{ X: 'Right', Y: 'Bottom' }} />
<ToastComponent position={{ X: 100, Y: 50 }} />
```

---

### progressDirection
**Type:** `ProgressDirectionType` (`'Ltr'` | `'Rtl'`)  
**Default:** `'Rtl'`

Direction of progress bar fill. `'Rtl'` fills right-to-left (default), `'Ltr'` fills left-to-right.

```tsx
<ToastComponent showProgressBar={true} progressDirection="Ltr" />
```

---

### showCloseButton
**Type:** `boolean`  
**Default:** `false`

Shows a close button allowing users to manually dismiss the toast before timeout.

```tsx
<ToastComponent showCloseButton={true} />
```

---

### showProgressBar
**Type:** `boolean`  
**Default:** `false`

Displays a progress bar that visually indicates remaining display time.

```tsx
<ToastComponent showProgressBar={true} />
```

---

### target
**Type:** `HTMLElement | Element | string`  
**Default:** `null` (renders in `document.body`)

Target container element or selector where the toast renders. Toast position is calculated relative to this element.

```tsx
<ToastComponent target="#my-panel" />
<ToastComponent target={document.getElementById('panel')!} />
```

---

### template
**Type:** `string | Function`  
**Default:** `null`

HTML string, element ID selector, or function returning JSX for fully custom toast layout. When set, overrides `title` and `content` rendering.

```tsx
<ToastComponent template="#myTemplate" />
<ToastComponent template={() => <div>Custom content</div>} />
```

---

### timeOut
**Type:** `number`  
**Default:** `5000`

Duration in milliseconds before the toast auto-dismisses. Set to `0` for a persistent toast that stays until manually closed.

```tsx
<ToastComponent timeOut={3000} />
<ToastComponent timeOut={0} showCloseButton={true} />
```

---

### title
**Type:** `string | Function`  
**Default:** `null`

Headline text of the toast. Accepts plain text, HTML strings, or JSX-returning functions.

```tsx
<ToastComponent title="Upload Complete" />
```

---

### width
**Type:** `string | number`  
**Default:** `'300'`

Width of the toast in pixels, numbers, or percentages. Number values are treated as pixels. On mobile, the default is `100%`.

```tsx
<ToastComponent width={400} />
<ToastComponent width="100%" />
```

---

## Methods

### show
**Signature:** `show(toastObj?: ToastModel): void`

Displays the toast. Optionally pass a `ToastModel` object to override component-level properties for this specific invocation.

```tsx
// Show with component defaults
toastInstance.show();

// Show with per-call overrides
toastInstance.show({
  title: 'Dynamic Title',
  content: 'Dynamic content',
  cssClass: 'e-toast-success',
  timeOut: 3000
});
```

---

### hide
**Signature:** `hide(element?: HTMLElement | Element | string): void`

Hides a specific toast element or all toasts when `'All'` is passed.

```tsx
// Hide all visible toasts
toastInstance.hide('All');

// Hide a specific toast element
toastInstance.hide(specificElement);
```

---

### destroy
**Signature:** `destroy(): void`

Removes the component from the DOM and detaches all event handlers, attributes, and classes.

```tsx
toastInstance.destroy();
```

---

## Events

### beforeOpen
**Type:** `EmitType<ToastBeforeOpenArgs>`

Fires before the toast is shown. Set `e.cancel = true` to prevent display.

```tsx
<ToastComponent
  beforeOpen={(e: ToastBeforeOpenArgs) => {
    if (someCondition) e.cancel = true;
  }}
/>
```

**`ToastBeforeOpenArgs` properties:**
| Property | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set to `true` to cancel the open |
| `element` | `HTMLElement` | The toast DOM element |
| `options` | `ToastModel` | The toast configuration being shown |

---

### open
**Type:** `EmitType<ToastOpenArgs>`

Fires after the toast is shown on the target container.

```tsx
<ToastComponent
  open={(e: ToastOpenArgs) => {
    console.log('Toast opened', e.element);
  }}
/>
```

---

### click
**Type:** `EmitType<ToastClickEventArgs>`

Fires when the user clicks on the toast body. Set `e.clickToClose = true` to dismiss the toast on click.

```tsx
<ToastComponent
  click={(e: ToastClickEventArgs) => {
    e.clickToClose = true;
  }}
/>
```

**`ToastClickEventArgs` properties:**
| Property | Type | Description |
|---|---|---|
| `clickToClose` | `boolean` | Set to `true` to close toast on click |
| `element` | `HTMLElement` | The toast DOM element |
| `originalEvent` | `MouseEvent` | The native click event |

---

### beforeClose
**Type:** `EmitType<ToastBeforeCloseArgs>`

Fires before the toast closes. Set `e.cancel = true` to prevent closure.

```tsx
<ToastComponent
  beforeClose={(e: any) => {
    if (e.type === 'swipe') e.cancel = true; // block swipe on mobile
  }}
/>
```

**`e.type` values:** `'swipe'` | `'timeout'` | `'close'`

---

### close
**Type:** `EmitType<ToastCloseArgs>`

Fires after the toast hides.

```tsx
<ToastComponent
  close={(e: ToastCloseArgs) => {
    console.log('Toast closed', e.options);
  }}
/>
```

---

### created
**Type:** `EmitType<Event>`

Fires after the Toast component mounts to the DOM. This is the standard place to call `show()` for auto-displaying toasts.

```tsx
<ToastComponent
  created={() => toastInstance.show()}
/>
```

---

### destroyed
**Type:** `EmitType<Event>`

Fires after the Toast component is destroyed.

---

### beforeSanitizeHtml
**Type:** `EmitType<BeforeSanitizeHtmlArgs>`

Fires before HTML content is sanitized. Use to customize sanitization rules.

---

## Supporting Interfaces

### ToastPositionModel
```ts
interface ToastPositionModel {
  X?: 'Left' | 'Center' | 'Right' | number | string;
  Y?: 'Top' | 'Bottom' | number | string;
}
```

### ToastAnimationSettingsModel
```ts
interface ToastAnimationSettingsModel {
  show?: { effect?: Effect; duration?: number; easing?: string };
  hide?: { effect?: Effect; duration?: number; easing?: string };
}
```

### ButtonModelPropsModel
```ts
interface ButtonModelPropsModel {
  model?: ButtonModel;       // Syncfusion ButtonModel props (content, cssClass, iconCss, etc.)
  click?: EmitType<Event>;   // Click handler for the button
}
```

### ToastModel
Any property listed under [Properties](#properties) can be passed as `ToastModel` to `show()` or `ToastUtility.show()`.
