---
name: user-configuration
description: Configure users in Chat-UI with avatars, status indicators, and custom styling for multi-user conversations.
---

# User Configuration

## Table of Contents
- [Basic User Setup](#basic-user-setup)
- [User Properties](#user-properties)
- [Avatar Configuration](#avatar-configuration)
- [User Status Indicators](#user-status-indicators)
- [Custom User Styling](#custom-user-styling)
- [Multiple Users](#multiple-users)

## Basic User Setup

### Define Current User

The `user` property is required and represents the logged-in user:

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    return (
        <ChatUIComponent user={currentUser} headerText="Chat" />
    );
}
```

## User Properties

### Complete User Model

```tsx
interface UserModel {
    id: string;              // Unique user identifier (REQUIRED)
    user: string;            // Display name (REQUIRED)
    avatarUrl?: string;      // Profile image URL
    avatarBgColor?: string;  // Avatar background color
    cssClass?: string;       // Custom CSS class
    statusIconCss?: string;  // Status icon class
}
```

## Avatar Configuration

### Using Avatar URLs

Display profile images for users:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user1: UserModel = {
        id: "user1",
        user: "Albert",
        avatarUrl: 'https://ej2.syncfusion.com/demos/src/avatar/images/pic01.png'
    };

    const user2: UserModel = {
        id: "user2",
        user: "Michale Suyama",
        avatarUrl: 'https://ej2.syncfusion.com/demos/src/avatar/images/pic03.png'
    };

    return (
        <ChatUIComponent user={user1}>
            <MessagesDirective>
                <MessageDirective text="Hello!" author={user1} />
                <MessageDirective text="Hi there!" author={user2} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Avatar Fallback to Initials

If no avatar URL is provided, initials are displayed automatically:

```tsx
const user: UserModel = {
    id: "user1",
    user: "Albert Brown"  // Shows "AB" as fallback
};
```

## Avatar Background Color

### Set Avatar Background

Customize avatar background color using hex values:

```tsx
const users: UserModel[] = [
    {
        id: "user1",
        user: "Albert",
        avatarBgColor: "#0c888e"  // Teal background
    },
    {
        id: "user2",
        user: "Michale",
        avatarBgColor: "#e3165b"  // Pink background
    },
    {
        id: "user3",
        user: "Reena",
        avatarBgColor: "#6d3e94"  // Purple background
    }
];
```

### Avatar with URL and Color

```tsx
const user: UserModel = {
    id: "user1",
    user: "Albert",
    avatarUrl: 'https://example.com/photo.jpg',
    avatarBgColor: "#0c888e"  // Used as fallback if URL fails
};
```

## User Status Indicators

### Presence Status Icons

Display online/offline/busy status:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const onlineUser: UserModel = {
        id: "user1",
        user: "Albert",
        statusIconCss: 'e-icons e-user-online'
    };

    const awayUser: UserModel = {
        id: "user2",
        user: "Michale",
        statusIconCss: 'e-icons e-user-away'
    };

    const busyUser: UserModel = {
        id: "user3",
        user: "Reena",
        statusIconCss: 'e-icons e-user-busy'
    };

    const offlineUser: UserModel = {
        id: "user4",
        user: "John",
        statusIconCss: 'e-icons e-user-offline'
    };

    return (
        <ChatUIComponent user={onlineUser}>
            <MessagesDirective>
                <MessageDirective text="I'm available" author={onlineUser} />
                <MessageDirective text="Be back soon" author={awayUser} />
                <MessageDirective text="In a meeting" author={busyUser} />
                <MessageDirective text="Offline now" author={offlineUser} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Available Status Icons

| Status | CSS Class | Usage |
|--------|-----------|-------|
| Available/Online | `e-user-online` | User is actively online |
| Away | `e-user-away` | User is away but app is open |
| Busy | `e-user-busy` | User is in a meeting/busy |
| Offline | `e-user-offline` | User is offline |

## Custom User Styling

### CSS Class for User Messages

Apply custom styles to specific user messages:

```tsx
import React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert",
        cssClass: 'current-user-style'
    };

    const supportAgent: UserModel = {
        id: "user2",
        user: "Support Team",
        cssClass: 'support-agent-style'
    };

    return (
        <ChatUIComponent user={currentUser}>
            <MessagesDirective>
                <MessageDirective text="I need help" author={currentUser} />
                <MessageDirective text="How can I assist?" author={supportAgent} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Custom CSS

```css
.current-user-style {
    color: #0078d4;
    font-weight: 500;
}

.current-user-style .e-chat-avatar {
    border: 2px solid #0078d4;
}

.support-agent-style {
    color: #0c888e;
}

.support-agent-style .e-chat-avatar {
    background-color: #c4f7e9;
}
```

## Multiple Users

### Multi-User Conversation

Configure different users for a realistic chat scenario:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    // Current logged-in user
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert",
        avatarBgColor: "#0c888e",
        statusIconCss: 'e-icons e-user-online'
    };

    // Other users in conversation
    const users: Record<string, UserModel> = {
        user2: {
            id: "user2",
            user: "Michale Suyama",
            avatarUrl: 'https://ej2.syncfusion.com/demos/src/avatar/images/pic03.png',
            avatarBgColor: "#e3165b",
            statusIconCss: 'e-icons e-user-online',
            cssClass: 'other-user-style'
        },
        user3: {
            id: "user3",
            user: "Reena",
            avatarBgColor: "#6d3e94",
            statusIconCss: 'e-icons e-user-away',
            cssClass: 'other-user-style'
        }
    };

    return (
        <ChatUIComponent user={currentUser} headerText="Team Chat">
            <MessagesDirective>
                <MessageDirective text="Morning everyone!" author={currentUser} />
                <MessageDirective text="Hi Albert!" author={users.user2} />
                <MessageDirective text="Good morning!" author={users.user3} />
                <MessageDirective text="Let's start the standup" author={currentUser} />
                <MessageDirective text="I'm ready" author={users.user2} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Dynamic User Management

```tsx
import React, { useState } from 'react';

function App() {
    const [users, setUsers] = useState<UserModel[]>([
        { id: "user1", user: "Albert", statusIconCss: 'e-icons e-user-online' }
    ]);

    const addUser = (newUser: UserModel) => {
        setUsers([...users, newUser]);
    };

    const updateUserStatus = (userId: string, status: string) => {
        setUsers(users.map(u => 
            u.id === userId 
                ? { ...u, statusIconCss: `e-icons e-user-${status}` }
                : u
        ));
    };

    return (
        <>
            <ChatUIComponent user={users[0]} />
        </>
    );
}
```

## Best Practices

1. **Always provide unique IDs** for each user to avoid conflicts
2. **Use real avatar URLs** for better user experience
3. **Update status icons** in real-time when users go online/offline
4. **Set appropriate background colors** for better visual distinction
5. **Use meaningful CSS classes** for user-specific styling
6. **Validate user data** before rendering messages

## Common Patterns

### Support Chat Setup

```tsx
const supportChat = {
    currentUser: { id: "cust1", user: "John Doe" },
    agent: {
        id: "agent1",
        user: "Support Team",
        avatarUrl: 'https://example.com/logo.png',
        statusIconCss: 'e-icons e-user-online'
    }
};
```

### Team Collaboration Setup

```tsx
const teamUsers: UserModel[] = [
    { id: "1", user: "Project Manager", statusIconCss: 'e-icons e-user-online' },
    { id: "2", user: "Developer", statusIconCss: 'e-icons e-user-online' },
    { id: "3", user: "Designer", statusIconCss: 'e-icons e-user-away' },
    { id: "4", user: "QA Engineer", statusIconCss: 'e-icons e-user-busy' }
];
```
