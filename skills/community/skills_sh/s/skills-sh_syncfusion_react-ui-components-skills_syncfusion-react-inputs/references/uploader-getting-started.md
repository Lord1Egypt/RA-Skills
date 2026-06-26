# Getting Started – Syncfusion React Uploader

## Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [License Registration](#license-registration)
- [CSS Theme Imports](#css-theme-imports)
- [Basic Usage](#basic-usage)
- [Drop Area Configuration](#drop-area-configuration)
- [Success and Failure Handling](#success-and-failure-handling)
- [React with Hooks (Functional Components)](#react-with-hooks-functional-components)
- [React Class Component](#react-class-component)

---

## Dependencies

The React Uploader component requires the following packages:

```
@syncfusion/ej2-react-inputs
  └── @syncfusion/ej2-inputs
        ├── @syncfusion/ej2-base
        ├── @syncfusion/ej2-buttons
        ├── @syncfusion/ej2-popups
        └── @syncfusion/ej2-splitbuttons
```

---

## Installation

Install the inputs package (includes UploaderComponent):

```bash
npm install @syncfusion/ej2-react-inputs
```

Or install the full Syncfusion suite:

```bash
npm install @syncfusion/ej2-react-inputs @syncfusion/ej2-base @syncfusion/ej2-buttons @syncfusion/ej2-popups
```

---

## License Registration

Register your Syncfusion license key before rendering any component (typically in `main.tsx` or `index.tsx`):

```tsx
import { registerLicense } from '@syncfusion/ej2-base';
registerLicense('YOUR_LICENSE_KEY');
```

> Get your free license key at [syncfusion.com/products/communitylicense](https://www.syncfusion.com/products/communitylicense).

---

## CSS Theme Imports

Import required CSS files. The Uploader depends on base, buttons, inputs, and popups styles.

**Material theme (recommended):**
```tsx
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';
```

> Import order matters — follow the dependency sequence above.

**Available themes:** `material`, `material3`, `bootstrap5`, `fluent`, `tailwind`, `highcontrast`

Replace `material` with the desired theme name in all import paths.

**Global stylesheet (styles.css / index.css):**
```css
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material.css';
@import '../node_modules/@syncfusion/ej2-react-inputs/styles/material.css';
```

---

## Basic Usage

The simplest uploader renders a browse button, a drop zone, and a file list. By default, `autoUpload` is `true`, so files upload immediately on selection.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return <UploaderComponent asyncSettings={asyncSettings} />;
}

export default App;
```

**Disable auto upload** (show Upload/Clear buttons instead):

```tsx
<UploaderComponent
  asyncSettings={asyncSettings}
  autoUpload={false}
/>
```

> From v16.2.41+, Syncfusion EJ2 AJAX is used internally for server requests.

---

## Drop Area Configuration

By default, the Uploader acts as its own drop target. Configure an external element as the drop area using the `dropArea` property.

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const dropAreaRef = useRef<HTMLDivElement>(null);
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  return (
    <div>
      <div ref={dropAreaRef} style={{ border: '2px dashed #ccc', padding: '40px', textAlign: 'center' }}>
        Drop files here
      </div>
      <UploaderComponent
        asyncSettings={asyncSettings}
        dropArea={dropAreaRef.current}
      />
    </div>
  );
}
```

> `dropArea` accepts an `HTMLElement` reference or a CSS selector string.

---

## Success and Failure Handling

Handle upload and remove operation results using `success` and `failure` events.

```tsx
import React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const onSuccess = (args: any): void => {
    // args.operation: 'upload' | 'remove'
    if (args.operation === 'upload') {
      console.log('File uploaded:', args.file.name);
    } else {
      console.log('File removed:', args.file.name);
    }
  };

  const onFailure = (args: any): void => {
    // args.operation: 'upload' | 'remove'
    console.error(`${args.operation} failed for:`, args.file.name);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      success={onSuccess}
      failure={onFailure}
    />
  );
}
```

---

## React with Hooks (Functional Components)

Full example using hooks with manual upload, ref access, and programmatic control:

```tsx
import React, { useRef } from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const uploaderRef = useRef<UploaderComponent>(null);

  const asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  const handleUpload = () => {
    // Programmatically upload all queued files
    uploaderRef.current?.upload(uploaderRef.current.getFilesData());
  };

  const handleClear = () => {
    uploaderRef.current?.clearAll();
  };

  return (
    <div>
      <UploaderComponent
        ref={uploaderRef}
        asyncSettings={asyncSettings}
        autoUpload={false}
      />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
}
```

---

## React Class Component

```tsx
import * as React from 'react';
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';

class App extends React.Component {
  public asyncSettings = {
    saveUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/react/production/api/FileUploader/Remove'
  };

  public onSuccess(args: any): void {
    console.log('Operation:', args.operation, '| File:', args.file.name);
  }

  public render() {
    return (
      <UploaderComponent
        asyncSettings={this.asyncSettings}
        autoUpload={false}
        success={this.onSuccess}
      />
    );
  }
}

export default App;
```

---

## Gotchas

- **CSS import order** — Must match the dependency sequence; wrong order can break layout.
- **License key** — Must be registered before any Syncfusion component renders.
- **dropArea timing** — When using a `ref` for `dropArea`, pass the `.current` after the DOM has mounted (use `useEffect` or set it in component state).
- **autoUpload default is `true`** — Files upload immediately. Set `autoUpload={false}` to show manual Upload/Clear buttons.
- **AJAX library** — From v16.2.41+, the component uses EJ2 AJAX internally; use a Promise polyfill (e.g., `bluebird`) for IE support.
