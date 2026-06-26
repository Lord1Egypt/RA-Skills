# Drag-Drop and Content Management

## Table of Contents
- [Overview](#overview)
- [Enable Drag-and-Drop](#enable-dragand-drop)
- [Block Reordering](#block-reordering)
- [Content Insertion](#content-insertion)
- [Block Nesting](#block-nesting)
- [Handle Positioning](#handle-positioning)
- [Drag-Drop Events](#dragdrop-events)
- [Programmatic Block Movement](#programmatic-block-movement)

## Overview

The BlockEditor supports intuitive drag-and-drop functionality for reordering blocks, inserting new content, and managing nested structures. Users can:

- **Drag blocks** to reorder content within the editor
- **Move blocks** between different nesting levels
- **Drop content** from external sources
- **Handle visual indicators** showing drop targets

## Enable Drag-and-Drop

Use the `enableDragAndDrop` prop to enable or disable drag-and-drop reordering. The default is `true`.

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: ContentType.Text, content: 'Section 1' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Drag this block using the handle on the left' }]
        },
        {
            id: 'block-3',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'This block can also be dragged' }]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            blocks={blocks}
            enableDragAndDrop={true}
        />
    );
}

export default App;
```

### Disable Drag-and-Drop

```tsx
<BlockEditorComponent
    id="block-editor"
    blocks={blocks}
    enableDragAndDrop={false}
/>
```

> ⚠️ The correct prop is `enableDragAndDrop` — **not** `showBlockHandle`. There is no `showBlockHandle` prop in the BlockEditor API.

## Block Reordering

Blocks can be reordered by dragging them to new positions.

### User-Driven Reordering

1. Users hover over a block to see the drag handle (three dots or similar)
2. Click and hold the handle
3. Drag the block up or down
4. Release to drop at the new position

### Visual Feedback

The editor provides visual indicators:
- **Highlight on hover** - Block is draggable
- **Drop target line** - Shows where block will be placed
- **Opacity change** - Indicates drag in progress

### Constraints

- Blocks maintain their data integrity during moves
- Block IDs remain unchanged
- Child blocks move with their parent
- Read-only mode disables dragging

## Content Insertion

### Drop Zones

The editor creates drop zones between blocks:

```
[Block 1]
  ↓  ← Drop zone here
[Block 2]
  ↓  ← Drop zone here
[Block 3]
```

### External Content Drops

Users can drop external content (text, links, files):

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [droppedContent, setDroppedContent] = React.useState<string>('');

    const handleBlockDrop = (event: any) => {
        event.preventDefault();
        
        // Get dropped data
        const droppedText = event.dataTransfer.getData('text/plain');
        const droppedHtml = event.dataTransfer.getData('text/html');
        
        setDroppedContent(droppedText || droppedHtml || '');
    };

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Drop text or images here'
                }
            ]
        }
    ];

    return (
        <div
            onDrop={handleBlockDrop}
            onDragOver={(e) => e.preventDefault()}
        >
            <BlockEditorComponent
                id="block-editor"
                blocks={blocks}
                ref={editorRef}
            />
            {droppedContent && (
                <div>
                    <p>Dropped content: {droppedContent}</p>
                </div>
            )}
        </div>
    );
}

export default App;
```

## Block Nesting

Nested blocks support parent-child relationships.

### Create Nested Structure

For blocks that support nesting (e.g., `Quote`, `Callout`, `CollapsibleHeading`, `CollapsibleParagraph`), place `children` inside the `properties` object — it is **not** a top-level property of `BlockModel`.

```tsx
const nestedBlocks: BlockModel[] = [
    {
        id: 'quote-1',
        blockType: 'Quote',
        content: [{ contentType: ContentType.Text, content: 'A wise saying' }],
        properties: {
            children: [
                {
                    id: 'child-1',
                    blockType: 'Paragraph',
                    content: [{ contentType: ContentType.Text, content: 'Attribution line' }]
                }
            ]
        }
    },
    {
        id: 'para-2',
        blockType: 'Paragraph',
        content: [{ contentType: ContentType.Text, content: 'Regular paragraph (not nested)' }]
    }
];
```

> ⚠️ `children` is NOT a top-level property on `BlockModel`. It lives inside `properties` for block types that support nesting (`IQuoteBlockSettings`, `ICalloutBlockSettings`, `ICollapsibleBlockSettings`, `ICollapsibleHeadingBlockSettings`).

### Drag Blocks Between Nesting Levels

Dragging a block to the right indents it (nests it). Dragging left outdents it:

```
Original:          After dragging right:     After dragging left:
[Block 1]          [Block 1]                 [Block 1]
[Block 2]  drag→     └─ [Block 2]            [Block 2]
[Block 3]          [Block 3]                 [Block 3]
```

### Collapsible Nested Blocks

For `CollapsibleHeading` and `CollapsibleParagraph`, both `isExpanded` and `children` belong inside `properties`:

```tsx
const collapsibleBlock: BlockModel = {
    id: 'collapsible-1',
    blockType: 'CollapsibleHeading',
    content: [{ contentType: ContentType.Text, content: 'Click to collapse/expand' }],
    properties: {
        level: 1,
        isExpanded: true,  // Initially expanded — lives in properties
        children: [
            {
                id: 'child-1',
                blockType: 'Paragraph',
                content: [{ contentType: ContentType.Text, content: 'Hidden content' }]
            }
        ]
    }
};
```

## Handle Positioning

### Drag Handle Location

The drag handle appears on the left side of each block. It's typically:
- **Always visible** - For easier access
- **Hover to show** - To reduce visual clutter
- **Hidden** - In read-only mode

### Customize Handle Appearance

Use CSS to style the drag handle. Enable drag-and-drop with `enableDragAndDrop={true}`:

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <div>
            <style>{`
                .e-block-handle {
                    color: #2196f3;
                    cursor: grab;
                    font-size: 18px;
                }
                .e-block-handle:active {
                    cursor: grabbing;
                }
            `}</style>
            <BlockEditorComponent
                id="block-editor"
                enableDragAndDrop={true}
            />
        </div>
    );
}

export default App;
```

## Drag-Drop Events

The BlockEditor provides three drag-related events: `blockDragStart`, `blockDragging`, and `blockDropped`.

### `BlockDragEventArgs` Interface

Used by `blockDragStart` and `blockDragging`:

| Property | Type | Description |
|---|---|---|
| `blocks` | `BlockModel[]` | The blocks being dragged |
| `cancel` | `boolean` | Set to `true` to cancel the drag |
| `dropIndex` | `number` | Current potential drop index |
| `event` | `MouseEvent \| TouchEvent` | The native browser event |
| `fromIndex` | `number` | Original index of the dragged block |
| `target` | `HTMLElement` | The current drag target element |

### `BlockDropEventArgs` Interface

Used by `blockDropped`:

| Property | Type | Description |
|---|---|---|
| `blocks` | `BlockModel[]` | The blocks that were dropped |
| `dropIndex` | `number` | Index where the blocks were dropped |
| `event` | `MouseEvent \| TouchEvent` | The native browser event |
| `fromIndex` | `number` | Original index before the drop |
| `target` | `HTMLElement` | The element the block was dropped onto |

### Block Drag Events Example

```tsx
import {
    BlockEditorComponent,
    BlockModel,
    BlockDragEventArgs,
    BlockDropEventArgs,
    ContentType
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [draggedBlocks, setDraggedBlocks] = React.useState<BlockModel[]>([]);

    const onBlockDragStart = (args: BlockDragEventArgs) => {
        console.log('Drag started — from index:', args.fromIndex);
        console.log('Dragging blocks:', args.blocks);
        setDraggedBlocks(args.blocks);
        // Set args.cancel = true to prevent dragging
    };

    const onBlockDragging = (args: BlockDragEventArgs) => {
        console.log('Dragging — current drop index:', args.dropIndex);
    };

    const onBlockDropped = (args: BlockDropEventArgs) => {
        console.log('Dropped — from index:', args.fromIndex, '→ drop index:', args.dropIndex);
        console.log('Dropped blocks:', args.blocks);
        setDraggedBlocks([]);
    };

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Drag-enabled block 1' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Drag-enabled block 2' }]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            ref={editorRef}
            blocks={blocks}
            enableDragAndDrop={true}
            blockDragStart={onBlockDragStart}
            blockDragging={onBlockDragging}
            blockDropped={onBlockDropped}
        />
    );
}

export default App;
```

## Programmatic Block Movement

### Move Blocks via API

Use the `moveBlock` method to reorder blocks programmatically:

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Block 1'
                }
            ]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Block 2'
                }
            ]
        },
        {
            id: 'block-3',
            blockType: 'Paragraph',
            content: [
                {
                    contentType: ContentType.Text,
                    content: 'Block 3'
                }
            ]
        }
    ];

    // Move block-1 after block-2
    const moveBlockUp = () => {
        editorRef.current?.moveBlock('block-1', 'block-2');
        console.log('Moved block-1 after block-2');
    };

    // Move block-3 before block-1
    const moveBlockDown = () => {
        editorRef.current?.moveBlock('block-3', 'block-1');
        console.log('Moved block-3 before block-1');
    };

    // Swap two blocks
    const swapBlocks = () => {
        editorRef.current?.moveBlock('block-1', 'block-3');
        console.log('Swapped block-1 and block-3');
    };

    return (
        <div>
            <div style={{ marginBottom: '10px' }}>
                <button onClick={moveBlockUp}>Move Block 1 Down</button>
                <button onClick={moveBlockDown}>Move Block 3 Up</button>
                <button onClick={swapBlocks}>Swap Blocks</button>
            </div>
            <BlockEditorComponent
                id="block-editor"
                ref={editorRef}
                blocks={blocks}
                enableDragAndDrop={true}
            />
        </div>
    );
}

export default App;
```

### Add Blocks at Specific Positions

```tsx
const addBlockAfter = () => {
    const newBlock: BlockModel = {
        blockType: 'Paragraph',
        content: [
            {
                contentType: ContentType.Text,
                content: 'New paragraph inserted after block-2'
            }
        ]
    };
    
    // Add after block-2
    editorRef.current?.addBlock(newBlock, 'block-2', true);
};

const addBlockBefore = () => {
    const newBlock: BlockModel = {
        blockType: 'Paragraph',
        content: [
            {
                contentType: ContentType.Text,
                content: 'New paragraph inserted before block-2'
            }
        ]
    };
    
    // Add before block-2
    editorRef.current?.addBlock(newBlock, 'block-2', false);
};
```

## Complete Example

```tsx
import { BlockEditorComponent, BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [blocks, setBlocks] = React.useState<BlockModel[]>([
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: ContentType.Text, content: 'Drag-Drop Demo' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Drag blocks using the handle' }]
        },
        {
            id: 'block-3',
            blockType: 'BulletList',
            content: [{ contentType: ContentType.Text, content: 'Drag to reorder' }]
        }
    ]);

    const reorderBlocks = (fromId: string, toId: string) => {
        editorRef.current?.moveBlock(fromId, toId);
    };

    return (
        <div style={{ padding: '20px' }}>
            <BlockEditorComponent
                id="block-editor"
                ref={editorRef}
                blocks={blocks}
                enableDragAndDrop={true}
            />
        </div>
    );
}

export default App;
```
