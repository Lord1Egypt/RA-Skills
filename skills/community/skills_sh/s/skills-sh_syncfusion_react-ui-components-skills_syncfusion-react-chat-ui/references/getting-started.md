---
name: getting-started
description: Get started with Syncfusion React Chat-UI component installation, setup, and basic implementation.
---

# Getting Started with Chat-UI

## Table of Contents
- [Installation](#installation)
- [Project Setup](#project-setup)
- [CSS Configuration](#css-configuration)
- [Basic Implementation](#basic-implementation)
- [First Message Example](#first-message-example)

## Installation

### Install via npm

```bash
npm install @syncfusion/ej2-react-interactive-chat --save
```

Or using yarn:

```bash
yarn add @syncfusion/ej2-react-interactive-chat
```

## CSS Configuration

### Import Required Stylesheets

Add the following imports to your `src/App.css` or main CSS file:

```css
/* Import base theme styles */
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";

/* Import component-specific styles */
@import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/material.css";

/* Import Chat-UI styles */
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/material.css";
```

### Available Themes

Choose one of these themes to import:
- `material.css` - Material Design (recommended)
- `bootstrap5.css` - Bootstrap 5 styling
- `fluent.css` - Microsoft Fluent Design
- `tailwind.css` - Tailwind CSS styling
- `bootstrap.css` - Bootstrap 4 styling
- `highcontrast.css` - High contrast accessibility theme

## Basic Implementation

### Minimal Chat Component

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    return (
        <ChatUIComponent user={currentUser} id="chat-ui" />
    );
}

export default App;
```

### With Messages

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    const otherUser: UserModel = {
        id: "user2",
        user: "Michale Suyama"
    };

    return (
        <ChatUIComponent user={currentUser} headerText="Chat">
            <MessagesDirective>
                <MessageDirective 
                    text="Hi, how are you?" 
                    author={currentUser} 
                />
                <MessageDirective 
                    text="I'm good, thanks for asking!" 
                    author={otherUser} 
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

### TypeScript Configuration

For TypeScript projects, create types for your user and message models:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

interface AppUser extends UserModel {
    department?: string;
}

interface AppMessage extends MessageModel {
    priority?: 'low' | 'medium' | 'high';
}

function App() {
    const currentUser: AppUser = {
        id: "user1",
        user: "Albert",
        department: "Support"
    };

    const messages: AppMessage[] = [
        {
            text: "Hello!",
            author: currentUser,
            priority: 'high'
        }
    ];

    return (
        <ChatUIComponent user={currentUser}>
            <MessagesDirective>
                {messages.map((msg, index) => (
                    <MessageDirective key={index} {...msg} />
                ))}
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

## First Message Example

### Complete Working Example

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';
import ReactDOM from 'react-dom';
import '../styles/index.css';

function App() {
    // Define current user
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert",
        avatarBgColor: "#0c888e"
    };

    // Define other user in conversation
    const supportAgent: UserModel = {
        id: "user2",
        user: "Michale Suyama",
        avatarUrl: 'https://ej2.syncfusion.com/demos/src/avatar/images/pic03.png'
    };

    return (
        <div style={{ height: '600px', width: '100%' }}>
            <ChatUIComponent 
                user={currentUser}
                headerText="Support Chat"
                placeholder="Type your message..."
                showHeader={true}
                showFooter={true}
            >
                <MessagesDirective>
                    <MessageDirective 
                        text="Welcome! How can I help you today?" 
                        author={supportAgent}
                        timeStamp={new Date('2024-01-15 09:00')}
                    />
                    <MessageDirective 
                        text="Hi, I need help with my account." 
                        author={currentUser}
                        timeStamp={new Date('2024-01-15 09:05')}
                    />
                    <MessageDirective 
                        text="I'd be happy to assist! What's the issue?" 
                        author={supportAgent}
                        timeStamp={new Date('2024-01-15 09:06')}
                    />
                </MessagesDirective>
            </ChatUIComponent>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
```