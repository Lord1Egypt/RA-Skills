# API Reference — Syncfusion React Signature

Source: https://ej2.syncfusion.com/react/documentation/api/signature/index-default

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Types](#types)

---

## Properties

### `backgroundColor`
- **Type:** `string`
- **Default:** `''`
- Gets or sets the background color of the canvas. Accepts hex codes (`#ffffff`), RGB (`rgb(255,255,255)`), or CSS color names (`white`). An empty string renders the canvas with a transparent/default background.

### `backgroundImage`
- **Type:** `string`
- **Default:** `''`
- Gets or sets the background image for the canvas. Accepts a hosted URL or a base64-encoded image string. An empty string means no background image.

### `disabled`
- **Type:** `boolean`
- **Default:** `false`
- Gets or sets whether the component is disabled. When `true`, the component is non-interactive and displayed with reduced opacity. Cannot receive focus while disabled.

### `enablePersistence`
- **Type:** `boolean`
- **Default:** `false`
- Gets or sets whether to persist the component state between page reloads. When `true`, the last signature value is stored in browser local storage and restored on reload.

### `isReadOnly`
- **Type:** `boolean`
- **Default:** `false`
- Gets or sets whether the component is in read-only mode. When `true`, the component can receive focus but no new strokes can be drawn. Use to display an existing signature without allowing edits.

### `maxStrokeWidth`
- **Type:** `number`
- **Default:** `2`
- Gets or sets the maximum stroke width. The component calculates variable stroke width using `maxStrokeWidth`, `minStrokeWidth`, and `velocity`.

### `minStrokeWidth`
- **Type:** `number`
- **Default:** `0.5`
- Gets or sets the minimum stroke width. Works together with `maxStrokeWidth` and `velocity` to create natural stroke variation.

### `saveWithBackground`
- **Type:** `boolean`
- **Default:** `true`
- Gets or sets whether to save the signature including its background color and background image. When `false`, only the stroke content is saved (transparent background for PNG).

### `signatureValue`
- **Type:** `string`
- Gets or sets the last signature URL to maintain persisted state. Used internally for `enablePersistence`.

### `strokeColor`
- **Type:** `string`
- **Default:** `'#000000'`
- Gets or sets the color of the signature strokes. Accepts hex codes, RGB values, or CSS color names.

### `velocity`
- **Type:** `number`
- **Default:** `0.7`
- Gets or sets the velocity factor used to calculate stroke width variation based on drawing speed. Values between 0 and 1; lower values produce greater width variation between slow and fast strokes.

---

## Methods

### `canRedo()`
- **Returns:** `boolean`
- Returns `true` if the redo history contains actions that can be reapplied. Call before invoking `redo()` to avoid no-op calls.

### `canUndo()`
- **Returns:** `boolean`
- Returns `true` if the undo history contains actions that can be reverted. Call before invoking `undo()` to avoid no-op calls.

### `clear()`
- **Returns:** `void`
- Erases all signature strokes from the canvas. This action is added to the undo history, so the user can undo a clear.

### `destroy()`
- **Returns:** `void`
- Removes the component from the DOM and detaches all related event handlers. Restores the original input element in the DOM.

### `draw(text, fontFamily?, fontSize?)`
- **Returns:** `void`
- Renders a text string onto the canvas as a typed signature.
- **Parameters:**
  - `text` (string) — the text to draw
  - `fontFamily` (string, optional) — font family, default `'Arial'`
  - `fontSize` (number, optional) — font size in pixels, default `30`

### `getBlob(url)`
- **Returns:** `Blob`
- Converts the given base64 string or URL to a `Blob` object.
- **Parameters:**
  - `url` (string) — a base64 string or URL of the signature

### `getSignature(type?)`
- **Returns:** `string`
- Returns the current canvas content as a base64-encoded string.
- **Parameters:**
  - `type` (SignatureFileType, optional) — `'Png'` | `'Jpeg'` | `'Svg'`, default `'Png'`

### `isEmpty()`
- **Returns:** `boolean`
- Returns `true` if the canvas contains no signature strokes. Use to guard `clear()` calls or disable save/clear buttons.

### `load(signature, width?, height?)`
- **Returns:** `void`
- Loads a signature image onto the canvas from a base64 string or a hosted URL.
- **Parameters:**
  - `signature` (string) — base64 string or URL of the PNG/JPEG/SVG image
  - `width` (number, optional) — width at which to render the loaded image
  - `height` (number, optional) — height at which to render the loaded image

### `redo()`
- **Returns:** `void`
- Reapplies the most recently undone action. Check `canRedo()` before calling.

### `refresh()`
- **Returns:** `void`
- Refreshes the Signature component, re-rendering it in its current state. Useful after container resizing.

### `save(type?, fileName?)`
- **Returns:** `void`
- Downloads the signature as an image file to the user's browser.
- **Parameters:**
  - `type` (SignatureFileType, optional) — `'Png'` | `'Jpeg'` | `'Svg'`, default `'Png'`
  - `fileName` (string, optional) — name of the downloaded file (without extension)

### `saveAsBlob()`
- **Returns:** `Blob`
- Returns the current canvas content as a `Blob` object (binary data). Use for file upload, FormData, or database storage.

### `undo()`
- **Returns:** `void`
- Reverts the most recent action. Check `canUndo()` before calling.

---

## Events

### `beforeSave`
- **Type:** `EmitType<SignatureBeforeSaveEventArgs>`
- Raised before the signature is saved via the keyboard shortcut `Ctrl + S`. Use `SignatureBeforeSaveEventArgs` to customize the `fileName` and `type` (`SignatureFileType`) before the download occurs.
- **Note:** This event is only triggered by the keyboard shortcut — not when calling `save()` programmatically.

### `change`
- **Type:** `EmitType<SignatureChangeEventArgs>`
- Raised after every user action: completing a stroke, undo, redo, and clear. Use this event to update dependent UI elements such as toolbar button states.

### `created`
- **Type:** `EmitType<Event>`
- Triggered once, after the component has finished rendering. Use to initialize dependent controls or set initial state.

---

## Types

### `SignatureFileType`
Enum for supported save/export formats:
- `'Png'` — PNG image format (default)
- `'Jpeg'` — JPEG image format
- `'Svg'` — SVG vector format

**Usage:**
```tsx
import { SignatureFileType } from '@syncfusion/ej2-react-inputs';

// Use as a string literal or as the enum value
signature.save('Png', 'my-signature');
signature.save('Jpeg' as SignatureFileType, 'my-signature');
```
