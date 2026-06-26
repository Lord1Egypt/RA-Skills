---
name: timestamp-and-timebreaks
description: Display and format timestamps in Chat-UI and configure time breaks for message organization.
---

# Timestamp and Time Breaks

## Table of Contents
- [Timestamp Display](#timestamp-display)
- [Timestamp Format](#timestamp-format)
- [Time Breaks](#time-breaks)
- [Time Break Customization](#time-break-customization)

## Timestamp Display

### Show Timestamps

Display message timestamps globally:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            showTimeStamp={true}  // Enable timestamps
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Hello!" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={new Date('2024-01-15 09:30')}
                />
                <MessageDirective 
                    text="Hi there!" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={new Date('2024-01-15 09:32')}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Hide Timestamps

```tsx
<ChatUIComponent 
    user={{ id: "user1", user: "Albert" }}
    showTimeStamp={false}  // Hide timestamps
/>
```

## Timestamp Format

### Default Format

Default format: `dd/MM/yyyy hh:mm a`

Example: `15/01/2024 09:30 AM`

### Custom Timestamp Format

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            timeStampFormat="MMMM hh:mm a"  // Format: "January 09:30 AM"
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Good morning!" 
                    author={{ id: "user1", user: "Albert" }}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Common Format Patterns

```tsx
// Date and time
timeStampFormat="dd/MM/yyyy hh:mm a"      // 15/01/2024 09:30 AM
timeStampFormat="MM/dd/yyyy hh:mm:ss a"   // 01/15/2024 09:30:45 AM

// Time only
timeStampFormat="hh:mm a"                  // 09:30 AM
timeStampFormat="HH:mm"                    // 09:30 (24-hour)
timeStampFormat="h:mm a"                   // 9:30 AM

// Long format
timeStampFormat="MMMM d, yyyy hh:mm a"    // January 15, 2024 09:30 AM
timeStampFormat="dddd, MMMM d hh:mm a"   // Monday, January 15 09:30 AM

// Short format
timeStampFormat="MMM d hh:mm"              // Jan 15 09:30
timeStampFormat="M/d/yy h:mm a"            // 1/15/24 9:30 AM
```

### Per-Message Format

Set format for individual messages:

```tsx
<MessagesDirective>
    <MessageDirective 
        text="Custom time" 
        author={{ id: "user1", user: "Albert" }}
        timeStamp={new Date('2024-01-15 09:30')}
        timeStampFormat="hh:mm a"  // Only time
    />
    <MessageDirective 
        text="Full datetime" 
        author={{ id: "user2", user: "Support" }}
        timeStamp={new Date('2024-01-15 10:00')}
        timeStampFormat="dd/MM/yyyy hh:mm a"  // Full format
    />
</MessagesDirective>
```

## Time Breaks

### Show Time Breaks

Display date separators between messages:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const today = new Date('2024-01-15');
    const yesterday = new Date('2024-01-14');

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            showTimeBreak={true}  // Enable time breaks
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Message from yesterday" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={yesterday}
                />
                <MessageDirective 
                    text="Message from today" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={today}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Hide Time Breaks

```tsx
<ChatUIComponent 
    user={{ id: "user1", user: "Albert" }}
    showTimeBreak={false}  // Disable time breaks (default)
/>
```

## Time Break Customization

### Custom Time Break Template

Create custom separator appearance:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const timeBreakTemplate = (context) => {
        const date = new Date(context.messageDate);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        let label = '';
        if (date.toDateString() === today.toDateString()) {
            label = 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            label = 'Yesterday';
        } else {
            label = date.toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric'
            });
        }

        return (
            <div style={{
                textAlign: 'center',
                margin: '16px 0',
                padding: '8px 0'
            }}>
                <span style={{
                    backgroundColor: '#e0e0e0',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    color: '#666',
                    fontWeight: '500'
                }}>
                    {label}
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
                    text="Yesterday's message" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={new Date(Date.now() - 86400000)}
                />
                <MessageDirective 
                    text="Today's message" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={new Date()}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}
```

### Styled Time Break

```tsx
const timeBreakTemplate = (context) => {
    const date = new Date(context.messageDate);
    const formatted = date.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric'
    });

    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            margin: '20px 0',
            gap: '12px'
        }}>
            <div style={{ flex: 1, height: '1px', backgroundColor: '#ddd' }} />
            <span style={{
                color: '#999',
                fontSize: '12px',
                whiteSpace: 'nowrap'
            }}>
                {formatted}
            </span>
            <div style={{ flex: 1, height: '1px', backgroundColor: '#ddd' }} />
        </div>
    );
};
```

## Complete Example

### Full Timestamp and Time Break Setup

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const twoDaysAgo = new Date(today);
    twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

    const timeBreakTemplate = (context) => {
        const date = new Date(context.messageDate);
        const isToday = date.toDateString() === today.toDateString();
        const isYesterday = date.toDateString() === yesterday.toDateString();

        let label = '';
        if (isToday) {
            label = 'Today';
        } else if (isYesterday) {
            label = 'Yesterday';
        } else {
            label = date.toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric'
            });
        }

        return (
            <div style={{
                textAlign: 'center',
                margin: '16px 0',
                opacity: 0.6
            }}>
                <span style={{
                    fontSize: '12px',
                    color: '#999'
                }}>
                    {label}
                </span>
            </div>
        );
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            headerText="Message History"
            showTimeStamp={true}
            timeStampFormat="hh:mm a"
            showTimeBreak={true}
            timeBreakTemplate={timeBreakTemplate}
        >
            <MessagesDirective>
                <MessageDirective 
                    text="Conversation from 2 days ago" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={new Date(twoDaysAgo.getFullYear(), twoDaysAgo.getMonth(), twoDaysAgo.getDate(), 10, 30)}
                />
                <MessageDirective 
                    text="Yesterday's discussion" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 14, 15)}
                />
                <MessageDirective 
                    text="Today's update" 
                    author={{ id: "user2", user: "Support" }}
                    timeStamp={new Date(today.getFullYear(), today.getMonth(), today.getDate(), 9, 45)}
                />
                <MessageDirective 
                    text="Just now" 
                    author={{ id: "user1", user: "Albert" }}
                    timeStamp={new Date()}
                />
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

## Best Practices

1. **Choose appropriate formats** for your use case
2. **Use 24-hour format** for professional applications
3. **Display time breaks** for long conversations
4. **Update timestamps** in real-time when needed
5. **Make timestamps visible** but not intrusive
6. **Test timestamp display** with different locales
7. **Consider timezone** handling for multi-user chats

## Format Codes Reference

| Code | Example | Description |
|------|---------|-------------|
| `d` | 1 | Day of month (1-31) |
| `dd` | 01 | Day of month (01-31) |
| `M` | 1 | Month (1-12) |
| `MM` | 01 | Month (01-12) |
| `MMM` | Jan | Month abbreviation |
| `MMMM` | January | Full month name |
| `yy` | 24 | 2-digit year |
| `yyyy` | 2024 | 4-digit year |
| `h` | 9 | Hour (1-12) |
| `hh` | 09 | Hour (01-12) |
| `H` | 9 | Hour (0-23) |
| `HH` | 09 | Hour (00-23) |
| `m` | 5 | Minute (0-59) |
| `mm` | 05 | Minute (00-59) |
| `s` | 5 | Second (0-59) |
| `ss` | 05 | Second (00-59) |
| `a` | AM/PM | AM or PM |
| `ddd` | Mon | Weekday abbreviation |
| `dddd` | Monday | Full weekday name |
