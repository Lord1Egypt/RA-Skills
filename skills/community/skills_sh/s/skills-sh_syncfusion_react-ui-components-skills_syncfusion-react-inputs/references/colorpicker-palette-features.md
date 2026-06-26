# Palette Features — Syncfusion React ColorPicker

## Table of Contents
- [Custom Palette Colors](#custom-palette-colors)
- [Custom Palette Tile Rendering](#custom-palette-tile-rendering)
- [No-Color Support](#no-color-support)
- [Custom No-Color Option](#custom-no-color-option)
- [Show Recent Colors](#show-recent-colors)
- [Palette Column Count](#palette-column-count)

---

## Custom Palette Colors

By default the palette shows a standard set of colors. Use `presetColors` to load your own groups. Each key becomes a named section; values are arrays of hex strings.

```tsx
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const presets: { [key: string]: string[] } = {
    'custom1': [
      '#ef9a9a', '#e57373', '#ef5350', '#f44336',
      '#f48fb1', '#f06292', '#ec407a', '#e91e63',
      '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0',
      '#b39ddb', '#9575cd', '#7e57c2', '#673AB7'
    ],
    'custom2': [
      '#9FA8DA', '#7986CB', '#5C6BC0', '#3F51B5',
      '#90CAF9', '#64B5F6', '#42A5F5', '#2196F3',
      '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4',
      '#80DEEA', '#4DD0E1', '#26C6DA', '#00BCD4'
    ],
    'custom3': [
      '#80CBC4', '#4DB6AC', '#26A69A', '#009688',
      '#A5D6A7', '#81C784', '#66BB6A', '#4CAF50',
      '#C5E1A5', '#AED581', '#9CCC65', '#8BC34A',
      '#E6EE9C', '#DCE775', '#D4E157', '#CDDC39'
    ]
  };

  function onChange(args: ColorPickerEventArgs): void {
    (document.getElementById('preview') as HTMLElement).style.backgroundColor =
      args.currentValue.hex;
  }

  return (
    <div id="container">
      <div className="wrap">
        <div id="preview" />
        <h4>Select Color</h4>
        <ColorPickerComponent
          id="element"
          mode="Palette"
          modeSwitcher={false}
          inline={true}
          showButtons={false}
          columns={4}
          presetColors={presets}
          change={onChange}
        />
      </div>
    </div>
  );
}
export default App;
```

---

## Custom Palette Tile Rendering

Use the `beforeTileRender` event to add custom classes or modify each palette tile's DOM element before it is rendered.

```tsx
import { ColorPickerComponent, PaletteTileEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const presets: { [key: string]: string[] } = {
    'brand': ['#0078d4', '#106ebe', '#005a9e', '#004578']
  };

  function tileRender(args: PaletteTileEventArgs): void {
    // Add custom CSS classes to each tile element
    args.element.classList.add('e-icons');
    args.element.classList.add('e-custom-tile');
  }

  return (
    <ColorPickerComponent
      mode="Palette"
      presetColors={presets}
      beforeTileRender={tileRender}
      inline={true}
      showButtons={false}
    />
  );
}
export default App;
```

The `args.element` is the tile's `<span>` DOM element. You can set styles, titles, or ARIA attributes on it directly.

---

## No-Color Support

The `noColor` property adds a special "no color" tile as the first tile in the palette. Clicking it clears the current color selection (sets value to empty).

```tsx
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import { useEffect } from 'react';

function App() {
  let preview: HTMLElement;

  function onChange(args: ColorPickerEventArgs): void {
    preview.style.backgroundColor = args.currentValue.hex;
    preview.textContent = args.currentValue.hex ? args.currentValue.hex : 'No color';
  }

  useEffect(() => {
    preview = document.getElementById('preview') as HTMLElement;
    preview.style.backgroundColor = '#ba68c8';
    preview.textContent = '#ba68c8';
  }, []);

  return (
    <div id="container">
      <div className="wrap">
        <div id="preview" />
        <h4>Select Color</h4>
        <ColorPickerComponent
          id="colorpicker"
          value="#ba68c8"
          mode="Palette"
          noColor={true}
          showButtons={false}
          modeSwitcher={false}
          change={onChange}
        />
      </div>
    </div>
  );
}
export default App;
```

> **Important:** When `noColor={true}`, always set `modeSwitcher={false}` — the no-color tile only exists in palette mode.

---

## Custom No-Color Option

Instead of the built-in `noColor` tile, you can build a fully custom "No color" list item and manually clear the picker's value:

```tsx
import { ColorPickerComponent, PaletteTileEventArgs, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

function App() {
  let colorPicker: ColorPickerComponent;
  let splitBtn: SplitButtonComponent;

  const presets: { [key: string]: string[] } = {
    'custom': [
      '#f44336', '#e91e63', '#9c27b0', '#673ab7',
      '#2196f3', '#03a9f4', '#00bcd4', '#009688',
      '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107'
    ]
  };

  function beforeTileRender(args: PaletteTileEventArgs): void {
    args.element.classList.add('e-custom-tile');
  }

  function onChange(args: ColorPickerEventArgs): void {
    const preview = document.getElementById('preview') as HTMLElement;
    (document.querySelector('.e-split-btn .e-picker-icon') as HTMLElement).style.borderBottomColor =
      args.currentValue.hex;
    preview.style.backgroundColor = args.currentValue.hex;
    preview.textContent = args.currentValue.hex;
    if (splitBtn.element.getAttribute('aria-expanded')) {
      splitBtn.toggle();
      splitBtn.element.focus();
    }
  }

  function onCreated(): void {
    const preview = document.getElementById('preview') as HTMLElement;
    preview.style.backgroundColor = '#ba68c8';
    preview.textContent = '#ba68c8';

    document.getElementById('no-color')!.onclick = (): void => {
      // Programmatically clear the color picker value
      colorPicker.setProperties({ value: '' }, true);
      (document.querySelector('.e-split-btn .e-picker-icon') as HTMLElement).style.borderBottomColor =
        'transparent';
      preview.textContent = 'No color';
      preview.style.backgroundColor = 'transparent';
    };
  }

  return (
    <div id="container">
      <div className="wrap">
        <ul id="target">
          <li className="e-item e-palette-item">
            <ColorPickerComponent
              id="colorpicker"
              ref={(scope) => { colorPicker = scope as ColorPickerComponent; }}
              value="#f44336"
              mode="Palette"
              inline={true}
              columns={4}
              presetColors={presets}
              showButtons={false}
              modeSwitcher={false}
              beforeTileRender={beforeTileRender}
              change={onChange}
              created={onCreated}
            />
          </li>
          <li className="e-item" id="no-color">
            <span className="e-menu-icon e-nocolor" />
            No color
          </li>
        </ul>
        <div>
          <div id="preview" />
          <h4>Select color</h4>
          <SplitButtonComponent
            id="splitbtn"
            iconCss="e-cp-icons e-picker-icon"
            target="#target"
            ref={(scope) => { splitBtn = scope as SplitButtonComponent; }}
          />
        </div>
      </div>
    </div>
  );
}
export default App;
```

---

## Show Recent Colors

The `showRecentColors` property displays up to **10 recently selected colors** as tiles at the top of the palette. Only works in **palette mode**.

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent showRecentColors={true} />
      </div>
    </div>
  );
}
export default App;
```

> Recent colors are tracked per session and appear at the top of the palette as users select colors.

---

## Palette Column Count

The `columns` property controls how many tiles appear per row in the palette grid. Default is `10`.

```tsx
<ColorPickerComponent
  mode="Palette"
  columns={4}
  inline={true}
  showButtons={false}
/>
```

Combine with `presetColors` to display a tight brand palette with fewer columns:

```tsx
const brandColors: { [key: string]: string[] } = {
  'primary': ['#0078d4', '#106ebe', '#005a9e', '#004578'],
  'secondary': ['#ff8c00', '#ea4300', '#d13438', '#a4262c']
};

<ColorPickerComponent
  mode="Palette"
  presetColors={brandColors}
  columns={4}
  modeSwitcher={false}
  inline={true}
  showButtons={false}
/>
```
