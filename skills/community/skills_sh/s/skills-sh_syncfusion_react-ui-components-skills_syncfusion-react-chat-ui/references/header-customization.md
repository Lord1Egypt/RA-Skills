---
name: header-customization
description: Customize Chat-UI header with text, icons, and toolbar items for enhanced user experience.
---

# Header Customization

## Table of Contents
- [Header Visibility](#header-visibility)
- [Header Text and Icon](#header-text-and-icon)
- [Toolbar Configuration](#toolbar-configuration)
- [Toolbar Item Types](#toolbar-item-types)
- [Toolbar Item Properties](#toolbar-item-properties)
- [Toolbar Click Events](#toolbar-click-events)

## Header Visibility

### Show or Hide Header

Control whether the header section is displayed:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            {/* Header visible (default) */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                showHeader={true}
            />

            {/* Header hidden */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                showHeader={false}
            />
        </>
    );
}
```

## Header Text and Icon

### Set Header Title

Display a title in the header:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerText="Customer Support"
        />
    );
}
```

### Set Header Icon

Add an icon to the header:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerText="Support Team"
            headerIconCss="e-icons e-people"
        />
    );
}
```

### Available Header Icons

Common icon classes:
- `e-people` - Group/team
- `e-person` - Single user
- `e-chat` - Chat bubble
- `e-phone` - Phone
- `e-mail` - Email
- `e-info` - Information
- `e-home` - Home

## Toolbar Configuration

### Basic Toolbar Setup

Add toolbar items to the header:

```tsx
import { ChatUIComponent, ToolbarSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const headerToolbar: ToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Refresh' },
            { iconCss: 'e-icons e-menu', align: 'Right', tooltip: 'Menu' }
        ]
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerToolbar={headerToolbar}
        />
    );
}
```

## Toolbar Item Types

### Button Items

Regular clickable buttons:

```tsx
const headerToolbar: ToolbarSettingsModel = {
    items: [
        { type: 'Button', iconCss: 'e-icons e-refresh', tooltip: 'Refresh' },
        { type: 'Button', text: 'Help', align: 'Right' }
    ]
};
```

### Separator

Visual separator between toolbar items:

```tsx
const headerToolbar: ToolbarSettingsModel = {
    items: [
        { iconCss: 'e-icons e-search' },
        { type: 'Separator' },
        { iconCss: 'e-icons e-user', align: 'Right' }
    ]
};
```

### Input Items

For custom input elements:

```tsx
const headerToolbar: ToolbarSettingsModel = {
    items: [
        { type: 'Input', template: '<input type="text" placeholder="Search..." />' }
    ]
};
```

## Toolbar Item Properties

### Icon CSS

Set icon styling:

```tsx
const item = {
    iconCss: 'e-icons e-menu'
};
```

### Text

Display text label:

```tsx
const item = {
    text: 'Options',
    align: 'Right'
};
```

### Tooltip

Show tooltip on hover:

```tsx
const item = {
    iconCss: 'e-icons e-refresh',
    tooltip: 'Refresh conversation',
    align: 'Right'
};
```

### Alignment

Position item in toolbar:

```tsx
// Left alignment (default)
{ iconCss: 'e-icons e-search', align: 'Left' }

// Center alignment
{ iconCss: 'e-icons e-info', align: 'Center' }

// Right alignment
{ iconCss: 'e-icons e-user', align: 'Right' }
```

### Visibility

Show or hide toolbar item:

```tsx
const item = {
    iconCss: 'e-icons e-menu',
    visible: true  // or false
};
```

### Disabled State

Disable toolbar item:

```tsx
const item = {
    iconCss: 'e-icons e-refresh',
    disabled: false  // or true
};
```

### CSS Class

Apply custom styling:

```tsx
const item = {
    iconCss: 'e-icons e-user',
    cssClass: 'custom-toolbar-item'
};
```

### Tab Index

Enable keyboard navigation:

```tsx
const item = {
    text: 'Settings',
    tabIndex: 1
};
```

## Toolbar Click Events

### Handle Toolbar Item Click

```tsx
import { ChatUIComponent, ToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleToolbarClick = (args: ToolbarItemClickedEventArgs) => {
        console.log('Toolbar item clicked:', args.item);
        
        if (args.item.iconCss === 'e-icons e-refresh') {
            console.log('Refresh clicked');
            // Reload conversation
        } else if (args.item.text === 'Close') {
            console.log('Close clicked');
            // Close chat
        }
    };

    const headerToolbar: ToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Refresh' },
            { text: 'Close', align: 'Right' }
        ],
        itemClicked: handleToolbarClick
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerToolbar={headerToolbar}
        />
    );
}
```

## Complete Header Example

### Full Customization

```tsx
import { ChatUIComponent, ToolbarSettingsModel, ToolbarItemClickedEventArgs, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const chatRef = useRef(null);
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleToolbarClick = (args: ToolbarItemClickedEventArgs) => {
        if (args.item.iconCss === 'e-icons e-refresh') {
            setIsRefreshing(true);
            setTimeout(() => setIsRefreshing(false), 1000);
            console.log('Refreshing...');
        }
        else if (args.item.text === 'Info') {
            alert('Syncfusion Chat Support');
        }
        else if (args.item.text === 'Settings') {
            console.log('Open settings');
        }
    };

    const headerToolbar: ToolbarSettingsModel = {
        items: [
            { text: 'Info', align: 'Right', tooltip: 'Chat information' },
            { type: 'Separator' },
            { text: 'Settings', align: 'Right', tooltip: 'Settings' },
            { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Refresh' }
        ],
        itemClicked: handleToolbarClick
    };

    return (
        <ChatUIComponent 
            ref={chatRef}
            user={{ id: "user1", user: "Albert" }}
            headerText="Support Chat"
            headerIconCss="e-icons e-chat"
            showHeader={true}
            headerToolbar={headerToolbar}
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Welcome to support!" 
                    author={{ id: "agent", user: "Support" }}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

### Custom CSS for Toolbar

```css
/* Style toolbar items */
.custom-toolbar-item {
    font-weight: 500;
}

.custom-toolbar-item:hover {
    background-color: #f0f0f0;
    cursor: pointer;
}

.custom-toolbar-item.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Style specific icons */
.e-icons.e-refresh {
    transition: transform 0.3s ease;
}

.e-icons.e-refresh:hover {
    transform: rotate(180deg);
}
```

## Dynamic Toolbar Management

### Enable/Disable Toolbar Items

```tsx
function App() {
    const [toolbarConfig, setToolbarConfig] = useState<ToolbarSettingsModel>({
        items: [
            { iconCss: 'e-icons e-refresh', disabled: false },
            { text: 'Archive', disabled: false }
        ]
    });

    const toggleItemDisabled = (index: number) => {
        const newItems = [...toolbarConfig.items];
        newItems[index].disabled = !newItems[index].disabled;
        setToolbarConfig({ ...toolbarConfig, items: newItems });
    };

    return (
        <>
            <button onClick={() => toggleItemDisabled(0)}>
                Toggle Refresh
            </button>
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                headerToolbar={toolbarConfig}
            />
        </>
    );
}
```

## Best Practices

1. **Use intuitive icons** for toolbar items
2. **Provide tooltips** for clarity
3. **Group related items** together
4. **Use separator** to organize toolbar logically
5. **Disable items** when not available
6. **Align important items** to the right
7. **Test keyboard navigation** with tab keys
