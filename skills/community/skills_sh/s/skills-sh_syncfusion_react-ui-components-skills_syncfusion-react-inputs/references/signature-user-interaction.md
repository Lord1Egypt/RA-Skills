# User Interaction in Syncfusion React Signature

## Table of Contents
- [Undo and Redo](#undo-and-redo)
- [Clear](#clear)
- [Disabled](#disabled)
- [ReadOnly](#readonly)
- [Draw Text as Signature](#draw-text-as-signature)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Change Event](#change-event)

---

## Undo and Redo

The Signature component maintains a snapshot history of every drawing action. Use `undo()` and `redo()` to navigate this history, and `canUndo()` / `canRedo()` to check availability before calling them.

| Method | Returns | Description |
|--------|---------|-------------|
| `undo()` | `void` | Reverts the last stroke/action |
| `redo()` | `void` | Re-applies the last undone action |
| `canUndo()` | `boolean` | `true` if undo history is available |
| `canRedo()` | `boolean` | `true` if redo history is available |

```tsx
import { SignatureComponent, SignatureChangeEventArgs } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const sigRef = React.useRef<SignatureComponent>(null);
  const [undoEnabled, setUndoEnabled] = React.useState(false);
  const [redoEnabled, setRedoEnabled] = React.useState(false);

  function handleChange(args: SignatureChangeEventArgs) {
    if (sigRef.current) {
      setUndoEnabled(sigRef.current.canUndo());
      setRedoEnabled(sigRef.current.canRedo());
    }
  }

  return (
    <div>
      <ButtonComponent disabled={!undoEnabled} onClick={() => sigRef.current?.undo()}>Undo</ButtonComponent>
      <ButtonComponent disabled={!redoEnabled} onClick={() => sigRef.current?.redo()}>Redo</ButtonComponent>
      <SignatureComponent id="signature" ref={sigRef} change={handleChange} />
    </div>
  );
}
export default App;
```

---

## Clear

The `clear()` method erases all strokes from the canvas. This action is added to the undo history, so the user can undo a clear operation. Use `isEmpty()` to check if the canvas is already empty.

| Method | Returns | Description |
|--------|---------|-------------|
| `clear()` | `void` | Clears all strokes from the canvas |
| `isEmpty()` | `boolean` | `true` if the canvas has no strokes |

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const sigRef = React.useRef<SignatureComponent>(null);

  function handleClear(): void {
    if (sigRef.current && !sigRef.current.isEmpty()) {
      sigRef.current.clear();
    }
  }

  return (
    <div>
      <ButtonComponent onClick={handleClear}>Clear</ButtonComponent>
      <SignatureComponent id="signature" ref={sigRef} />
    </div>
  );
}
export default App;
```

---

## Disabled

Set `disabled={true}` to prevent any interaction with the component. The canvas appears with reduced opacity to indicate the disabled state. The component cannot receive focus while disabled.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function onDisableChange(args: ChangeEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.disabled = args.checked;
  }

  return (
    <div>
      <CheckBoxComponent label="Disabled" change={onDisableChange} />
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

## ReadOnly

Set `isReadOnly={true}` to prevent drawing while still allowing the component to receive focus. Useful for displaying a previously captured signature without allowing modification.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function onReadOnlyChange(args: ChangeEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.isReadOnly = args.checked;
  }

  return (
    <div>
      <CheckBoxComponent label="ReadOnly" change={onReadOnlyChange} />
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

**Difference from `disabled`:**
- `disabled` — component cannot receive focus; full interaction blocked
- `isReadOnly` — component can receive focus; only drawing is blocked

---

## Draw Text as Signature

The `draw(text, fontFamily?, fontSize?)` method renders a text string onto the canvas as a signature. Useful for auto-generating a typed signature.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `string` | — | Text to render on the canvas |
| `fontFamily` | `string` | `'Arial'` | Font family (e.g., `'Serif'`, `'Cursive'`) |
| `fontSize` | `number` | `30` | Font size in pixels |

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const fontData: string[] = ['Arial', 'Serif', 'Sans-serif', 'Cursive', 'Fantasy'];
  const sizeData: number[] = [20, 30, 40, 50];

  function drawText(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const text: string = (document.getElementById('textInput') as HTMLInputElement).value;
    const font: string = (document.getElementById('fontDDL') as any).value;
    const size: number = (document.getElementById('sizeDDL') as any).value;
    signature.draw(text, font, size);
  }

  return (
    <div>
      <div>
        <label>Text: </label>
        <input type="text" id="textInput" placeholder="Enter your name" />
      </div>
      <div>
        <label>Font: </label>
        <DropDownListComponent id="fontDDL" dataSource={fontData} value="Arial" />
      </div>
      <div>
        <label>Size: </label>
        <DropDownListComponent id="sizeDDL" dataSource={sizeData} value={30} />
      </div>
      <ButtonComponent isPrimary={true} onClick={drawText}>Draw</ButtonComponent>
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

## Keyboard Shortcuts

The Signature component supports built-in keyboard shortcuts when the canvas has focus:

| Key | Action |
|-----|--------|
| `Ctrl + Z` | Undo the last action |
| `Ctrl + Y` | Redo the last action |
| `Ctrl + S` | Save the signature (triggers `beforeSave` event) |
| `Delete` | Clear all signature strokes |

The `beforeSave` event is raised for keyboard-triggered saves (`Ctrl + S`), allowing customization of the file name and type before saving.

---

## Change Event

The `change` event fires after every user action — completing a stroke, undo, redo, and clear. Use it to update UI controls (e.g., enable/disable undo/redo/clear buttons).

```tsx
import { SignatureComponent, SignatureChangeEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function handleChange(args: SignatureChangeEventArgs): void {
    // Called after each stroke, undo, redo, or clear
    console.log('Signature changed', args);
  }

  return (
    <SignatureComponent id="signature" change={handleChange} />
  );
}
export default App;
```
