# Inline Toolbar Customization

## Table of Contents
- [Overview](#overview)
- [Built-in Toolbar Items](#built-in-toolbar-items)
- [Toolbar Item Properties](#toolbar-item-properties)
- [Item Types](#item-types)
- [Configuring Toolbar Items](#configuring-toolbar-items)
- [Toolbar Positioning](#toolbar-positioning)
- [Tab Navigation](#tab-navigation)
- [Custom Templates](#custom-templates)
- [Event Handling](#event-handling)
- [Complete Examples](#complete-examples)

## Overview

The inline toolbar appears at the bottom of the prompt input area. By default, it contains a "Send" button. You can customize it by adding custom buttons, separators, input fields, or even custom templates for more complex interactions.

Toolbar configuration uses the `inlineToolbarSettings` property with the `InlineToolbarSettingsModel` interface.

## Built-in Toolbar Items

The component includes one built-in toolbar item by default:

| Item | Type | Action | Purpose |
|------|------|--------|---------|
| `send` | Button | Submits prompt | Triggers the promptRequest event |

This send button appears automatically in all modes.

## Toolbar Item Properties

Each toolbar item (custom or modified) supports these properties:

| Property | Type | Enum | Description |
|----------|------|------|-------------|
| `id` | string | - | Unique identifier for the item |
| `text` | string | - | Display text (for buttons, labels) |
| `iconCss` | string | - | CSS class for icon display |
| `type` | string | Button, Separator, Input | Item type determines rendering |
| `visible` | boolean | - | Show/hide item (default: true) |
| `disabled` | boolean | - | Enable/disable interaction |
| `align` | string | Left, Center, Right | Horizontal alignment |
| `tooltip` | string | - | Tooltip on hover |
| `cssClass` | string | - | Additional CSS classes |
| `tabIndex` | number | - | Tab key navigation order |
| `template` | string \| React.Component | - | Custom HTML or React component |

## Item Types

### Type: Button

Standard clickable button:

```tsx
{
    id: 'clear',
    text: 'Clear',
    type: 'Button',
    iconCss: 'e-icons e-close'
}
```

### Type: Separator

Visual separator between items:

```tsx
{
    type: 'Separator'
}
```

### Type: Input

Input field for user interaction:

```tsx
{
    id: 'max-tokens',
    type: 'Input',
    text: 'Max tokens'
}
```

## Configuring Toolbar Items

### Basic Toolbar Customization

```tsx
import { InlineAIAssistComponent, InlineToolbarSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            {
                id: 'save-prompt',
                text: 'Save',
                type: 'Button',
                iconCss: 'e-icons e-save',
                tooltip: 'Save this prompt for later'
            },
            {
                id: 'history',
                text: 'History',
                type: 'Button',
                iconCss: 'e-icons e-history',
                tooltip: 'View prompt history'
            },
            {
                type: 'Separator'
            },
            {
                id: 'settings',
                text: 'Settings',
                type: 'Button',
                iconCss: 'e-icons e-settings',
                align: 'Right'
            }
        ]
    };

    return (
        <InlineAIAssistComponent inlineToolbarSettings={inlineToolbarSettings} />
    );
};

export default App;
```

### Toolbar Items with Icons

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'bold',
            iconCss: 'e-icons e-bold',
            type: 'Button',
            tooltip: 'Bold'
        },
        {
            id: 'italic',
            iconCss: 'e-icons e-italic',
            type: 'Button',
            tooltip: 'Italic'
        },
        {
            id: 'underline',
            iconCss: 'e-icons e-underline',
            type: 'Button',
            tooltip: 'Underline'
        },
        {
            type: 'Separator'
        },
        {
            id: 'clear-format',
            text: 'Clear',
            type: 'Button',
            iconCss: 'e-icons e-close'
        }
    ]
};
```

### Conditional Visibility

```tsx
const App: React.FC = () => {
    const [isLoggedIn, setIsLoggedIn] = React.useState(false);

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            {
                id: 'save',
                text: 'Save',
                type: 'Button',
                visible: isLoggedIn  // Only show if logged in
            },
            {
                id: 'clear',
                text: 'Clear',
                type: 'Button'
            }
        ]
    };

    return (
        <InlineAIAssistComponent inlineToolbarSettings={inlineToolbarSettings} />
    );
};
```

### Disabling Toolbar Items

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'undo',
            text: 'Undo',
            type: 'Button',
            disabled: true  // Button is disabled
        },
        {
            id: 'redo',
            text: 'Redo',
            type: 'Button',
            disabled: false
        }
    ]
};
```

## Toolbar Positioning

Control where the toolbar appears using the `toolbarPosition` property:

### Position: Inline (Default)

Toolbar items render inline with the input field:

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    toolbarPosition: 'Inline',  // or omit (default)
    items: [
        { id: 'btn1', text: 'Button 1', type: 'Button' }
    ]
};
```

**Appearance:** Buttons appear in same row as input, compact layout

### Position: Bottom

Toolbar renders in a dedicated footer area below the input:

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    toolbarPosition: 'Bottom',
    items: [
        { id: 'save', text: 'Save', type: 'Button' },
        { id: 'cancel', text: 'Cancel', type: 'Button' }
    ]
};
```

**Appearance:** Full-width footer bar with buttons

### Choosing Positions

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    toolbarPosition: 'Bottom',  // Use when you have many toolbar items
    items: [
        { id: 'save', text: 'Save' },
        { id: 'draft', text: 'Draft' },
        { id: 'preview', text: 'Preview' },
        { id: 'settings', text: 'Settings' },
        { id: 'help', text: 'Help' }
    ]
};
```

## Tab Navigation

Enable keyboard navigation using Tab key with the `tabIndex` property:

### Basic Tab Navigation

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'button1',
            text: 'First Button',
            type: 'Button',
            tabIndex: 1  // First in tab order
        },
        {
            id: 'button2',
            text: 'Second Button',
            type: 'Button',
            tabIndex: 2  // Second in tab order
        }
    ]
};
```

### Tab Navigation Rules

- **Positive tabIndex:** Follows specified order (1, 2, 3...)
- **tabIndex: 0:** Uses DOM order for navigation
- **Negative tabIndex:** Item not in tab order (keyboard inaccessible)
- **No tabIndex:** Default behavior (uses DOM order)

### Example: Custom Tab Order

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'save',
            text: 'Save',
            tabIndex: 1  // First focus
        },
        {
            id: 'cancel',
            text: 'Cancel',
            tabIndex: 2  // Second focus
        },
        {
            id: 'help',
            text: 'Help',
            tabIndex: 3  // Third focus
        }
    ]
};
```

## Custom Templates

Use the `template` property for complex item rendering:

### String Template

```tsx
const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'custom-btn',
            template: '<button class="e-btn e-small"><span class="e-icons">✨</span> AI</button>'
        }
    ]
};
```

### React Component Template

```tsx
const CustomToolbarItem: React.FC = () => {
    return (
        <button className="e-btn e-small">
            <span>⚡</span> Quick Action
        </button>
    );
};

const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        {
            id: 'custom-item',
            template: <CustomToolbarItem />
        }
    ]
};
```

### Template with State

```tsx
const App: React.FC = () => {
    const [promptCount, setPromptCount] = React.useState(0);

    const PromptCounterTemplate: React.FC = () => {
        return (
            <span className="prompt-counter">
                Prompts: {promptCount}
            </span>
        );
    };

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            {
                id: 'counter',
                template: <PromptCounterTemplate />
            }
        ]
    };

    return (
        <InlineAIAssistComponent inlineToolbarSettings={inlineToolbarSettings} />
    );
};
```

## Event Handling

Handle toolbar item clicks using the `itemClick` event:

### ToolbarItemClickEventArgs Properties

The `itemClick` event provides detailed information about the clicked toolbar item:

```tsx
interface ToolbarItemClickEventArgs {
    cancel: boolean;           // Set to true to cancel the default action
    dataIndex: number;         // Index of the message data (not applicable for inline toolbar)
    event: Event;              // Native browser click event
    item: ToolbarItemModel;    // The toolbar item that was clicked
    name: string;              // Event name ('itemClick')
}
```

#### Property Details

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | boolean | Set to `true` to prevent default toolbar item action. Default: `false` |
| `dataIndex` | number | Index of associated message data. **Note:** Not applicable for inline toolbar items (always undefined in this context) |
| `event` | Event | Native browser event object for the click |
| `item` | ToolbarItemModel | Complete toolbar item model including id, text, iconCss, etc. |
| `name` | string | Name of the event, always `'itemClick'` |

### Basic Item Click Handler

```tsx
import { ToolbarItemClickEventArgs } from '@syncfusion/ej2-react-interactive-chat';

const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
    console.log('Toolbar item clicked:', args.item.id);
    console.log('Item text:', args.item.text);
    console.log('Event name:', args.name);
};

const inlineToolbarSettings: InlineToolbarSettingsModel = {
    items: [
        { id: 'save', text: 'Save', type: 'Button' }
    ],
    itemClick: handleToolbarItemClick
};

<InlineAIAssistComponent inlineToolbarSettings={inlineToolbarSettings} />
```

### Using cancel Property

Prevent the default action by setting `cancel` to `true`:

```tsx
const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
    // Validate before allowing action
    if (args.item.id === 'submit' && !isFormValid()) {
        args.cancel = true;  // Prevent default action
        alert('Please fill all required fields');
        return;
    }
    
    // Proceed with action
    processToolbarAction(args.item.id);
};
```

### Using event Property

Access the native browser event for advanced scenarios:

```tsx
const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
    // Check modifier keys
    if (args.event instanceof MouseEvent) {
        if (args.event.ctrlKey) {
            console.log('Ctrl + Click detected');
            openInNewTab(args.item.id);
            return;
        }
        
        if (args.event.shiftKey) {
            console.log('Shift + Click detected');
            selectMultiple(args.item.id);
            return;
        }
    }
    
    // Get click coordinates
    const clickX = (args.event as MouseEvent).clientX;
    const clickY = (args.event as MouseEvent).clientY;
    console.log(`Clicked at: (${clickX}, ${clickY})`);
    
    // Normal click
    handleNormalClick(args.item.id);
};
```

### Using item Property

Access complete toolbar item details:

```tsx
const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
    const { item } = args;
    
    console.log('Item ID:', item.id);
    console.log('Item Text:', item.text);
    console.log('Item Type:', item.type);
    console.log('Item Icon:', item.iconCss);
    console.log('Item Disabled:', item.disabled);
    console.log('Item Tooltip:', item.tooltip);
    
    // Use item properties for conditional logic
    if (item.disabled) {
        console.log('Item is disabled, should not trigger');
        return;
    }
    
    // Execute action based on item type
    if (item.type === 'Button') {
        executeButtonAction(item.id);
    }
};
```

### Using name Property

Check event type for multi-event handlers:

```tsx
const handleToolbarEvent = (args: ToolbarItemClickEventArgs) => {
    // Verify it's an itemClick event
    if (args.name === 'itemClick') {
        console.log('Item click event confirmed');
        processItemClick(args.item);
    }
    
    // Log event name for debugging
    console.log(`Event triggered: ${args.name}`);
};
```

### Complete Event Args Example

```tsx
const CompleteEventExample: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [clickLog, setClickLog] = React.useState<string[]>([]);

    const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
        // Log all event properties
        const logEntry = `
            Event: ${args.name}
            Item ID: ${args.item.id}
            Item Text: ${args.item.text}
            Cancelled: ${args.cancel}
            DataIndex: ${args.dataIndex}
            Event Type: ${args.event.type}
            Timestamp: ${new Date().toLocaleTimeString()}
        `;
        
        setClickLog(prev => [logEntry, ...prev]);
        
        // Conditional cancellation
        if (args.item.id === 'delete') {
            const confirmed = confirm('Are you sure you want to delete?');
            if (!confirmed) {
                args.cancel = true;  // Cancel the action
                return;
            }
        }
        
        // Handle based on modifier keys
        if (args.event instanceof MouseEvent) {
            if (args.event.ctrlKey && args.item.id === 'open') {
                console.log('Opening in new window...');
                args.cancel = true;  // Prevent default, handle custom
                window.open('/new-window', '_blank');
                return;
            }
        }
        
        // Normal processing
        console.log(`Processing: ${args.item.id}`);
    };

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            { id: 'save', text: 'Save', type: 'Button' },
            { id: 'open', text: 'Open', type: 'Button' },
            { id: 'delete', text: 'Delete', type: 'Button' }
        ],
        itemClick: handleToolbarItemClick
    };

    return (
        <div>
            <InlineAIAssistComponent
                ref={assistRef}
                inlineToolbarSettings={inlineToolbarSettings}
            />
            
            <div className="event-log">
                <h4>Event Log:</h4>
                {clickLog.map((log, index) => (
                    <pre key={index}>{log}</pre>
                ))}
            </div>
        </div>
    );
};
```

### Advanced Click Handler with Logic

```tsx
const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
    // Access all properties
    const { item, event, cancel, name, dataIndex } = args;
    
    console.log(`Event: ${name}`);
    console.log(`Item: ${item.id}`);
    console.log(`DataIndex: ${dataIndex}`); // undefined for inline toolbar
    
    switch (item.id) {
        case 'save':
            saveCurrentPrompt();
            break;
        case 'clear':
            clearInput();
            break;
        case 'history':
            showPromptHistory();
            break;
        default:
            console.log('Unknown toolbar action');
    }
};
```

### Validation Example

```tsx
const ValidationExample: React.FC = () => {
    const [isValid, setIsValid] = React.useState(false);

    const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
        // Prevent submission if validation fails
        if (args.item.id === 'submit' && !isValid) {
            args.cancel = true;
            alert('Form validation failed. Please check your input.');
            return;
        }
        
        // Confirm dangerous actions
        if (args.item.id === 'reset') {
            const confirmed = confirm('This will reset all data. Continue?');
            if (!confirmed) {
                args.cancel = true;
                return;
            }
        }
        
        // Proceed with action
        console.log(`Action: ${args.item.id}`);
    };

    return (
        <InlineAIAssistComponent
            inlineToolbarSettings={{
                items: [
                    { id: 'submit', text: 'Submit', type: 'Button' },
                    { id: 'reset', text: 'Reset', type: 'Button' }
                ],
                itemClick: handleToolbarItemClick
            }}
        />
    );
};
```

### Analytics Tracking Example

```tsx
const AnalyticsExample: React.FC = () => {
    const handleToolbarItemClick = (args: ToolbarItemClickEventArgs) => {
        // Track to analytics
        analytics.track('toolbar_item_clicked', {
            itemId: args.item.id,
            itemText: args.item.text,
            eventName: args.name,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent
        });
        
        // Log click position for heatmap
        if (args.event instanceof MouseEvent) {
            heatmap.track({
                x: args.event.clientX,
                y: args.event.clientY,
                element: args.item.id
            });
        }
        
        // Normal action handling
        processToolbarAction(args.item.id);
    };

    return (
        <InlineAIAssistComponent
            inlineToolbarSettings={{
                items: [
                    { id: 'action1', text: 'Action 1', type: 'Button' },
                    { id: 'action2', text: 'Action 2', type: 'Button' }
                ],
                itemClick: handleToolbarItemClick
            }}
        />
    );
};
```

## Complete Examples

### Example 1: Content Editor Toolbar

```tsx
const ContentEditor: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        toolbarPosition: 'Bottom',
        items: [
            {
                id: 'format-bold',
                iconCss: 'e-icons e-bold',
                type: 'Button',
                tooltip: 'Bold',
                align: 'Left'
            },
            {
                id: 'format-italic',
                iconCss: 'e-icons e-italic',
                type: 'Button',
                tooltip: 'Italic'
            },
            {
                type: 'Separator'
            },
            {
                id: 'clear',
                text: 'Clear',
                type: 'Button',
                align: 'Right'
            },
            {
                id: 'submit',
                text: 'Submit',
                type: 'Button',
                align: 'Right'
            }
        ],
        itemClick: (args) => {
            switch (args.item.id) {
                case 'format-bold':
                    document.execCommand('bold');
                    break;
                case 'format-italic':
                    document.execCommand('italic');
                    break;
                case 'clear':
                    assistRef.current?.hidePopup();
                    break;
                case 'submit':
                    assistRef.current?.showPopup();
                    break;
            }
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            inlineToolbarSettings={inlineToolbarSettings}
        />
    );
};
```

### Example 2: Development Assistant Toolbar

```tsx
const CodeAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            {
                id: 'format-json',
                text: 'Format JSON',
                type: 'Button',
                iconCss: 'e-icons e-settings'
            },
            {
                id: 'validate',
                text: 'Validate',
                type: 'Button',
                iconCss: 'e-icons e-check-box'
            },
            {
                type: 'Separator'
            },
            {
                id: 'minify',
                text: 'Minify',
                type: 'Button',
                align: 'Right'
            }
        ],
        itemClick: (args) => {
            if (args.item.id === 'format-json') {
                assistRef.current?.executePrompt('Format this JSON code');
            } else if (args.item.id === 'validate') {
                assistRef.current?.executePrompt('Validate this code');
            }
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            inlineToolbarSettings={inlineToolbarSettings}
        />
    );
};
```

### Example 3: Input Field Toolbar

```tsx
const PromptWithSettings: React.FC = () => {
    const inlineToolbarSettings: InlineToolbarSettingsModel = {
        items: [
            {
                id: 'temperature',
                text: 'Temperature',
                type: 'Input'
            },
            {
                type: 'Separator'
            },
            {
                id: 'quick-prompt',
                text: 'Quick',
                type: 'Button',
                iconCss: 'e-icons e-lightning'
            },
            {
                id: 'detailed-prompt',
                text: 'Detailed',
                type: 'Button',
                iconCss: 'e-icons e-list'
            }
        ]
    };

    return (
        <InlineAIAssistComponent inlineToolbarSettings={inlineToolbarSettings} />
    );
};
```

## Best Practices

1. **Clear Icons:** Use consistent Syncfusion icon set
2. **Descriptive Tooltips:** Help users understand button purpose
3. **Logical Grouping:** Use separators to organize related items
4. **Alignment:** Use `align: 'Right'` for secondary actions
5. **Tab Order:** Set `tabIndex` for important interactive items
6. **Responsive:** Consider mobile devices (fewer items, larger buttons)
7. **Accessibility:** Always include tooltips for icon-only buttons
8. **Performance:** Avoid complex templates in toolbar items
9. **Consistency:** Match your app's design language
10. **User Feedback:** Visual feedback when items are clicked
