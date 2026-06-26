# Block Editor Menus and Commands

## Table of Contents
- [Overview](#overview)
- [Slash Command Menu](#slash-command-menu)
- [Context Menu](#context-menu)
- [Inline Toolbar](#inline-toolbar)
- [Block Actions Menu](#block-actions-menu)
- [Menu Customization](#menu-customization)
- [Events and Callbacks](#events-and-callbacks)

## Overview

The BlockEditor provides multiple intuitive menus for content creation and editing:

| Menu Type | Prop | Trigger | Use Case |
|-----------|------|---------|----------|
| **Slash Commands** | `commandMenuSettings` | Type `/` in editor | Insert or transform blocks |
| **Context Menu** | `contextMenuSettings` | Right-click on block | Cut, copy, paste, indent, custom actions |
| **Inline Toolbar** | `inlineToolbarSettings` | Select text | Bold, italic, underline, links, formatting |
| **Block Actions** | `blockActionMenuSettings` | Click block action icon | Move, delete, custom per-block actions |
| **Block Transform** | `transformSettings` | Click transform icon | Change a block's type |

## Slash Command Menu

The Slash Command menu provides keyboard-driven access to insert or transform blocks. Press "/" to open it.

### Built-in Commands

Default commands available in the Slash menu:

| Command | Type | Description |
|---------|------|-------------|
| Heading 1-4 | Structure | Insert heading blocks |
| Paragraph | Text | Insert paragraph block |
| Bullet List | List | Unordered list |
| Numbered List | List | Ordered numbered list |
| Checklist | List | To-do list with checkboxes |
| Quote | Structure | Blockquote with attribution |
| Callout | Structure | Highlighted info box |
| Code | Structure | Code block with syntax highlighting |
| Divider | Utility | Horizontal separator |
| Table | Data | Tabular structure |
| Image | Media | Image insertion |
| Toggle | Structure | Collapsible content block |

### Customize Slash Command Menu

```tsx
import { BlockEditorComponent, CommandMenuSettingsModel, CommandFilteringEventArgs, CommandItemSelectEventArgs } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const commandMenuSettings: CommandMenuSettingsModel = {
        popupWidth: '350px',
        popupHeight: '400px',
        commands: [
            {
                id: 'timestamp-cmd',
                label: 'Insert Timestamp',
                groupBy: 'Custom',
                iconCss: 'e-icons e-schedule',
                tooltip: 'Insert current date and time',
                type: 'Paragraph'
            },
            {
                id: 'separator-cmd',
                label: 'Insert Divider',
                groupBy: 'Utility',
                iconCss: 'e-icons e-divider',
                type: 'Divider',
                disabled: false
            }
        ],
        // Fires when user types to filter commands — use args.text (not args.searchText)
        filtering: (args: CommandFilteringEventArgs) => {
            console.log('Filter query:', args.text);
            console.log('Filtered commands:', args.commands);
            // Set args.cancel = true to prevent default filtering
        },
        // Fires when user selects a command — use args.command for the selected item
        itemSelect: (args: CommandItemSelectEventArgs) => {
            console.log('Selected command id:', args.command.id);
            console.log('Selected command label:', args.command.label);
            console.log('Native event:', args.event);
            // Set args.cancel = true to prevent default block insertion
        }
    };

    return (
        <BlockEditorComponent
            id="block-editor"
            commandMenuSettings={commandMenuSettings}
        />
    );
}

export default App;
```

### `CommandMenuSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `commands` | `CommandItemModel[]` | Array of command items in the slash menu |
| `popupHeight` | `string` | CSS height of the popup |
| `popupWidth` | `string` | CSS width of the popup |

### `CommandMenuSettingsModel` Events

| Event | Args Type | Description |
|---|---|---|
| `filtering` | `CommandFilteringEventArgs` | Fires when user types to filter commands |
| `itemSelect` | `CommandItemSelectEventArgs` | Fires when a command item is clicked |

### `CommandItemModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier |
| `label` | `string` | Display label in the menu |
| `type` | `string \| BlockType` | Block type to insert |
| `iconCss` | `string` | CSS class for the item icon |
| `groupBy` | `string` | Group header text |
| `tooltip` | `string` | Tooltip shown on hover |
| `shortcut` | `string` | Keyboard shortcut string |
| `disabled` | `boolean` | Whether the item is disabled |

### `CommandFilteringEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `text` | `string` | The query typed by the user |
| `commands` | `CommandItemModel[]` | Filtered command list |
| `cancel` | `boolean` | Set `true` to prevent filtering |
| `event` | `Event` | Native browser event |

### `CommandItemSelectEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `command` | `CommandItemModel` | The command item that was selected |
| `cancel` | `boolean` | Set `true` to prevent block insertion |
| `element` | `HTMLElement` | The clicked HTML element |
| `event` | `Event` | Native browser event |
| `isInteracted` | `boolean` | `true` if triggered by user interaction |

## Context Menu

The Context Menu appears on right-click and provides block-specific actions.

### Built-in Context Menu Items

Default options in the context menu:

- **Undo** - Reverse last action
- **Redo** - Re-apply last undone action
- **Cut** - Remove and copy to clipboard
- **Copy** - Copy to clipboard
- **Paste** - Insert from clipboard
- **Indent** - Increase block indentation
- **Outdent** - Decrease block indentation
- **Link** - Add or edit hyperlink
- **Delete** - Remove block

### Customize Context Menu

```tsx
import {
    BlockEditorComponent,
    ContextMenuSettingsModel,
    ContextMenuBeforeOpenEventArgs,
    ContextMenuBeforeCloseEventArgs,
    ContextMenuItemSelectEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const contextMenuSettings: ContextMenuSettingsModel = {
        enable: true,
        showItemOnClick: false,

        // Fires BEFORE the context menu opens — use beforeOpen (not opening)
        beforeOpen: (args: ContextMenuBeforeOpenEventArgs) => {
            console.log('Context menu opening');
            console.log('Items:', args.items);
            console.log('Parent item:', args.parentItem);
            // Set args.cancel = true to prevent the menu from opening
        },

        // Fires BEFORE the context menu closes — use beforeClose (not closing)
        beforeClose: (args: ContextMenuBeforeCloseEventArgs) => {
            console.log('Context menu closing');
            // Set args.cancel = true to keep the menu open
        },

        // Fires when a menu item is clicked — use args.item (not args.label)
        itemSelect: (args: ContextMenuItemSelectEventArgs) => {
            console.log('Selected item:', args.item.text);
            console.log('Selected item id:', args.item.id);
            // Set args.cancel = true to prevent the default action
        },

        // Define menu items
        items: [
            { id: 'undo', text: 'Undo', iconCss: 'e-icons e-undo' },
            { id: 'redo', text: 'Redo', iconCss: 'e-icons e-redo' },
            { separator: true },
            { id: 'cut', text: 'Cut', iconCss: 'e-icons e-cut' },
            { id: 'copy', text: 'Copy', iconCss: 'e-icons e-copy' },
            { id: 'paste', text: 'Paste', iconCss: 'e-icons e-paste' },
            { separator: true },
            {
                id: 'more',
                text: 'More Options',
                iconCss: 'e-icons e-settings',
                // Nested sub-menu via items array
                items: [
                    { id: 'custom-action', text: 'Custom Action' }
                ]
            }
        ]
    };

    return (
        <BlockEditorComponent
            id="block-editor"
            contextMenuSettings={contextMenuSettings}
        />
    );
}

export default App;
```

### `ContextMenuSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `enable` | `boolean` | Whether the context menu is enabled |
| `itemTemplate` | `string \| Function` | Custom template for rendering menu items |
| `items` | `ContextMenuItemModel[]` | Array of context menu items |
| `showItemOnClick` | `boolean` | Show sub-items on click instead of hover |

### `ContextMenuSettingsModel` Events

| Event | Args Type | Description |
|---|---|---|
| `beforeOpen` | `ContextMenuBeforeOpenEventArgs` | Fires before the menu opens |
| `beforeClose` | `ContextMenuBeforeCloseEventArgs` | Fires before the menu closes |
| `itemSelect` | `ContextMenuItemSelectEventArgs` | Fires when a menu item is clicked |

> ⚠️ The events are named `beforeOpen` and `beforeClose` — **not** `opening` or `closing`.

### `ContextMenuItemModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier |
| `text` | `string` | Display text |
| `iconCss` | `string` | CSS class for icon |
| `separator` | `boolean` | Renders as a divider line |
| `shortcut` | `string` | Keyboard shortcut label |
| `items` | `ContextMenuItemModel[]` | Nested sub-menu items |

### `ContextMenuBeforeOpenEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set `true` to prevent the menu from opening |
| `event` | `Event` | Native browser event |
| `items` | `ContextMenuItemModel[]` | Current menu items |
| `parentItem` | `ContextMenuItemModel` | Parent item (for sub-menus) |

### `ContextMenuBeforeCloseEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set `true` to prevent the menu from closing |
| `event` | `Event` | Native browser event |
| `items` | `ContextMenuItemModel[]` | Current menu items |

### `ContextMenuItemSelectEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `item` | `ContextMenuItemModel` | The item that was clicked |
| `cancel` | `boolean` | Set `true` to cancel the action |
| `event` | `Event` | Native browser event |

## Inline Toolbar

The inline toolbar appears when text is selected within a block. Configure it using the `inlineToolbarSettings` prop.

### Default Toolbar Behavior

When text is selected, the inline toolbar floats above the selection offering common formatting actions like Bold, Italic, Underline, StrikeThrough, and hyperlink insertion.

### Configure Inline Toolbar

```tsx
import { BlockEditorComponent, InlineToolbarSettingsModel, ToolbarItemClickEventArgs } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        enable: true,
        popupWidth: '100%',
        items: ['Bold', 'Italic', 'Underline', 'StrikeThrough', 'InlineCode', 'Link', 'FontColor', 'BackgroundColor'],
        itemClick: (args: ToolbarItemClickEventArgs) => {
            console.log('Toolbar item clicked:', args.item.text);
            console.log('Is user interaction:', args.isInteracted);
            // Set args.cancel = true to prevent default formatting
        }
    };

    return (
        <BlockEditorComponent
            id="block-editor"
            inlineToolbarSettings={inlineToolbarSettings}
        />
    );
}

export default App;
```

### `InlineToolbarSettingsModel` Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `enable` | `boolean` | — | Whether the inline toolbar is shown on text selection |
| `items` | `string[]` | — | Array of toolbar item identifiers to display |
| `popupWidth` | `string \| number` | `'100%'` | Width of the inline toolbar popup |

### `InlineToolbarSettingsModel` Events

| Event | Args Type | Description |
|---|---|---|
| `itemClick` | `ToolbarItemClickEventArgs` | Fires when an inline toolbar item is clicked |

### `ToolbarItemClickEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `item` | `IToolbarItemModel` | The toolbar item that was clicked |
| `cancel` | `boolean` | Set `true` to prevent the formatting action |
| `event` | `Event` | Native browser event |
| `isInteracted` | `boolean` | `true` if triggered by user interaction |

> ⚠️ The correct prop is `inlineToolbarSettings` — **not** `toolbarSettings`. There is no `ToolbarSettingsModel` in the BlockEditor API.

## Block Actions Menu

The block action menu is a per-block popup triggered by the block action icon. Configure it using `blockActionMenuSettings`.

### Configure Block Actions Menu

```tsx
import {
    BlockEditorComponent,
    BlockActionMenuSettingsModel,
    BlockActionMenuBeforeOpenEventArgs,
    BlockActionMenuBeforeCloseEventArgs,
    BlockActionItemSelectEventArgs,
    BlockModel,
    ContentType
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const blockActionMenuSettings: BlockActionMenuSettingsModel = {
        enable: true,
        enableTooltip: true,
        popupWidth: '200px',
        popupHeight: 'auto',
        items: [
            {
                id: 'delete',
                label: 'Delete Block',
                iconCss: 'e-icons e-delete',
                tooltip: 'Remove this block'
            },
            {
                id: 'duplicate',
                label: 'Duplicate',
                iconCss: 'e-icons e-copy',
                tooltip: 'Copy this block'
            },
            {
                id: 'move-up',
                label: 'Move Up',
                iconCss: 'e-icons e-chevron-up',
                shortcut: 'Ctrl+Shift+Up'
            }
        ],
        beforeOpen: (args: BlockActionMenuBeforeOpenEventArgs) => {
            console.log('Block action menu opening');
            console.log('Available items:', args.items);
            // args.cancel = true to prevent opening
        },
        beforeClose: (args: BlockActionMenuBeforeCloseEventArgs) => {
            console.log('Block action menu closing');
        },
        itemSelect: (args: BlockActionItemSelectEventArgs) => {
            console.log('Action selected:', args.item.id);
            console.log('Action label:', args.item.label);
            console.log('Is user interaction:', args.isInteracted);
            // args.cancel = true to prevent default action
        }
    };

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Hover to see the block action menu icon' }]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            blocks={blocks}
            blockActionMenuSettings={blockActionMenuSettings}
        />
    );
}

export default App;
```

### `BlockActionMenuSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `enable` | `boolean` | Whether the block action menu is enabled |
| `enableTooltip` | `boolean` | Whether tooltips are shown on action items |
| `items` | `BlockActionItemModel[]` | Array of action items in the menu |
| `popupHeight` | `string` | CSS height of the action menu popup |
| `popupWidth` | `string` | CSS width of the action menu popup |

### `BlockActionMenuSettingsModel` Events

| Event | Args Type | Description |
|---|---|---|
| `beforeOpen` | `BlockActionMenuBeforeOpenEventArgs` | Fires before the menu opens |
| `beforeClose` | `BlockActionMenuBeforeCloseEventArgs` | Fires before the menu closes |
| `itemSelect` | `BlockActionItemSelectEventArgs` | Fires when an action item is clicked |

### `BlockActionItemModel` Properties

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier |
| `label` | `string` | Display label |
| `iconCss` | `string` | CSS class for the icon |
| `tooltip` | `string` | Tooltip text shown on hover |
| `shortcut` | `string` | Keyboard shortcut string |
| `disabled` | `boolean` | Whether the item is disabled |

### `BlockActionMenuBeforeOpenEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set `true` to prevent the menu from opening |
| `event` | `Event` | Native browser event |
| `items` | `BlockActionItemModel[]` | Menu items |

### `BlockActionMenuBeforeCloseEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `cancel` | `boolean` | Set `true` to prevent the menu from closing |
| `event` | `Event` | Native browser event |
| `items` | `BlockActionItemModel[]` | Menu items |

### `BlockActionItemSelectEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `item` | `BlockActionItemModel` | The action item that was clicked |
| `cancel` | `boolean` | Set `true` to cancel the action |
| `element` | `HTMLElement` | The HTML element that triggered the click |
| `isInteracted` | `boolean` | `true` if triggered by user interaction |

## Block Transform Menu

The transform menu allows users to change a block's type. Configure it using `transformSettings`.

### Configure Transform Settings

```tsx
import {
    BlockEditorComponent,
    TransformSettingsModel,
    TransformItemSelectEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const transformSettings: TransformSettingsModel = {
        popupWidth: '250px',
        popupHeight: 'auto',
        items: ['Paragraph', 'Heading', 'BulletList', 'NumberedList', 'Checklist', 'Quote', 'Code', 'Callout'],
        itemSelect: (args: TransformItemSelectEventArgs) => {
            console.log('Transform selected:', args.command.id);
            console.log('Native event:', args.event);
            // args.cancel = true to prevent the transform
        }
    };

    return (
        <BlockEditorComponent
            id="block-editor"
            transformSettings={transformSettings}
        />
    );
}

export default App;
```

### `TransformSettingsModel` Properties

| Property | Type | Description |
|---|---|---|
| `items` | `string[]` | Block types available for transformation |
| `popupHeight` | `string` | CSS height of the transform popup |
| `popupWidth` | `string` | CSS width of the transform popup |

### `TransformSettingsModel` Events

| Event | Args Type | Description |
|---|---|---|
| `itemSelect` | `TransformItemSelectEventArgs` | Fires when a transform option is selected |

### `TransformItemSelectEventArgs` Properties

| Property | Type | Description |
|---|---|---|
| `command` | `TransformItemModel` | The selected transform item |
| `cancel` | `boolean` | Set `true` to prevent the transform |
| `element` | `HTMLElement` | The HTML element associated with the selection |
| `event` | `Event` | Native browser event |

## Menu Customization

### Disable a Menu Entirely

```tsx
<BlockEditorComponent
    id="block-editor"
    contextMenuSettings={{ enable: false }}
    blockActionMenuSettings={{ enable: false }}
/>
```

### Filter Slash Commands Dynamically

```tsx
import { BlockEditorComponent, CommandMenuSettingsModel, CommandFilteringEventArgs } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const commandMenuSettings: CommandMenuSettingsModel = {
        // Use args.text — not args.searchText
        filtering: (args: CommandFilteringEventArgs) => {
            const allowedTypes = ['Paragraph', 'Heading', 'BulletList'];
            // Filter commands to only show allowed types
            args.commands = args.commands.filter(cmd =>
                allowedTypes.includes(cmd.type as string)
            );
        }
    };

    return (
        <BlockEditorComponent
            id="block-editor"
            commandMenuSettings={commandMenuSettings}
        />
    );
}

export default App;
```

## Complete Example with All Menus

```tsx
import {
    BlockEditorComponent,
    BlockModel,
    ContentType,
    CommandMenuSettingsModel,
    CommandFilteringEventArgs,
    CommandItemSelectEventArgs,
    ContextMenuSettingsModel,
    ContextMenuBeforeOpenEventArgs,
    ContextMenuItemSelectEventArgs,
    InlineToolbarSettingsModel,
    ToolbarItemClickEventArgs,
    BlockActionMenuSettingsModel,
    BlockActionItemSelectEventArgs,
    TransformSettingsModel,
    TransformItemSelectEventArgs
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const editorRef = React.useRef<BlockEditorComponent>(null);

    const commandMenuSettings: CommandMenuSettingsModel = {
        popupWidth: '300px',
        // Use args.text — not args.searchText
        filtering: (args: CommandFilteringEventArgs) => console.log('Filter query:', args.text),
        // Use args.command — not args.label/args.id directly
        itemSelect: (args: CommandItemSelectEventArgs) => console.log('Command selected:', args.command.label)
    };

    const contextMenuSettings: ContextMenuSettingsModel = {
        enable: true,
        // Use beforeOpen — not opening
        beforeOpen: (args: ContextMenuBeforeOpenEventArgs) => console.log('Context menu opening', args.items),
        // Use args.item — not args.label
        itemSelect: (args: ContextMenuItemSelectEventArgs) => console.log('Context action:', args.item.text)
    };

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        enable: true,
        items: ['Bold', 'Italic', 'Underline', 'Link', 'FontColor'],
        itemClick: (args: ToolbarItemClickEventArgs) => console.log('Toolbar clicked:', args.item.text)
    };

    const blockActionMenuSettings: BlockActionMenuSettingsModel = {
        enable: true,
        items: [
            { id: 'delete', label: 'Delete', iconCss: 'e-icons e-delete' },
            { id: 'duplicate', label: 'Duplicate', iconCss: 'e-icons e-copy' }
        ],
        itemSelect: (args: BlockActionItemSelectEventArgs) => console.log('Action:', args.item.id)
    };

    const transformSettings: TransformSettingsModel = {
        items: ['Paragraph', 'Heading', 'BulletList', 'Code'],
        itemSelect: (args: TransformItemSelectEventArgs) => console.log('Transform to:', args.command.id)
    };

    const blocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: ContentType.Text, content: 'Block Editor with All Menus' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [{ contentType: ContentType.Text, content: 'Try "/" for commands, right-click for context menu, or select text for the inline toolbar.' }]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            ref={editorRef}
            blocks={blocks}
            enableDragAndDrop={true}
            commandMenuSettings={commandMenuSettings}
            contextMenuSettings={contextMenuSettings}
            inlineToolbarSettings={inlineToolbarSettings}
            blockActionMenuSettings={blockActionMenuSettings}
            transformSettings={transformSettings}
        />
    );
}

export default App;
```
