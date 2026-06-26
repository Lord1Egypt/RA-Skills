# Customization in Syncfusion React Signature

## Table of Contents
- [Stroke Width](#stroke-width)
- [Stroke Color](#stroke-color)
- [Background Color](#background-color)
- [Background Image](#background-image)

---

## Stroke Width

Control stroke thickness using `maxStrokeWidth`, `minStrokeWidth`, and `velocity`. The component calculates a variable stroke width based on these three values to produce a natural, smooth signature.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `maxStrokeWidth` | `number` | `2` | Maximum thickness of the stroke |
| `minStrokeWidth` | `number` | `0.5` | Minimum thickness of the stroke |
| `velocity` | `number` | `0.7` | Rate of stroke width change (0–1); lower values = greater width variation |

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="signature-control">
      <h4>Sign here</h4>
      <SignatureComponent
        id="signature"
        maxStrokeWidth={3}
        minStrokeWidth={0.5}
        velocity={0.7}
      />
    </div>
  );
}
export default App;
```

**Tip:** Increase `maxStrokeWidth` for bold strokes. Lower `velocity` produces more dramatic width variation between fast and slow strokes.

---

## Stroke Color

Use `strokeColor` to set the pen/ink color. Accepts hex codes (`#000000`), RGB values (`rgb(0,0,0)`), or CSS color names (`red`). The default is `#000000` (black).

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function applyColor(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const color: string = (document.getElementById('colorInput') as HTMLInputElement).value;
    signature.strokeColor = color;
  }

  return (
    <div>
      <input type="text" id="colorInput" placeholder="e.g. #e91e63 or red" />
      <ButtonComponent isPrimary={true} onClick={applyColor}>Set Stroke Color</ButtonComponent>
      <div id="signature-control">
        <SignatureComponent id="signature" strokeColor="#000000" />
      </div>
    </div>
  );
}
export default App;
```

---

## Background Color

Use `backgroundColor` to fill the canvas background. Accepts hex codes, RGB values, or CSS color names. The default is `''` (transparent/white).

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function applyBg(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const bgColor: string = (document.getElementById('bgInput') as HTMLInputElement).value;
    signature.backgroundColor = bgColor;
  }

  return (
    <div>
      <input type="text" id="bgInput" placeholder="e.g. #f0f0f0 or lightyellow" />
      <ButtonComponent isPrimary={true} onClick={applyBg}>Set Background Color</ButtonComponent>
      <div id="signature-control">
        <SignatureComponent id="signature" backgroundColor="#ffffff" />
      </div>
    </div>
  );
}
export default App;
```

**Note:** `backgroundColor` affects the visual appearance. Whether the background is included when saving is controlled by `saveWithBackground` (see open-save.md).

---

## Background Image

Use `backgroundImage` to set a URL or base64-encoded image as the canvas background. The image fills the canvas behind the signature strokes.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function applyImage(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const url: string = (document.getElementById('imgInput') as HTMLInputElement).value;
    signature.backgroundImage = url;
  }

  return (
    <div>
      <input type="text" id="imgInput" placeholder="Enter image URL or base64" />
      <ButtonComponent isPrimary={true} onClick={applyImage}>Set Background Image</ButtonComponent>
      <div id="signature-control">
        <SignatureComponent id="signature" />
      </div>
    </div>
  );
}
export default App;
```

**Tip:** Hosted URLs and local base64 strings are both supported. Use a transparent background image for watermark or template effects.
