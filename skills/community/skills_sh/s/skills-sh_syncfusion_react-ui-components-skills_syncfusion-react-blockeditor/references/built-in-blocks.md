# Built-in Block Types

## Table of Contents
- [Block Type Overview](#block-type-overview)
- [Text Blocks (Paragraph and Headings)](#text-blocks-paragraph-and-headings)
- [List Block Types](#list-block-types)
- [Code Blocks](#code-blocks)
- [Table Blocks](#table-blocks)
- [Embed Blocks](#embed-blocks)
- [Nested Block Types](#nested-block-types)
- [Block Indentation](#block-indentation)
- [CSS Class Styling](#css-class-styling)

## Block Type Overview

The BlockEditorComponent supports multiple built-in block types to handle different content scenarios. Each block type is optimized for specific use cases:

| Block Type | Use Case | Supports Children |
|-----------|----------|------------------|
| Paragraph | Regular text content | No |
| Heading 1-4 | Section headers | No |
| BulletList | Unordered lists | No |
| NumberedList | Ordered lists | No |
| Checklist | To-do items | No |
| Code | Code snippets | No |
| Table | Tabular data | No |
| Quote | Blockquotes | Yes (children content) |
| Callout | Highlighted information | Yes (children content) |
| CollapsibleParagraph | Expandable text | Yes (children content) |
| CollapsibleHeading 1-4 | Expandable headers | Yes (children content) |
| Image | Image display | No |
| Divider | Horizontal separator | No |
| Template | Custom block rendering | No |

## Text Blocks (Paragraph and Headings)

### Paragraph Block

The paragraph block is the default block type for regular text content:

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blocks: BlockModel[] = [
        {
            id: 'para-1',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'This is a standard paragraph block.'
                }
            ]
        }
    ];

    return <BlockEditorComponent id="editor" blocks={blocks} />;
}

export default App;
```

### Heading Blocks

Create headings with different levels (1-4):

```tsx
const headingBlocks: BlockModel[] = [
    {
        id: 'h1',
        blockType: 'Heading',
        properties: { level: 1 },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Main Title (Level 1)'
            }
        ]
    },
    {
        id: 'h2',
        blockType: 'Heading',
        properties: { level: 2 },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Subtitle (Level 2)'
            }
        ]
    },
    {
        id: 'h3',
        blockType: 'Heading',
        properties: { level: 3 },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Section (Level 3)'
            }
        ]
    },
    {
        id: 'h4',
        blockType: 'Heading',
        properties: { level: 4 },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Subsection (Level 4)'
            }
        ]
    }
];
```

## List Block Types

### Bullet List

Create unordered lists with bullet points:

```tsx
const bulletListBlocks: BlockModel[] = [
    {
        id: 'bullet-1',
        blockType: 'BulletList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'First item'
            }
        ]
    },
    {
        id: 'bullet-2',
        blockType: 'BulletList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'Second item'
            }
        ]
    },
    {
        id: 'bullet-3',
        blockType: 'BulletList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'Third item'
            }
        ]
    }
];
```

### Numbered List

Create ordered lists with sequential numbering:

```tsx
const numberedListBlocks: BlockModel[] = [
    {
        id: 'num-1',
        blockType: 'NumberedList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'First step'
            }
        ]
    },
    {
        id: 'num-2',
        blockType: 'NumberedList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'Second step'
            }
        ]
    },
    {
        id: 'num-3',
        blockType: 'NumberedList',
        content: [
            {
                contentType: ContentType.Text,
                content: 'Third step'
            }
        ]
    }
];
```

### Checklist Block

Create interactive to-do lists with checkboxes:

```tsx
const checklistBlocks: BlockModel[] = [
    {
        id: 'check-1',
        blockType: 'Checklist',
        properties: { isChecked: false },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Task one - not started'
            }
        ]
    },
    {
        id: 'check-2',
        blockType: 'Checklist',
        properties: { isChecked: true },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Task two - completed'
            }
        ]
    },
    {
        id: 'check-3',
        blockType: 'Checklist',
        properties: { isChecked: false },
        content: [
            {
                contentType: ContentType.Text,
                content: 'Task three - pending'
            }
        ]
    }
];
```

## Code Blocks

Code blocks use `ContentType.Text` for their content — **not** `ContentType.Code` (which does not exist). The language is set via `properties.language` (`ICodeBlockSettings`).

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const codeBlocks: BlockModel[] = [
        {
            id: 'code-1',
            blockType: 'Code',
            properties: { language: 'javascript' },
            content: [
                {
                    contentType: ContentType.Text,  // Always ContentType.Text
                    content: 'function greet(name) {\n  console.log(`Hello, ${name}!`);\n}'
                }
            ]
        },
        {
            id: 'code-2',
            blockType: 'Code',
            properties: { language: 'python' },
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'def greet(name):\n    print(f"Hello, {name}!")'
                }
            ]
        },
        {
            id: 'code-3',
            blockType: 'Code',
            properties: { language: 'tsx' },
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'const Greeting = ({ name }) => (\n  <div>Hello, {name}!</div>\n);'
                }
            ]
        }
    ];

    return <BlockEditorComponent id="editor" blocks={codeBlocks} />;
}

export default App;
```

### Configure Available Languages (`codeBlockSettings`)

Use the `codeBlockSettings` component prop to control which languages appear in the language picker:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="editor"
            codeBlockSettings={{
                defaultLanguage: 'javascript',
                languages: [
                    { label: 'JavaScript', language: 'javascript' },
                    { label: 'TypeScript', language: 'typescript' },
                    { label: 'Python', language: 'python' },
                    { label: 'HTML', language: 'html' },
                    { label: 'CSS', language: 'css' },
                    { label: 'JSON', language: 'json' },
                    { label: 'SQL', language: 'sql' },
                    { label: 'Bash', language: 'bash' }
                ]
            }}
        />
    );
}

export default App;
```

### `CodeBlockSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `defaultLanguage` | `string` | Default syntax highlighting language for new code blocks |
| `languages` | `CodeLanguageModel[]` | Languages shown in the language selector dropdown |

### `CodeLanguageModel` Properties

| Property | Type | Description |
|---|---|---|
| `label` | `string` | Display name in the dropdown (e.g., `'JavaScript'`) |
| `language` | `string` | Language identifier for syntax highlighting (e.g., `'javascript'`) |

### Supported Language Values

Common `language` values: `javascript`, `typescript`, `jsx`, `tsx`, `python`, `java`, `csharp`, `cpp`, `c`, `html`, `css`, `scss`, `xml`, `json`, `sql`, `yaml`, `markdown`, `bash`, `shell`

## Table Blocks

Table blocks use `ITableBlockSettings` in `properties`. Columns and rows are defined as typed model arrays — **not** as simple `rows: 3, columns: 3` numbers.

```tsx
import { BlockEditorComponent, BlockModel, ContentType, TableColumnType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const tableBlock: BlockModel = {
        id: 'table-1',
        blockType: 'Table',
        properties: {
            enableHeader: true,
            enableRowNumbers: false,
            readOnly: false,
            width: '100%',
            columns: [
                { id: 'col-name', headerText: 'Name', type: TableColumnType.Text, width: '40%' },
                { id: 'col-due', headerText: 'Due Date', type: TableColumnType.Date, width: '30%' },
                { id: 'col-owner', headerText: 'Owner', type: TableColumnType.Mention, width: '30%' }
            ],
            rows: [
                {
                    id: 'row-1',
                    height: 'auto',
                    cells: [
                        {
                            id: 'cell-1-1',
                            columnId: 'col-name',
                            blocks: [{ blockType: 'Paragraph', content: [{ contentType: ContentType.Text, content: 'Task A' }] }]
                        },
                        { id: 'cell-1-2', columnId: 'col-due', blocks: [] },
                        { id: 'cell-1-3', columnId: 'col-owner', blocks: [] }
                    ]
                }
            ]
        },
        content: []
    };

    return <BlockEditorComponent id="editor" blocks={[tableBlock]} />;
}

export default App;
```

### `ITableBlockSettings` Properties

| Property | Type | Description |
|---|---|---|
| `columns` | `TableColumnModel[]` | Column definitions (type, header, width) |
| `rows` | `TableRowModel[]` | Row definitions containing cells |
| `enableHeader` | `boolean` | Whether to show a header row |
| `enableRowNumbers` | `boolean` | Whether to show row numbers |
| `readOnly` | `boolean` | Whether the table is in read-only mode |
| `width` | `string \| number` | Table width (e.g., `'100%'`, `'500px'`) |

### `TableColumnModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique column identifier |
| `headerText` | `string` | Column header text |
| `type` | `TableColumnType` | Content type for this column |
| `width` | `string \| number` | Column width |

### `TableColumnType` (Enum)

| Member | Description |
|---|---|
| `Text` | Plain text content |
| `Date` | Date values |
| `Mention` | User mention content |
| `Label` | Label content |
| `Link` | Hyperlink content |

### `TableRowModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique row identifier |
| `height` | `string \| number` | Row height |
| `cells` | `TableCellModel[]` | Cells in this row |

### `TableCellModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique cell identifier |
| `columnId` | `string` | The column this cell belongs to |
| `blocks` | `BlockModel[]` | Content of the cell |

## Image Blocks

Image blocks use `IImageBlockSettings` in `properties`. Configure global image upload settings via the `imageBlockSettings` component prop.

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const imageBlocks: BlockModel[] = [
        {
            id: 'image-1',
            blockType: 'Image',
            // IImageBlockSettings — per-block image data
            properties: {
                src: 'https://example.com/photo.jpg',
                altText: 'A descriptive alt text',
                width: '100%',
                height: 'auto'
            },
            content: []
        }
    ];

    return (
        <BlockEditorComponent
            id="editor"
            blocks={imageBlocks}
            // Global image upload configuration
            imageBlockSettings={{
                saveUrl: '/api/upload-image',
                allowedTypes: ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
                maxFileSize: 5000000,      // 5 MB
                enableResize: true,
                minWidth: '100px',
                maxWidth: '100%',
                minHeight: '50px',
                maxHeight: '800px',
                saveFormat: 'Blob'         // or 'Base64'
            }}
        />
    );
}

export default App;
```

### `IImageBlockSettings` Properties (per-block)

| Property | Type | Description |
|---|---|---|
| `src` | `string` | Image source URL or path |
| `altText` | `string` | Alternative text for accessibility |
| `width` | `string \| number` | Display width |
| `height` | `string \| number` | Display height |

### `ImageBlockSettingsModel` Properties (component-level)

| Property | Type | Default | Description |
|---|---|---|---|
| `saveUrl` | `string` | — | Server endpoint for image uploads |
| `path` | `string` | — | Base server path for storing uploaded images |
| `allowedTypes` | `string[]` | — | Allowed file extensions (e.g., `['.jpg', '.png']`) |
| `maxFileSize` | `number` | `30000000` | Max file size in bytes (default 30 MB) |
| `enableResize` | `boolean` | — | Enable resize handles on images |
| `width` | `string \| number` | — | Default display width |
| `height` | `string \| number` | — | Default display height |
| `minWidth` | `string \| number` | — | Minimum resize width |
| `maxWidth` | `string \| number` | — | Maximum resize width |
| `minHeight` | `string \| number` | — | Minimum resize height |
| `maxHeight` | `string \| number` | — | Maximum resize height |
| `saveFormat` | `SaveFormat` | — | `'Base64'` or `'Blob'` |

### `SaveFormat` (Enum)

| Member | Description |
|---|---|
| `Base64` | Saves image as a Base64-encoded string |
| `Blob` | Saves image as a Blob object |

## Nested Block Types

Nested blocks allow children content to be expanded or collapsed. These blocks support parent-child relationships for creating hierarchical document structures.

### Quote Block with Children

For `Quote` blocks, nested blocks are placed in `properties.children` (part of `IQuoteBlockSettings`), **not** as a top-level `children` key on `BlockModel`.

```tsx
const quoteBlock: BlockModel = {
    id: 'quote-1',
    blockType: 'Quote',
    content: [
        { contentType: ContentType.Text, content: 'To be or not to be, that is the question.' }
    ],
    // children and placeholder live inside properties (IQuoteBlockSettings)
    properties: {
        placeholder: 'Add a quote...',
        children: [
            {
                id: 'quote-attr',
                blockType: 'Paragraph',
                content: [{ contentType: ContentType.Text, content: '— William Shakespeare' }]
            }
        ]
    }
};
```

### Callout Block

```tsx
const calloutBlock: BlockModel = {
    id: 'callout-1',
    blockType: 'Callout',
    content: [
        { contentType: ContentType.Text, content: 'Important Information' }
    ]
    // ICalloutBlockSettings has no additional documented properties
};
```

### Collapsible Heading (Levels 1–4)

`children`, `isExpanded`, and `placeholder` are all inside `properties` (`ICollapsibleHeadingBlockSettings`):

```tsx
const collapsibleHeading: BlockModel = {
    id: 'collapsible-h1',
    blockType: 'CollapsibleHeading',
    content: [
        { contentType: ContentType.Text, content: 'Expandable Section' }
    ],
    // ICollapsibleHeadingBlockSettings
    properties: {
        isExpanded: true,
        placeholder: 'Heading text...',
        children: [
            {
                id: 'child-para',
                blockType: 'Paragraph',
                content: [{ contentType: ContentType.Text, content: 'Content shown when expanded.' }]
            },
            {
                id: 'child-list',
                blockType: 'BulletList',
                content: [{ contentType: ContentType.Text, content: 'Nested list item' }]
            }
        ]
    }
};
```

Other collapsible heading levels:

```tsx
const collapsibleH2: BlockModel = {
    blockType: 'CollapsibleHeading',
    content: [{ contentType: ContentType.Text, content: 'Level 2' }],
    properties: { isExpanded: true, children: [] }
};
```

### Collapsible Paragraph

```tsx
const collapsiblePara: BlockModel = {
    id: 'collapsible-para',
    blockType: 'CollapsibleParagraph',
    content: [
        { contentType: ContentType.Text, content: 'Click to expand' }
    ],
    // ICollapsibleBlockSettings
    properties: {
        isExpanded: false,
        placeholder: 'Summary text...',
        children: [
            {
                id: 'para-detail',
                blockType: 'Paragraph',
                content: [{ contentType: ContentType.Text, content: 'Hidden content revealed on expansion.' }]
            }
        ]
    }
};
```

### Nested Block Properties Summary

> ⚠️ `children` and `isExpanded` are **not** top-level `BlockModel` properties. They live inside `properties` for each applicable block type:

| Block Type | `properties` Interface | Nested Fields |
|---|---|---|
| `Quote` | `IQuoteBlockSettings` | `children`, `placeholder` |
| `CollapsibleHeading` | `ICollapsibleHeadingBlockSettings` | `children`, `isExpanded`, `placeholder` |
| `CollapsibleParagraph` | `ICollapsibleBlockSettings` | `children`, `isExpanded`, `placeholder` |
| `Heading` | `IHeadingBlockSettings` | `level`, `placeholder` |
| `Checklist` | `IChecklistBlockSettings` | `isChecked`, `placeholder` |
| `Code` | `ICodeBlockSettings` | `language` |
| `Image` | `IImageBlockSettings` | `src`, `altText`, `width`, `height` |
| `Table` | `ITableBlockSettings` | `columns`, `rows`, `enableHeader`, `enableRowNumbers`, `readOnly`, `width` |

## Block Indentation

Control the indentation level of blocks for creating nested structures:

```tsx
const indentedBlocks: BlockModel[] = [
    {
        id: 'level-0',
        blockType: 'Paragraph',
        indent: 0,
        content: [{ contentType: ContentType.Text, content: 'No indentation' }]
    },
    {
        id: 'level-1',
        blockType: 'Paragraph',
        indent: 1,
        content: [{ contentType: ContentType.Text, content: 'One level indent' }]
    },
    {
        id: 'level-2',
        blockType: 'Paragraph',
        indent: 2,
        content: [{ contentType: ContentType.Text, content: 'Two levels indent' }]
    },
    {
        id: 'level-1b',
        blockType: 'Paragraph',
        indent: 1,
        content: [{ contentType: ContentType.Text, content: 'Back to one level' }]
    }
];

export function App() {
    return <BlockEditorComponent id="editor" blocks={indentedBlocks} />;
}
```

Indentation is useful for:
- Creating hierarchical lists
- Organizing nested paragraphs
- Visual content structure
- Outline-style documents

## CSS Class Styling

Apply custom CSS classes to individual blocks for specialized styling:

```tsx
const styledBlocks: BlockModel[] = [
    {
        id: 'default',
        blockType: 'Paragraph',
        content: [{ contentType: ContentType.Text, content: 'Default paragraph' }]
    },
    {
        id: 'info-block',
        blockType: 'Paragraph',
        cssClass: 'info-block highlight',
        content: [{ contentType: ContentType.Text, content: 'This is an info block' }]
    },
    {
        id: 'warning-block',
        blockType: 'Paragraph',
        cssClass: 'warning-block',
        content: [{ contentType: ContentType.Text, content: 'This is a warning' }]
    },
    {
        id: 'success-block',
        blockType: 'Paragraph',
        cssClass: 'success-block',
        content: [{ contentType: ContentType.Text, content: 'Operation successful!' }]
    }
];
```

Add corresponding styles in your CSS file:

```css
.info-block {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
    padding: 10px 15px;
}

.warning-block {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
    padding: 10px 15px;
}

.success-block {
    background-color: #e8f5e9;
    border-left: 4px solid #4caf50;
    padding: 10px 15px;
}

.highlight {
    font-weight: bold;
}
```
