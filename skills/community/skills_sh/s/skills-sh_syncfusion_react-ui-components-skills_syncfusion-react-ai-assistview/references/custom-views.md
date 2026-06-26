# Custom Views

## Table of Contents
- [Multiple View Architecture](#multiple-view-architecture)
- [View Types](#view-types)
- [Creating Views with ViewDirective](#creating-views-with-viewdirective)
- [Setting View Names](#setting-view-names)
- [Customizing View Icons](#customizing-view-icons)
- [View Templates](#view-templates)
- [Setting Active View](#setting-active-view)
- [Switching Between Views](#switching-between-views)
- [Use Cases](#use-cases)

## Multiple View Architecture

The AI AssistView supports multiple views, allowing you to organize different content within the same component:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent id="aiAssistView">
            <ViewsDirective>
                <ViewDirective type='Assist'></ViewDirective>
                <ViewDirective type='Custom'></ViewDirective>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

## View Types

### Assist View

The standard conversation view for prompts and responses:

```tsx
<ViewDirective 
    type='Assist'
    name='Chat'
    iconCss='e-assistview-icon'
/>
```

### Custom View

A custom content panel for additional features:

```tsx
<ViewDirective 
    type='Custom'
    name='Settings'
    iconCss='e-icons e-settings'
/>
```

## Creating Views with ViewDirective

### Basic View Setup

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent id="aiAssistView">
            <ViewsDirective>
                <ViewDirective type='Assist'></ViewDirective>
                <ViewDirective type='Custom'></ViewDirective>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

## Setting View Names

### Name Property

The `name` property sets the header label for each view:

```tsx
<AIAssistViewComponent id="aiAssistView">
    <ViewsDirective>
        <ViewDirective 
            type='Assist' 
            name='Conversation'
        />
        <ViewDirective 
            type='Custom' 
            name='Settings'
        />
        <ViewDirective 
            type='Custom' 
            name='History'
        />
    </ViewsDirective>
</AIAssistViewComponent>
```

## Customizing View Icons

### Using Icon Classes

Customize view icons with CSS classes:

```tsx
<AIAssistViewComponent id="aiAssistView">
    <ViewsDirective>
        <ViewDirective 
            type='Assist' 
            name='Chat' 
            iconCss='e-assistview-icon'
        />
        <ViewDirective 
            type='Custom' 
            name='Settings' 
            iconCss='e-icons e-settings'
        />
        <ViewDirective 
            type='Custom' 
            name='History' 
            iconCss='e-icons e-history'
        />
    </ViewsDirective>
</AIAssistViewComponent>
```

### Available Icon Classes

```
e-assistview-icon     - AI Assistant
e-icons e-settings    - Settings/gear
e-icons e-history     - History
e-icons e-info        - Information
e-icons e-help        - Help
e-icons e-download    - Download
e-icons e-upload      - Upload
e-icons e-user        - User
```

### Custom Icons

```tsx
<style>{`
    .custom-chat-icon::before { content: '💬'; font-size: 16px; }
    .custom-settings-icon::before { content: '⚙️'; font-size: 16px; }
    .custom-history-icon::before { content: '📜'; font-size: 16px; }
`}</style>

<ViewDirective 
    type='Assist' 
    name='Chat' 
    iconCss='custom-chat-icon'
/>
<ViewDirective 
    type='Custom' 
    name='Settings' 
    iconCss='custom-settings-icon'
/>
```

## View Templates

### Setting Custom View Content

The `viewTemplate` property allows custom HTML content for views:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const settingsTemplate = `
        <div class="settings-panel">
            <h3>Settings</h3>
            <div class="setting-item">
                <label>Theme:</label>
                <select>
                    <option>Light</option>
                    <option>Dark</option>
                </select>
            </div>
            <div class="setting-item">
                <label>Language:</label>
                <select>
                    <option>English</option>
                    <option>Spanish</option>
                </select>
            </div>
        </div>
    `;

    const historyTemplate = `
        <div class="history-panel">
            <h3>Conversation History</h3>
            <div class="history-list">
                <p>Previous conversations will appear here</p>
            </div>
        </div>
    `;

    return (
        <AIAssistViewComponent id="aiAssistView">
            <ViewsDirective>
                <ViewDirective type='Assist' name='Chat'/>
                <ViewDirective 
                    type='Custom' 
                    name='Settings' 
                    iconCss='e-icons e-settings'
                    viewTemplate={settingsTemplate}
                />
                <ViewDirective 
                    type='Custom' 
                    name='History' 
                    iconCss='e-icons e-history'
                    viewTemplate={historyTemplate}
                />
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

### Dynamic Template Content

```tsx
const getSettingsTemplate = (user: any) => {
    return `
        <div class="settings-panel">
            <h3>Settings for ${user.name}</h3>
            <div>
                <label>Email: ${user.email}</label>
            </div>
            <div>
                <label>Language: ${user.language}</label>
            </div>
        </div>
    `;
};

<ViewDirective 
    type='Custom' 
    name='Settings' 
    viewTemplate={getSettingsTemplate(currentUser)}
/>
```

## Setting Active View

### ActiveView Property

The `activeView` property specifies which view is displayed when the component loads. It uses zero-based indexing to refer to views in the order they're defined.

**Type:** `number`  
**Default:** `0` (first view)

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            activeView={0}  // Show first view (Assist) on load
        >
            <ViewsDirective>
                <ViewDirective type='Assist' name='Chat'/>
                <ViewDirective type='Custom' name='Settings'/>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

### View Index Values

```tsx
activeView={0}  // First view (index 0)
activeView={1}  // Second view (index 1)
activeView={2}  // Third view (index 2)
// etc.
```

### Setting Initial View on Load

Control which view users see first:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    // Open directly to Settings view (index 1)
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            activeView={1}
        >
            <ViewsDirective>
                <ViewDirective type='Assist' name='Chat' iconCss='e-assistview-icon'/>
                <ViewDirective type='Custom' name='Settings' iconCss='e-icons e-settings'/>
                <ViewDirective type='Custom' name='History' iconCss='e-icons e-history'/>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

### Conditional Initial View

Set initial view based on user preferences or application state:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [initialView, setInitialView] = useState(0);

    useEffect(() => {
        // Load user's last view from localStorage
        const savedView = localStorage.getItem('lastActiveView');
        if (savedView) {
            setInitialView(parseInt(savedView, 10));
        }
    }, []);

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            activeView={initialView}
        >
            <ViewsDirective>
                <ViewDirective type='Assist' name='Chat'/>
                <ViewDirective type='Custom' name='Settings'/>
                <ViewDirective type='Custom' name='History'/>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}

export default App;
```

### Dynamic View Selection Based on Role

```tsx
function App() {
    const userRole = getUserRole(); // Your function to get user role
    
    // Admins see settings first, users see chat first
    const initialView = userRole === 'admin' ? 1 : 0;

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            activeView={initialView}
        >
            <ViewsDirective>
                <ViewDirective type='Assist' name='Chat'/>
                <ViewDirective type='Custom' name='Admin Settings'/>
            </ViewsDirective>
        </AIAssistViewComponent>
    );
}
```

## Switching Between Views

### Programmatic View Switching

Change the active view dynamically using the component reference:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const switchToSettings = () => {
        if (assistInstance.current) {
            assistInstance.current.activeView = 1;  // Switch to Settings (index 1)
        }
    };

    const switchToChat = () => {
        if (assistInstance.current) {
            assistInstance.current.activeView = 0;  // Switch to Chat (index 0)
        }
    };

    const switchToHistory = () => {
        if (assistInstance.current) {
            assistInstance.current.activeView = 2;  // Switch to History (index 2)
        }
    };

    return (
        <div>
            <div className="view-switcher">
                <button onClick={switchToChat}>Chat</button>
                <button onClick={switchToSettings}>Settings</button>
                <button onClick={switchToHistory}>History</button>
            </div>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                activeView={0}
            >
                <ViewsDirective>
                    <ViewDirective type='Assist' name='Chat'/>
                    <ViewDirective type='Custom' name='Settings'/>
                    <ViewDirective type='Custom' name='History'/>
                </ViewsDirective>
            </AIAssistViewComponent>
        </div>
    );
}

export default App;
```

### Switch View with State Persistence

Save the current view when switching:

```tsx
import { AIAssistViewComponent, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [currentView, setCurrentView] = useState(0);

    const switchView = (viewIndex: number) => {
        if (assistInstance.current) {
            assistInstance.current.activeView = viewIndex;
            setCurrentView(viewIndex);
            
            // Save to localStorage
            localStorage.setItem('lastActiveView', viewIndex.toString());
        }
    };

    return (
        <div>
            <div className="view-tabs">
                <button 
                    className={currentView === 0 ? 'active' : ''}
                    onClick={() => switchView(0)}
                >
                    Chat
                </button>
                <button 
                    className={currentView === 1 ? 'active' : ''}
                    onClick={() => switchView(1)}
                >
                    Settings
                </button>
                <button 
                    className={currentView === 2 ? 'active' : ''}
                    onClick={() => switchView(2)}
                >
                    History
                </button>
            </div>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                activeView={currentView}
            >
                <ViewsDirective>
                    <ViewDirective type='Assist' name='Chat'/>
                    <ViewDirective type='Custom' name='Settings'/>
                    <ViewDirective type='Custom' name='History'/>
                </ViewsDirective>
            </AIAssistViewComponent>
        </div>
    );
}

export default App;
```

### Conditional View Switching

Switch views based on events or conditions:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // Switch to response view after prompt
    setTimeout(() => {
        assistInstance.current?.addPromptResponse('Processing...');
        
        // Automatically switch to results view
        if (assistInstance.current) {
            assistInstance.current.activeView = 1;  // Switch to results view
        }
    }, 1000);
};

// Or switch based on user action
const handleToolbarClick = (action: string) => {
    if (action === 'settings') {
        assistInstance.current.activeView = 1;
    } else if (action === 'history') {
        assistInstance.current.activeView = 2;
    }
};
```

### Getting Current Active View

Read the current active view index:

```tsx
const getCurrentView = () => {
    const viewIndex = assistInstance.current?.activeView;
    console.log('Current view index:', viewIndex);
    
    const viewNames = ['Chat', 'Settings', 'History'];
    console.log('Current view name:', viewNames[viewIndex]);
    
    return viewIndex;
};
```

## Complete Multi-View Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, ViewsDirective, ViewDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const chatViewTemplate = '';  // Default assist view

    const settingsTemplate = `
        <div class="settings-view">
            <h3>Assistant Settings</h3>
            <div class="setting">
                <label>Tone:</label>
                <select>
                    <option>Formal</option>
                    <option>Casual</option>
                    <option>Technical</option>
                </select>
            </div>
            <div class="setting">
                <label>Response Length:</label>
                <select>
                    <option>Brief</option>
                    <option>Detailed</option>
                </select>
            </div>
        </div>
    `;

    const historyTemplate = `
        <div class="history-view">
            <h3>Recent Conversations</h3>
            <div class="history-item">
                <p>Conversation from 2 hours ago</p>
            </div>
            <div class="history-item">
                <p>Conversation from yesterday</p>
            </div>
        </div>
    `;

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
        }, 1000);
    };

    return (
        <div style={{ height: '100vh' }}>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                activeView={0}
            >
                <ViewsDirective>
                    <ViewDirective 
                        type='Assist' 
                        name='Chat'
                        iconCss='e-assistview-icon'
                    />
                    <ViewDirective 
                        type='Custom' 
                        name='Settings'
                        iconCss='e-icons e-settings'
                        viewTemplate={settingsTemplate}
                    />
                    <ViewDirective 
                        type='Custom' 
                        name='History'
                        iconCss='e-icons e-history'
                        viewTemplate={historyTemplate}
                    />
                </ViewsDirective>
            </AIAssistViewComponent>
        </div>
    );
}

export default App;
```

## Use Cases

### Chat + Settings + History

Combine conversation, user settings, and history view:
- Main chat for AI interaction
- Settings for customization
- History for accessing past conversations

### Chat + Documentation

Display chat alongside inline documentation:
- Left side: AI chat
- Right side: Help/docs

### Chat + Analytics

Show conversation analytics in separate view:
- Main chat area
- Analytics panel showing usage stats

### Multi-Language Support

Switch between language-specific views:
- English chat view
- Spanish chat view  
- French chat view

## Best Practices

**Keep views focused**: Each view should have clear purpose  
**Use meaningful names**: Labels should describe view content  
**Consistent iconography**: Use recognizable icons  
**Organize logically**: Group related views together  
**Provide defaults**: Set sensible activeView on load  
**Performance**: Minimize view content for smooth switching
