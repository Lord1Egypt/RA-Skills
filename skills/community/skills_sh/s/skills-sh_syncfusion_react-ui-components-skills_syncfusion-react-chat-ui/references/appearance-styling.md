---
name: appearance-styling
description: Style and customize Chat-UI appearance with placeholder, dimensions, and CSS classes.
---

# Appearance and Styling

## Table of Contents
- [Placeholder Text](#placeholder-text)
- [Width Configuration](#width-configuration)
- [Height Configuration](#height-configuration)
- [Compact Mode Layout](#compact-mode-layout)
- [CSS Class Application](#css-class-application)
- [Theme Styling](#theme-styling)

## Placeholder Text

### Set Input Placeholder

Customize the hint text in the message input field:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            placeholder="Type your message here..."
        />
    );
}
```

### Default Placeholder

Default value: `"Type your message…"`

### Custom Placeholders

```tsx
// For support chat
placeholder="Describe your issue..."

// For team chat
placeholder="Share your thoughts..."

// For customer service
placeholder="How can we help?"

// Minimal
placeholder="Say something..."
```

## Width Configuration

### Set Component Width

Control the horizontal size:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            {/* Full width (default) */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                width="100%"
            />

            {/* Fixed width */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                width="450px"
            />

            {/* Viewport width */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                width="80vw"
            />
        </>
    );
}
```

### Width Variations

```tsx
// Small sidebar
width="320px"

// Medium panel
width="500px"

// Large panel
width="700px"

// Responsive
width="100%"

// Container percentage
width="90%"
```

## Height Configuration

### Set Component Height

Control the vertical size:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            {/* Full height (default) */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                height="100%"
            />

            {/* Fixed height */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                height="500px"
            />

            {/* Viewport height */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                height="80vh"
            />
        </>
    );
}
```

### Height Variations

```tsx
// Small window
height="300px"

// Medium window
height="500px"

// Large window
height="700px"

// Full screen
height="100vh"

// Fill container
height="100%"
```

### Responsive Height

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [height, setHeight] = useState('100vh');

    useEffect(() => {
        const handleResize = () => {
            const headerHeight = 60;
            const footerHeight = 50;
            const newHeight = window.innerHeight - headerHeight - footerHeight;
            setHeight(`${newHeight}px`);
        };

        window.addEventListener('resize', handleResize);
        handleResize();

        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            height={height}
        />
    );
}
```

## Compact Mode Layout

### Enable Compact Mode

Display all messages aligned to the left side, creating a simplified chat view ideal for dense group conversations or compact displays:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user = { id: "user1", user: "Albert" };
    const agent = { id: "user2", user: "Support" };

    return (
        <ChatUIComponent 
            user={user}
            enableCompactMode={true}  // Enable compact layout
        >
            <MessagesDirective>
                <MessageDirective text="My message" author={user} />
                <MessageDirective text="Agent response" author={agent} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Default Mode vs Compact Mode

**Default Mode (enableCompactMode={false}):**
- Current user messages aligned to the right
- Other users' messages aligned to the left
- Clear visual distinction between participants

**Compact Mode (enableCompactMode={true}):**
- All messages aligned to the left
- More space-efficient layout
- Better for group chats with many participants
- Ideal for mobile or embedded displays

### Use Case: Mobile Chat

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [isCompact, setIsCompact] = useState(false);

    useEffect(() => {
        // Enable compact mode on smaller screens
        const handleResize = () => {
            setIsCompact(window.innerWidth < 768);
        };

        handleResize();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableCompactMode={isCompact}
            height="100vh"
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Message 1" 
                    author={{ id: "user1", user: "Albert" }}
                />
                <MessageDirective 
                    text="Message 2" 
                    author={{ id: "user2", user: "Support" }}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Use Case: Group Chat

Compact mode is particularly useful for group conversations with multiple participants:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const users: Record<string, UserModel> = {
        user1: { id: "user1", user: "Albert", avatarBgColor: "#0c888e" },
        user2: { id: "user2", user: "Michale", avatarBgColor: "#e3165b" },
        user3: { id: "user3", user: "Reena", avatarBgColor: "#6d3e94" },
        user4: { id: "user4", user: "John", avatarBgColor: "#3c78d8" }
    };

    return (
        <ChatUIComponent 
            user={users.user1}
            headerText="Team Discussion"
            enableCompactMode={true}  // Better for group chats
            height="600px"
        >
            <MessagesDirective>
                <MessageDirective text="Let's discuss the project" author={users.user1} />
                <MessageDirective text="I have some updates" author={users.user2} />
                <MessageDirective text="Great! Let's hear them" author={users.user3} />
                <MessageDirective text="I'll share my findings too" author={users.user4} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Custom Styling for Compact Mode

```css
/* Adjust spacing in compact mode */
.e-chat-ui.e-compact-mode .e-message {
    margin-bottom: 8px;
}

.e-chat-ui.e-compact-mode .e-message-bubble {
    max-width: 85%;
}

.e-chat-ui.e-compact-mode .e-avatar {
    width: 32px;
    height: 32px;
}
```

### Toggle Compact Mode

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [compactMode, setCompactMode] = useState(false);

    return (
        <div>
            <div style={{ padding: '10px', marginBottom: '10px' }}>
                <label>
                    <input 
                        type="checkbox"
                        checked={compactMode}
                        onChange={(e) => setCompactMode(e.target.checked)}
                    />
                    {' '}Enable Compact Mode
                </label>
            </div>
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                enableCompactMode={compactMode}
                height="500px"
            />
        </div>
    );
}
```

## CSS Class Application

### Apply Custom CSS Class

Add custom styling via CSS classes:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';
import './custom-chat.css';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            cssClass="custom-chat-container"
        />
    );
}
```

### Custom CSS Styles

Create a `custom-chat.css` file:

```css
/* Main container styling */
.custom-chat-container {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
}

/* Header styling */
.custom-chat-container .e-chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 16px;
    border-radius: 8px 8px 0 0;
}

.custom-chat-container .e-chat-header-text {
    color: white;
    font-weight: 600;
}

/* Message area */
.custom-chat-container .e-chat-messages {
    padding: 16px;
    background-color: #fafafa;
}

/* Input footer */
.custom-chat-container .e-footer {
    padding: 12px;
    background-color: #ffffff;
    border-top: 1px solid #e0e0e0;
}

.custom-chat-container .e-input-group {
    border: 1px solid #ddd;
    border-radius: 4px;
}

/* Message bubbles */
.custom-chat-container .e-chat-message {
    margin-bottom: 12px;
}

.custom-chat-container .e-message-right {
    text-align: right;
}

.custom-chat-container .e-message-left {
    text-align: left;
}
```

## Theme Styling

### Material Theme (Default)

```css
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/material.css";
```

### Bootstrap 5 Theme

```css
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/bootstrap5.css";
```

### Fluent Theme

```css
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/fluent.css";
```

### Tailwind Theme

```css
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/tailwind.css";
```

### High Contrast Theme

```css
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/highcontrast.css";
```

## Complete Styling Example

### Integrated Styling

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';
import './app-styles.css';

function App() {
    return (
        <div className="chat-wrapper">
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                headerText="Support Chat"
                placeholder="Ask me anything..."
                width="100%"
                height="600px"
                cssClass="app-chat-style"
            >
                <MessagesDirective>
                    <MessageDirective 
                        text="Hello! How can I assist you today?" 
                        author={{ id: "agent", user: "Support Agent" }}
                    />
                </MessagesDirective>
            </ChatUIComponent>
        </div>
    );
}

export default App;
```

### Corresponding CSS

```css
/* Wrapper styling */
.chat-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

/* Chat container */
.app-chat-style {
    border-radius: 12px;
    border: 1px solid #d0d0d0;
    overflow: hidden;
    transition: all 0.3s ease;
}

.app-chat-style:hover {
    border-color: #0078d4;
    box-shadow: 0 4px 12px rgba(0, 120, 212, 0.15);
}

/* Header customization */
.app-chat-style .e-chat-header {
    background-color: #0078d4;
    padding: 16px 20px;
}

.app-chat-style .e-chat-header-text {
    color: white;
    font-size: 16px;
    font-weight: 600;
}

/* Message styling */
.app-chat-style .e-message-bubble {
    border-radius: 12px;
    padding: 10px 14px;
}

.app-chat-style .e-message-right {
    background-color: #0078d4;
    color: white;
}

.app-chat-style .e-message-left {
    background-color: #f0f0f0;
    color: #333;
}

/* Footer input */
.app-chat-style .e-input-group {
    border-radius: 4px;
    border: 1px solid #d0d0d0;
}

.app-chat-style .e-input-group input {
    font-size: 14px;
}

.app-chat-style .e-send-button {
    background-color: #0078d4;
    border: none;
    cursor: pointer;
}

.app-chat-style .e-send-button:hover {
    background-color: #005a9e;
}
```

## Dark Mode Support

### Enable Dark Mode

```css
.app-chat-style.dark-mode {
    background-color: #1e1e1e;
    color: #ffffff;
}

.app-chat-style.dark-mode .e-chat-header {
    background-color: #2d2d2d;
}

.app-chat-style.dark-mode .e-message-left {
    background-color: #333333;
    color: #ffffff;
}

.app-chat-style.dark-mode .e-message-right {
    background-color: #0078d4;
}

.app-chat-style.dark-mode .e-input-group {
    background-color: #333;
    border-color: #444;
}

.app-chat-style.dark-mode .e-input-group input {
    background-color: #333;
    color: #fff;
}
```

## Responsive Design

### Mobile and Desktop

```css
/* Desktop */
@media (min-width: 768px) {
    .chat-wrapper {
        max-width: 900px;
    }
    
    .app-chat-style {
        width: 600px;
        height: 700px;
    }
}

/* Tablet */
@media (min-width: 480px) and (max-width: 767px) {
    .app-chat-style {
        width: 100%;
        height: 500px;
    }
}

/* Mobile */
@media (max-width: 479px) {
    .chat-wrapper {
        padding: 0;
    }
    
    .app-chat-style {
        width: 100%;
        height: 100vh;
        border-radius: 0;
    }
}
```

## Best Practices

1. **Use semantic color schemes** for better UX
2. **Ensure sufficient contrast** for accessibility
3. **Test responsive design** on different devices
4. **Apply consistent branding** with company colors
5. **Optimize for both light and dark themes**
6. **Maintain readable font sizes** (minimum 14px)
7. **Use proper spacing** for visual hierarchy

