---
name: typing-indicator
description: Display typing indicators in Chat-UI to show real-time user activity.
---

# Typing Indicator

## Table of Contents
- [Basic Typing Indicator](#basic-typing-indicator)
- [Multiple Users Typing](#multiple-users-typing)
- [Typing Indicator Template](#typing-indicator-template)
- [Dynamic Typing Management](#dynamic-typing-management)

## Basic Typing Indicator

### Show Single User Typing

Display typing indicator for one user:

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const typingUsers: UserModel[] = [
        { id: "user2", user: "Support Agent" }
    ];

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            typingUsers={typingUsers}
        />
    );
}
```

### Hide Typing Indicator

Empty the array to hide the indicator:

```tsx
const [typingUsers, setTypingUsers] = React.useState<UserModel[]>([]);

// Show typing after 1 second, hide after 3 seconds
setTimeout(() => {
    setTypingUsers([{ id: "user2", user: "Agent" }]);
    setTimeout(() => setTypingUsers([]), 2000);
}, 1000);
```

## Multiple Users Typing

### Show Multiple Users

Display when multiple users are typing:

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const typingUsers: UserModel[] = [
        { id: "user2", user: "Michale" },
        { id: "user3", user: "Reena" }
    ];

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            typingUsers={typingUsers}
        />
    );
}
```

### Default Multi-User Format

System automatically displays:
- 1 user: "User is typing..."
- 2 users: "User1 and User2 are typing..."
- 3+ users: "User1, User2, and X others are typing..."

## Typing Indicator Template

### Custom Typing Indicator Display

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const typingUsers: UserModel[] = [
        { id: "user2", user: "Michale" },
        { id: "user3", user: "Reena" }
    ];

    const typingUsersTemplate = (context) => {
        if (!context.users || context.users.length === 0) {
            return null;
        }

        const userNames = context.users.map(u => u.user).join(', ');

        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px 0',
                color: '#666',
                fontSize: '14px'
            }}>
                <span>{userNames} {context.users.length === 1 ? 'is' : 'are'} typing</span>
                <span style={{ marginLeft: '4px', display: 'flex', gap: '2px' }}>
                    <span style={{ 
                        width: '4px', 
                        height: '4px', 
                        borderRadius: '50%', 
                        backgroundColor: '#999',
                        animation: 'bounce 1.4s infinite'
                    }} />
                    <span style={{ 
                        width: '4px', 
                        height: '4px', 
                        borderRadius: '50%', 
                        backgroundColor: '#999',
                        animation: 'bounce 1.4s infinite 0.2s'
                    }} />
                    <span style={{ 
                        width: '4px', 
                        height: '4px', 
                        borderRadius: '50%', 
                        backgroundColor: '#999',
                        animation: 'bounce 1.4s infinite 0.4s'
                    }} />
                </span>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            typingUsers={typingUsers}
            typingUsersTemplate={typingUsersTemplate}
        />
    );
}
```

Add animation styles to your CSS:

```css
@keyframes bounce {
    0%, 60%, 100% {
        opacity: 0.3;
        transform: translateY(0);
    }
    30% {
        opacity: 1;
        transform: translateY(-10px);
    }
}
```

### Advanced Typing Template

```tsx
const typingUsersTemplate = (context) => {
    if (!context.users || context.users.length === 0) {
        return null;
    }

    const formatUserList = () => {
        const names = context.users.map(u => u.user);
        if (names.length === 1) {
            return names[0];
        } else if (names.length === 2) {
            return `${names[0]} and ${names[1]}`;
        } else {
            return `${names[0]}, ${names[1]}, and ${names.length - 2} other${names.length - 2 > 1 ? 's' : ''}`;
        }
    };

    return (
        <div style={{
            padding: '8px 12px',
            backgroundColor: '#f0f0f0',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '14px',
            color: '#666'
        }}>
            <span className="e-icons e-spinner" style={{
                animation: 'spin 1s linear infinite',
                fontSize: '16px'
            }}></span>
            <span>{formatUserList()} {context.users.length === 1 ? 'is' : 'are'} typing...</span>
        </div>
    );
};
```

## Dynamic Typing Management

### Simulate Real Typing

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useRef } from 'react';

function App() {
    const [typingUsers, setTypingUsers] = useState<UserModel[]>([]);
    const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    const agentUser: UserModel = { id: "user2", user: "Support Agent" };

    const handleUserTyping = () => {
        // Show typing indicator
        if (!typingUsers.includes(agentUser)) {
            setTypingUsers([agentUser]);
        }

        // Clear existing timeout
        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }

        // Hide typing after 2 seconds of inactivity
        typingTimeoutRef.current = setTimeout(() => {
            setTypingUsers([]);
        }, 2000);
    };

    return (
        <div>
            <button onClick={handleUserTyping}>
                Agent is Typing...
            </button>
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                typingUsers={typingUsers}
            />
        </div>
    );
}
```

### Typing with Auto-Response

```tsx
import { ChatUIComponent, UserModel, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const chatRef = useRef<ChatUIComponent>(null);
    const [typingUsers, setTypingUsers] = useState<UserModel[]>([]);
    
    const currentUser = { id: "user1", user: "Albert" };
    const agentUser = { id: "user2", user: "Support Agent" };

    const simulateAgentResponse = (userMessage: string) => {
        // Show typing indicator
        setTypingUsers([agentUser]);

        // Simulate typing delay (2-4 seconds)
        const delay = Math.random() * 2000 + 2000;
        
        setTimeout(() => {
            // Hide typing indicator
            setTypingUsers([]);

            // Add response message
            const agentResponse: MessageModel = {
                author: agentUser,
                text: `Thank you for your message: "${userMessage}". How else can I help?`,
                timeStamp: new Date()
            };

            chatRef.current?.addMessage(agentResponse);
        }, delay);
    };

    return (
        <ChatUIComponent 
            ref={chatRef}
            user={currentUser}
            typingUsers={typingUsers}
            messageSend={(args) => {
                if (!args.cancel) {
                    // Simulate agent response after user sends message
                    setTimeout(() => {
                        simulateAgentResponse(args.message.text);
                    }, 500);
                }
            }}
        />
    );
}
```

## Complete Example

### Full Typing Indicator Setup

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [typingUsers, setTypingUsers] = useState<UserModel[]>([]);
    
    const currentUser = { id: "user1", user: "Albert" };
    const supportAgent: UserModel = { id: "user2", user: "Support Agent" };
    const manager: UserModel = { id: "user3", user: "Manager" };

    useEffect(() => {
        // Simulate typing users at different times
        setTimeout(() => {
            setTypingUsers([supportAgent]);
        }, 2000);

        setTimeout(() => {
            setTypingUsers([supportAgent, manager]);
        }, 5000);

        setTimeout(() => {
            setTypingUsers([]);
        }, 8000);
    }, []);

    const typingUsersTemplate = (context) => {
        if (!context.users || context.users.length === 0) {
            return null;
        }

        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 0',
                color: '#666'
            }}>
                <span style={{ fontSize: '14px' }}>
                    {context.users.map(u => u.user).join(', ')}
                    {' '}{context.users.length === 1 ? 'is' : 'are'} typing
                </span>
                <span style={{ display: 'flex', gap: '2px' }}>
                    {[0, 1, 2].map(i => (
                        <span key={i} style={{
                            width: '4px',
                            height: '4px',
                            borderRadius: '50%',
                            backgroundColor: '#999',
                            animation: `bounce 1.4s infinite ${i * 0.2}s`
                        }} />
                    ))}
                </span>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={currentUser}
            headerText="Support Chat"
            typingUsers={typingUsers}
            typingUsersTemplate={typingUsersTemplate}
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Hello! I have a question about my order." 
                    author={currentUser}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

## Best Practices

1. **Show typing only when necessary** to avoid noise
2. **Clear typing indicator** after 3-5 seconds automatically
3. **Support multiple users typing** for team chats
4. **Provide visual feedback** with animations
5. **Update typing status** in real-time
6. **Test with slow networks** for delays
7. **Clear timeouts** on component unmount

## Accessibility

```tsx
const typingUsersTemplate = (context) => {
    if (!context.users || context.users.length === 0) {
        return null;
    }

    const ariaLabel = `${context.users.map(u => u.user).join(', ')} ${context.users.length === 1 ? 'is' : 'are'} typing`;

    return (
        <div role="status" aria-live="polite" aria-label={ariaLabel}>
            {context.users.map(u => u.user).join(', ')} 
            {' '}{context.users.length === 1 ? 'is' : 'are'} typing...
        </div>
    );
};
```
