---
name: syncfusion-react-rich-text-editor
description: "Implements the Syncfusion React Rich Text Editor (RichTextEditorComponent) from ej2-react-richtexteditor, supporting HTML (WYSIWYG) and Markdown editing. Use this skill for toolbar configuration, image/video/audio insertion, paste cleanup, AI assistant integration, emoji picker, slash menu, mentions, import/export Word/PDF, form validation, and source code view in React applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "File Viewers & Editors"
---

# Syncfusion React Rich Text Editor

A WYSIWYG (What You See Is What You Get) editor for creating and formatting rich content as HTML or Markdown. Supports toolbars, media insertion, AI assistance, smart editing features, form validation, and deep customization.

## When to Use This Skill

- Setting up a rich text / WYSIWYG editor in a React app
- Configuring toolbar items, types, or positions
- Switching between HTML and Markdown editor modes
- Inserting images, video, audio, or files
- Working with smart editing features: emoji, slash menu, mentions, mail merge
- Integrating AI assistant into the editor
- Handling editor value: get, set, two-way binding, auto-save, import/export
- Applying paste cleanup, form validation, or read-only mode
- Customizing styles, accessibility, or keyboard shortcuts

## Quick Start

```bash
npm install @syncfusion/ej2-react-richtexteditor
```

```tsx
// src/App.css - add CSS imports
// @import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
// @import '../node_modules/@syncfusion/ej2-richtexteditor/styles/tailwind3.css';

import {
  HtmlEditor, Image, Inject, Link,
  QuickToolbar, RichTextEditorComponent, Toolbar
} from '@syncfusion/ej2-react-richtexteditor';

function App() {
  return (
    <RichTextEditorComponent height={450}>
      <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar]} />
    </RichTextEditorComponent>
  );
}
export default App;
```

## Module Injection Reference

Inject only the modules your app needs — this keeps the bundle lean.

| Module | What it enables |
|---|---|
| `Toolbar` | Toolbar rendering and commands |
| `HtmlEditor` | HTML editing mode (default) |
| `MarkdownEditor` | Markdown editing mode |
| `Link` | Hyperlink insert/edit/remove |
| `Image` | Image insertion and management |
| `Video` | Video insertion |
| `Audio` | Audio insertion |
| `Table` | HTML table insert/edit |
| `QuickToolbar` | Floating toolbar for images/links |
| `PasteCleanup` | Clean up pasted content formatting |
| `ClipboardCleanup` | Clean clipboard on copy/cut |
| `FileManager` | File browser for server-side images |
| `Resize` | Resizable editor area |
| `Count` | Character count display |
| `EmojiPicker` | Emoji search and insert |
| `SlashMenu` | Slash `/` command menu |
| `ImportExport` | Import Word, export Word/PDF |
| `CodeBlock` | Inline code block formatting |
| `AutoFormat` | Auto-convert Markdown syntax while typing |
| `FormatPainter` | Copy-paste text formatting |
| `AIAssistant` | AI assistant integration |

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation, npm setup, CSS imports
- Basic component implementation
- Module injection patterns
- Toolbar configuration basics
- Running the application

### Editor Modes
📄 **Read:** [references/editor-modes.md](references/editor-modes.md)
- HTML editor mode (default WYSIWYG)
- Markdown editor mode with preview
- IFrame vs DIV mode
- Inline editing
- Resizable editor

### Toolbar Configuration
📄 **Read:** [references/toolbar-configuration.md](references/toolbar-configuration.md)
- Default toolbar items
- Toolbar types: Expand, MultiRow, Scrollable
- Toolbar position (top/bottom)
- Sticky/floating toolbar
- Quick toolbar for images and links

### Toolbar Tools
📄 **Read:** [references/toolbar-tools.md](references/toolbar-tools.md)
- Built-in tools reference (Bold, Italic, Formats, etc.)
- Custom toolbar items with templates
- Text formatting tools
- Styling tools (font, color, alignment)
- Fullscreen tool

### Inserting Media
📄 **Read:** [references/insert-media.md](references/insert-media.md)
- Inserting images (URL, upload, base64)
- Video insertion and configuration
- Audio insertion
- File browser integration

### Inserting Content
📄 **Read:** [references/insert-content.md](references/insert-content.md)
- Tables: insert, resize, merge cells
- Hyperlinks: create, edit, open in new tab
- Code blocks
- Custom format blocks

### Smart Editing Features
📄 **Read:** [references/smart-editing.md](references/smart-editing.md)
- Emoji picker
- Slash menu (type `/` to open)
- Mentions (tag users)
- Mail merge

### Managing Editor Value
📄 **Read:** [references/editor-value.md](references/editor-value.md)
- Setting initial value
- Getting value via property, event, or method
- Two-way binding with React state
- Auto-save with `saveInterval`
- Import/export Word and PDF
- Markdown preview
- Character count and maxLength
- Source code view

### Paste & Clipboard
📄 **Read:** [references/paste-clipboard.md](references/paste-clipboard.md)
- Paste cleanup configuration
- Clipboard cleanup on copy/cut
- Executing editor commands programmatically

### Validation & Security
📄 **Read:** [references/validation-security.md](references/validation-security.md)
- Form support and submission
- XHTML validation
- Read-only mode
- XSS prevention

### AI Assistant
📄 **Read:** [references/ai-assistant.md](references/ai-assistant.md)
- AI integration setup
- AI assistant properties
- Customizing AI toolbar and responses

### Accessibility & Globalization
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance
- Keyboard shortcuts
- Globalization, localization, RTL
- Style encapsulation

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS variable customization
- Style encapsulation (shadow DOM)
- Third-party integrations (CodeMirror, Mention library)
- Spell/grammar check

### Undo / Redo
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- Undo/redo manager behavior
- Keyboard shortcuts
- Programmatic undo/redo

### Enter Key & Selection
📄 **Read:** [references/enter-key-selection.md](references/enter-key-selection.md)
- Enter key configuration (P, BR, DIV)
- Selection API
- Cursor positioning

### Events
📄 **Read:** [references/events.md](references/events.md)
- Infer EventArgs Type value for each events 
- Lifecycle events: `created`, `destroyed`, `focus`, `blur`
- Content change: `change` event with `ChangeEventArgs`
- Action events: `actionBegin` (cancelable), `actionComplete`
- Toolbar events: `toolbarClick`, `updatedToolbarStatus`
- Dialog & popup events: `beforeDialogOpen/Close`, `beforePopupOpen/Close`
- Media & file events: image/audio/video upload, select, remove, drop
- Paste & clipboard events: `beforePasteCleanup`, `afterPasteCleanup`
- AI Assistant events: `aiAssistantPromptRequest`, `aiAssistantToolbarClick`
- Resize, slash menu, selection, quick toolbar, import/export events

### Methods
📄 **Read:** [references/methods.md](references/methods.md)
- Focus & content: `focusIn`, `focusOut`, `getHtml`, `getText`, `getSelectedHtml`
- Toolbar: `enableToolbarItem`, `disableToolbarItem`, `removeToolbarItem`
- Dialog: `showDialog`, `closeDialog` with `DialogType` enum
- Selection: `selectAll`, `getRange`, `selectRange`
- Undo/redo: `clearUndoRedo`
- AI Assistant: `executeAIPrompt`, `addAIPromptResponse`, `getAIPromptHistory`, `clearAIPromptHistory`
- Utility: `executeCommand` (all `CommandName` values), `sanitizeHtml`, `destroy`

### Properties Reference
📄 **Read:** [references/properties.md](references/properties.md)
- Core: `height`, `width`, `enabled`, `readonly`, `placeholder`, `cssClass`
- Toolbar: `toolbarSettings`, `quickToolbarSettings`, `floatingToolbarOffset`
- Editor mode & behavior: `editorMode`, `iframeSettings`, `inlineMode`, `enterKey`
- Value & content: `value`, `maxLength`, `showCharCount`, `saveInterval`, `enableHtmlSanitizer`
- Media: `insertImageSettings`, `insertVideoSettings`, `insertAudioSettings`, `fileManagerSettings`
- Font, color & format: `fontFamily`, `fontSize`, `fontColor`, `backgroundColor`, `format`, `codeBlockSettings`
- Paste: `pasteCleanupSettings`, `enableClipboardCleanup`
- AI Assistant: `aiAssistantSettings` (full configuration reference)
- Import/export: `importWord`, `exportWord`, `exportPdf`
- Misc: `undoRedoSteps`, `keyConfig`, `slashMenuSettings`, `emojiPickerSettings`

### How-To Guides
📄 **Read:** [references/how-to.md](references/how-to.md)
- Capture Ctrl keys to update value
- Change default font family
- Check uploaded image size
- Customize placeholder style
- Customize shortcut keys
- File attachment
- Format code blocks
- Position cursor at end of content
- Rename images on server
- RTE inside Dialog or Tab
- Set cursor at specific range
- Tailwind preflight fix
- Update value programmatically

## Common Patterns

### Read value on change
```tsx
import { ChangeEventArgs } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  const onChange = (args: ChangeEventArgs) => {
    console.log(args.value); // HTML string
  };
  return (
    <RichTextEditorComponent change={onChange}>
      <Inject services={[Toolbar, HtmlEditor]} />
    </RichTextEditorComponent>
  );
}
```

### Controlled value with React state
```tsx
const [content, setContent] = useState('<p>Hello</p>');
<RichTextEditorComponent value={content} change={(e) => setContent(e.value)}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### Markdown mode
```tsx
import { MarkdownEditor } from '@syncfusion/ej2-react-richtexteditor';
<RichTextEditorComponent editorMode="Markdown">
  <Inject services={[Toolbar, MarkdownEditor]} />
</RichTextEditorComponent>
```
