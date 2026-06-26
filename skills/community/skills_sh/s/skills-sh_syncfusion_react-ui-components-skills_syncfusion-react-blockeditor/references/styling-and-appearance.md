# Styling and Appearance

## Table of Contents
- [CSS Theming](#css-theming)
- [Available Themes](#available-themes)
- [Block Styling](#block-styling)
- [Typography Options](#typography-options)
- [Indentation and Nesting](#indentation-and-nesting)
- [Placeholder Customization](#placeholder-customization)
- [Dark Mode Support](#dark-mode-support)
- [Custom Styling Examples](#custom-styling-examples)

## CSS Theming

The BlockEditor uses Syncfusion's centralized theme system. Import theme CSS files to style the component.

### Basic Theme Import

```css
/* Material theme */
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-blockeditor/styles/material.css";
```

### Theme Import in React Component

```tsx
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-splitbuttons/styles/material.css';
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-dropdowns/styles/material.css';
import '@syncfusion/ej2-react-blockeditor/styles/material.css';

import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';

function App() {
    return <BlockEditorComponent id="editor" />;
}
```

## Available Themes

Syncfusion provides multiple built-in themes. Replace the theme name in imports:

### Theme Options

| Theme | Import Path | Best For |
|-------|-------------|----------|
| Material | `material.css` | Google Material Design |
| Bootstrap 5 | `bootstrap5.css` | Bootstrap ecosystem |
| Fluent | `fluent.css` | Microsoft Fluent Design |
| Tailwind | `tailwind3.css` | Tailwind CSS projects |
| Material Dark | `material-dark.css` | Dark mode Material |
| Bootstrap Dark | `bootstrap5-dark.css` | Dark mode Bootstrap |
| Tailwind Dark | `tailwind3-dark.css` | Dark mode Tailwind |

### Switching Themes

```tsx
// Theme selector component
function ThemeSwitcher() {
    const [theme, setTheme] = React.useState('material');

    const handleThemeChange = (newTheme: string) => {
        setTheme(newTheme);
        // Dynamically update theme imports
        document.documentElement.dataset.theme = newTheme;
    };

    return (
        <div>
            <select onChange={(e) => handleThemeChange(e.target.value)}>
                <option value="material">Material</option>
                <option value="bootstrap5">Bootstrap 5</option>
                <option value="fluent">Fluent</option>
                <option value="tailwind3">Tailwind</option>
            </select>
        </div>
    );
}
```

## Block Styling

### CSS Class Property

Apply custom CSS classes to blocks using the `cssClass` property:

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            cssClass: 'default-block',
            content: [{
                contentType: ContentType.Text,
                content: 'Default styling'
            }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            cssClass: 'highlight-block important',
            content: [{
                contentType: ContentType.Text,
                content: 'Highlighted and important'
            }]
        },
        {
            id: 'block-3',
            blockType: 'Paragraph',
            cssClass: 'warning-block',
            content: [{
                contentType: ContentType.Text,
                content: 'Warning message'
            }]
        }
    ];

    return (
        <div>
            <style>{`
                .highlight-block {
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 10px 15px;
                }
                
                .important {
                    font-weight: bold;
                    color: #cc0000;
                }
                
                .warning-block {
                    background-color: #f8d7da;
                    border-left: 4px solid #f5c6cb;
                    color: #721c24;
                    padding: 10px 15px;
                }
                
                .default-block {
                    padding: 8px 0;
                }
            `}</style>
            <BlockEditorComponent id="editor" blocks={blocks} />
        </div>
    );
}

export default App;
```

### Block Type-Specific Styling

```css
/* Style all paragraph blocks */
.e-block[data-block-type="Paragraph"] {
    line-height: 1.6;
    color: #333;
}

/* Style heading blocks */
.e-block[data-block-type="Heading"] {
    margin-top: 20px;
    margin-bottom: 10px;
    color: #1a1a1a;
}

/* Style list items */
.e-block[data-block-type="BulletList"],
.e-block[data-block-type="NumberedList"] {
    margin-left: 20px;
}

/* Style code blocks */
.e-block[data-block-type="Code"] {
    background-color: #f5f5f5;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    padding: 10px;
}

/* Style table blocks */
.e-block[data-block-type="Table"] {
    margin: 10px 0;
}
```

## Typography Options

### Text Formatting

The BlockEditor supports inline formatting through the toolbar:

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [{
                contentType: ContentType.Text,
                content: 'Select text and use the toolbar to: Bold, Italic, Underline'
            }]
        }
    ];

    return <BlockEditorComponent id="editor" blocks={blocks} />;
}
```

### Custom Font Styling

```css
/* Apply custom fonts */
.e-block-editor {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    line-height: 1.5;
}

/* Heading styles */
.e-block[data-block-type="Heading"] h1 {
    font-size: 2.5rem;
    font-weight: 700;
}

.e-block[data-block-type="Heading"] h2 {
    font-size: 2rem;
    font-weight: 700;
}

.e-block[data-block-type="Heading"] h3 {
    font-size: 1.5rem;
    font-weight: 600;
}

.e-block[data-block-type="Heading"] h4 {
    font-size: 1.25rem;
    font-weight: 600;
}

/* Quote styling */
.e-block[data-block-type="Quote"] {
    border-left: 4px solid #ccc;
    padding-left: 15px;
    color: #666;
    font-style: italic;
    margin-left: 0;
}

/* Code block styling */
.e-block[data-block-type="Code"] code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 14px;
    line-height: 1.4;
}
```

## Indentation and Nesting

### Indentation Styling

```tsx
const indentedBlocks: BlockModel[] = [
    {
        id: 'level-0',
        blockType: 'BulletList',
        indent: 0,
        content: [{
            contentType: ContentType.Text,
            content: 'Level 0 - Main item'
        }]
    },
    {
        id: 'level-1',
        blockType: 'BulletList',
        indent: 1,
        content: [{
            contentType: ContentType.Text,
            content: 'Level 1 - Nested item'
        }]
    },
    {
        id: 'level-2',
        blockType: 'BulletList',
        indent: 2,
        content: [{
            contentType: ContentType.Text,
            content: 'Level 2 - Deeper nesting'
        }]
    }
];
```

### Nested Block Styling

```css
/* Indent based on nesting level */
.e-block {
    margin-left: 0;
}

.e-block[data-indent="1"] {
    margin-left: 20px;
}

.e-block[data-indent="2"] {
    margin-left: 40px;
}

.e-block[data-indent="3"] {
    margin-left: 60px;
}

/* Nested content styling */
.e-block-children {
    margin-top: 5px;
    margin-bottom: 5px;
}
```

## Placeholder Customization

### Empty Block Placeholders

```tsx
import { BlockEditorComponent, BlockModel } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            properties: {
                placeholder: 'Start typing your content here...'
            },
            content: []
        }
    ];

    return <BlockEditorComponent id="editor" blocks={blocks} />;
}
```

### Placeholder Styling

```css
/* Global placeholder styling */
.e-block-editor [data-placeholder]::before {
    content: attr(data-placeholder);
    color: #999;
    font-style: italic;
    pointer-events: none;
}

/* Heading placeholder */
.e-block[data-block-type="Heading"][data-placeholder]::before {
    color: #ccc;
    font-size: 1.5rem;
}

/* Code block placeholder */
.e-block[data-block-type="Code"][data-placeholder]::before {
    color: #bbb;
    font-family: 'Courier New', monospace;
}
```

## Dark Mode Support

### Dark Theme Import

```tsx
import '@syncfusion/ej2-base/styles/material-dark.css';
import '@syncfusion/ej2-inputs/styles/material-dark.css';
import '@syncfusion/ej2-popups/styles/material-dark.css';
import '@syncfusion/ej2-buttons/styles/material-dark.css';
import '@syncfusion/ej2-splitbuttons/styles/material-dark.css';
import '@syncfusion/ej2-navigations/styles/material-dark.css';
import '@syncfusion/ej2-dropdowns/styles/material-dark.css';
import '@syncfusion/ej2-react-blockeditor/styles/material-dark.css';

import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';

function App() {
    return <BlockEditorComponent id="editor" />;
}
```

### System Dark Mode Support

```tsx
function AppWithDarkMode() {
    const [isDark, setIsDark] = React.useState(false);

    React.useEffect(() => {
        // Detect system dark mode preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setIsDark(prefersDark);
        
        // Update document class
        if (prefersDark) {
            document.documentElement.classList.add('dark-mode');
        }
    }, []);

    const toggleDarkMode = () => {
        setIsDark(!isDark);
        document.documentElement.classList.toggle('dark-mode');
    };

    return (
        <div>
            <button onClick={toggleDarkMode}>
                {isDark ? 'Light Mode' : 'Dark Mode'}
            </button>
            <BlockEditorComponent id="editor" />
        </div>
    );
}
```

### Custom Dark Mode Styles

```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #000000;
    --border-color: #cccccc;
}

.dark-mode {
    --bg-primary: #1e1e1e;
    --text-primary: #e0e0e0;
    --border-color: #444444;
}

.e-block-editor {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.e-block {
    border-color: var(--border-color);
}

.dark-mode .e-block[data-block-type="Code"] {
    background-color: #2d2d2d;
    color: #e0e0e0;
}
```

## Custom Styling Examples

### Example 1: Info/Warning/Success Blocks

```tsx
function StyledBlocksExample() {
    const blocks: BlockModel[] = [
        {
            id: 'info',
            blockType: 'Paragraph',
            cssClass: 'block-info',
            content: [{
                contentType: ContentType.Text,
                content: 'ℹ️ This is an informational message.'
            }]
        },
        {
            id: 'warning',
            blockType: 'Paragraph',
            cssClass: 'block-warning',
            content: [{
                contentType: ContentType.Text,
                content: '⚠️ This is a warning message.'
            }]
        },
        {
            id: 'success',
            blockType: 'Paragraph',
            cssClass: 'block-success',
            content: [{
                contentType: ContentType.Text,
                content: '✓ Operation completed successfully.'
            }]
        }
    ];

    return (
        <div>
            <style>{`
                .block-info {
                    background-color: #e3f2fd;
                    border-left: 4px solid #2196f3;
                    color: #1976d2;
                    padding: 12px 15px;
                    border-radius: 2px;
                }
                
                .block-warning {
                    background-color: #fff3e0;
                    border-left: 4px solid #ff9800;
                    color: #e65100;
                    padding: 12px 15px;
                    border-radius: 2px;
                }
                
                .block-success {
                    background-color: #e8f5e9;
                    border-left: 4px solid #4caf50;
                    color: #2e7d32;
                    padding: 12px 15px;
                    border-radius: 2px;
                }
            `}</style>
            <BlockEditorComponent id="editor" blocks={blocks} />
        </div>
    );
}
```

### Example 2: Responsive Styling

```css
/* Default (desktop) */
.e-block-editor {
    font-size: 16px;
    line-height: 1.6;
}

/* Tablet */
@media (max-width: 768px) {
    .e-block-editor {
        font-size: 14px;
        padding: 10px;
    }
    
    .e-block {
        margin-left: 0 !important;
    }
}

/* Mobile */
@media (max-width: 480px) {
    .e-block-editor {
        font-size: 13px;
    }
    
    .e-block-header {
        display: none;
    }
}
```

### Example 3: High Contrast Accessibility

```css
/* High contrast mode */
@media (prefers-contrast: more) {
    .e-block-editor {
        border: 2px solid #000;
    }
    
    .e-block {
        border: 1px solid #000;
        padding: 8px;
    }
    
    .block-info {
        background-color: #ffffff;
        border: 2px solid #0066cc;
        font-weight: bold;
    }
}
```
