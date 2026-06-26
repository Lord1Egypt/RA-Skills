# Getting Started with Block Editor

## Table of Contents
- [Installation](#installation)
- [Basic Implementation](#basic-implementation)
- [CSS Imports](#css-imports)
- [Creating Your First Document](#creating-your-first-document)
- [Setting Initial Content](#setting-initial-content)
- [Running the Application](#running-the-application)

## Installation

To install the Syncfusion BlockEditor component, use npm:

```bash
npm install @syncfusion/ej2-react-blockeditor --save
```

This installs the core BlockEditor package for React applications.

## Basic Implementation

### Functional Component Example

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        // Create a basic block editor component
        <BlockEditorComponent id="block-editor"></BlockEditorComponent>
    );
}

export default App;
```

### Class Component Example

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
    public render() {
        return (
            // Create a basic block editor component
            <BlockEditorComponent id="block-editor"></BlockEditorComponent>
        );
    }
}
```

Both functional and class components are supported. The `id` prop is required and serves as the unique identifier for the component instance.

## CSS Imports

The BlockEditor requires CSS styles from multiple Syncfusion packages. Import these in your main CSS file or at the component level:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-blockeditor/styles/material.css";
```

### Available Themes

Replace `material` with any of these supported theme names:
- `tailwind3` - Tailwind CSS 3 design
- `bootstrap5` - Bootstrap 5 styling
- `fluent` - Microsoft Fluent design
- `material-dark` - Material dark theme
- `bootstrap5-dark` - Bootstrap 5 dark theme

Example for Tailwind theme:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-blockeditor/styles/tailwind3.css";
```

## Creating Your First Document

Create a simple React component with the BlockEditor:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import '@syncfusion/ej2-react-blockeditor/styles/material.css';

function App() {
    return (
        <div style={{ padding: '20px' }}>
            <h1>My First Block Editor</h1>
            <BlockEditorComponent id="block-editor"></BlockEditorComponent>
        </div>
    );
}

export default App;

ReactDOM.render(<App />, document.getElementById('container'));
```

This creates an empty block editor where users can start typing or use the "/" command to insert blocks.

## Setting Initial Content

### Using Block Data

To pre-populate the editor with content, use the `blocks` property with an array of BlockModel objects:

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const initialBlocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Welcome to Block Editor'
                }
            ]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'This is a sample paragraph with initial content.'
                }
            ]
        },
        {
            id: 'block-3',
            blockType: 'BulletList',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'First list item'
                }
            ]
        },
        {
            id: 'block-4',
            blockType: 'BulletList',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Second list item'
                }
            ]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            blocks={initialBlocks}
        />
    );
}

export default App;
```

### Block Properties Explained

Each block requires:
- **blockType** - The type of content (Paragraph, Heading, BulletList, etc.)
- **content** - Array of ContentModel objects containing the text and formatting
- **id** (optional) - Unique identifier for the block
- **properties** (optional) - Type-specific settings (e.g., heading level)

### Content Type Options

The `ContentType` enum defines the four valid content types for any `ContentModel.contentType` field:

```tsx
enum ContentType {
    Text = 'Text',       // Plain or inline-formatted text
    Link = 'Link',       // Hyperlink — requires ILinkContentSettings in properties
    Mention = 'Mention', // User mention — requires IMentionContentSettings in properties
    Label = 'Label'      // Label/tag — requires ILabelContentSettings in properties
}
```

> ⚠️ `Image`, `Code`, and `Embed` are **not** valid `ContentType` values. Images and code are represented as `blockType` values (`'Image'`, `'Code'`), not as content types.

### Block Type Reference

All valid `blockType` values (from the `BlockType` enum):

| Value | Description |
|---|---|
| `'Paragraph'` | Standard text paragraph |
| `'Heading'` | Heading (configure `level: 1–4` in `properties`) |
| `'BulletList'` | Unordered bullet list |
| `'NumberedList'` | Ordered numbered list |
| `'Checklist'` | To-do list with checkboxes (use `properties.isChecked`) |
| `'Code'` | Code block with syntax highlighting (use `properties.language`) |
| `'Table'` | Data table |
| `'Quote'` | Blockquote (supports nested `properties.children`) |
| `'Callout'` | Highlighted callout box |
| `'Image'` | Image block (configure via `imageBlockSettings` prop) |
| `'Divider'` | Horizontal separator line |
| `'CollapsibleHeading'` | Collapsible heading (use `properties.isExpanded`, `properties.children`) |
| `'CollapsibleParagraph'` | Collapsible paragraph (use `properties.isExpanded`, `properties.children`) |
| `'Template'` | Custom template block (use `BlockModel.template`) |

## Component Sizing

Use `width` and `height` props to control the editor container dimensions. Both accept CSS string values or numeric pixel values.

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="block-editor"
            width="800px"
            height="600px"
        />
    );
}

export default App;
```

| Prop | Type | Default | Description |
|---|---|---|---|
| `width` | `string \| number` | `'100%'` | Width of the editor container |
| `height` | `string \| number` | `'auto'` | Height of the editor container |

---

## Running the Application

After setting up your component and CSS imports:

### For Vite

```bash
npm run dev
```

The development server typically starts at `http://localhost:5173`

### For Create React App

```bash
npm start
```

The development server typically starts at `http://localhost:3000`

### For Next.js

```bash
npm run dev
```

The development server typically starts at `http://localhost:3000`

Your BlockEditor should now be ready to use! Users can:
- Type directly in the editor
- Press "/" to open the command menu
- Right-click for context menu options
- Drag blocks to reorder them
- Use keyboard shortcuts for formatting
