---
name: templating-system
description: Customize Chat-UI appearance with templates for messages, empty states, typing indicators, suggestions, and footer.
---

# Templating System

## Table of Contents
- [Empty Chat Template](#empty-chat-template)
- [Message Template](#message-template)
- [Time Break Template](#time-break-template)
- [Typing Users Template](#typing-users-template)
- [Suggestion Template](#suggestion-template)
- [Footer Template](#footer-template)

## Empty Chat Template

### Display Welcome Message

Show custom content when chat has no messages:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const emptyChatTemplate = () => {
        return (
            <div style={{ 
                textAlign: 'center', 
                padding: '40px',
                color: '#666'
            }}>
                <h3 style={{ fontSize: '24px', marginBottom: '10px' }}>
                    <span className="e-icons e-chat"></span>
                </h3>
                <h4>No Messages Yet</h4>
                <p>Start a conversation to see your messages here.</p>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            emptyChatTemplate={emptyChatTemplate}
        />
    );
}
```

## Message Template

### Custom Message Rendering

Control how each message is displayed:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const messageTemplate = (context: { message: MessageModel; index: number }) => {
        const isCurrentUser = context.message.author?.id === "user1";
        
        return (
            <div style={{
                marginBottom: '12px',
                textAlign: isCurrentUser ? 'right' : 'left'
            }}>
                <div style={{
                    display: 'inline-block',
                    backgroundColor: isCurrentUser ? '#0078d4' : '#f0f0f0',
                    color: isCurrentUser ? 'white' : 'black',
                    padding: '10px 16px',
                    borderRadius: '12px',
                    maxWidth: '70%',
                    wordWrap: 'break-word'
                }}>
                    {context.message.text}
                </div>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            messageTemplate={messageTemplate}
        >
            <MessagesDirective>
                <MessageDirective text="Hello!" author={{ id: "user1", user: "Albert" }} />
                <MessageDirective text="Hi there!" author={{ id: "user2", user: "Support" }} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Message Template with Rich Content

```tsx
const messageTemplate = (context) => {
    const message = context.message;
    const user = message.author;
    
    return (
        <div className="e-card" style={{ marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
                <strong>{user.user}</strong>
                <span style={{ fontSize: '12px', marginLeft: '8px', color: '#999' }}>
                    {new Date(message.timeStamp).toLocaleTimeString()}
                </span>
            </div>
            <div style={{ padding: '8px 0' }}>
                {message.text}
            </div>
            {message.status && (
                <div style={{ fontSize: '12px', color: '#999', marginTop: '4px' }}>
                    {message.status.text}
                </div>
            )}
        </div>
    );
};
```

## Time Break Template

### Custom Date Separator

Customize how date separators appear:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const timeBreakTemplate = (context) => {
        const date = new Date(context.messageDate);
        const formattedDate = date.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        return (
            <div style={{
                textAlign: 'center',
                margin: '16px 0',
                color: '#999'
            }}>
                <span style={{
                    backgroundColor: '#f0f0f0',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px'
                }}>
                    {formattedDate}
                </span>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            showTimeBreak={true}
            timeBreakTemplate={timeBreakTemplate}
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Message from today" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={new Date()}
                />
                <MessageDirective 
                    text="Message from yesterday" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={new Date(Date.now() - 86400000)}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

## Typing Users Template

### Custom Typing Indicator

Display who is typing with custom styling:

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

        const userNames = context.users
            .map((u, i) => {
                const isLast = i === context.users.length - 1;
                const isSecondToLast = i === context.users.length - 2;
                
                if (isLast && i > 0) return `and ${u.user}`;
                if (isSecondToLast && context.users.length === 2) return u.user;
                return u.user;
            })
            .join(', ');

        return (
            <div style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px 0',
                color: '#666',
                fontSize: '14px'
            }}>
                <span>{userNames} {context.users.length === 1 ? 'is' : 'are'} typing</span>
                <span style={{ marginLeft: '4px' }}>
                    <span style={{ animation: 'pulse 1s infinite' }}>•</span>
                    <span style={{ animation: 'pulse 1s infinite 0.2s' }}>•</span>
                    <span style={{ animation: 'pulse 1s infinite 0.4s' }}>•</span>
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

## Suggestion Template

### Custom Suggestion Buttons

Style suggestion/quick-reply buttons:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const suggestions = [
        "I need help with billing",
        "How do I reset my password?",
        "Check order status"
    ];

    const suggestionTemplate = (context) => {
        return (
            <button style={{
                backgroundColor: '#0078d4',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '20px',
                margin: '4px',
                cursor: 'pointer',
                fontSize: '14px'
            }}>
                {context.suggestion}
            </button>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            suggestions={suggestions}
            suggestionTemplate={suggestionTemplate}
        />
    );
}
```

## Footer Template

### Custom Input Area

Replace the default footer with custom content:

```tsx
import { ChatUIComponent, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const chatRef = useRef<ChatUIComponent>(null);
    const [inputValue, setInputValue] = useState('');

    const footerTemplate = () => {
        const handleSend = () => {
            if (inputValue.trim()) {
                const newMessage: MessageModel = {
                    author: { id: "user1", user: "Albert" },
                    text: inputValue,
                    timeStamp: new Date()
                };
                
                chatRef.current?.addMessage(newMessage);
                setInputValue('');
            }
        };

        const handleKeyPress = (e: React.KeyboardEvent) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        };

        return (
            <div style={{
                display: 'flex',
                padding: '12px',
                gap: '8px',
                borderTop: '1px solid #e0e0e0'
            }}>
                <input 
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type a message..."
                    style={{
                        flex: 1,
                        padding: '8px 12px',
                        border: '1px solid #d0d0d0',
                        borderRadius: '4px',
                        fontSize: '14px'
                    }}
                />
                <button 
                    onClick={handleSend}
                    style={{
                        backgroundColor: '#0078d4',
                        color: 'white',
                        border: 'none',
                        padding: '8px 16px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px'
                    }}
                >
                    <span className="e-icons e-send-1"></span>
                </button>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            ref={chatRef}
            user={{ id: "user1", user: "Albert" }}
            footerTemplate={footerTemplate}
        />
    );
}
```

## Complete Template Example

### Full Customization

```tsx
function App() {
    const emptyChatTemplate = () => (
        <div style={{ textAlign: 'center', padding: '40px' }}>
            <h3>Start a Conversation</h3>
            <p>Select from suggestions below or type your message</p>
        </div>
    );

    const messageTemplate = (ctx) => (
        <div style={{
            display: 'flex',
            justifyContent: ctx.message.author?.id === "user1" ? 'flex-end' : 'flex-start',
            marginBottom: '12px'
        }}>
            <div style={{
                backgroundColor: ctx.message.author?.id === "user1" ? '#0078d4' : '#f0f0f0',
                color: ctx.message.author?.id === "user1" ? 'white' : 'black',
                padding: '10px 14px',
                borderRadius: '8px',
                maxWidth: '70%'
            }}>
                {ctx.message.text}
            </div>
        </div>
    );

    const typingUsersTemplate = (ctx) => (
        <div style={{ color: '#999', fontSize: '12px', padding: '8px 0' }}>
            {ctx.users?.map(u => u.user).join(', ')} typing...
        </div>
    );

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            emptyChatTemplate={emptyChatTemplate}
            messageTemplate={messageTemplate}
            typingUsersTemplate={typingUsersTemplate}
        />
    );
}
```

## Best Practices

1. **Keep templates simple** for better performance
2. **Use memoization** for complex templates
3. **Handle null/undefined** gracefully
4. **Match design system** styling
5. **Test responsiveness** across devices
6. **Optimize re-renders** with proper React keys
