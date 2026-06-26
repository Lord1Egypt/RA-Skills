# Integration Examples

## Table of Contents
- [RichTextEditor with Preview Toggle](#richtexteditor-with-preview-toggle)
- [Side-by-Side Editor and Preview with Splitter](#side-by-side-editor-and-preview-with-splitter)

---

## RichTextEditor with Preview Toggle

This example integrates `MarkdownConverter` with the Syncfusion `RichTextEditorComponent` in Markdown editor mode. A custom Preview toolbar button toggles between the Markdown source and the rendered HTML preview.

**Required packages:**
```bash
npm install @syncfusion/ej2-react-richtexteditor @syncfusion/ej2-markdown-converter @syncfusion/ej2-base
```

**Required CSS imports:**
```tsx
import '@syncfusion/ej2-react-richtexteditor/styles/material.css';
```

```tsx
import * as React from 'react';
import { useRef } from 'react';
import {
  RichTextEditorComponent, Inject, Link, Image,
  MarkdownEditor, Toolbar, Table
} from '@syncfusion/ej2-react-richtexteditor';
import { MarkdownFormatter, KeyboardEventArgs } from '@syncfusion/ej2-richtexteditor';
import { createElement } from '@syncfusion/ej2-base';
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);
  let mdsource: HTMLElement;
  let textArea: HTMLTextAreaElement;

  const toolbarSettings = {
    items: [
      'Bold', 'Italic', 'StrikeThrough', '|',
      'Formats', 'Blockquote', 'OrderedList', 'UnorderedList',
      'SuperScript', 'SubScript', '|',
      'CreateLink', 'Image', 'CreateTable', '|',
      {
        tooltipText: 'Preview',
        template:
          '<button id="preview-code" class="e-tbar-btn e-control e-btn e-icon-btn" aria-label="Preview Code">' +
          '<span class="e-btn-icon e-md-preview e-icons"></span></button>'
      },
      '|', 'Undo', 'Redo'
    ]
  };

  // Called on every keyup — updates preview if it is currently active
  function markDownConversion(): void {
    if (mdsource.classList.contains('e-active')) {
      const id = rteRef.current!.getID() + 'html-view';
      const htmlPreview = rteRef.current!.element.querySelector('#' + id) as HTMLElement;
      htmlPreview.innerHTML = MarkdownConverter.toHtml(
        (rteRef.current!.contentModule.getEditPanel() as HTMLTextAreaElement).value
      ) as string;
    }
  }

  // Toggles between Markdown source view and HTML preview
  function fullPreview(): void {
    const id = rteRef.current!.getID() + 'html-preview';
    let htmlPreview = rteRef.current!.element.querySelector('#' + id) as HTMLElement;
    const previewTextArea = rteRef.current!.element.querySelector('.e-rte-content') as HTMLElement;

    if (mdsource.classList.contains('e-active')) {
      // Switch back to Markdown source
      mdsource.classList.remove('e-active');
      mdsource.parentElement!.title = 'Preview';
      textArea.style.display = 'block';
      htmlPreview.style.display = 'none';
      previewTextArea.style.overflow = 'hidden';
    } else {
      // Switch to HTML preview
      mdsource.classList.add('e-active');
      if (!htmlPreview) {
        htmlPreview = createElement('div', { className: 'e-content e-pre-source' });
        htmlPreview.id = id;
        textArea.parentNode!.appendChild(htmlPreview);
        previewTextArea.style.overflow = 'auto';
      }
      if (previewTextArea.style.overflow === 'hidden') {
        previewTextArea.style.overflow = 'auto';
      }
      textArea.style.display = 'none';
      htmlPreview.style.display = 'block';
      htmlPreview.innerHTML = MarkdownConverter.toHtml(
        (rteRef.current!.contentModule.getEditPanel() as HTMLTextAreaElement).value
      ) as string;
      mdsource.parentElement!.title = 'Code View';
    }
  }

  const onCreate = () => {
    textArea = rteRef.current!.contentModule.getEditPanel() as HTMLTextAreaElement;
    // Update preview on every keyup
    textArea.addEventListener('keyup', (e: KeyboardEventArgs) => {
      markDownConversion();
    });

    mdsource = document.getElementById('preview-code')!;
    mdsource.addEventListener('click', (e: MouseEvent) => {
      fullPreview();
      // Disable editing toolbar items when in preview mode
      if ((e.currentTarget as HTMLElement).classList.contains('e-active')) {
        rteRef.current!.disableToolbarItem([
          'Bold', 'Italic', 'StrikeThrough', 'OrderedList', 'UnorderedList',
          'SuperScript', 'SubScript', 'CreateLink', 'Image', 'CreateTable',
          'Formats', 'Blockquote', 'Undo', 'Redo'
        ]);
      } else {
        rteRef.current!.enableToolbarItem([
          'Bold', 'Italic', 'StrikeThrough', 'OrderedList', 'UnorderedList',
          'SuperScript', 'SubScript', 'CreateLink', 'Image', 'CreateTable',
          'Formats', 'Blockquote', 'Undo', 'Redo'
        ]);
      }
    });
  };

  return (
    <RichTextEditorComponent
      id="markdown-editor"
      ref={rteRef}
      height="520px"
      value="# Welcome\nType **Markdown** here and click Preview to see the HTML output."
      placeholder="Enter your Markdown here..."
      formatter={new MarkdownFormatter({ listTags: { 'OL': '1., 2., 3.' } })}
      editorMode="Markdown"
      toolbarSettings={toolbarSettings}
      created={onCreate}
    >
      <Inject services={[Link, Image, MarkdownEditor, Toolbar, Table]} />
    </RichTextEditorComponent>
  );
}

export default App;
```

**Key points:**
- `editorMode="Markdown"` enables Markdown editing mode in the RichTextEditor.
- The `created` callback wires up the keyup listener and Preview button click handler.
- `disableToolbarItem` / `enableToolbarItem` prevents editing while in preview mode.
- The HTML preview `div` is created lazily on first toggle.

---

## Side-by-Side Editor and Preview with Splitter

This example uses the Syncfusion `SplitterComponent` to display the RichTextEditor (Markdown mode) on the left and a live HTML preview on the right, with automatic conversion on every change.

**Required packages:**
```bash
npm install @syncfusion/ej2-react-richtexteditor @syncfusion/ej2-react-layouts @syncfusion/ej2-markdown-converter @syncfusion/ej2-base
```

**Required CSS imports:**
```tsx
import '@syncfusion/ej2-react-richtexteditor/styles/material.css';
import '@syncfusion/ej2-react-layouts/styles/material.css';
```

```tsx
import * as React from 'react';
import { useRef } from 'react';
import {
  RichTextEditorComponent, Inject, Link, Image,
  MarkdownEditor, Toolbar, Table, ToolbarType
} from '@syncfusion/ej2-react-richtexteditor';
import {
  SplitterComponent, PanesDirective, PaneDirective
} from '@syncfusion/ej2-react-layouts';
import { Browser } from '@syncfusion/ej2-base';
import { MarkdownConverter } from '@syncfusion/ej2-markdown-converter';

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);
  const splitterRef = useRef<SplitterComponent>(null);
  const srcAreaRef = useRef<HTMLDivElement>(null);

  const toolbarSettings = {
    type: ToolbarType.Expand,
    enableFloating: false,
    items: [
      'Bold', 'Italic', 'StrikeThrough', '|',
      'Formats', 'Blockquote', 'OrderedList', 'UnorderedList', '|',
      'CreateLink', 'Image', 'CreateTable', '|',
      'Undo', 'Redo'
    ]
  };

  // Converts current editor content and updates the preview pane
  const updateValue = () => {
    if (srcAreaRef.current && rteRef.current) {
      srcAreaRef.current.innerHTML = MarkdownConverter.toHtml(
        (rteRef.current.contentModule.getEditPanel() as HTMLTextAreaElement).value,
        { async: true, gfm: true, lineBreak: true, silence: true }
      ) as string;
    }
  };

  const onCreate = () => {
    updateValue(); // Render initial content
    // Switch splitter to vertical layout on mobile devices
    if (Browser.isDevice && splitterRef.current) {
      splitterRef.current.orientation = 'Vertical';
    }
  };

  // Refresh RTE layout when the splitter is resized
  const onResizing = () => {
    if (rteRef.current) {
      rteRef.current.refreshUI();
    }
  };

  return (
    <SplitterComponent
      id="splitter-rte-markdown-preview"
      ref={splitterRef}
      height="450px"
      width="100%"
      resizing={onResizing}
    >
      <PanesDirective>
        <PaneDirective
          resizable={true}
          size="50%"
          min="40%"
          content={() => (
            <RichTextEditorComponent
              id="markdown-editor"
              ref={rteRef}
              height="100%"
              value="# Welcome\nEdit this **Markdown** content and see the live preview on the right."
              placeholder="Enter your Markdown here..."
              floatingToolbarOffset={0}
              editorMode="Markdown"
              toolbarSettings={toolbarSettings}
              saveInterval={1}
              actionComplete={updateValue}
              change={updateValue}
              created={onCreate}
            >
              <Inject services={[Link, Image, MarkdownEditor, Toolbar, Table]} />
            </RichTextEditorComponent>
          )}
        />
        <PaneDirective
          min="40%"
          content={() => (
            <div
              className="source-code"
              ref={srcAreaRef}
              style={{ padding: '10px' }}
            />
          )}
        />
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**Key points:**
- `actionComplete` and `change` events both trigger `updateValue` for live updates.
- `saveInterval={1}` ensures the RTE value updates frequently for near-real-time preview.
- `Browser.isDevice` switches the Splitter to vertical orientation on mobile.
- `onResizing` calls `refreshUI()` to prevent layout issues when the splitter is dragged.
- All four `MarkdownConverterOptions` are passed for robust user-input handling.
