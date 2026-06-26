# Methods and API Reference

## Table of Contents
- [Block Management Methods](#block-management-methods)
- [Selection and Cursor Methods](#selection-and-cursor-methods)
- [Focus Management](#focus-management)
- [Formatting Methods](#formatting-methods)
- [Data Export and Import Methods](#data-export-and-import-methods)
- [Practical Examples](#practical-examples)
- [Common Patterns](#common-patterns)

## Block Management Methods

### addBlock()

Add a new block to the editor at a specified position.

**Signature:**
```tsx
addBlock(block: BlockModel, targetBlockId?: string, insertAfter?: boolean): void
```

**Parameters:**
- `block` - The block to add (BlockModel object)
- `targetBlockId` - ID of reference block (optional)
- `insertAfter` - true = after target, false = before target (default: true)

**Example:**
```tsx
const editorRef = React.useRef<BlockEditorComponent>(null);

const addNewParagraph = () => {
    const newBlock: BlockModel = {
        blockType: 'Paragraph',
        content: [
            {
                contentType: ContentType.Text,
                content: 'This is a newly added paragraph'
            }
        ]
    };
    
    // Add at end
    editorRef.current?.addBlock(newBlock);
    
    // Add after specific block
    editorRef.current?.addBlock(newBlock, 'block-2', true);
    
    // Add before specific block
    editorRef.current?.addBlock(newBlock, 'block-2', false);
};
```

### removeBlock()

Remove a block from the editor by its ID.

**Signature:**
```tsx
removeBlock(blockId: string): void
```

**Example:**
```tsx
const removeSelectedBlock = () => {
    editorRef.current?.removeBlock('block-to-delete-id');
    console.log('Block removed');
};
```

### moveBlock()

Move a block from one position to another.

**Signature:**
```tsx
moveBlock(sourceBlockId: string, targetBlockId: string, insertAfter?: boolean): void
```

**Parameters:**
- `sourceBlockId` - ID of block to move
- `targetBlockId` - ID of reference block
- `insertAfter` - true = after target, false = before target (default: true)

**Example:**
```tsx
const reorderBlocks = () => {
    // Move block-1 after block-3
    editorRef.current?.moveBlock('block-1', 'block-3', true);
    
    // Move block-2 before block-1
    editorRef.current?.moveBlock('block-2', 'block-1', false);
};
```

### updateBlock()

Update properties of an existing block.

**Signature:**
```tsx
updateBlock(blockId: string, updates: Partial<BlockModel>): boolean
```

**Returns:** true if successful, false otherwise

**Example:**
```tsx
const updateBlockContent = () => {
    const success = editorRef.current?.updateBlock('block-1', {
        content: [
            {
                contentType: ContentType.Text,
                content: 'Updated content'
            }
        ],
        indent: 2,
        cssClass: 'highlight'
    });
    
    if (success) {
        console.log('Block updated');
    }
};
```

### getBlock()

Retrieve a block model by its ID.

**Signature:**
```tsx
getBlock(blockId: string): BlockModel | null
```

**Returns:** Block object or null if not found

**Example:**
```tsx
const getBlockInfo = () => {
    const block = editorRef.current?.getBlock('block-1');
    
    if (block) {
        console.log('Block type:', block.blockType);
        console.log('Content:', block.content);
        console.log('ID:', block.id);
    } else {
        console.log('Block not found');
    }
};
```

### getBlockCount()

Get the total number of blocks in the editor.

**Signature:**
```tsx
getBlockCount(): number
```

**Example:**
```tsx
const displayBlockCount = () => {
    const count = editorRef.current?.getBlockCount() ?? 0;
    console.log(`Total blocks: ${count}`);
    
    if (count === 0) {
        console.log('Editor is empty');
    }
};
```

## Selection and Cursor Methods

### setSelection()

Set text selection within a block.

**Signature:**
```tsx
setSelection(startBlockId: string, startOffset: number, endBlockId: string, endOffset: number): void
```

**Example:**
```tsx
const selectTextRange = () => {
    // Select from position 0-10 in block-1
    editorRef.current?.setSelection('block-1', 0, 'block-1', 10);
};
```

### setCursorPosition()

Set the cursor position in a specific block.

**Signature:**
```tsx
setCursorPosition(blockId: string, offset: number): void
```

**Example:**
```tsx
const moveToStartOfBlock = () => {
    // Move cursor to position 0 (start)
    editorRef.current?.setCursorPosition('block-1', 0);
};

const moveToEndOfBlock = () => {
    const block = editorRef.current?.getBlock('block-1');
    if (block && block.content) {
        const textLength = block.content[0].content?.length ?? 0;
        editorRef.current?.setCursorPosition('block-1', textLength);
    }
};
```

### getSelectedBlocks()

Get all currently selected blocks.

**Signature:**
```tsx
getSelectedBlocks(): BlockModel[]
```

**Example:**
```tsx
const getSelection = () => {
    const selected = editorRef.current?.getSelectedBlocks() ?? [];
    console.log(`${selected.length} blocks selected`);
    
    selected.forEach(block => {
        console.log('Selected block:', block.id);
    });
};
```

### getRange()

Get the current text selection range.

**Signature:**
```tsx
getRange(): Range | null
```

**Example:**
```tsx
const getCurrentSelection = () => {
    const range = editorRef.current?.getRange();
    
    if (range) {
        console.log('Selection start:', range.startOffset);
        console.log('Selection end:', range.endOffset);
        console.log('Selected text:', range.toString());
    }
};
```

### selectRange()

Select a range of text.

**Signature:**
```tsx
selectRange(range: Range): void
```

**Example:**
```tsx
const selectFromRange = () => {
    const range = document.createRange();
    // Configure range...
    editorRef.current?.selectRange(range);
};
```

### selectBlock()

Select an entire block.

**Signature:**
```tsx
selectBlock(blockId: string): void
```

**Example:**
```tsx
const selectEntireBlock = () => {
    editorRef.current?.selectBlock('block-1');
    console.log('Block selected');
};
```

### selectAllBlocks()

Select all blocks in the editor.

**Signature:**
```tsx
selectAllBlocks(): void
```

**Example:**
```tsx
const selectAll = () => {
    editorRef.current?.selectAllBlocks();
    console.log('All blocks selected');
};
```

## Focus Management

### focusIn()

Set focus to the editor.

**Signature:**
```tsx
focusIn(): void
```

**Example:**
```tsx
const setFocus = () => {
    editorRef.current?.focusIn();
    console.log('Editor focused');
};
```

### focusOut()

Remove focus from the editor.

**Signature:**
```tsx
focusOut(): void
```

**Example:**
```tsx
const removeFocus = () => {
    editorRef.current?.focusOut();
    console.log('Editor focus removed');
};
```

## Formatting Methods

### executeToolbarAction()

Execute a toolbar formatting action.

**Signature:**
```tsx
executeToolbarAction(action: string): void
```

**Example:**
```tsx
const applyFormatting = () => {
    // Apply bold formatting
    editorRef.current?.executeToolbarAction('Bold');
    
    // Apply italic
    editorRef.current?.executeToolbarAction('Italic');
    
    // Apply underline
    editorRef.current?.executeToolbarAction('Underline');
};
```

### enableToolbarItems()

Enable specific toolbar items.

**Signature:**
```tsx
enableToolbarItems(items: string[]): void
```

**Example:**
```tsx
const enableFormatting = () => {
    editorRef.current?.enableToolbarItems(['Bold', 'Italic', 'Link']);
};
```

### disableToolbarItems()

Disable specific toolbar items.

**Signature:**
```tsx
disableToolbarItems(items: string[]): void
```

**Example:**
```tsx
const disableEditing = () => {
    editorRef.current?.disableToolbarItems(['Bold', 'Italic', 'Underline', 'Link']);
};
```

## Data Export and Import Methods

### getDataAsJson()

Export editor content as JSON.

**Signature:**
```tsx
getDataAsJson(): string
```

**Example:**
```tsx
const exportAsJson = () => {
    const jsonContent = editorRef.current?.getDataAsJson();
    console.log('Exported JSON:', jsonContent);
    
    // Save to file or send to server
    const blob = new Blob([jsonContent], { type: 'application/json' });
    downloadFile(blob, 'content.json');
};
```

### getDataAsHtml()

Export editor content as HTML.

**Signature:**
```tsx
getDataAsHtml(): string
```

**Example:**
```tsx
const exportAsHtml = () => {
    const htmlContent = editorRef.current?.getDataAsHtml();
    console.log('Exported HTML:', htmlContent);
    
    // Display preview
    document.getElementById('preview').innerHTML = htmlContent;
};
```

### renderBlocksFromJson()

Import and render blocks from JSON.

**Signature:**
```tsx
renderBlocksFromJson(jsonContent: string): void
```

**Example:**
```tsx
const importFromJson = (jsonString: string) => {
    try {
        editorRef.current?.renderBlocksFromJson(jsonString);
        console.log('Content imported from JSON');
    } catch (error) {
        console.error('Failed to import:', error);
    }
};
```

### parseHtmlToBlocks()

Parse HTML and convert to block structure.

**Signature:**
```tsx
parseHtmlToBlocks(htmlContent: string): BlockModel[]
```

**Example:**
```tsx
const importFromHtml = (htmlString: string) => {
    const blocks = editorRef.current?.parseHtmlToBlocks(htmlString) ?? [];
    console.log(`Parsed ${blocks.length} blocks from HTML`);
    
    // Can use blocks array or render directly
    editorRef.current?.renderBlocksFromJson(JSON.stringify(blocks));
};
```

### print()

Print the editor content.

**Signature:**
```tsx
print(): void
```

**Example:**
```tsx
const printContent = () => {
    editorRef.current?.print();
};
```

## Practical Examples

### Example 1: Create and Manage Dynamic Content

```tsx
function DynamicContentManager() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const addParagraph = () => {
        const newBlock: BlockModel = {
            blockType: 'Paragraph',
            content: [{
                contentType: ContentType.Text,
                content: `Paragraph added at ${new Date().toLocaleTimeString()}`
            }]
        };
        editorRef.current?.addBlock(newBlock);
    };

    const addHeading = () => {
        const newBlock: BlockModel = {
            blockType: 'Heading',
            properties: { level: 2 },
            content: [{
                contentType: ContentType.Text,
                content: 'New Section'
            }]
        };
        editorRef.current?.addBlock(newBlock);
    };

    const displayStats = () => {
        const count = editorRef.current?.getBlockCount() ?? 0;
        alert(`Total blocks: ${count}`);
    };

    return (
        <div>
            <div style={{ marginBottom: '10px' }}>
                <button onClick={addParagraph}>Add Paragraph</button>
                <button onClick={addHeading}>Add Heading</button>
                <button onClick={displayStats}>Show Stats</button>
            </div>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}
```

### Example 2: Export and Share Content

```tsx
function ExportManager() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const exportAndDownload = () => {
        const jsonContent = editorRef.current?.getDataAsJson();
        if (jsonContent) {
            const blob = new Blob([jsonContent], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'content.json';
            a.click();
        }
    };

    const exportAsHTML = () => {
        const htmlContent = editorRef.current?.getDataAsHtml();
        if (htmlContent) {
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'content.html';
            a.click();
        }
    };

    return (
        <div>
            <button onClick={exportAndDownload}>Export as JSON</button>
            <button onClick={exportAsHTML}>Export as HTML</button>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}
```

### Example 3: Content Search and Selection

```tsx
function ContentSearch() {
    const editorRef = React.useRef<BlockEditorComponent>(null);
    const [searchTerm, setSearchTerm] = React.useState('');
    const [matches, setMatches] = React.useState<BlockModel[]>([]);

    const searchContent = () => {
        const blocks: BlockModel[] = [];
        let count = 0;
        
        while (count < (editorRef.current?.getBlockCount() ?? 0)) {
            const block = editorRef.current?.getBlock(`block-${count}`);
            if (block && block.content[0]?.content?.includes(searchTerm)) {
                blocks.push(block);
            }
            count++;
        }
        
        setMatches(blocks);
        console.log(`Found ${blocks.length} matches`);
    };

    const selectFirstMatch = () => {
        if (matches.length > 0) {
            editorRef.current?.selectBlock(matches[0].id!);
            editorRef.current?.focusIn();
        }
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button onClick={searchContent}>Search</button>
            <button onClick={selectFirstMatch} disabled={matches.length === 0}>
                Go to First Match
            </button>
            <BlockEditorComponent id="editor" ref={editorRef} />
        </div>
    );
}
```

## Common Patterns

### Pattern 1: Batch Operations

```tsx
const batchAddBlocks = () => {
    const newBlocks: BlockModel[] = [
        {
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: ContentType.Text, content: 'Title' }]
        },
        {
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Introduction' }]
        },
        {
            blockType: 'BulletList',
            content: [{ contentType: ContentType.Text, content: 'Point 1' }]
        }
    ];
    
    newBlocks.forEach((block, index) => {
        editorRef.current?.addBlock(block);
    });
};
```

### Pattern 2: Conditional Formatting

```tsx
const applyConditionalFormatting = (blockId: string) => {
    const block = editorRef.current?.getBlock(blockId);
    if (block?.blockType === 'Paragraph') {
        const textLength = block.content[0].content?.length ?? 0;
        if (textLength > 100) {
            editorRef.current?.updateBlock(blockId, {
                cssClass: 'long-paragraph'
            });
        }
    }
};
```

### Pattern 3: Content Validation

```tsx
const validateContent = (): boolean => {
    const count = editorRef.current?.getBlockCount() ?? 0;
    if (count === 0) {
        alert('Add at least one block');
        return false;
    }
    return true;
};
```
