# Open and Save in Syncfusion React Signature

## Table of Contents
- [Open / Load Signature](#open--load-signature)
- [Save as Base64](#save-as-base64)
- [Save as Blob](#save-as-blob)
- [Save as Image File](#save-as-image-file)
- [Save with Background](#save-with-background)

---

## Open / Load Signature

The `load(signature, width?, height?)` method loads a previously saved signature onto the canvas. Accepts a base64 string or a hosted/online image URL in PNG, JPEG, or SVG format.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function loadSignature(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const value: string = (document.getElementById('signInput') as HTMLInputElement).value;
    signature.load(value);
  }

  return (
    <div>
      <input type="text" id="signInput" placeholder="Enter base64 or URL of signature" />
      <ButtonComponent isPrimary={true} onClick={loadSignature}>Open</ButtonComponent>
      <div id="signature-control">
        <SignatureComponent id="signature" />
      </div>
    </div>
  );
}
export default App;
```

**Parameters:**
- `signature` (string) — base64 string or URL of the image
- `width` (number, optional) — width to render the loaded image
- `height` (number, optional) — height to render the loaded image

---

## Save as Base64

The `getSignature(type?)` method returns the current canvas content as a base64-encoded string. Supports `'Png'`, `'Jpeg'`, and `'Svg'` formats (default: `'Png'`).

The returned base64 string can be stored in a database or passed back to `load()` to restore the signature.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const [base64, setBase64] = React.useState<string>('');

  function getBase64(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const result: string = signature.getSignature();
    setBase64(result);
    console.log(result); // data:image/png;base64,...
  }

  return (
    <div>
      <SignatureComponent id="signature" />
      <ButtonComponent cssClass="e-primary" onClick={getBase64}>Save as Base64</ButtonComponent>
      {base64 && <img src={base64} alt="Saved signature" style={{ border: '1px solid #ccc', marginTop: 8 }} />}
    </div>
  );
}
export default App;
```

---

## Save as Blob

Two methods are available for blob output:

- **`saveAsBlob()`** — Returns a `Blob` object directly from the current canvas content.
- **`getBlob(url)`** — Converts a given base64/URL string to a `Blob` object.

Use blobs for file uploads, form submissions, or binary storage.

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function saveBlob(): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    const blob: Blob = signature.saveAsBlob();
    // Use blob for upload, FormData, etc.
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'signature.png';
    link.click();
  }

  return (
    <div>
      <SignatureComponent id="signature" />
      <ButtonComponent cssClass="e-primary" onClick={saveBlob}>Save as Blob</ButtonComponent>
    </div>
  );
}
export default App;
```

---

## Save as Image File

The `save(type?, fileName?)` method downloads the signature as an image file directly to the user's browser. Accepts `'Png'`, `'Jpeg'`, or `'Svg'` as the file type. The default is `'Png'`.

```tsx
import { SignatureComponent, SignatureFileType } from '@syncfusion/ej2-react-inputs';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const items = [{ text: 'Png' }, { text: 'Jpeg' }, { text: 'Svg' }];

  function onSelect(args: MenuEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.save(args.item.text as SignatureFileType, 'Signature');
  }

  return (
    <div>
      <div>
        <SplitButtonComponent
          content="Save"
          iconCss="e-sign-icons e-save"
          items={items}
          select={onSelect}
        />
      </div>
      <div id="signature-control">
        <SignatureComponent id="signature" />
      </div>
    </div>
  );
}
export default App;
```

**Parameters:**
- `type` (SignatureFileType, optional) — `'Png'` | `'Jpeg'` | `'Svg'`
- `fileName` (string, optional) — name of the downloaded file (without extension)

---

## Save with Background

The `saveWithBackground` property controls whether the background color and background image are included when saving. The default is `true`.

- `true` — background is included in the saved image
- `false` — signature strokes only, on a transparent/white background

```tsx
import { SignatureComponent, SignatureFileType } from '@syncfusion/ej2-react-inputs';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const items = [{ text: 'Png' }, { text: 'Jpeg' }, { text: 'Svg' }];

  function onSelect(args: MenuEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.save(args.item.text as SignatureFileType, 'Signature');
  }

  return (
    <div>
      <SplitButtonComponent content="Save" items={items} select={onSelect} />
      <div id="signature-control">
        {/* saveWithBackground={true} saves the purple background with the signature */}
        <SignatureComponent
          id="signature"
          backgroundColor="rgb(103 58 183)"
          saveWithBackground={true}
        />
      </div>
    </div>
  );
}
export default App;
```

**Tip:** Set `saveWithBackground={false}` when you need a transparent PNG for overlaying the signature on other documents.
