# Accessibility Features

## Table of Contents
- [WCAG 2.1 Compliance](#wcag-21-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [ARIA Attributes](#aria-attributes)
- [Focus Management](#focus-management)
- [Color Contrast and Visual Indicators](#color-contrast-and-visual-indicators)
- [Testing for Accessibility](#testing-for-accessibility)

## WCAG 2.1 Compliance

The BlockEditor is designed to meet WCAG 2.1 accessibility standards at the **AA level** for most features and **AAA level** for critical interactions.

### WCAG 2.1 Principles

**1. Perceivable** - Content must be perceivable to all users
- ✓ Text alternatives for images
- ✓ Color not sole means of conveying information
- ✓ Sufficient color contrast ratios
- ✓ Readable font sizes and line spacing

**2. Operable** - Users must be able to navigate and control
- ✓ Full keyboard accessibility
- ✓ No keyboard traps
- ✓ Focus indicators always visible
- ✓ No content with seizure triggers

**3. Understandable** - Information must be clear
- ✓ Language marked in code
- ✓ Consistent navigation
- ✓ Clear labels and instructions
- ✓ Predictable interactions

**4. Robust** - Content must work with assistive technologies
- ✓ Valid HTML/ARIA
- ✓ Semantic markup
- ✓ Proper roles and attributes
- ✓ Screen reader compatible

### Compliance Checklist

```tsx
// BlockEditor with accessibility best practices
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function AccessibleBlockEditor() {
    return (
        <div>
            {/* Descriptive heading */}
            <h1>Document Editor</h1>
            
            {/* Usage instructions */}
            <p id="editor-instructions">
                Use "/" for commands, Tab to navigate, Enter to edit blocks, 
                and arrow keys to move between blocks.
            </p>
            
            {/* Accessible editor */}
            <BlockEditorComponent
                id="editor"
                aria-label="Block-based document editor"
                aria-describedby="editor-instructions"
                blocks={[]}
            />
        </div>
    );
}

export default AccessibleBlockEditor;
```

## Keyboard Navigation

### Essential Keyboard Shortcuts

| Key | Action | Purpose |
|-----|--------|---------|
| Tab | Focus next element | Navigate forward |
| Shift+Tab | Focus previous element | Navigate backward |
| Enter | Edit/Select block | Activate focused item |
| / | Open command menu | Quick access to commands |
| Escape | Close menu/Cancel | Exit current context |
| Arrow Up | Previous block | Navigate between blocks |
| Arrow Down | Next block | Navigate between blocks |
| Arrow Left | Start of line/Previous char | Text cursor control |
| Arrow Right | End of line/Next char | Text cursor control |
| Ctrl+A | Select all | Select all blocks |
| Ctrl+Z | Undo | Reverse last action |
| Ctrl+Y | Redo | Redo last undone action |
| Ctrl+B | Bold | Toggle bold formatting |
| Ctrl+I | Italic | Toggle italic formatting |
| Ctrl+U | Underline | Toggle underline |
| Ctrl+K | Insert link | Link insertion |
| Backspace | Delete/Outdent | Delete or decrease indent |
| Delete | Delete content | Remove block content |

### Keyboard Navigation Example

```tsx
function KeyboardNavigationDemo() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    // Custom keyboard handler
    const handleKeyDown = (event: KeyboardEvent) => {
        // Cmd/Ctrl + S: Save
        if ((event.metaKey || event.ctrlKey) && event.key === 's') {
            event.preventDefault();
            console.log('Save with keyboard shortcut');
        }

        // Alt + H: Focus heading
        if (event.altKey && event.key === 'h') {
            event.preventDefault();
            editorRef.current?.focusIn();
        }

        // Alt + L: Focus list
        if (event.altKey && event.key === 'l') {
            event.preventDefault();
            console.log('Navigate to list block');
        }
    };

    React.useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    return <BlockEditorComponent id="editor" ref={editorRef} />;
}
```

### No Keyboard Traps

The BlockEditor ensures no keyboard traps where users get stuck unable to navigate away:

```tsx
// Proper focus management prevents traps
<BlockEditorComponent
    id="editor"
    showBlockHandle={true}  // Draggable but not a trap
    enableKeyboardInteraction={true}  // Full keyboard support
/>
```

## Screen Reader Support

### Semantic HTML

The BlockEditor generates semantic HTML that screen readers can interpret:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function ScreenReaderAccessible() {
    const blocks = [
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: 'Text', content: 'Main Title' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [{ contentType: 'Text', content: 'Introductory paragraph' }]
        },
        {
            id: 'block-3',
            blockType: 'BulletList',
            content: [{ contentType: 'Text', content: 'List item' }]
        }
    ];

    return (
        <>
            <h1>Document with Screen Reader Support</h1>
            <BlockEditorComponent
                id="editor"
                blocks={blocks}
                aria-label="Accessible block editor"
                role="main"
            />
        </>
    );
}
```

### Testing with Screen Readers

Supported screen readers:
- **NVDA** (Windows) - Free, open-source
- **JAWS** (Windows) - Commercial
- **VoiceOver** (macOS/iOS) - Built-in
- **Narrator** (Windows 10+) - Built-in
- **TalkBack** (Android) - Built-in

## ARIA Attributes

### Essential ARIA Attributes

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function AccessibleEditor() {
    return (
        <div>
            {/* Main editor container */}
            <BlockEditorComponent
                id="editor"
                role="main"
                aria-label="Document editor"
                aria-describedby="help-text"
                aria-live="polite"  // Announce changes
            />
            
            {/* Help text for screen readers */}
            <div id="help-text" className="sr-only">
                This is a block-based document editor. Press "/" to see available commands.
                Use Tab to navigate between blocks.
            </div>

            {/* Status region for dynamic updates */}
            <div
                aria-live="assertive"
                aria-atomic="true"
                className="sr-only"
                id="status-region"
            >
                {/* Editor status updates announced here */}
            </div>
        </div>
    );
}

export default AccessibleEditor;
```

### Block-Level ARIA

```tsx
import { BlockModel } from '@syncfusion/ej2-react-blockeditor';

const accessibleBlocks: BlockModel[] = [
    {
        id: 'heading-1',
        blockType: 'Heading',
        properties: {
            level: 1,
            'aria-level': '1'
        },
        content: [{ contentType: 'Text', content: 'Section Title' }]
    },
    {
        id: 'list-1',
        blockType: 'BulletList',
        content: [{ contentType: 'Text', content: 'Item 1' }],
        properties: {
            role: 'list',
            'aria-label': 'Key points'
        }
    }
];
```

### ARIA Live Regions

```tsx
// Announce changes to screen reader users
<div aria-live="polite" aria-atomic="true">
    Block added successfully
</div>

<div aria-live="assertive" aria-atomic="true">
    Warning: Unsaved changes!
</div>
```

## Focus Management

### Visible Focus Indicators

```css
/* Ensure focus is always visible */
.e-block-editor:focus,
.e-block-editor *:focus {
    outline: 2px solid #4A90E2;
    outline-offset: 2px;
}

/* Keyboard focus vs mouse click */
.e-block-editor:focus-visible {
    outline: 3px solid #4A90E2;
}

/* High contrast mode support */
@media (prefers-contrast: more) {
    .e-block-editor:focus {
        outline: 3px solid;
        outline-offset: 3px;
    }
}
```

### Programmatic Focus Control

```tsx
function FocusManagement() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const setFocusToEditor = () => {
        editorRef.current?.focusIn();
    };

    const setFocusToBlock = (blockId: string) => {
        editorRef.current?.setCursorPosition(blockId, 0);
        editorRef.current?.focusIn();
    };

    const trapFocusInEditor = () => {
        // Prevent focus from leaving editor
        editorRef.current?.focusIn();
    };

    return (
        <div>
            <button onClick={setFocusToEditor}>Focus Editor</button>
            <button onClick={() => setFocusToBlock('block-1')}>Focus First Block</button>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}
```

### Focus Order

```tsx
// Maintain logical focus order
<div>
    <button tabIndex={0}>Save</button>  {/* First */}
    <button tabIndex={0}>Undo</button>  {/* Second */}
    <BlockEditorComponent 
        id="editor" 
        tabIndex={0}  {/* Third - editor content */}
    />
    <button tabIndex={0}>Export</button>  {/* Fourth */}
</div>
```

## Color Contrast and Visual Indicators

### WCAG Contrast Requirements

**Text contrast:**
- Normal text: 4.5:1 (AA) / 7:1 (AAA)
- Large text (18pt+): 3:1 (AA) / 4.5:1 (AAA)

### High Contrast Styles

```css
/* Default high contrast support */
.e-block-editor {
    color: #000000;
    background-color: #ffffff;
}

/* Ensure sufficient contrast */
.e-toolbar button {
    color: #000000;
    background-color: #f0f0f0;
    border: 1px solid #333333;
    min-contrast-ratio: 4.5;
}

/* Focus indicators with strong contrast */
.e-block-editor:focus {
    outline: 3px solid #000000;
}

/* Support forced colors mode */
@media (forced-colors: active) {
    .e-block-editor {
        border: 1px solid CanvasText;
        color: CanvasText;
        background-color: Canvas;
    }
    
    .e-block-editor:focus {
        outline: 3px solid Highlight;
    }
}
```

### Visual Indicators Beyond Color

```css
/* Don't rely on color alone */
.block-success {
    /* Use both color AND icon/symbol */
    background: linear-gradient(
        90deg,
        #4caf50 0%,
        #4caf50 4px,
        #e8f5e9 4px
    );
    padding-left: 12px;
}

.block-success::before {
    content: '✓';  /* Symbol in addition to color */
    margin-right: 5px;
    font-weight: bold;
}

.block-error {
    background: linear-gradient(
        90deg,
        #f44336 0%,
        #f44336 4px,
        #ffebee 4px
    );
    padding-left: 12px;
}

.block-error::before {
    content: '⚠';  /* Symbol */
    margin-right: 5px;
}
```

## Testing for Accessibility

### Automated Testing

```tsx
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('BlockEditor should not have accessibility violations', async () => {
    const { container } = render(<BlockEditorComponent id="editor" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

```
□ Keyboard navigation works for all features
□ Tab order is logical
□ Focus indicators are visible
□ Screen reader announces all content
□ Color contrast meets WCAG AA (4.5:1 for normal text)
□ No keyboard traps
□ All interactive elements are labeled
□ Error messages are announced
□ Form inputs have associated labels
□ Images have alt text
□ Focus management is appropriate
□ No auto-playing content
□ Motion/animation can be disabled
```

### Screen Reader Testing

```tsx
// Test with screen reader
function ScreenReaderTest() {
    const blocks = [
        {
            id: 'test-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: 'Text', content: 'Test Heading' }]
        },
        {
            id: 'test-2',
            blockType: 'Paragraph',
            content: [{ contentType: 'Text', content: 'Test paragraph content' }]
        }
    ];

    return (
        <BlockEditorComponent
            id="editor"
            blocks={blocks}
            // Enable screen reader features
            aria-label="Screen reader test editor"
            aria-live="polite"
        />
    );
}
```

## Complete Accessible Example

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function FullyAccessibleEditor() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [status, setStatus] = React.useState('');

    const blocks: BlockModel[] = [
        {
            id: 'title',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{
                contentType: ContentType.Text,
                content: 'Accessible Document Editor'
            }]
        },
        {
            id: 'intro',
            blockType: 'Paragraph',
            content: [{
                contentType: ContentType.Text,
                content: 'This editor is fully accessible using keyboard and screen readers.'
            }]
        }
    ];

    const save = () => {
        setStatus('Document saved');
        setTimeout(() => setStatus(''), 3000);
    };

    return (
        <div>
            {/* Main content */}
            <header>
                <h1>Document Editor</h1>
                <p id="instructions">
                    Press "/" to insert blocks, Tab to navigate, Ctrl+S to save.
                </p>
            </header>

            {/* Toolbar with accessible buttons */}
            <nav aria-label="Editor controls">
                <button onClick={save} aria-label="Save document">
                    Save
                </button>
                <button 
                    onClick={() => editorRef.current?.focusIn()}
                    aria-label="Focus on editor"
                >
                    Edit
                </button>
            </nav>

            {/* Main editor */}
            <BlockEditorComponent
                id="editor"
                ref={editorRef}
                blocks={blocks}
                role="main"
                aria-label="Block-based document editor"
                aria-describedby="instructions"
                aria-live="polite"
            />

            {/* Status announcements */}
            <div
                aria-live="assertive"
                aria-atomic="true"
                role="status"
                className="sr-only"
            >
                {status}
            </div>
        </div>
    );
}

export default FullyAccessibleEditor;
```

## Accessibility Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [NVDA Screen Reader](https://www.nvaccess.org/)
- [Axe DevTools](https://www.deque.com/axe/devtools/)
