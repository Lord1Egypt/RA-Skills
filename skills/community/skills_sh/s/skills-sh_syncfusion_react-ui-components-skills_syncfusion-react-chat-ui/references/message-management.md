---
name: message-management
description: Manage messages in Chat-UI - adding, updating, pinning, forwarding, and tracking delivery status.
---

# Message Management

## Table of Contents
- [Basic Message Configuration](#basic-message-configuration)
- [Adding Messages Dynamically](#adding-messages-dynamically)
- [Updating Messages](#updating-messages)
- [Auto Scroll to Bottom](#auto-scroll-to-bottom)
- [Load Messages On Demand](#load-messages-on-demand)
- [Pinned Messages](#pinned-messages)
- [Message Replies](#message-replies)
- [Forwarding Messages](#forwarding-messages)
- [Message Status](#message-status)
- [Message Toolbar](#message-toolbar)
- [Markdown Content](#markdown-content)

## Basic Message Configuration

### Setting Message Text

The `text` property defines the message content:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user: UserModel = { id: "user1", user: "Albert" };
    const agent: UserModel = { id: "user2", user: "Support" };

    return (
        <ChatUIComponent user={user}>
            <MessagesDirective>
                <MessageDirective 
                    text="This is a simple message" 
                    author={agent}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Message ID

Assign unique IDs to messages for programmatic access:

```tsx
<MessagesDirective>
    <MessageDirective 
        id="msg-1"
        text="Hello" 
        author={agent}
    />
    <MessageDirective 
        id="msg-2"
        text="Hi there" 
        author={user}
    />
</MessagesDirective>
```

## Adding Messages Dynamically

### Add Message as Object

Use `addMessage()` with a MessageModel object for full control:

```tsx
import { ChatUIComponent, UserModel, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const chatRef = useRef<ChatUIComponent>(null);
    const user: UserModel = { id: "user1", user: "Albert" };
    const agent: UserModel = { id: "user2", user: "Support" };

    const addMessageWithConfig = () => {
        const newMessage: MessageModel = {
            id: `msg-${Date.now()}`,
            author: agent,
            text: "Thank you for your message!",
            timeStamp: new Date(),
            status: {
                text: 'Delivered',
                iconCss: 'e-icons e-chat-delivered'
            }
        };

        chatRef.current?.addMessage(newMessage);
    };

    return (
        <>
            <button onClick={addMessageWithConfig}>Add Message</button>
            <ChatUIComponent ref={chatRef} user={user} height="400px" />
        </>
    );
}
```

### Add Message as String

For simple text messages, pass a string:

```tsx
const addSimpleMessage = () => {
    chatRef.current?.addMessage("This is a quick message!");
};
```

## Updating Messages

### Modify Existing Messages

Use `updateMessage()` to edit previously sent messages:

```tsx
import { ChatUIComponent, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const chatRef = useRef<ChatUIComponent>(null);

    const editMessage = () => {
        const updatedMessage: MessageModel = {
            text: "Updated message content (edited)",
            author: { id: "user1", user: "Albert" }
        };

        chatRef.current?.updateMessage(updatedMessage, 'msg-1');
    };

    return (
        <>
            <button onClick={editMessage}>Edit First Message</button>
            <ChatUIComponent ref={chatRef} user={{ id: "user1", user: "Albert" }} />
        </>
    );
}
```

## Auto Scroll to Bottom

### Enable Auto-Scrolling

Automatically scroll to the latest message when new messages are added:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user = { id: "user1", user: "Albert" };
    const agent = { id: "user2", user: "Support" };

    return (
        <ChatUIComponent 
            user={user}
            autoScrollToBottom={true}  // Enable auto-scroll
        >
            <MessagesDirective>
                <MessageDirective text="Hello" author={user} />
                <MessageDirective text="Hi there!" author={agent} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Disable Auto-Scrolling

Keep scroll position when new messages arrive:

```tsx
<ChatUIComponent 
    user={user}
    autoScrollToBottom={false}  // Disable auto-scroll (default)
/>
```

### Use Case: User Control

Allow users to toggle auto-scroll behavior:

```tsx
import { ChatUIComponent, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useRef } from 'react';

function App() {
    const [autoScroll, setAutoScroll] = useState(true);
    const chatRef = useRef<ChatUIComponent>(null);
    const user = { id: "user1", user: "Albert" };

    const addMessage = () => {
        const newMessage: MessageModel = {
            author: { id: "user2", user: "Support" },
            text: "New message arrived!",
            timeStamp: new Date()
        };
        chatRef.current?.addMessage(newMessage);
    };

    return (
        <div>
            <div style={{ marginBottom: '10px' }}>
                <label>
                    <input 
                        type="checkbox" 
                        checked={autoScroll}
                        onChange={(e) => setAutoScroll(e.target.checked)}
                    />
                    Auto-scroll to latest message
                </label>
                <button onClick={addMessage} style={{ marginLeft: '10px' }}>
                    Add Message
                </button>
            </div>
            <ChatUIComponent 
                ref={chatRef}
                user={user}
                autoScrollToBottom={autoScroll}
                height="400px"
            />
        </div>
    );
}
```

## Load Messages On Demand

### Enable Progressive Loading

Load older messages as the user scrolls up, improving performance for large conversation histories:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            loadOnDemand={true}  // Enable on-demand loading
        />
    );
}
```

### How It Works

When `loadOnDemand` is enabled:
- Initial load shows recent messages only
- Scrolling to the top triggers loading of older messages
- Improves performance for conversations with thousands of messages
- Reduces initial page load time

### Use Case: Large Message History

```tsx
import { ChatUIComponent, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [messages, setMessages] = useState<MessageModel[]>([]);
    const user = { id: "user1", user: "Albert" };

    // Simulate loading more messages when scrolling up
    const loadMoreMessages = () => {
        // Fetch older messages from server
        fetch('/api/messages?before=' + messages[0]?.timeStamp)
            .then(res => res.json())
            .then(olderMessages => {
                setMessages([...olderMessages, ...messages]);
            });
    };

    return (
        <ChatUIComponent 
            user={user}
            messages={messages}
            loadOnDemand={true}
            height="600px"
        />
    );
}
```

### Best Practices for On-Demand Loading

1. **Load in batches** - Fetch 20-50 messages at a time
2. **Show loading indicator** when fetching older messages
3. **Cache loaded messages** to avoid re-fetching
4. **Set appropriate threshold** for triggering load
5. **Handle edge cases** (no more messages to load)

```tsx
import { ChatUIComponent, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [messages, setMessages] = useState<MessageModel[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const user = { id: "user1", user: "Albert" };

    useEffect(() => {
        // Load initial messages
        loadInitialMessages();
    }, []);

    const loadInitialMessages = async () => {
        const response = await fetch('/api/messages?limit=20');
        const data = await response.json();
        setMessages(data.messages);
        setHasMore(data.hasMore);
    };

    const loadOlderMessages = async () => {
        if (isLoading || !hasMore) return;
        
        setIsLoading(true);
        const oldestMessageTime = messages[0]?.timeStamp;
        
        try {
            const response = await fetch(
                `/api/messages?before=${oldestMessageTime}&limit=20`
            );
            const data = await response.json();
            
            setMessages([...data.messages, ...messages]);
            setHasMore(data.hasMore);
        } catch (error) {
            console.error('Failed to load messages:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            {isLoading && (
                <div style={{ textAlign: 'center', padding: '10px' }}>
                    Loading older messages...
                </div>
            )}
            <ChatUIComponent 
                user={user}
                messages={messages}
                loadOnDemand={true}
                height="600px"
            />
        </div>
    );
}
```

## Pinned Messages

### Pin Important Messages

Set `isPinned` to highlight critical messages:

```tsx
<MessagesDirective>
    <MessageDirective 
        text="Regular message" 
        author={user}
    />
    <MessageDirective 
        text="This is important - DO NOT DELETE" 
        author={agent}
        isPinned={true}
    />
    <MessageDirective 
        text="Another regular message" 
        author={user}
    />
</MessagesDirective>
```

### Pin Message Dynamically

```tsx
const pinMessage = (messageId: string) => {
    const messages = chatRef.current?.messages || [];
    const messageToPin = messages.find(m => m.id === messageId);
    
    if (messageToPin) {
        messageToPin.isPinned = true;
        chatRef.current?.updateMessage(messageToPin, messageId);
    }
};
```

## Message Replies

### Reply to Original Message

Create threaded conversations with the `replyTo` property:

```tsx
import { ChatUIComponent, MessageReplyModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user: UserModel = { id: "user1", user: "Albert" };
    const agent: UserModel = { id: "user2", user: "Support" };

    const originalMessage: MessageReplyModel = {
        user: agent,
        text: "How can I help you?",
        messageID: "original-1"
    };

    return (
        <ChatUIComponent user={user}>
            <MessagesDirective>
                <MessageDirective 
                    id="original-1"
                    text="How can I help you?" 
                    author={agent}
                />
                <MessageDirective 
                    text="I need assistance with billing"
                    author={user}
                    replyTo={originalMessage}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

## Forwarding Messages

### Forward Message to Another Conversation

Use `isForwarded` property to indicate forwarded content:

```tsx
<MessagesDirective>
    <MessageDirective 
        text="Check out this update!" 
        author={user}
    />
    <MessageDirective 
        text="Check out this update! (forwarded)" 
        author={agent}
        isForwarded={true}
    />
</MessagesDirective>
```

### Forward Message Handler

```tsx
const forwardMessage = (messageId: string) => {
    const messages = chatRef.current?.messages || [];
    const msgToForward = messages.find(m => m.id === messageId);
    
    if (msgToForward) {
        const forwardedMsg: MessageModel = {
            ...msgToForward,
            isForwarded: true,
            id: `forwarded-${Date.now()}`,
            timeStamp: new Date()
        };
        
        chatRef.current?.addMessage(forwardedMsg);
    }
};
```

## Message Status

### Configure Message Status

Track message delivery state with status icons and text:

```tsx
import { ChatUIComponent, MessageStatusModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const user: UserModel = { id: "user1", user: "Albert" };
    const agent: UserModel = { id: "user2", user: "Support" };

    const deliveredStatus: MessageStatusModel = {
        iconCss: 'e-icons e-chat-delivered',
        text: 'Delivered',
        tooltip: 'Message delivered at 10:30 AM'
    };

    const readStatus: MessageStatusModel = {
        iconCss: 'e-icons e-chat-seen',
        text: 'Seen',
        tooltip: 'Seen by recipient at 10:32 AM'
    };

    return (
        <ChatUIComponent user={user}>
            <MessagesDirective>
                <MessageDirective 
                    text="Message 1" 
                    author={user}
                    status={deliveredStatus}
                />
                <MessageDirective 
                    text="Message 2" 
                    author={user}
                    status={readStatus}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

## Message Toolbar

### Customize Message Toolbar

Configure toolbar items for message actions:

```tsx
import { ChatUIComponent, MessageToolbarSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const messageToolbarSettings: MessageToolbarSettingsModel = {
        width: '100%',
        items: [
            { type: 'Button', iconCss: 'e-icons e-chat-forward', tooltip: 'Forward' },
            { type: 'Button', iconCss: 'e-icons e-chat-copy', tooltip: 'Copy' },
            { type: 'Button', iconCss: 'e-icons e-chat-reply', tooltip: 'Reply' },
            { type: 'Button', iconCss: 'e-icons e-chat-pin', tooltip: 'Pin' },
            { type: 'Button', iconCss: 'e-icons e-chat-trash', tooltip: 'Delete' }
        ]
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            messageToolbarSettings={messageToolbarSettings}
        />
    );
}
```

### Handle Toolbar Item Click

```tsx
const messageToolbarSettings: MessageToolbarSettingsModel = {
    items: [
        { type: 'Button', iconCss: 'e-icons e-chat-copy', tooltip: 'Copy' },
        { type: 'Button', iconCss: 'e-icons e-chat-trash', tooltip: 'Delete' }
    ],
    itemClicked: (args) => {
        if (args.item.iconCss === 'e-icons e-chat-copy') {
            navigator.clipboard.writeText(args.message.text);
            console.log('Copied to clipboard');
        } else if (args.item.iconCss === 'e-icons e-chat-trash') {
            console.log('Delete message:', args.message.id);
        }
    }
};
```

## Markdown Content

### Enable Markdown Rendering

Support rich text formatting in messages:

```tsx
import { ChatUIComponent, MessageModel, MessageSentEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import React, { useState } from 'react';

function App() {
    const [messages, setMessages] = useState<MessageModel[]>([
        {
            text: marked.parse('**Important:** This is bold text'),
            author: { id: "user2", user: "Agent" }
        }
    ]);

    const user = { id: "user1", user: "Albert" };

    const handleMessageSend = (args: MessageSentEventArgs) => {
        args.cancel = true;
        const parsedText = DOMPurify.sanitize(marked.parse(args.message.text));
        const newMessage: MessageModel = {
            text: parsedText,
            author: user,
            timeStamp: new Date()
        };
        setMessages([...messages, newMessage]);
    };

    return (
        <ChatUIComponent 
            user={user}
            messages={messages}
            messageSend={handleMessageSend}
        />
    );
}
```

### Supported Markdown

- **Bold:** `**text**` or `__text__`
- *Italic:* `*text*` or `_text_`
- [Links](url): `[text](url)`
- Lists: `- item` or `1. item`
- Code: `` `code` ``

## Best Practices

1. **Always assign message IDs** for programmatic access and updates
2. **Use timestamps** for message ordering and history
3. **Implement message status** for better UX and feedback
4. **Sanitize markdown** content to prevent XSS attacks
5. **Handle message limits** to prevent performance issues with large conversations
