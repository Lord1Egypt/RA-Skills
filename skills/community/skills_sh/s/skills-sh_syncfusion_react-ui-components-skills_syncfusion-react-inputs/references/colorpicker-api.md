# API Reference — Syncfusion React ColorPicker

**Component:** `ColorPickerComponent`  
**Import:** `import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';`  
**Source:** https://ej2.syncfusion.com/react/documentation/api/color-picker/

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Type References](#type-references)

---

## Properties

### columns
`number` — Default: `10`

Number of columns rendered in the palette grid. Controls how many swatches appear per row.

```tsx
<ColorPickerComponent mode="Palette" columns={4} />
```

---

### createPopupOnClick
`boolean` — Default: `false`

When `true`, the popup DOM element is created only when the picker is first opened (lazy creation). When `false`, the popup DOM is created on component initialization.

```tsx
<ColorPickerComponent createPopupOnClick={true} />
```

---

### cssClass
`string` — Default: `''`

CSS class(es) applied to the root element. Use to scope custom styles or apply built-in utility classes.

Built-in utility values:
- `"e-hide-value"` — hides the hex/RGB input area in Picker mode

```tsx
<ColorPickerComponent cssClass="e-hide-value my-custom-picker" />
```

---

### disabled
`boolean` — Default: `false`

Disables the component. When `true`, the SplitButton appears dimmed and the popup cannot be opened.

```tsx
<ColorPickerComponent disabled={true} />
```

---

### enableOpacity
`boolean` — Default: `true`

Shows or hides the opacity slider. When `false`, colors are always fully opaque and the hex value uses 6 digits.

```tsx
<ColorPickerComponent enableOpacity={false} />
```

---

### enablePersistence
`boolean` — Default: `false`

Persists the component's selected color value in `localStorage`. The value is restored on the next page load. Requires a unique `id` prop to work correctly.

```tsx
<ColorPickerComponent id="theme-picker" enablePersistence={true} />
```

---

### enableRtl
`boolean` — Default: `false`

Renders the component in right-to-left direction for RTL languages (Arabic, Hebrew, etc.).

```tsx
<ColorPickerComponent enableRtl={true} locale="ar-AE" />
```

---

### inline
`boolean` — Default: `false`

When `true`, renders the ColorPicker container directly in the page flow (no SplitButton trigger, no popup). When `false` (default), renders as a SplitButton that opens a popup.

```tsx
<ColorPickerComponent inline={true} showButtons={false} />
```

---

### locale
`string` — Default: `''`

Overrides the global culture/localization for this component instance. Pass a BCP 47 locale string (e.g., `"de-DE"`, `"ar-AE"`). Requires a matching translation object loaded via `L10n.load()`.

```tsx
<ColorPickerComponent locale="de-DE" />
```

---

### mode
`'Picker' | 'Palette'` — Default: `'Picker'`

Determines which panel is displayed initially:
- `'Picker'` — HSV gradient area with hue and opacity sliders
- `'Palette'` — Grid of color swatches

```tsx
<ColorPickerComponent mode="Palette" />
```

---

### modeSwitcher
`boolean` — Default: `true`

Shows or hides the mode switcher button that lets users toggle between Picker and Palette.

```tsx
// Palette only, no ability to switch
<ColorPickerComponent mode="Palette" modeSwitcher={false} />
```

---

### noColor
`boolean` — Default: `false`

Adds a "no color" tile as the first tile in the palette. Clicking it clears the selected color (sets value to empty string).

> Always combine with `modeSwitcher={false}` — the no-color tile only exists in palette mode.

```tsx
<ColorPickerComponent mode="Palette" noColor={true} modeSwitcher={false} />
```

---

### presetColors
`{ [key: string]: string[] }` — Default: `null`

Loads custom color groups into the palette. Each key is a group name; each value is an array of hex color strings.

```tsx
const presets = {
  'brand': ['#0078d4', '#106ebe', '#005a9e'],
  'accent': ['#e81123', '#ff8c00', '#00b294']
};
<ColorPickerComponent mode="Palette" presetColors={presets} />
```

---

### showButtons
`boolean` — Default: `true`

Shows or hides the Apply and Cancel control buttons.
- When `true`: `change` event fires on Apply click
- When `false`: `change` event fires immediately on color selection; popup closes automatically

```tsx
<ColorPickerComponent showButtons={false} />
```

---

### showRecentColors
`boolean` — Default: `false`

Displays up to 10 recently selected colors as tiles at the top of the palette. Only available in palette mode (`mode="Palette"`).

```tsx
<ColorPickerComponent showRecentColors={true} />
```

---

### value
`string` — Default: `'#008000ff'`

Initial color value. Accepts 3, 4, 6, or 8 digit hex codes with or without the `#` prefix.

| Format | Example | Notes |
|--------|---------|-------|
| 3-digit | `"035"` | Short hex, opaque |
| 6-digit | `"#ff5733"` | Standard hex, opaque |
| 4-digit | `"035a"` | Last digit = opacity |
| 8-digit | `"#ff5733ff"` | Last 2 digits = opacity |

```tsx
<ColorPickerComponent value="#ff5733" />
```

---

## Methods

Access methods via a component ref:

```tsx
let colorPicker: ColorPickerComponent;
<ColorPickerComponent ref={(scope) => { colorPicker = scope as ColorPickerComponent; }} />
```

---

### destroy()
`() => void`

Removes the component from the DOM and detaches all event handlers. The original input element is preserved in the DOM.

```tsx
colorPicker.destroy();
```

---

### focusIn()
`() => void`

Sets focus to the ColorPicker's native element.

```tsx
colorPicker.focusIn();
```

---

### getPersistData()
`() => string`

Returns the properties that are maintained in the persisted state as a JSON string. Used internally by `enablePersistence`.

```tsx
const persistedData = colorPicker.getPersistData();
```

---

### getValue(value?, type?)
`(value?: string, type?: string) => string`

Converts a color value to the specified format. Can be used to convert between hex, RGB, RGBA, HSV, and other formats.

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `string` (optional) | Color to convert. Uses current picker value if omitted. |
| `type` | `string` (optional) | Target format: `'Hex'`, `'RGB'`, `'HSV'`, etc. |

```tsx
// Get current value in hex
const hex = colorPicker.getValue();

// Convert a hex string to RGB
const rgb = colorPicker.getValue('#278787', 'RGB');

// Convert RGB string to Hex
const hexOut = colorPicker.getValue('rgb(38,133,133)', 'Hex');

// Convert RGB to HSV
const hsv = colorPicker.getValue('rgb(180,71.1,52.9)', 'HSV');
```

---

### toggle()
`() => void`

Opens the ColorPicker popup if it is currently closed; closes it if it is currently open.

```tsx
colorPicker.toggle(); // show/hide
```

---

## Events

### beforeClose
`EmitType<BeforeOpenCloseEventArgs>`

Fires before the ColorPicker popup closes. Set `args.cancel = true` to prevent closing.

```tsx
function beforeClose(args: BeforeOpenCloseEventArgs): void {
  // args.cancel = true; // prevent close
}
<ColorPickerComponent beforeClose={beforeClose} />
```

---

### beforeModeSwitch
`EmitType<ModeSwitchEventArgs>`

Fires before switching between Picker and Palette modes.

```tsx
function beforeModeSwitch(args: ModeSwitchEventArgs): void {
  console.log('Switching to:', args.mode);
}
<ColorPickerComponent beforeModeSwitch={beforeModeSwitch} />
```

---

### beforeOpen
`EmitType<BeforeOpenCloseEventArgs>`

Fires before the ColorPicker popup opens. Set `args.cancel = true` to prevent opening.

```tsx
function beforeOpen(args: BeforeOpenCloseEventArgs): void {
  // args.cancel = true; // prevent open
}
<ColorPickerComponent beforeOpen={beforeOpen} />
```

---

### beforeTileRender
`EmitType<PaletteTileEventArgs>`

Fires before each palette tile is rendered. Use to add custom CSS classes or modify the tile element.

```tsx
function tileRender(args: PaletteTileEventArgs): void {
  args.element.classList.add('e-custom-tile');
}
<ColorPickerComponent beforeTileRender={tileRender} />
```

---

### change
`EmitType<ColorPickerEventArgs>`

Fires when the selected color is confirmed/applied.
- If `showButtons={true}`: fires when Apply is clicked
- If `showButtons={false}`: fires immediately on color selection

```tsx
function onChange(args: ColorPickerEventArgs): void {
  console.log(args.currentValue.hex);   // "#ff5733"
  console.log(args.currentValue.rgba);  // "rgba(255,87,51,1)"
  console.log(args.previousValue.hex);  // previous color
}
<ColorPickerComponent change={onChange} />
```

---

### created
`EmitType<Event>`

Fires once after the component has finished rendering.

```tsx
function onCreated(): void {
  console.log('ColorPicker is ready');
}
<ColorPickerComponent created={onCreated} />
```

---

### onModeSwitch
`EmitType<ModeSwitchEventArgs>`

Fires after switching between Picker and Palette modes (after the switch completes).

```tsx
function afterSwitch(args: ModeSwitchEventArgs): void {
  console.log('Now showing:', args.mode);
}
<ColorPickerComponent onModeSwitch={afterSwitch} />
```

---

### open
`EmitType<OpenEventArgs>`

Fires after the ColorPicker popup has opened.

```tsx
function onOpen(args: OpenEventArgs): void {
  console.log('Popup opened', args.element);
}
<ColorPickerComponent open={onOpen} />
```

---

### select
`EmitType<ColorPickerEventArgs>`

Fires when a color is selected in the picker or palette while `showButtons={true}`. This fires before Apply — use it to preview the color before it is confirmed.

```tsx
function onSelect(args: ColorPickerEventArgs): void {
  // Preview the color before user clicks Apply
  previewElem.style.backgroundColor = args.currentValue.rgba;
}
<ColorPickerComponent showButtons={true} select={onSelect} />
```

---

## Type References

### ColorPickerEventArgs
```ts
{
  currentValue: { hex: string; rgba: string };
  previousValue: { hex: string; rgba: string };
  value: string;
}
```

### ModeSwitchEventArgs
```ts
{
  mode: 'Picker' | 'Palette';
}
```

### PaletteTileEventArgs
```ts
{
  element: HTMLElement; // The tile <span> element
  value: string;        // The tile's color value
}
```

### BeforeOpenCloseEventArgs
```ts
{
  cancel: boolean;      // Set to true to prevent open/close
  element: HTMLElement;
}
```

### OpenEventArgs
```ts
{
  element: HTMLElement; // The popup element
}
```
