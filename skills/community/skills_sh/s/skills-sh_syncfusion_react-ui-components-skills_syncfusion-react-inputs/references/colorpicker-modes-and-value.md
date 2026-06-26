# Modes and Color Value — Syncfusion React ColorPicker

## Table of Contents
- [Inline Rendering](#inline-rendering)
- [Picker vs Palette Mode](#picker-vs-palette-mode)
- [Setting Color Value](#setting-color-value)
- [Opacity Support](#opacity-support)
- [Render Palette Alone](#render-palette-alone)

---

## Inline Rendering

By default the ColorPicker renders as a **SplitButton** that opens a popup. Set `inline={true}` to render the picker container directly in the page without any popup.

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent inline={true} showButtons={false} />
      </div>
    </div>
  );
}
export default App;
```

> When using inline mode, `showButtons={false}` is recommended because Apply/Cancel are only meaningful in popup contexts — color changes apply immediately in inline mode.

---

## Picker vs Palette Mode

The `mode` property controls which panel is shown initially:

| Value | Renders |
|-------|---------|
| `'Picker'` (default) | HSV gradient with hue and opacity sliders |
| `'Palette'` | Grid of color swatches |

The mode switcher button (visible by default) lets users toggle between the two at runtime.

**Open with Palette initially:**

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent mode="Palette" />
      </div>
    </div>
  );
}
export default App;
```

---

## Setting Color Value

Use the `value` property to set the initial color. It accepts:

| Format | Example | Notes |
|--------|---------|-------|
| 3-digit hex | `"035"` | Short form, no opacity |
| 6-digit hex | `"#ff5733"` | Standard hex, no opacity |
| 4-digit hex | `"035a"` | Last digit = opacity |
| 8-digit hex | `"#ff5733ff"` | Last two digits = opacity |

The `#` prefix is optional.

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        {/* 4-digit hex: last digit "a" = ~67% opacity */}
        <ColorPickerComponent value="035a" />
      </div>
    </div>
  );
}
export default App;
```

**Listening to color changes:**

The `change` event fires when the color is confirmed (Apply button clicked, or immediately if `showButtons={false}`).

```tsx
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function onChange(args: ColorPickerEventArgs): void {
    console.log('Hex:', args.currentValue.hex);    // "#ff5733"
    console.log('RGBA:', args.currentValue.rgba);  // "rgba(255,87,51,1)"
  }
  return <ColorPickerComponent value="#ff5733ff" change={onChange} />;
}
export default App;
```

The `select` event fires on every tile/color selection in the picker (before Apply), useful when `showButtons={true}`.

---

## Opacity Support

The opacity slider is enabled by default. To hide it, set `enableOpacity={false}`:

```tsx
<ColorPickerComponent enableOpacity={false} />
```

When opacity is disabled, colors are always fully opaque. The hex value stored will be 6-digit.

---

## Render Palette Alone

To lock the component to palette-only (hide the mode switcher so users cannot switch to Picker):

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent
          mode="Palette"
          modeSwitcher={false}
          showButtons={false}
        />
      </div>
    </div>
  );
}
export default App;
```

> To render only the **Picker** (no palette, no mode switch), set `mode="Picker"` and `modeSwitcher={false}`.

---

## Mode Switch Events

To react when the user switches between Picker and Palette:

```tsx
import { ColorPickerComponent, ModeSwitchEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function beforeSwitch(args: ModeSwitchEventArgs): void {
    console.log('Switching to:', args.mode);
  }
  function afterSwitch(args: ModeSwitchEventArgs): void {
    console.log('Now in:', args.mode);
  }
  return (
    <ColorPickerComponent
      beforeModeSwitch={beforeSwitch}
      onModeSwitch={afterSwitch}
    />
  );
}
export default App;
```
