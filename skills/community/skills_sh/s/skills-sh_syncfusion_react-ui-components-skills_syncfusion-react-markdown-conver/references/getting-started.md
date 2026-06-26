# Getting Started with Syncfusion React Markdown Converter

## 1. Install Syncfusion Packages

Install both the Markdown Converter and the Rich Text Editor packages:

```bash
npm install @syncfusion/ej2-markdown-converter
npm install @syncfusion/ej2-react-richtexteditor
```

The `ej2-markdown-converter` package provides the `MarkdownConverter` utility. The `ej2-react-richtexteditor` package provides the `ejs-richtexteditor` component used to author Markdown content.

## 2. Add CSS References

Add the following imports to `src/styles.css`. These load the material3 theme for all required Syncfusion sub-packages:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-layouts/styles/material3.css';
```

> **Note:** `ej2-layouts` is only required if you are using the Splitter component for a side-by-side preview layout.

## 3. Module Injection

The Rich Text Editor in Markdown mode uses a modular architecture — inject only the modules your feature requires. All modules are passed via the `<Inject services={[...]} />` child component.

| Module | Purpose |
|--------|---------|
| `ToolbarService` | Enables the editor toolbar |
| `LinkService` | Enables hyperlink support in Markdown |
| `ImageService` | Enables image insertion |
| `MarkdownEditorService` | Activates Markdown editing mode |
| `TableService` | Enables table insertion |

```tsx
import {
  ToolbarService,
  LinkService,
  ImageService,
  MarkdownEditorService,
  TableService
} from '@syncfusion/ej2-react-richtexteditor';
```

## 4. Basic AppComponent

A minimal working example:

```tsx
import React, { useRef, useEffect } from 'react';
import { RichTextEditorComponent, MarkdownEditor, Inject, Toolbar, Link, Image, Table, ToolbarSettingsModel, MarkdownFormatter } from '@syncfusion/ej2-react-richtexteditor';
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

function App() {
  return (
    <RichTextEditorComponent
      editorMode="Markdown"
      height="520px"
    >
      <Inject services={[MarkdownEditor, Toolbar, Image, Link, Table]} />
    </RichTextEditorComponent>
  );
}

export default App;
```

## 5. Run the App

```bash
npm run dev
```

The browser opens with the Markdown Editor. Click **Preview** in the toolbar to see the real-time HTML output of your Markdown content.

## Common Setup Issues

- **Missing CSS:** If the editor renders unstyled, verify all `@import` lines in `styles.css` match the packages installed in `node_modules/@syncfusion`.
- **Module not found errors:** Ensure both `@syncfusion/ej2-markdown-converter` and `@syncfusion/ej2-react-richtexteditor` are listed in `package.json` dependencies.
