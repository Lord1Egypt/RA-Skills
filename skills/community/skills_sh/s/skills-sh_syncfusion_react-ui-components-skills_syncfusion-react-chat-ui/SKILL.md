---
name: syncfusion-react-chat-ui
description: Implement the Syncfusion React Chat UI component. Use this skill to create and customize messaging interfaces, including chat setup, message rendering, file attachments, typing indicators, conversation layout, theming, event handling, and real-time updates in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React Chat-UI in Syncfusion React

## Component Overview

The Chat-UI component provides a complete conversational interface with real-time messaging, file attachments, user presence, and extensive customization options. This skill guides you through implementing chat interfaces for customer support, team collaboration, and interactive applications.

### Key Capabilities

The Chat-UI component is an interactive messaging interface featuring:
- **Rich Message Support:** Text, markdown, formatted content
- **User Management:** Multi-user conversations, presence status, avatars
- **File Attachments:** Upload, preview, download with restrictions
- **Event System:** Lifecycle, interaction, and attachment events
- **Templates:** Customizable UI for messages, suggestions, footer
- **Internationalization:** Multi-language and RTL support

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation
- Basic component initialization
- CSS theming and imports

### Message Management
📄 **Read:** [references/message-management.md](references/message-management.md)
- Adding and updating messages
- Auto-scroll to latest messages
- Progressive message loading (on-demand)
- Message configuration (pinned, reply, forward)
- Message status tracking
- Message toolbar customization

### User Configuration
📄 **Read:** [references/user-configuration.md](references/user-configuration.md)
- User model setup
- Avatar customization
- User presence status
- CSS class customization

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Component lifecycle events
- Message sending events
- User typing events (with complete event arguments)
- Attachment upload and click events
- Toolbar click events

### Templating System
📄 **Read:** [references/templating-system.md](references/templating-system.md)
- Empty chat template
- Message custom rendering
- Time break template
- Typing indicator template
- Suggestion template
- Footer template customization

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enable attachment support
- Configure upload endpoints
- File type and size restrictions
- Drag-and-drop support
- Attachment templates (preview and footer)
- Handle attachment click events

### Header Customization
📄 **Read:** [references/header-customization.md](references/header-customization.md)
- Header visibility and text
- Header icon styling
- Toolbar configuration
- Toolbar item types and events

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- Pompact mode layout for dense conversations
- Claceholder text configuration
- Width and height customization
- CSS class application
- Component-level styling

### Timestamp and Time Breaks
📄 **Read:** [references/timestamp-and-timebreaks.md](references/timestamp-and-timebreaks.md)
- Show/hide timestamps
- Timestamp format customization
- Time break separators
- Date-wise organization

### Typing Indicator
📄 **Read:** [references/typing-indicator.md](references/typing-indicator.md)
- Show/hide typing indicator
- Multi-user typing display
- Typing indicator template customization

### Mention Integration
📄 **Read:** [references/mention-integration.md](references/mention-integration.md)
- Configure mentionable users
- Customize mention trigger character
- Predefined mentions in messages
- Mention selection events

### Globalization and RTL
📄 **Read:** [references/globalization-rtl.md](references/globalization-rtl.md)
- Localization and language support
- Right-to-Left (RTL) layout
- Typing indicator localization


## Quick Start Example

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';
import * as ReactDOM from "react-dom";

function App() {
    const currentUserModel: UserModel = {
        id: "user1",
        user: "Albert"
    };

    const otherUserModel: UserModel = {
        id: "user2",
        user: "Michale Suyama"
    };

    return (
        <ChatUIComponent user={currentUserModel} headerText="Chat Support">
            <MessagesDirective>
                <MessageDirective text="Hello, how can I help?" author={currentUserModel} />
                <MessageDirective text="I need assistance with my order." author={otherUserModel} />
            </MessagesDirective>
        </ChatUIComponent>
    );
}

ReactDOM.render(<App />, document.getElementById('container'));
```

## Common Patterns

### Create a Support Chat Interface
```tsx
<ChatUIComponent 
  user={currentUser}
  headerText="Support Chat"
  enableAttachments={true}
  showTimeStamp={true}
  showHeader={true}
  messageToolbarSettings={{ items: ['Copy', 'Reply', 'Delete'] }}
>
  <MessagesDirective>
    {/* messages populate here */}
  </MessagesDirective>
</ChatUIComponent>
```

### Add Message Dynamically
```tsx
const chatRef = useRef<ChatUIComponent>(null);

const addNewMessage = () => {
  chatRef.current.addMessage({
    author: userModel,
    text: "Your message here",
    timeStamp: new Date()
  });
};
```

### Configure Multiple Templates
Implement `messageTemplate`, `emptyChatTemplate`, `timeBreakTemplate`, and `suggestionTemplate` for complete customization.

## Key Props

| Prop | Type | Purpose |
|------|------|---------|
| `user` | UserModel | Current logged-in user |
| `messages` | MessageModel[] | Initial message list |
| `headerText` | string | Header title |
| `placeholder` | string | Input field hint |
| `enableAttachments` | boolean | File upload support |
| `showTimeStamp` | boolean | Display message timestamps |
| `showHeader` | boolean | Show header section |
| `showFooter` | boolean | Show input footer |
| `autoScrollToBottom` | boolean | Auto-scroll to latest message |
| `loadOnDemand` | boolean | Progressive message loading |
| `enableCompactMode` | boolean | Left-aligned compact layout |
| `enableRtl` | boolean | Right-to-left layout |
| `locale` | string | Language/culture code |

## Common Use Cases

**Use Case 1: Customer Support Chat**
- Multiple support agents handling customer queries
- File attachment for screenshots and auto-scroll
- Typing indicators to show agent engagement
- Progressive loading for long conversation histories
- Typing indicators to show agent engagement

**Use Case 2: Team Collaboration**
- Mention team members with @
- Compact mode for group conversations
- Pin important discussions
- Forward messages for reference
- Message editing and deletion

**Use Case 3: Multilingual Chat Application**
- RTL support for Arabic/Hebrew
- Localized UI strings
- Support for multiple cultures

---

**For complete examples and advanced scenarios, explore individual reference files above.**
