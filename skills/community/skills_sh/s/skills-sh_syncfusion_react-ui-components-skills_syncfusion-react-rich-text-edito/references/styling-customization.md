# Styling & Customization in Syncfusion React Rich Text Editor

## Table of Contents
- [Theme Selection](#theme-selection)
- [CSS Variable Customization](#css-variable-customization)
- [Styling Editor Content Output](#styling-editor-content-output)
- [Third-Party Integration](#third-party-integration)
- [Spell and Grammar Check](#spell-and-grammar-check)

## Theme Selection

Import the theme CSS files that match your app's design system. Replace `tailwind3` with any available theme:

Available themes: `material3`, `material3-dark`, `bootstrap5`, `bootstrap5-dark`, `fluent2`, `fluent2-dark`, `tailwind3`, `tailwind3-dark`, `fabric`, `highcontrast`

```css
/* src/App.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/material3.css';
```

## CSS Variable Customization

Override built-in CSS variables to adjust colors, fonts, and sizes without changing the theme:

```css
/* Override RTE primary accent color */
:root {
  --color-sf-primary: #6200ee;
  --color-sf-on-primary: #ffffff;
}

/* Customize toolbar height */
.e-richtexteditor .e-rte-toolbar {
  min-height: 44px;
}

/* Customize editor content area font */
.e-richtexteditor .e-rte-content {
  font-family: 'Georgia', serif;
  font-size: 16px;
  line-height: 1.6;
}
```

## Styling Editor Content Output

When you render the RTE's HTML value **outside** the editor (e.g., in a read-only preview), apply the `e-rte-content` class and include these styles so the output matches what users saw in the editor:

```html
<div class="e-rte-content" dangerouslySetInnerHTML={{ __html: savedContent }} />
```

```css
/* Add to your global CSS */
.e-rte-content p { margin: 0 0 10px; }
.e-rte-content h1 { font-size: 2.17em; font-weight: 400; margin: 10px 0; }
.e-rte-content h2 { font-size: 1.74em; font-weight: 400; margin: 10px 0; }
.e-rte-content h3 { font-size: 1.31em; font-weight: 400; margin: 10px 0; }
.e-rte-content blockquote { border-left: solid 2px #333; padding-left: 5px; margin: 10px 0; }
.e-rte-content .e-rte-table { border-collapse: collapse; }
.e-rte-content .e-rte-table td, .e-rte-content .e-rte-table th {
  border: 1px solid #bdbdbd; padding: 2px 5px; min-width: 20px;
}
```

### Tailwind CSS Preflight Conflict

If you're using Tailwind CSS and its preflight resets are overriding the RTE's styles, add a wrapper with `@layer` to scope the conflict:

```css
/* Disable Tailwind preflight for RTE elements */
.e-richtexteditor, .e-rte-content {
  /* Reset Tailwind's border-box and other base resets */
}
```

Or exclude the RTE wrapper from Tailwind's preflight. See `how-to.md` for the full solution.

## Third-Party Integration

### CodeMirror (Enhanced Source Code Editor)

Replace the plain textarea source view with CodeMirror for syntax highlighting:

```bash
npm install codemirror
```

```tsx
import CodeMirror from 'codemirror';
import 'codemirror/mode/xml/xml';
import 'codemirror/lib/codemirror.css';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);

  const sourceCodeChange = (args: SourceEventArgs) => {
    if (args.mode === 'SourceCode') {
      const srcView = (rteRef.current as any).element.querySelector('.e-rte-srctextarea');
      const mirrorView = CodeMirror(srcView.parentNode, {
        value: srcView.value,
        lineNumbers: true,
        mode: 'xml',
      });
      mirrorView.on('change', () => {
        srcView.value = mirrorView.getValue();
      });
    }
  };

  return (
    <RichTextEditorComponent ref={rteRef} actionBegin={sourceCodeChange}>
      <Inject services={[Toolbar, HtmlEditor]} />
    </RichTextEditorComponent>
  );
}
```

## Spell and Grammar Check

Integrate browser-native spell checking or a third-party service:

### Browser Native Spell Check

```tsx
<RichTextEditorComponent>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

The RTE's `contenteditable` area inherits the browser's built-in spell checking. No additional configuration needed — the browser will underline misspelled words.

### Custom Spell Check Integration

For full spell/grammar services (like LanguageTool or Grammarly), attach to the `created` event and initialize the third-party SDK on the editor's content area:

```tsx
const onCreated = () => {
  const editArea = (rteRef.current as any).contentModule.getEditPanel();
  // Initialize your spell-check service on editArea
  mySpellChecker.attach(editArea);
};

<RichTextEditorComponent ref={rteRef} created={onCreated}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```
