---
name: events-and-interactions
description: Handle events and user interactions in Chat-UI including message events, attachment events, and toolbar click events.
---

# Events and Interactions

## Table of Contents
- [Component Lifecycle](#component-lifecycle)
- [Message Events](#message-events)
- [Typing Events](#typing-events)
- [Attachment Events](#attachment-events)
- [Toolbar Events](#toolbar-events)

## Component Lifecycle

### Created Event

Fires after the Chat component is fully initialized:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleCreated = () => {
        console.log('Chat component initialized');
        // Perform initialization tasks
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            created={handleCreated}
        />
    );
}
```

## Message Events

### Message Send Event

Triggered before sending a message:

```tsx
import { ChatUIComponent, MessageSentEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleMessageSend = (args: MessageSentEventArgs) => {
        console.log('Message being sent:', args.message.text);
        
        // Validate message before sending
        if (args.message.text.trim().length === 0) {
            args.cancel = true;  // Prevent empty messages
        }
        
        // Add timestamp
        args.message.timeStamp = new Date();
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            messageSend={handleMessageSend}
        />
    );
}
```

### Message Sent Example with Validation

```tsx
const handleMessageSend = (args: MessageSentEventArgs) => {
    const message = args.message.text.trim();
    
    // Validate message content
    if (message.length === 0) {
        args.cancel = true;
        alert('Please enter a message');
        return;
    }
    
    // Check for spam/profanity
    const bannedWords = ['spam', 'abuse'];
    if (bannedWords.some(word => message.toLowerCase().includes(word))) {
        args.cancel = true;
        alert('Message contains inappropriate content');
        return;
    }
    
    // Log message for analytics
    console.log('User sent:', message);
};
```

## Typing Events

### User Typing Event

Fires while user is typing in the input field:

```tsx
import { ChatUIComponent, TypingEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [isTyping, setIsTyping] = useState(false);

    const handleUserTyping = (args: TypingEventArgs) => {
        console.log('User is typing:', args.isTyping);
        console.log('Current message:', args.message);
        console.log('User:', args.user.user);
        
        setIsTyping(args.isTyping);
    };

    return (
        <div>
            {isTyping && <p>You are typing...</p>}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                userTyping={handleUserTyping}
            />
        </div>
    );
}
```

### Typing Event Arguments

The `TypingEventArgs` interface provides complete typing event details:

| Property | Type | Description |
|----------|------|-------------|
| `event` | Event | The underlying input event that triggered the typing action |
| `isTyping` | boolean | `true` when user is actively typing, `false` when typing ends or message is sent |
| `message` | string | Current content of the message being typed |
| `name` | string | Name of the event ('userTyping') |
| `user` | UserModel | The current user who is typing |

### Detect Typing Status

Use `isTyping` to determine when user starts and stops typing:

```tsx
import { ChatUIComponent, TypingEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    const handleUserTyping = (args: TypingEventArgs) => {
        if (args.isTyping) {
            console.log('User started typing');
            
            // Notify server that user is typing
            notifyServer({ userId: args.user.id, isTyping: true });
            
            // Clear previous timeout
            if (typingTimeoutRef.current) {
                clearTimeout(typingTimeoutRef.current);
            }
            
            // Stop typing indicator after 2 seconds of inactivity
            typingTimeoutRef.current = setTimeout(() => {
                notifyServer({ userId: args.user.id, isTyping: false });
            }, 2000);
        } else {
            console.log('User stopped typing');
            notifyServer({ userId: args.user.id, isTyping: false });
        }
    };

    const notifyServer = (data: any) => {
        // Send typing status to server via WebSocket or API
        console.log('Notifying server:', data);
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            userTyping={handleUserTyping}
        />
    );
}
```

### Access Message Content

Use the `message` property to access what the user is typing:

```tsx
const handleUserTyping = (args: TypingEventArgs) => {
    const messageLength = args.message.length;
    
    console.log('Current message:', args.message);
    console.log('Character count:', messageLength);
    
    // Warn if message is too long
    if (messageLength > 1000) {
        console.warn('Message exceeds recommended length');
    }
    
    // Check for specific keywords
    if (args.message.includes('@urgent')) {
        console.log('Urgent message detected');
    }
};
```

### Real-Time Typing Notifications

Broadcast typing status to other users in real-time:

```tsx
import { ChatUIComponent, TypingEventArgs, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [typingUsers, setTypingUsers] = useState<UserModel[]>([]);
    const currentUser = { id: "user1", user: "Albert" };

    const handleUserTyping = (args: TypingEventArgs) => {
        // Send typing status via WebSocket
        const ws = new WebSocket('ws://example.com/chat');
        ws.send(JSON.stringify({
            type: 'typing',
            userId: args.user.id,
            userName: args.user.user,
            isTyping: args.isTyping,
            message: args.message
        }));
    };

    useEffect(() => {
        // Listen for other users' typing status
        const ws = new WebSocket('ws://example.com/chat');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'typing' && data.userId !== currentUser.id) {
                if (data.isTyping) {
                    // Add user to typing list
                    setTypingUsers(prev => [
                        ...prev.filter(u => u.id !== data.userId),
                        { id: data.userId, user: data.userName }
                    ]);
                } else {
                    // Remove user from typing list
                    setTypingUsers(prev => prev.filter(u => u.id !== data.userId));
                }
            }
        };

        return () => ws.close();
    }, []);

    return (
        <ChatUIComponent 
            user={currentUser}
            userTyping={handleUserTyping}
            typingUsers={typingUsers}
        />
    );
}
```

### Complete Typing Example with Analytics

```tsx
import { ChatUIComponent, TypingEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const typingStartTime = useRef<number | null>(null);
    const characterCount = useRef(0);

    const handleUserTyping = (args: TypingEventArgs) => {
        // Track when user starts typing
        if (args.isTyping && !typingStartTime.current) {
            typingStartTime.current = Date.now();
            characterCount.current = args.message.length;
            
            console.log('Started typing at:', new Date(typingStartTime.current));
        }
        
        // Track when user stops typing
        if (!args.isTyping && typingStartTime.current) {
            const duration = Date.now() - typingStartTime.current;
            const finalLength = args.message.length;
            const charsTyped = finalLength - characterCount.current;
            
            // Log analytics
            console.log('Typing session ended:', {
                duration: `${(duration / 1000).toFixed(1)}s`,
                charactersTyped: charsTyped,
                wordsPerMinute: Math.round((charsTyped / 5) / (duration / 60000)),
                user: args.user.user
            });
            
            // Reset tracking
            typingStartTime.current = null;
            characterCount.current = 0;
        }
        
        // Access current message content
        console.log('Current message:', args.message);
        console.log('Message length:', args.message.length);
        
        // Access event details
        if (args.event) {
            console.log('Event type:', args.event.type);
        }
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            userTyping={handleUserTyping}
        />
    );
}
```

## Attachment Events

### Before Attachment Upload

Fires before files are uploaded:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, BeforeAttachmentUploadEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleBeforeUpload = (args: BeforeAttachmentUploadEventArgs) => {
        console.log('Uploading:', args.files);
        
        // Validate file size
        const maxSize = 5 * 1024 * 1024;  // 5MB
        args.files.forEach(file => {
            if (file.size > maxSize) {
                console.warn('File too large:', file.name);
            }
        });
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        beforeAttachmentUpload: handleBeforeUpload
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Attachment Upload Success

Fires after successful file upload:

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, AttachmentUploadSuccessEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleUploadSuccess = (args: AttachmentUploadSuccessEventArgs) => {
        console.log('File uploaded successfully:', args);
        console.log('File name:', args.fileName);
        console.log('Upload response:', args.response);
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        attachmentUploadSuccess: handleUploadSuccess
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Attachment Upload Failure

Fires when file upload fails:

```tsx
const handleUploadFailure = (args: AttachmentUploadFailureEventArgs) => {
    console.error('Upload failed:', args.error);
    alert(`Failed to upload ${args.fileName}`);
};

const attachmentSettings: FileAttachmentSettingsModel = {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
    attachmentUploadFailure: handleUploadFailure
};
```

### Attachment Removed Event

Fires when user removes an attachment:

```tsx
const handleAttachmentRemoved = (args: AttachmentRemovedEventArgs) => {
    console.log('Attachment removed:', args.fileName);
    // Update UI or clean up
};

const attachmentSettings: FileAttachmentSettingsModel = {
    saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
    removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
    attachmentRemoved: handleAttachmentRemoved
};
```

### Attachment Click Event

Fires when user clicks on an attachment (either in the footer before sending or in a message after sending):

```tsx
import { ChatUIComponent, FileAttachmentSettingsModel, ChatAttachmentClickEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
        console.log('Attachment clicked:', args.file.name);
        console.log('File info:', {
            name: args.file.name,
            type: args.file.type,
            size: args.file.size,
            url: args.file.url
        });
        
        // Cancel default preview behavior if needed
        if (args.file.type === 'application/pdf') {
            args.cancel = true;
            window.open(args.file.url, '_blank');
        }
    };

    const attachmentSettings: FileAttachmentSettingsModel = {
        saveUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Save',
        removeUrl: 'https://services.syncfusion.com/js/production/api/FileUploader/Remove',
        attachmentClick: handleAttachmentClick
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            enableAttachments={true}
            attachmentSettings={attachmentSettings}
        />
    );
}
```

### Attachment Click Event Arguments

The `ChatAttachmentClickEventArgs` interface provides:

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | boolean | Set to `true` to prevent default preview rendering |
| `event` | Event | The underlying click event object |
| `file` | FileInfo | Complete file information including name, type, size, and URL |
| `name` | string | Name of the event ('attachmentClick') |

### FileInfo Properties

The `file` object in the event arguments contains:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Name of the file |
| `type` | string | MIME type of the file (e.g., 'image/png', 'application/pdf') |
| `size` | number | File size in bytes |
| `url` | string | URL or path to access the file |
| `fileSource` | string | Base64 or Blob source for the file |

### Handle Different File Types

```tsx
const handleAttachmentClick = (args: ChatAttachmentClickEventArgs) => {
    const file = args.file;
    
    // Handle images
    if (file.type?.startsWith('image/')) {
        showImagePreview(file.url);
        args.cancel = true;
    }
    // Handle PDFs
    else if (file.type === 'application/pdf') {
        window.open(file.url, '_blank');
        args.cancel = true;
    }
    // Handle videos
    else if (file.type?.startsWith('video/')) {
        playVideo(file.url);
        args.cancel = true;
    }
    // For other files, allow default download behavior
};
```

## Toolbar Events

### Toolbar Item Click Event

Fires when user clicks on message toolbar items:

```tsx
import { ChatUIComponent, MessageToolbarSettingsModel, MessageToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const chatRef = useRef<ChatUIComponent>(null);

    const handleToolbarClick = (args: MessageToolbarItemClickedEventArgs) => {
        const icon = args.item.iconCss;
        
        if (icon === 'e-icons e-chat-copy') {
            navigator.clipboard.writeText(args.message.text);
            console.log('Copied to clipboard');
        } 
        else if (icon === 'e-icons e-chat-reply') {
            console.log('Reply to message:', args.message.id);
        }
        else if (icon === 'e-icons e-chat-pin') {
            console.log('Pin message:', args.message.id);
        }
        else if (icon === 'e-icons e-chat-trash') {
            console.log('Delete message:', args.message.id);
        }
    };

    const messageToolbarSettings: MessageToolbarSettingsModel = {
        items: [
            { type: 'Button', iconCss: 'e-icons e-chat-copy', tooltip: 'Copy' },
            { type: 'Button', iconCss: 'e-icons e-chat-reply', tooltip: 'Reply' },
            { type: 'Button', iconCss: 'e-icons e-chat-pin', tooltip: 'Pin' },
            { type: 'Button', iconCss: 'e-icons e-chat-trash', tooltip: 'Delete' }
        ],
        itemClicked: handleToolbarClick
    };

    return (
        <ChatUIComponent 
            ref={chatRef}
            user={{ id: "user1", user: "Albert" }}
            messageToolbarSettings={messageToolbarSettings}
        />
    );
}
```

### Header Toolbar Click Event

Fires when header toolbar items are clicked:

```tsx
import { ChatUIComponent, ToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleHeaderToolbarClick = (args: ToolbarItemClickedEventArgs) => {
        if (args.item.iconCss === 'e-icons e-menu') {
            console.log('Menu clicked');
        }
        else if (args.item.iconCss === 'e-icons e-refresh') {
            console.log('Refresh clicked');
        }
    };

    const headerToolbar: ToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-refresh', align: 'Right', tooltip: 'Refresh' },
            { iconCss: 'e-icons e-menu', align: 'Right', tooltip: 'Menu' }
        ],
        itemClicked: handleHeaderToolbarClick
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerToolbar={headerToolbar}
        />
    );
}
```

## Advanced Event Handling

### Combined Event Handler

```tsx
function App() {
    const chatRef = useRef<ChatUIComponent>(null);

    const eventLog: string[] = [];

    const logEvent = (eventName: string, details: any) => {
        const timestamp = new Date().toLocaleTimeString();
        eventLog.push(`[${timestamp}] ${eventName}: ${JSON.stringify(details)}`);
        console.log(eventLog[eventLog.length - 1]);
    };

    return (
        <ChatUIComponent 
            ref={chatRef}
            user={{ id: "user1", user: "Albert" }}
            created={() => logEvent('Created', 'Chat initialized')}
            messageSend={(args) => logEvent('MessageSend', args.message.text)}
            userTyping={() => logEvent('UserTyping', 'User typing...')}
        />
    );
}
```

## Best Practices

1. **Use event validation** to prevent invalid data
2. **Handle cancellations gracefully** with user feedback
3. **Implement error handling** for attachment events
4. **Log important events** for debugging and analytics
5. **Debounce typing events** to improve performance
6. **Validate file uploads** before processing

