# Advanced Features

## Table of Contents
- [Paste Cleanup and Sanitization](#paste-cleanup-and-sanitization)
- [Undo and Redo Functionality](#undo-and-redo-functionality)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Read-Only Mode](#read-only-mode)
- [XSS Protection and HTML Sanitization](#xss-protection-and-html-sanitization)
- [RTL (Right-to-Left) Support](#rtl-right-to-left-support)
- [Internationalization and Localization](#internationalization-and-localization)

## Paste Cleanup and Sanitization

### Paste Events

The BlockEditor provides paste event handling to clean and sanitize pasted content:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    // Listen for paste events (conceptual - actual implementation depends on version)
    const handlePaste = (event: ClipboardEvent) => {
        event.preventDefault();
        
        const pastedData = event.clipboardData?.getData('text/plain');
        if (pastedData) {
            console.log('Pasted content:', pastedData);
            
            // Can process and clean before inserting
            const cleanedData = sanitizeContent(pastedData);
            console.log('Cleaned content:', cleanedData);
        }
    };

    const sanitizeContent = (content: string): string => {
        // Remove script tags and dangerous attributes
        const temp = document.createElement('div');
        temp.textContent = content; // textContent prevents HTML parsing
        return temp.innerHTML;
    };

    React.useEffect(() => {
        const editor = editorRef.current?.element;
        editor?.addEventListener('paste', handlePaste);
        
        return () => {
            editor?.removeEventListener('paste', handlePaste);
        };
    }, []);

    return <BlockEditorComponent id="editor" ref={editorRef} />;
}

export default App;
```

### Configure Paste Settings

The `pasteCleanupSettings` prop accepts a `PasteCleanupSettingsModel` with four specific properties:

```tsx
import { BlockEditorComponent, PasteCleanupSettingsModel } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const pasteCleanupSettings: PasteCleanupSettingsModel = {
        // Preserve formatting when pasting
        keepFormat: false,

        // Paste as plain text, stripping all formatting
        plainText: false,

        // HTML tags to strip from pasted content
        deniedTags: ['script', 'style', 'iframe', 'object', 'embed'],

        // CSS style properties to preserve during paste
        allowedStyles: ['font-size', 'color', 'font-weight', 'font-style', 'text-decoration']
    };

    return (
        <BlockEditorComponent
            id="editor"
            pasteCleanupSettings={pasteCleanupSettings}
        />
    );
}

export default App;
```

### `PasteCleanupSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `keepFormat` | `boolean` | Whether to preserve formatting when pasting |
| `plainText` | `boolean` | When `true`, pastes as plain text stripping all formatting |
| `deniedTags` | `string[]` | HTML tags removed from pasted content (e.g., `['script', 'style']`) |
| `allowedStyles` | `string[]` | CSS style properties preserved during paste (e.g., `['font-size', 'color']`) |

> ⚠️ The correct properties are `deniedTags` and `allowedStyles` — **not** `deniedElements`, `allowedElements`, or `allowedAttributes`.

### Paste Events

```tsx
import {
    BlockEditorComponent,
    BeforePasteCleanupEventArgs,
    AfterPasteCleanupEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const handleBeforePasteCleanup = (args: BeforePasteCleanupEventArgs) => {
        console.log('Content before cleanup:', args.content);
        // args.cancel = true to skip cleanup entirely
    };

    const handleAfterPasteCleanup = (args: AfterPasteCleanupEventArgs) => {
        console.log('Content after cleanup:', args.content);
    };

    return (
        <BlockEditorComponent
            id="editor"
            beforePasteCleanup={handleBeforePasteCleanup}
            afterPasteCleanup={handleAfterPasteCleanup}
            pasteCleanupSettings={{ keepFormat: false, plainText: false }}
        />
    );
}

export default App;
```

#### `BeforePasteCleanupEventArgs`

| Property | Type | Description |
|---|---|---|
| `content` | `string` | The pasted content before cleanup |
| `cancel` | `boolean` | Set `true` to cancel the paste cleanup |

#### `AfterPasteCleanupEventArgs`

| Property | Type | Description |
|---|---|---|
| `content` | `string` | The pasted content after cleanup has been applied |

## Undo and Redo Functionality

### Configure Undo/Redo Stack Size

Use `undoRedoStack` to control how many undo steps are maintained:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        // Default is 30; increase for longer history, decrease to save memory
        <BlockEditorComponent
            id="editor"
            undoRedoStack={50}
        />
    );
}

export default App;
```

### Default Undo/Redo

Undo and Redo are enabled by default. Users can use:
- **Keyboard**: Ctrl+Z (undo), Ctrl+Y (redo)
- **Context menu**: Right-click → Undo / Redo

### Programmatic Undo/Redo

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const undo = () => {
        // Most Syncfusion components track undo/redo internally
        editorRef.current?.focusIn();
        document.execCommand('undo');
    };

    const redo = () => {
        editorRef.current?.focusIn();
        document.execCommand('redo');
    };

    return (
        <div>
            <div style={{ marginBottom: '10px' }}>
                <button onClick={undo}>↶ Undo</button>
                <button onClick={redo}>↷ Redo</button>
            </div>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}

export default App;
```

### Undo/Redo Limitations

The number of undo steps is typically limited (e.g., last 100 actions). This prevents excessive memory usage on long editing sessions.

## Keyboard Shortcuts

### Default Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+B / Cmd+B | Bold |
| Ctrl+I / Cmd+I | Italic |
| Ctrl+U / Cmd+U | Underline |
| Ctrl+Z / Cmd+Z | Undo |
| Ctrl+Y / Cmd+Y | Redo |
| Ctrl+A / Cmd+A | Select All |
| / | Open slash command menu |
| Shift+Enter | Soft line break |
| Backspace | Delete block (on empty line) |
| Tab | Indent block |
| Shift+Tab | Outdent block |

### Customize Keyboard Shortcuts

Use the `keyConfig` prop — a plain key-value object where keys are action identifiers and values are shortcut strings. There is no `KeyboardSettingsModel` type in the BlockEditor API.

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="editor"
            keyConfig={{
                bold: 'ctrl+b',
                italic: 'ctrl+i',
                underline: 'ctrl+u',
                undo: 'ctrl+z',
                redo: 'ctrl+y'
            }}
        />
    );
}

export default App;
```

**`keyConfig` type:** `{ [key: string]: string }` — keys are action names, values are shortcut combinations.

> ⚠️ There is no `KeyboardSettingsModel` in the BlockEditor API. Use `keyConfig` directly as shown above.

### Handle Custom Keyboard Events

```tsx
function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const handleKeyDown = (event: KeyboardEvent) => {
        // Ctrl+S: Save
        if (event.ctrlKey && event.key === 's') {
            event.preventDefault();
            console.log('Saving content...');
            const content = editorRef.current?.getDataAsJson();
            // Save to server or local storage
        }
        
        // Ctrl+P: Print
        if (event.ctrlKey && event.key === 'p') {
            event.preventDefault();
            editorRef.current?.print();
        }
    };

    React.useEffect(() => {
        const editor = editorRef.current?.element;
        editor?.addEventListener('keydown', handleKeyDown);
        
        return () => {
            editor?.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    return <BlockEditorComponent id="editor" ref={editorRef} />;
}
```

## Read-Only Mode

### Enable Read-Only Mode

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const [isReadOnly, setIsReadOnly] = React.useState(true);

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [{
                contentType: ContentType.Text,
                content: 'This content is in read-only mode'
            }]
        }
    ];

    const toggleReadOnly = () => {
        setIsReadOnly(!isReadOnly);
    };

    return (
        <div>
            <button onClick={toggleReadOnly}>
                {isReadOnly ? 'Enable Editing' : 'Disable Editing'}
            </button>
            <BlockEditorComponent
                id="editor"
                blocks={blocks}
                readonly={isReadOnly}
            />
        </div>
    );
}

export default App;
```

### Read-Only Effects

When read-only is enabled:
- ✓ Content is visible and selectable
- ✓ Links are clickable
- ✗ No editing allowed
- ✗ Toolbars hidden
- ✗ Menus disabled
- ✗ Drag-drop disabled
- ✗ Context menu hidden (copy/link options may still work)

### Partial Read-Only (Specific Blocks)

```tsx
const blocksWithPermissions: BlockModel[] = [
    {
        id: 'editable-1',
        blockType: 'Paragraph',
        properties: { readonly: false },
        content: [{ contentType: ContentType.Text, content: 'Editable block' }]
    },
    {
        id: 'readonly-1',
        blockType: 'Paragraph',
        properties: { readonly: true },
        content: [{ contentType: ContentType.Text, content: 'Read-only block' }]
    }
];
```

## XSS Protection and HTML Sanitization

### Built-in XSS Protection

The BlockEditor provides automatic protection against XSS attacks through content sanitization.

### Safe HTML Parsing

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const importUnsafeHtml = (htmlString: string) => {
        // The component sanitizes automatically
        const sanitized = sanitizeHtml(htmlString);
        const blocks = editorRef.current?.parseHtmlToBlocks(sanitized);
        console.log('Imported blocks:', blocks);
    };

    // Manual sanitization helper
    const sanitizeHtml = (html: string): string => {
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        // Remove script tags and event handlers
        const scripts = temp.querySelectorAll('script');
        scripts.forEach(script => script.remove());
        
        // Remove event attributes
        temp.querySelectorAll('*').forEach(el => {
            Array.from(el.attributes).forEach(attr => {
                if (attr.name.startsWith('on')) {
                    el.removeAttribute(attr.name);
                }
            });
        });
        
        return temp.innerHTML;
    };

    const dangerousHtml = `
        <p>Safe content</p>
        <script>alert('XSS')</script>
        <img src="x" onerror="alert('XSS')" />
    `;

    return (
        <div>
            <button onClick={() => importUnsafeHtml(dangerousHtml)}>
                Import Potentially Unsafe HTML
            </button>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}

export default App;
```

### Custom HTML Sanitizer

```tsx
import DOMPurify from 'dompurify';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const importWithDOMPurify = (htmlString: string) => {
        // Use DOMPurify library for advanced sanitization
        const sanitized = DOMPurify.sanitize(htmlString, {
            ALLOWED_TAGS: [
                'p', 'div', 'span', 'strong', 'em', 'u', 'br',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'a', 'img', 'table', 'tr', 'td', 'th'
            ],
            ALLOWED_ATTR: ['href', 'src', 'alt', 'title']
        });
        
        const blocks = editorRef.current?.parseHtmlToBlocks(sanitized);
        console.log('Safe blocks:', blocks);
    };

    return (
        <BlockEditorComponent id="editor" ref={editorRef} />
    );
}
```

## RTL (Right-to-Left) Support

### Enable RTL Mode

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const [isRtl, setIsRtl] = React.useState(false);

    return (
        <div dir={isRtl ? 'rtl' : 'ltr'}>
            <button onClick={() => setIsRtl(!isRtl)}>
                Toggle RTL
            </button>
            <BlockEditorComponent
                id="editor"
                enableRtl={isRtl}
            />
        </div>
    );
}

export default App;
```

### RTL CSS

```css
/* RTL-specific styles */
[dir="rtl"] .e-block-editor {
    text-align: right;
    direction: rtl;
}

[dir="rtl"] .e-block-handle {
    right: 0;
    left: auto;
}

[dir="rtl"] .e-toolbar {
    flex-direction: row-reverse;
}
```

## Internationalization and Localization

### Set Locale

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import { setCulture } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
    React.useEffect(() => {
        // Set locale (e.g., 'de', 'fr', 'es', 'ar', 'zh')
        setCulture('de'); // German
    }, []);

    return <BlockEditorComponent id="editor" locale="de" />;
}

export default App;
```

### Supported Locales

Common locale codes:
- `'en'` - English
- `'de'` - German
- `'fr'` - French
- `'es'` - Spanish
- `'pt'` - Portuguese
- `'ar'` - Arabic
- `'zh'` - Chinese (Simplified)
- `'ja'` - Japanese
- `'ko'` - Korean
- `'ru'` - Russian

### Custom Translations

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import { L10n } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
    React.useEffect(() => {
        // Define custom translations
        L10n.load({
            'de': {
                'blockeditor': {
                    'insertParagraph': 'Absatz einfügen',
                    'insertHeading': 'Überschrift einfügen',
                    'insertBulletList': 'Aufzählung einfügen'
                }
            }
        });
    }, []);

    return <BlockEditorComponent id="editor" locale="de" />;
}

export default App;
```

### Date and Number Formatting

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import { Internationalization } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
    const intl = new Internationalization('de-DE');

    const formatDate = (date: Date) => {
        return intl.formatDate(date, { type: 'date', format: 'long' });
    };

    const formatNumber = (num: number) => {
        return intl.formatNumber(num, { useGrouping: true });
    };

    return (
        <div>
            <p>Formatted date: {formatDate(new Date())}</p>
            <p>Formatted number: {formatNumber(1000.5)}</p>
            <BlockEditorComponent id="editor" locale="de" />
        </div>
    );
}

export default App;
```

## Content Change and Focus Events

### `blockChanged` Event

Fires whenever blocks are added, deleted, moved, or updated. This is the primary event for tracking content changes.

```tsx
import {
    BlockEditorComponent,
    BlockChangedEventArgs,
    BlockAction
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const handleBlockChanged = (args: BlockChangedEventArgs) => {
        args.changes.forEach(change => {
            console.log('Action:', change.action); // 'Insertion' | 'Deletion' | 'Moved' | 'Update'
            console.log('Block:', change.data.block);
            console.log('Previous block:', change.data.prevBlock);
            console.log('Current parent:', change.data.currentParent);
            console.log('Previous parent:', change.data.prevParent);
        });
    };

    return (
        <BlockEditorComponent
            id="editor"
            blockChanged={handleBlockChanged}
        />
    );
}

export default App;
```

#### `BlockChangedEventArgs`

| Property | Type | Description |
|---|---|---|
| `changes` | `BlockChange[]` | Array of change operations |

#### `BlockChange`

| Property | Type | Description |
|---|---|---|
| `action` | `BlockAction` | Type of action performed |
| `data` | `BlockData` | Data associated with the change |

#### `BlockAction` (Enum)

| Member | Description |
|---|---|
| `Insertion` | A new block was inserted |
| `Deletion` | A block was deleted |
| `Moved` | A block was moved |
| `Update` | A block was updated |

#### `BlockData`

| Property | Type | Description |
|---|---|---|
| `block` | `BlockModel` | The current block after the change |
| `prevBlock` | `BlockModel` | The block before the change |
| `currentParent` | `BlockModel` | Current parent block (for nested blocks) |
| `prevParent` | `BlockModel` | Previous parent block (if parent changed) |

---

### `focus` and `blur` Events

```tsx
import {
    BlockEditorComponent,
    FocusEventArgs,
    BlurEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const handleFocus = (args: FocusEventArgs) => {
        console.log('Editor focused on block:', args.blockId);
        console.log('Native event:', args.event);
    };

    const handleBlur = (args: BlurEventArgs) => {
        console.log('Editor lost focus from block:', args.blockId);
        console.log('Native event:', args.event);
    };

    return (
        <BlockEditorComponent
            id="editor"
            focus={handleFocus}
            blur={handleBlur}
        />
    );
}

export default App;
```

#### `FocusEventArgs`

| Property | Type | Description |
|---|---|---|
| `blockId` | `string` | ID of the block that received focus |
| `event` | `Event` | Native focus event |

#### `BlurEventArgs`

| Property | Type | Description |
|---|---|---|
| `blockId` | `string` | ID of the block that lost focus |
| `event` | `Event` | Native blur event |

---

### `selectionChanged` Event

Fires when the user's text selection within a block changes.

```tsx
import { BlockEditorComponent, SelectionChangedEventArgs } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const handleSelectionChanged = (args: SelectionChangedEventArgs) => {
        console.log('Selection changed', args.event);
    };

    return (
        <BlockEditorComponent
            id="editor"
            selectionChanged={handleSelectionChanged}
        />
    );
}

export default App;
```

#### `SelectionChangedEventArgs`

| Property | Type | Description |
|---|---|---|
| `event` | `Event` | Native browser event that triggered the selection change |

---

### `created` Event

Fires once when the BlockEditor component has fully initialized.

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const handleCreated = () => {
        console.log('BlockEditor is ready');
    };

    return (
        <BlockEditorComponent
            id="editor"
            created={handleCreated}
        />
    );
}

export default App;
```

---

## File Upload Events

The BlockEditor fires these events during image block uploads:

```tsx
import {
    BlockEditorComponent,
    BeforeUploadEventArgs,
    UploadingEventArgs,
    FileUploadSuccessEventArgs,
    FailureEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="editor"
            imageBlockSettings={{ saveUrl: '/api/upload', allowedTypes: ['.jpg', '.png', '.gif'] }}

            beforeFileUpload={(args: BeforeUploadEventArgs) => {
                console.log('Before upload:', args);
                // args.cancel = true to abort the upload
            }}

            fileUploading={(args: UploadingEventArgs) => {
                console.log('Uploading...', args);
            }}

            fileUploadSuccess={(args: FileUploadSuccessEventArgs) => {
                console.log('Upload succeeded. File URL:', args.fileUrl);
                console.log('File info:', args.file);
                console.log('Status:', args.statusText);
            }}

            fileUploadFailed={(args: FailureEventArgs) => {
                console.log('Upload failed:', args);
            }}
        />
    );
}

export default App;
```

#### `FileUploadSuccessEventArgs`

| Property | Type | Description |
|---|---|---|
| `file` | `FileInfo` | Details about the uploaded file |
| `fileUrl` | `string` | URL of the uploaded file on the server |
| `statusText` | `string` | Upload status description |
| `response` | `ResponseEventArgs` | Server response |
| `operation` | `string` | Upload operation type |
| `chunkIndex` | `number` | Chunk index (for chunked uploads) |
| `chunkSize` | `number` | Size of the upload chunk |
| `totalChunk` | `number` | Total number of chunks |
| `e` | `object` | Original event arguments |

---

## Complete Advanced Example

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import { setCulture } from '@syncfusion/ej2-base';
import * as React from 'react';

function AdvancedEditor() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [isReadOnly, setIsReadOnly] = React.useState(false);
    const [locale, setLocale] = React.useState('en');

    React.useEffect(() => {
        setCulture(locale);
    }, [locale]);

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [{
                contentType: ContentType.Text,
                content: 'Advanced BlockEditor with internationalization, RTL, and security features'
            }]
        }
    ];

    const exportSecurely = () => {
        const json = editorRef.current?.getDataAsJson();
        console.log('Exported safely:', json);
    };

    return (
        <div>
            <div style={{ marginBottom: '20px' }}>
                <button onClick={() => setIsReadOnly(!isReadOnly)}>
                    {isReadOnly ? 'Edit' : 'Read-Only'}
                </button>
                
                <select value={locale} onChange={(e) => setLocale(e.target.value)}>
                    <option value="en">English</option>
                    <option value="de">Deutsch</option>
                    <option value="fr">Français</option>
                    <option value="ar">العربية</option>
                </select>
                
                <button onClick={exportSecurely}>Export</button>
            </div>
            
            <BlockEditorComponent
                id="editor"
                ref={editorRef}
                blocks={blocks}
                readOnly={isReadOnly}
                locale={locale}
                enableRtl={locale === 'ar'}
                undoRedoStack={50}
                keyConfig={{ bold: 'ctrl+b', italic: 'ctrl+i', underline: 'ctrl+u' }}
                pasteCleanupSettings={{ keepFormat: false, plainText: false, deniedTags: ['script', 'style'] }}
            />
        </div>
    );
}

export default AdvancedEditor;
```
