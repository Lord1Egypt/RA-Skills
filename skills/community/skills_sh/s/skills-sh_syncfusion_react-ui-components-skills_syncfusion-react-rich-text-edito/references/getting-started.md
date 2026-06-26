# Getting Started with Syncfusion React Rich Text Editor

## Installation

```bash
npm install @syncfusion/ej2-react-richtexteditor
```

## CSS Imports

Add these to your `src/App.css`. Use the theme that matches your app (tailwind3, material, bootstrap5, fluent2, etc.).

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/tailwind3.css';
```

## Minimal Implementation

```tsx
import { HtmlEditor, Image, Inject, Link, QuickToolbar, RichTextEditorComponent, Toolbar } from '@syncfusion/ej2-react-richtexteditor';
import './App.css';

function App() {
  return (
    <RichTextEditorComponent>
      <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
export default App;
```

## Module Injection Pattern

The RTE uses a modular architecture — inject only the modules your feature requires. All modules are passed via the `<Inject services={[...]} />` child component.

```tsx
import { RichTextEditorComponent, Inject, Toolbar, HtmlEditor, Link, Image, QuickToolbar, Table, PasteCleanup, Count } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  return (
    <RichTextEditorComponent height={450}>
      <Inject services={[Toolbar, HtmlEditor, Link, Image, QuickToolbar, Table, PasteCleanup, Count]} />
    </RichTextEditorComponent>
  );
}
```

> Omitting a module silently disables its feature. If image upload isn't working, check that `Image` is injected.

## Basic Toolbar Configuration

Use `toolbarSettings.items` to specify which toolbar buttons appear.

```tsx
const toolbarSettings: ToolbarSettingsModel = {
  items: [
    'Bold', 'Italic', 'Underline', 'StrikeThrough',
    'FontName', 'FontSize', 'FontColor', 'BackgroundColor', '|',
    'Formats', 'Alignments', 'OrderedList', 'UnorderedList',
    'Outdent', 'Indent', '|',
    'CreateLink', 'Image', '|',
    'ClearFormat', 'Print', 'SourceCode', 'FullScreen', '|',
    'Undo', 'Redo'
  ]
};

function App() {
  return (
    <RichTextEditorComponent height={450} toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
```

> Use `|` for a vertical separator and `-` for a horizontal separator in the toolbar.

## Setting Initial Content

Pass HTML string via the `value` prop:

```tsx
const content: string = `<p>Welcome to <b>Syncfusion</b> Rich Text Editor.</p>
<ul>
  <li>WYSIWYG editing</li>
  <li>Markdown support</li>
  <li>Media insertion</li>
</ul>`;

function App() {
  return (
    <RichTextEditorComponent value={content} height={450}>
      <Inject services={[Toolbar, HtmlEditor]} />
    </RichTextEditorComponent>
  );
}
```

## Run the App

```bash
npm run dev
```

## Common Setup Gotchas

- **Missing styles**: All the `@syncfusion/ej2-*` CSS imports are required — the RTE uses styles from multiple packages.
- **Blank toolbar**: Ensure `Toolbar` is in the injected services AND `toolbarSettings.items` is configured.
- **Image upload fails**: `Image` module must be injected; also configure `insertImageSettings.saveUrl` for server upload.
- **TypeScript errors**: Import types like `ToolbarSettingsModel` from `@syncfusion/ej2-react-richtexteditor`.
