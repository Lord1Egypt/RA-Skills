# UI Customization — Syncfusion React ColorPicker

## Table of Contents
- [Hide the Input Value Area](#hide-the-input-value-area)
- [Custom Picker Handle](#custom-picker-handle)
- [Custom Primary Button with Icon](#custom-primary-button-with-icon)
- [Display Hex Code in Input Element](#display-hex-code-in-input-element)
- [Hide Control Buttons](#hide-control-buttons)
- [CSS Class Overrides](#css-class-overrides)
- [Excel-Like Custom UI](#excel-like-custom-ui)

---

## Hide the Input Value Area

By default, the Picker shows an input area at the bottom displaying the current hex/RGB values. To hide it, apply the `e-hide-value` class via `cssClass`:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent cssClass="e-hide-value" modeSwitcher={false} />
      </div>
    </div>
  );
}
export default App;
```

---

## Custom Picker Handle

The drag handle inside the Picker gradient area can be styled with CSS. Apply a custom class via `cssClass` and override the handle styles:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent
          id="colorpicker"
          value="#344aae"
          cssClass="e-custom-picker"
          modeSwitcher={false}
        />
      </div>
    </div>
  );
}
export default App;
```

Then in CSS override `.e-custom-picker .e-container .e-handler`:

```css
.e-custom-picker .e-container .e-handler {
  /* e.g. replace with an SVG icon or custom shape */
  background: url('./handle-icon.svg') no-repeat center;
  border-radius: 0;
}
```

---

## Custom Primary Button with Icon

By default, the SplitButton's left portion shows the currently selected color. You can customize it to show a picker icon instead, updating the icon's bottom border color on every change:

```tsx
import { addClass } from '@syncfusion/ej2-base';
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  let previewIcon: HTMLElement;
  let cp: ColorPickerComponent;

  function onChange(args: ColorPickerEventArgs): void {
    // Update the icon's bottom border to reflect selected color
    previewIcon.style.borderBottomColor = args.currentValue.rgba;
  }

  function onCreated(): void {
    const elem = cp.element.nextElementSibling as HTMLElement;
    previewIcon = elem.querySelector('.e-selected-color') as HTMLElement;
    addClass([previewIcon], 'e-icons');
  }

  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent
          ref={(scope) => { cp = scope as ColorPickerComponent; }}
          id="colorpicker"
          created={onCreated}
          change={onChange}
        />
      </div>
    </div>
  );
}
export default App;
```

> Syncfusion EJ2 provides a built-in icon font. Apply `e-icons` to any element to use it. Third-party icon libraries can also be used.

---

## Display Hex Code in Input Element

You can move the color picker's own `<input>` element into the SplitButton area so the current hex code appears in a text input:

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  let colorPicker: ColorPickerComponent;

  function onCreated(): void {
    const cpElem = colorPicker.element.nextElementSibling as HTMLElement;
    // Move the input element into the SplitButton wrapper
    cpElem.insertBefore(colorPicker.element, cpElem.children[1]);
  }

  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent
          ref={(scope) => { colorPicker = scope as ColorPickerComponent; }}
          id="colorpicker"
          type="text"
          created={onCreated}
          className="e-input"
        />
      </div>
    </div>
  );
}
export default App;
```

---

## Hide Control Buttons

By default, Apply and Cancel buttons appear in the popup. Setting `showButtons={false}` hides them — color changes apply immediately when a color is selected.

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent showButtons={false} />
      </div>
    </div>
  );
}
export default App;
```

> When `showButtons={false}`, the `change` event fires immediately on color selection rather than on Apply.

---

## CSS Class Overrides

Use these CSS selectors to customize specific parts of the ColorPicker UI. Apply them globally or scope them under a custom class via `cssClass`.

| CSS Class | What it Customizes |
|-----------|-------------------|
| `.e-custom-picker .e-container .e-handler` | Selection handle in picker gradient |
| `.color-picker.e-dropdown-popup ul .e-container` | Picker/palette container in popup |
| `.color-picker.e-dropdown-popup ul .e-item.e-palette-item` | Each palette item in popup |
| `.color-picker.e-dropdown-popup .e-container .e-switch` | Mode switcher control |
| `.color-picker.e-dropdown-popup .e-container .e-slider-preview` | Hue/opacity slider track |

For comprehensive theming, use the [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material) to generate a custom CSS file.

---

## Excel-Like Custom UI

You can combine the ColorPicker with SplitButton and Dialog to create an Excel-style color picker — a palette in the dropdown with a "More colors..." option that opens a full picker dialog:

```tsx
import * as React from 'react';
import { ColorPickerComponent, PaletteTileEventArgs, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { SplitButtonComponent, BeforeOpenCloseMenuEventArgs, OpenCloseMenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';

function App() {
  let colorPicker: ColorPickerComponent;
  let pickerDlg: DialogComponent;
  let animationSettings: object = { effect: 'Zoom' };

  function content(): JSX.Element {
    function onPickerChange(args: ColorPickerEventArgs): void {
      onPaletteChange(args);
      pickerDlg.hide();
    }
    return (
      <div className="dialogContent">
        <ColorPickerComponent
          id="picker"
          inline={true}
          modeSwitcher={false}
          change={onPickerChange}
          ref={(scope) => { colorPicker = scope as ColorPickerComponent; }}
        />
      </div>
    );
  }

  function onPaletteChange(args: ColorPickerEventArgs): void {
    const splitIcon = document.getElementById('split-btn')!.children[0] as HTMLElement;
    splitIcon.style.borderBottomColor = args.currentValue.rgba;
  }

  function onDdPopupOpen(args: OpenCloseMenuEventArgs): void {
    args.element.children[1].addEventListener('click', openPickerDlg);
  }

  function onBeforeDdPopupClose(args: BeforeOpenCloseMenuEventArgs): void {
    args.element.children[1].removeEventListener('click', openPickerDlg);
  }

  function openPickerDlg(): void {
    pickerDlg.show();
  }

  function pickerDlgOpen(): void {
    colorPicker.refresh();
    colorPicker.element.nextElementSibling!
      .querySelector('.e-ctrl-btn .e-cancel')!
      .addEventListener('click', pickerDlgClose);
  }

  function pickerDlgClose(): void {
    pickerDlg.hide();
  }

  function onSplitBtnCreated(): void {
    const splitIcon = document.getElementById('split-btn')!.children[0] as HTMLElement;
    splitIcon.style.borderBottomColor = '#008000';
  }

  return (
    <div id="container">
      <div className="wrap">
        <ul id="target">
          <li className="e-item e-palette-item">
            <ColorPickerComponent
              id="palette"
              mode="Palette"
              inline={true}
              showButtons={false}
              modeSwitcher={false}
              change={onPaletteChange}
            />
          </li>
          <li className="e-item">
            <span className="e-menu-icon" />
            More colors...
          </li>
        </ul>
        <h4>Select color</h4>
        <SplitButtonComponent
          id="split-btn"
          created={onSplitBtnCreated}
          iconCss="e-icons e-font-icon"
          target="#target"
          open={onDdPopupOpen}
          beforeClose={onBeforeDdPopupClose}
        />
        <DialogComponent
          id="picker-dialog"
          cssClass="e-dlg-picker"
          isModal={true}
          height="336px"
          width="270px"
          ref={(dialog) => { pickerDlg = dialog as DialogComponent; }}
          target=".wrap"
          content={content}
          overlayClick={pickerDlgClose}
          open={pickerDlgOpen}
          visible={false}
          animationSettings={animationSettings}
        />
      </div>
    </div>
  );
}
export default App;
```

This pattern requires `@syncfusion/ej2-react-popups` and `@syncfusion/ej2-react-splitbuttons` packages installed.
