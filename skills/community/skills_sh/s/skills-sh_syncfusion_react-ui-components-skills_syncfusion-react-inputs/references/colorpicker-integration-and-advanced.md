# Integration and Advanced — Syncfusion React ColorPicker

## Table of Contents
- [ColorPicker in DropDownButton](#colorpicker-in-dropdownbutton)
- [Toggle Popup Programmatically](#toggle-popup-programmatically)
- [State Persistence](#state-persistence)
- [Mode Switcher Visibility](#mode-switcher-visibility)
- [Disabled State](#disabled-state)
- [Popup Lifecycle Events](#popup-lifecycle-events)

---

## ColorPicker in DropDownButton

You can embed an inline ColorPicker inside a `DropDownButtonComponent` using the `target` property of the DropDownButton. The picker renders inline, and the DropDownButton acts as the trigger.

```tsx
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import { DropDownButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

function App() {
  let ddb: DropDownButtonComponent;
  let cp: ColorPickerComponent;

  function onChange(args: ColorPickerEventArgs): void {
    // Update the dropdown button's preview color
    (ddb.element.children[0] as HTMLElement).style.backgroundColor = args.currentValue.rgba;
    closePopup();
  }

  function closePopup(): void {
    ddb.toggle();
  }

  function onCreated(): void {
    // Wire the Cancel button to close the dropdown
    const parentElem = cp.element.parentElement as HTMLElement;
    const cancelBtn = parentElem.querySelector('.e-cancel') as HTMLElement;
    cancelBtn.addEventListener('click', closePopup.bind(this));
  }

  function open(): void {
    // Ensure the color picker tooltip z-index is above the dropdown popup
    const tooltip = document.getElementsByClassName('e-color-picker-tooltip')[0] as HTMLElement;
    const zindex = parseInt(tooltip.style.zIndex) + 2;
    tooltip.style.zIndex = zindex.toString();
  }

  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent
          ref={(scope) => { cp = scope as ColorPickerComponent; }}
          id="colorpicker"
          inline={true}
          change={onChange}
        />
        <DropDownButtonComponent
          id="dropdownbtn"
          open={open}
          target=".e-colorpicker-wrapper"
          ref={(scope) => { ddb = scope as DropDownButtonComponent; }}
          iconCss="e-dropdownbtn-preview"
          created={onCreated}
        />
      </div>
    </div>
  );
}
export default App;
```

**Key points:**
- The ColorPicker must be `inline={true}` so it renders a DOM element that `target` can reference
- The DropDownButton `target` points to the `.e-colorpicker-wrapper` CSS class (the wrapper rendered around the inline ColorPicker)
- Z-index management in `open()` prevents the tooltip from being hidden behind the popup

---

## Toggle Popup Programmatically

Use the `toggle()` method via a component ref to open or close the ColorPicker popup from code:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  let colorPicker: ColorPickerComponent;

  function openPicker(): void {
    colorPicker.toggle(); // opens popup if closed, closes if open
  }

  return (
    <div>
      <button onClick={openPicker}>Open Color Picker</button>
      <ColorPickerComponent
        ref={(scope) => { colorPicker = scope as ColorPickerComponent; }}
        id="colorpicker"
      />
    </div>
  );
}
export default App;
```

> `toggle()` acts as a show/hide switch — calling it when the popup is open will close it, and vice versa.

---

## State Persistence

Enable `enablePersistence` to save the selected color value in `localStorage` and restore it on page reload:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <ColorPickerComponent
      id="colorpicker"
      enablePersistence={true}
    />
  );
}
export default App;
```

> The component uses its `id` as the `localStorage` key, so `id` must be unique and consistent across page loads for persistence to work correctly.

---

## Mode Switcher Visibility

The mode switcher button (toggle between Picker and Palette) is visible by default. Hide it with `modeSwitcher={false}`:

```tsx
// Lock to Picker only
<ColorPickerComponent modeSwitcher={false} />

// Lock to Palette only
<ColorPickerComponent mode="Palette" modeSwitcher={false} />
```

When hiding the mode switcher in palette mode with `noColor={true}`, this also prevents users from accidentally switching to Picker where no-color tiles are not available.

---

## Disabled State

To prevent interaction with the ColorPicker, set `disabled={true}`. The SplitButton will appear dimmed and the popup will not open.

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent disabled={true} />
      </div>
    </div>
  );
}
export default App;
```

You can also toggle disabled state dynamically via `setProperties`:

```tsx
colorPickerRef.setProperties({ disabled: true });
colorPickerRef.setProperties({ disabled: false });
```

---

## Popup Lifecycle Events

Use these events to control popup open/close behavior, such as preventing the popup from opening under certain conditions:

```tsx
import { ColorPickerComponent, BeforeOpenCloseEventArgs, OpenEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function beforeOpen(args: BeforeOpenCloseEventArgs): void {
    // Cancel popup opening if needed
    // args.cancel = true;
    console.log('Popup about to open');
  }

  function onOpen(args: OpenEventArgs): void {
    console.log('Popup opened');
  }

  function beforeClose(args: BeforeOpenCloseEventArgs): void {
    // Cancel popup closing if needed
    // args.cancel = true;
    console.log('Popup about to close');
  }

  return (
    <ColorPickerComponent
      beforeOpen={beforeOpen}
      open={onOpen}
      beforeClose={beforeClose}
    />
  );
}
export default App;
```

| Event | Fires When |
|-------|-----------|
| `beforeOpen` | Before the popup opens — can be cancelled |
| `open` | After the popup has opened |
| `beforeClose` | Before the popup closes — can be cancelled |
