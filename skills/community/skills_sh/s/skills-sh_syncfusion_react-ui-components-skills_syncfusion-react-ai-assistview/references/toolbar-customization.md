# Toolbar Customization

## Table of Contents
- [Toolbar Types Overview](#toolbar-types-overview)
- [Footer Toolbar Configuration](#footer-toolbar-configuration)
- [Header Toolbar Setup](#header-toolbar-setup)
- [Response Toolbar Items](#response-toolbar-items)
- [Custom Toolbar Items](#custom-toolbar-items)
- [Toolbar Positioning](#toolbar-positioning)
- [Icon Customization](#icon-customization)
- [Item Click Handling](#item-click-handling)

## Toolbar Types Overview

The AI AssistView component provides **four toolbar configurations**:

1. **toolbarSettings**: Header toolbar (top of component)
2. **footerToolbarSettings**: Footer toolbar (below prompt input)
3. **responseToolbarSettings**: Toolbar for each response item
4. **promptToolbarSettings**: Toolbar for each prompt item

## Footer Toolbar Configuration

### Default Footer Toolbar

By default, the footer toolbar displays the send button and attachment button (when enabled):

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            enableAttachments={true}
        />
    );
}

export default App;
```

### Customizing Footer Toolbar Items

```tsx
const footerToolbarSettings = {
    items: [
        { text: 'Send', align: 'Right' },
        { text: 'Attach', align: 'Right' }
    ]
};

<AIAssistViewComponent 
    id="aiAssistView"
    footerToolbarSettings={footerToolbarSettings}
/>
```

## Header Toolbar Setup

### Adding Header Toolbar with Refresh Button

```tsx
const toolbarSettings = {
    items: [
        { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Refresh' }
    ],
    itemClicked: (args: ToolbarItemClickedEventArgs) => {
        if (args.item.iconCss === 'e-icons e-refresh') {
            assistInstance.current.prompts = [];
        }
    }
};

<AIAssistViewComponent 
    id="aiAssistView"
    ref={assistInstance}
    toolbarSettings={toolbarSettings}
    promptRequest={handlePromptRequest}
/>
```

### Multiple Header Items

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, ToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const toolbarSettings: ToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-settings', tooltip: 'Settings' },
            { iconCss: 'e-icons e-info', tooltip: 'Help' },
            { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Clear' }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            if (args.item.iconCss === 'e-icons e-refresh') {
                assistInstance.current.prompts = [];
            } else if (args.item.iconCss === 'e-icons e-settings') {
                console.log('Settings clicked');
            } else if (args.item.iconCss === 'e-icons e-info') {
                console.log('Help clicked');
            }
        }
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            toolbarSettings={toolbarSettings}
        />
    );
}

export default App;
```

## Response Toolbar Items

### Adding Actions to Responses

Add action buttons (copy, like, dislike, etc.) to each response:

```tsx
import { AIAssistViewComponent, ResponseToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const responseToolbarSettings: ResponseToolbarSettingsModel = {
        items: [
            { type: 'Button', iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
            { type: 'Button', iconCss: 'e-icons e-assist-like', tooltip: 'Like' },
            { type: 'Button', iconCss: 'e-icons e-assist-dislike', tooltip: 'Dislike' }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            const responseText = assistInstance.current.prompts[args.dataIndex].response;
            
            if (args.item.iconCss === 'e-icons e-assist-copy') {
                navigator.clipboard.writeText(responseText);
                console.log('Response copied');
            } else if (args.item.iconCss === 'e-icons e-assist-like') {
                console.log('Response liked at index:', args.dataIndex);
            } else if (args.item.iconCss === 'e-icons e-assist-dislike') {
                console.log('Response disliked at index:', args.dataIndex);
            }
        }
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            responseToolbarSettings={responseToolbarSettings}
        />
    );
}

export default App;
```

## Toolbar Item Properties

### ToolbarItemModel Interface

Each toolbar item can be configured with the following properties:

```tsx
interface ToolbarItemModel {
    align?: ItemAlign;                      // Alignment: 'Left', 'Center', 'Right'
    cssClass?: string;                      // Custom CSS class for styling
    disabled?: boolean;                     // Whether item is disabled
    iconCss?: string;                       // CSS class for icon
    tabIndex?: number;                      // Tab order for keyboard navigation
    template?: string | function | JSX.Element;  // Custom template
    text?: string;                          // Display text
    tooltip?: string;                       // Tooltip text on hover
    type?: ItemType;                        // Item type: 'Button', 'Separator', 'Input'
    visible?: boolean;                      // Whether item is visible
}
```

### Align Property

Control the alignment of toolbar items:

```tsx
const toolbarSettings = {
    items: [
        { text: 'Left', align: 'Left' },
        { text: 'Center', align: 'Center' },
        { text: 'Right', align: 'Right' }
    ]
};

<AIAssistViewComponent 
    id="aiAssistView"
    toolbarSettings={toolbarSettings}
/>
```

**Available Alignment Values:**
- `'Left'` - Align to left side of toolbar
- `'Center'` - Align to center of toolbar
- `'Right'` - Align to right side of toolbar

### cssClass Property

Apply custom styles to individual toolbar items:

```tsx
<style>{`
    .custom-toolbar-btn {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    .danger-btn {
        background-color: #f44336;
        color: white;
    }
    
    .primary-btn {
        background-color: #2196F3;
        color: white;
        font-weight: bold;
    }
`}</style>

const toolbarSettings = {
    items: [
        { text: 'Save', cssClass: 'primary-btn' },
        { text: 'Clear', cssClass: 'danger-btn' },
        { text: 'Export', cssClass: 'custom-toolbar-btn' }
    ]
};
```

### Disabled Property

Disable toolbar items dynamically:

```tsx
import { AIAssistViewComponent, ToolbarSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [hasContent, setHasContent] = useState(false);

    const toolbarSettings: ToolbarSettingsModel = {
        items: [
            { 
                text: 'Clear', 
                iconCss: 'e-icons e-close',
                disabled: !hasContent,  // Disabled when no content
                align: 'Right'
            },
            { 
                text: 'Export', 
                iconCss: 'e-icons e-download',
                disabled: !hasContent,
                align: 'Right'
            }
        ],
        itemClicked: (args) => {
            if (args.item.text === 'Clear') {
                assistInstance.current.prompts = [];
                setHasContent(false);
            }
        }
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
            setHasContent(true);
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            toolbarSettings={toolbarSettings}
            promptRequest={handlePromptRequest}
        />
    );
}
```

### TabIndex Property

Control keyboard navigation order:

```tsx
const toolbarSettings = {
    items: [
        { text: 'First', tabIndex: 1 },
        { text: 'Second', tabIndex: 2 },
        { text: 'Third', tabIndex: 3 },
        { text: 'Settings', tabIndex: 4, align: 'Right' }
    ]
};

// Users can tab through items in order: First → Second → Third → Settings
```

**Tab Index Guidelines:**
- `0` - Default tab order (DOM order)
- `Positive numbers` - Explicit tab order
- `-1` - Remove from tab sequence

### Template Property

Create custom toolbar item templates:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [theme, setTheme] = useState('light');

    const themeToggleTemplate = () => {
        return (
            <div style={{ padding: '0 10px' }}>
                <label>
                    <input 
                        type="checkbox" 
                        checked={theme === 'dark'}
                        onChange={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                    />
                    Dark Mode
                </label>
            </div>
        );
    };

    const searchTemplate = () => {
        return (
            <input 
                type="text" 
                placeholder="Search..." 
                style={{ padding: '4px 8px', borderRadius: '4px' }}
            />
        );
    };

    const toolbarSettings = {
        items: [
            { template: searchTemplate },
            { template: themeToggleTemplate, align: 'Right' }
        ]
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            toolbarSettings={toolbarSettings}
        />
    );
}
```

### Type Property

Specify the toolbar item type:

```tsx
const toolbarSettings = {
    items: [
        { type: 'Button', text: 'Save', iconCss: 'e-icons e-save' },
        { type: 'Separator' },  // Visual separator
        { type: 'Button', text: 'Export', iconCss: 'e-icons e-download' },
        { type: 'Separator' },
        { type: 'Button', text: 'Settings', iconCss: 'e-icons e-settings', align: 'Right' }
    ]
};
```

**Available Item Types:**
- `'Button'` - Clickable button (most common)
- `'Separator'` - Visual divider between items
- `'Input'` - Input field

### Visible Property

Control item visibility dynamically:

```tsx
import React, { useState } from 'react';

function App() {
    const [isAdmin, setIsAdmin] = useState(false);
    const [hasConversation, setHasConversation] = useState(false);

    const toolbarSettings = {
        items: [
            { 
                text: 'Admin Panel', 
                iconCss: 'e-icons e-settings',
                visible: isAdmin  // Only visible for admins
            },
            { 
                text: 'Export', 
                iconCss: 'e-icons e-download',
                visible: hasConversation  // Only visible when conversation exists
            },
            { 
                text: 'Help', 
                iconCss: 'e-icons e-help',
                visible: true  // Always visible
            }
        ]
    };

    return (
        <div>
            <label>
                <input 
                    type="checkbox" 
                    checked={isAdmin}
                    onChange={(e) => setIsAdmin(e.target.checked)}
                />
                Admin Mode
            </label>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                toolbarSettings={toolbarSettings}
            />
        </div>
    );
}
```

### Complete ToolbarItemModel Example

```tsx
import { AIAssistViewComponent, ToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [isSaving, setIsSaving] = useState(false);

    const toolbarSettings: ToolbarSettingsModel = {
        items: [
            {
                text: 'Save',
                iconCss: 'e-icons e-save',
                tooltip: 'Save conversation',
                cssClass: 'primary-action',
                disabled: isSaving,
                tabIndex: 1,
                align: 'Left',
                type: 'Button',
                visible: true
            },
            {
                type: 'Separator'
            },
            {
                text: 'Export',
                iconCss: 'e-icons e-download',
                tooltip: 'Export as JSON',
                cssClass: 'secondary-action',
                tabIndex: 2,
                align: 'Left',
                type: 'Button'
            },
            {
                text: 'Settings',
                iconCss: 'e-icons e-settings',
                tooltip: 'Open settings',
                tabIndex: 3,
                align: 'Right',
                type: 'Button'
            }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            if (args.item.text === 'Save') {
                setIsSaving(true);
                saveConversation();
                setTimeout(() => setIsSaving(false), 1000);
            } else if (args.item.text === 'Export') {
                exportConversation();
            } else if (args.item.text === 'Settings') {
                openSettings();
            }
        }
    };

    const saveConversation = () => {
        const prompts = assistInstance.current?.prompts;
        localStorage.setItem('conversation', JSON.stringify(prompts));
        console.log('Conversation saved');
    };

    const exportConversation = () => {
        const prompts = assistInstance.current?.prompts;
        const json = JSON.stringify(prompts, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'conversation.json';
        link.click();
    };

    const openSettings = () => {
        console.log('Open settings panel');
    };

    return (
        <>
            <style>{`
                .primary-action {
                    background-color: #2196F3;
                    color: white;
                    font-weight: bold;
                }
                
                .secondary-action {
                    background-color: #4CAF50;
                    color: white;
                }
            `}</style>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                toolbarSettings={toolbarSettings}
            />
        </>
    );
}

export default App;
```

## Custom Toolbar Items

### Adding Custom Items to Toolbar

```tsx
import { AIAssistViewComponent, ToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const toolbarSettings: ToolbarSettingsModel = {
        items: [
            { 
                text: 'Export', 
                prefixIcon: 'e-icons e-download',
                align: 'Right'
            },
            { 
                text: 'Save', 
                prefixIcon: 'e-icons e-save',
                align: 'Right'
            }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            if (args.item.text === 'Export') {
                exportConversation();
            } else if (args.item.text === 'Save') {
                saveConversation();
            }
        }
    };

    const exportConversation = () => {
        const prompts = assistInstance.current?.prompts;
        const json = JSON.stringify(prompts, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'conversation.json';
        link.click();
    };

    const saveConversation = () => {
        const prompts = assistInstance.current?.prompts;
        localStorage.setItem('savedConversation', JSON.stringify(prompts));
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            toolbarSettings={toolbarSettings}
        />
    );
}

export default App;
```

## Toolbar Positioning

### Inline Positioning (Default)

```tsx
const footerToolbarSettings = {
    items: [
        { text: 'Send', align: 'Right' },
        { text: 'Attach', align: 'Right' }
    ],
    toolbarPosition: 'Inline'  // Default
};

<AIAssistViewComponent 
    id="aiAssistView"
    footerToolbarSettings={footerToolbarSettings}
/>
```

### Bottom Positioning

```tsx
const footerToolbarSettings = {
    items: [
        { text: 'Send', align: 'Right' },
        { text: 'Attach', align: 'Right' }
    ],
    toolbarPosition: 'Bottom'  // Dedicated footer area
};

<AIAssistViewComponent 
    id="aiAssistView"
    footerToolbarSettings={footerToolbarSettings}
/>
```

## Icon Customization

### Using Syncfusion Icons

```tsx
const toolbarSettings = {
    items: [
        { iconCss: 'e-icons e-user', tooltip: 'User' },
        { iconCss: 'e-icons e-settings', tooltip: 'Settings' },
        { iconCss: 'e-icons e-close', tooltip: 'Close' },
        { iconCss: 'e-icons e-copy', tooltip: 'Copy' },
        { iconCss: 'e-icons e-download', tooltip: 'Download' }
    ]
};
```

### Custom CSS for Icons

```tsx
<style>{`
    .custom-refresh::before {
        content: '🔄';
        font-size: 18px;
    }
    .custom-save::before {
        content: '💾';
        font-size: 18px;
    }
    .custom-export::before {
        content: '📤';
        font-size: 18px;
    }
`}</style>

const toolbarSettings = {
    items: [
        { iconCss: 'custom-refresh', tooltip: 'Refresh' },
        { iconCss: 'custom-save', tooltip: 'Save' },
        { iconCss: 'custom-export', tooltip: 'Export' }
    ]
};
```

## Item Click Handling

### Accessing Item Click Data

```tsx
const handleItemClick = (args: ToolbarItemClickedEventArgs) => {
    console.log('Clicked item:', args.item);
    console.log('Item text:', args.item.text);
    console.log('Item icon:', args.item.iconCss);
    console.log('Item tooltip:', args.item.tooltip);
    
    // For response/prompt toolbars, access the associated item
    if ('dataIndex' in args) {
        console.log('Associated index:', args.dataIndex);
    }
};
```

### Practical Item Click Examples

```tsx
const responseToolbarSettings: ResponseToolbarSettingsModel = {
    items: [
        { type: 'Button', iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
        { type: 'Button', iconCss: 'e-icons e-edit', tooltip: 'Edit' },
        { type: 'Button', iconCss: 'e-icons e-delete', tooltip: 'Delete' }
    ],
    itemClicked: (args: ToolbarItemClickedEventArgs) => {
        const index = args.dataIndex;
        const responseItem = assistInstance.current.prompts[index];
        
        switch (args.item.iconCss) {
            case 'e-icons e-assist-copy':
                copyToClipboard(responseItem.response);
                break;
            case 'e-icons e-edit':
                editResponse(index);
                break;
            case 'e-icons e-delete':
                deleteResponse(index);
                break;
        }
    }
};
```

## Complete Toolbar Example

```tsx
import { 
    AIAssistViewComponent, 
    PromptRequestEventArgs,
    ToolbarSettingsModel,
    ResponseToolbarSettingsModel,
    FooterToolbarSettingsModel,
    ToolbarItemClickedEventArgs
} from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const toolbarSettings: ToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-settings' },
            { iconCss: 'e-icons e-refresh', align: 'Right' }
        ],
        itemClicked: (args) => handleHeaderToolbarClick(args)
    };

    const responseToolbarSettings: ResponseToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
            { iconCss: 'e-icons e-assist-like', tooltip: 'Like' },
            { iconCss: 'e-icons e-assist-dislike', tooltip: 'Dislike' }
        ],
        itemClicked: (args) => handleResponseToolbarClick(args)
    };

    const handleHeaderToolbarClick = (args: ToolbarItemClickedEventArgs) => {
        if (args.item.iconCss?.includes('refresh')) {
            assistInstance.current.prompts = [];
        }
    };

    const handleResponseToolbarClick = (args: ToolbarItemClickedEventArgs) => {
        const response = assistInstance.current.prompts[args.dataIndex].response;
        if (args.item.iconCss?.includes('copy')) {
            navigator.clipboard.writeText(response);
        }
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            toolbarSettings={toolbarSettings}
            responseToolbarSettings={responseToolbarSettings}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Best Practices

**Keep toolbars minimal**: Show only essential actions  
**Use clear icons**: Recognize at a glance what action performs  
**Add tooltips**: Help users understand toolbar items  
**Group by function**: Related items together  
**Handle errors gracefully**: Show feedback for toolbar actions  
**Disable when needed**: Disable unavailable actions appropriately
