---
name: mention-integration
description: Integrate user mentions in Chat-UI with custom trigger characters and selection handling.
---

# Mention Integration

## Table of Contents
- [Configure Mention Users](#configure-mention-users)
- [Customize Trigger Character](#customize-trigger-character)
- [Predefined Mentions](#predefined-mentions)
- [Mention Selection Event](#mention-selection-event)

## Configure Mention Users

### Setup Mention Users

Define users available for mentioning:

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    const mentionUsers: UserModel[] = [
        { id: "user2", user: "Michale Suyama" },
        { id: "user3", user: "Reena" },
        { id: "user4", user: "John Smith" }
    ];

    return (
        <ChatUIComponent 
            user={currentUser}
            mentionUsers={mentionUsers}
        />
    );
}
```

### Mention Trigger

When users type `@`, a dropdown appears with mention options:

```tsx
// User types: "@M"
// Dropdown shows:
// - Michale Suyama
// - (filtered by "M")
```

## Customize Trigger Character

### Change Trigger Character

Use different trigger character instead of `@`:

```tsx
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const mentionUsers: UserModel[] = [
        { id: "user2", user: "Michale" },
        { id: "user3", user: "Reena" }
    ];

    return (
        <>
            {/* Default: @ trigger */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                mentionUsers={mentionUsers}
                mentionTriggerChar="@"  // Default
            />

            {/* Alternative triggers */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                mentionUsers={mentionUsers}
                mentionTriggerChar="#"  // Hash tag
            />

            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                mentionUsers={mentionUsers}
                mentionTriggerChar="+"  // Plus sign
            />
        </>
    );
}
```

## Predefined Mentions

### Include Mentions in Messages

Use placeholder syntax to include predefined mentions:

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel, MessageModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    const michale: UserModel = {
        id: "user2",
        user: "Michale"
    };

    const reena: UserModel = {
        id: "user3",
        user: "Reena"
    };

    const messages: MessageModel[] = [
        {
            text: "Hi {0}, can you review this?",
            author: currentUser,
            mentionUsers: [michale]  // {0} = Michale
        },
        {
            text: "Sure {0}, I'll check it out.",
            author: michale,
            mentionUsers: [currentUser]  // {0} = Albert
        },
        {
            text: "{0} and {1}, please join the call.",
            author: currentUser,
            mentionUsers: [michale, reena]  // {0} = Michale, {1} = Reena
        }
    ];

    return (
        <ChatUIComponent user={currentUser} messages={messages} />
    );
}
```

### Placeholder Mapping

```tsx
// Single mention
text: "Hey {0}!"
mentionUsers: [user1]
// Result: "Hey User1!"

// Multiple mentions
text: "{0} and {1} are here"
mentionUsers: [user1, user2]
// Result: "User1 and User2 are here"

// Three mentions
text: "{0}, {1}, and {2} should see this"
mentionUsers: [user1, user2, user3]
// Result: "User1, User2, and User3 should see this"
```

## Mention Selection Event

### Handle Mention Selection

Respond when user selects a mention:

```tsx
import { ChatUIComponent, MentionSelectEventArgs, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const mentionUsers: UserModel[] = [
        { id: "user2", user: "Michale Suyama" },
        { id: "user3", user: "Reena" }
    ];

    const handleMentionSelect = (args: MentionSelectEventArgs) => {
        console.log('Mention selected:', args.user.user);
        console.log('User ID:', args.user.id);
        // args.user contains the selected user details
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            mentionUsers={mentionUsers}
            mentionSelect={handleMentionSelect}
        />
    );
}
```

### Log Mention Selection

```tsx
const handleMentionSelect = (args: MentionSelectEventArgs) => {
    const selectedUser = args.user;
    
    console.log(`User mentioned: ${selectedUser.user}`);
    console.log(`User ID: ${selectedUser.id}`);
    
    // Send analytics
    trackEvent('mention_selected', {
        mentionedUser: selectedUser.user,
        timestamp: new Date()
    });
};
```

## Complete Example

### Full Mention Setup

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel, MessageModel, MentionSelectEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const currentUser: UserModel = {
        id: "user1",
        user: "Albert"
    };

    const mentionUsers: UserModel[] = [
        { id: "user2", user: "Michale Suyama", avatarBgColor: "#e3165b" },
        { id: "user3", user: "Reena", avatarBgColor: "#6d3e94" },
        { id: "user4", user: "John Smith", avatarBgColor: "#3c78d8" },
        { id: "user5", user: "Sarah Johnson", avatarBgColor: "#f5a623" }
    ];

    const initialMessages: MessageModel[] = [
        {
            text: "Hey team, let's sync up!",
            author: currentUser
        },
        {
            text: "{0}, can you prepare the report?",
            author: { id: "user2", user: "Manager" },
            mentionUsers: [mentionUsers[0]]  // Michale
        },
        {
            text: "Sure, {0} and {1} - I'll have it by tomorrow.",
            author: currentUser,
            mentionUsers: [mentionUsers[0], mentionUsers[1]]  // Michale and Reena
        }
    ];

    const handleMentionSelect = (args: MentionSelectEventArgs) => {
        console.log(`@${args.user.user} mentioned`);
    };

    return (
        <ChatUIComponent 
            user={currentUser}
            headerText="Team Chat"
            mentionUsers={mentionUsers}
            mentionTriggerChar="@"
            mentionSelect={handleMentionSelect}
            messages={initialMessages}
        >
            <MessagesDirective>
                {initialMessages.map((msg, index) => (
                    <MessageDirective 
                        key={index}
                        text={msg.text}
                        author={msg.author}
                        mentionUsers={msg.mentionUsers}
                    />
                ))}
            </MessagesDirective>
        </ChatUIComponent>
    );
}

export default App;
```

## Mention Display

### How Mentions Appear

In the chat interface:
- Typed mentions: `@Michale Suyama` → clickable user pill
- Placeholder mentions: `{0}` → replaced with user name
- Color coded: Different users get different colors
- Hoverable: Shows user details on hover

### Mention Styling

Users are typically displayed as:
- Pills/badges with user color
- Clickable to open user profile
- Highlighted with special formatting

## Best Practices

1. **Limit mention users** to relevant people (5-50)
2. **Alphabetically sort** mention list
3. **Show avatars** in mention dropdown
4. **Handle large teams** with search capability
5. **Validate mentions** before sending
6. **Log mention analytics** for engagement
7. **Notify mentioned users** appropriately

## Advanced: Dynamic Mention Users

```tsx
import React, { useState, useEffect } from 'react';
import { ChatUIComponent, UserModel } from '@syncfusion/ej2-react-interactive-chat';

function App() {
    const [mentionUsers, setMentionUsers] = useState<UserModel[]>([]);

    useEffect(() => {
        // Fetch team members from API
        fetchTeamMembers().then(members => {
            setMentionUsers(members);
        });
    }, []);

    const fetchTeamMembers = async (): Promise<UserModel[]> => {
        // API call to get team members
        const response = await fetch('/api/team/members');
        const data = await response.json();
        return data.map(member => ({
            id: member.id,
            user: member.name
        }));
    };

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            mentionUsers={mentionUsers}
        />
    );
}
```
