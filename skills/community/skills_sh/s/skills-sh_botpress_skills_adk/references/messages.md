# Messages & Events

Understanding how to send messages and events is critical for building conversational AI agents. This guide covers all message types, when to use them, and common pitfalls.

## Table of Contents

**Quick Links:**

- [Core Concepts](#core-concepts) - Messages vs Events, Agnostic vs Channel-Specific
- [Sending Messages in Conversations](#sending-messages-in-conversations) - Using `conversation.send()`
- [Message Metadata](#message-metadata-chat-integration) - Adding custom data to messages
- [All Message Types](#all-message-types) - Complete reference (text, image, file, card, etc.)
  - [File Messages & Metadata](#file-message-metadata) - File-specific metadata usage
  - [Custom Component (Webchat)](#custom-component-webchat) - Webchat-only custom UI components
- [Accessing Messages on Frontend](#accessing-messages-on-the-frontend) - Webchat SDK integration
- [Sending from Workflows](#sending-messages-from-workflows) - Using `client.createMessage()`
- [Sending Events (Ephemeral)](#sending-events-ephemeral) - Non-persistent notifications
- [Channel Compatibility](#channel-compatibility) - What works where
- [Common Mistakes](#common-mistakes) - Pitfalls to avoid
- [Best Practices](#best-practices) - Recommended patterns

## Core Concepts

### Messages vs Events

**Messages** are persistent conversation history items that users can see:

- Appear in chat history
- Survive page reloads
- Part of conversation context
- Sent using `conversation.send()` in conversations

**Events** are ephemeral signals that don't persist:

- NOT in conversation history
- Lost on page reload
- Used for real-time notifications
- Sent using integration actions (e.g., `bp.webchat.actions.customEvent()`)

### Agnostic vs Channel-Specific

**Agnostic Messages** work across multiple channels (defined in `@botpress/sdk`):

- `text`, `image`, `audio`, `video`, `file`, `location`
- `card`, `carousel`, `choice`, `dropdown`, `bloc`, `markdown`

**Channel-Specific Messages** only work in specific integrations:

- `customComponent` (webchat only)
- Platform-specific fields (e.g., Slack threads)

## Sending Messages in Conversations

### Basic Syntax

In conversation handlers, use `conversation.send()`:

```typescript
import { Conversation } from '@botpress/runtime'

export const Chat = new Conversation({
  channel: 'chat.channel',

  async handler({ message, conversation }) {
    // Send a message
    await conversation.send({
      type: 'text',
      payload: { text: 'Hello!' },
    })
  },
})
```

**CRITICAL**: Never use `client.createMessage()` directly in conversations. Always use `conversation.send()`.

```typescript
// ❌ WRONG - Don't use client directly
await client.createMessage({
  conversationId: conversation.id,
  type: 'text',
  payload: { text: 'Hello' },
})

// ✅ CORRECT - Use conversation.send()
await conversation.send({
  type: 'text',
  payload: { text: 'Hello' },
})
```

### Why Use `conversation.send()`?

- Automatically handles conversation context
- Type-safe for the channel
- Manages message tracking
- Integrates with ADK runtime

## Message Metadata (Chat Integration)

The **chat** integration supports an optional `metadata` field on **all message types**. This allows you to attach arbitrary custom data that will be available to the frontend.

```typescript
await conversation.send({
  type: 'text',
  payload: {
    text: 'Your order has been confirmed',
    metadata: {
      orderId: 'order_123',
      customerId: 'cust_456',
      trackingNumber: 'TRACK789',
      internalRef: 'ref_abc',
      // Any custom data you need
    },
  },
})
```

**Metadata Schema**:

- Type: `Record<string, any>` (key-value pairs)
- Keys: strings
- Values: any type (string, number, boolean, object, array)
- Optional on all message types

**Use Cases**:

- File identifiers for tracking
- Unique keys for deduplication
- Custom display properties
- Analytics tracking data
- Frontend state management

**Channel Support**:

- ✅ **chat**: Full metadata support on all message types
- ❓ **webchat**: Check generated types after adding dependency
- ❓ **Other channels**: Varies by integration

## All Message Types

### Text

Basic text message - works everywhere.

```typescript
await conversation.send({
  type: 'text',
  payload: {
    text: 'Hello, world!',
  },
})
```

### Markdown

Formatted text with markdown - **channel support varies**.

```typescript
await conversation.send({
  type: 'markdown',
  payload: {
    markdown: '**Bold** _italic_ `code` [link](https://example.com)',
  },
})
```

**Note**: Markdown support depends on the channel. Use `text` for guaranteed cross-channel compatibility.

### Image

Display an image from a URL.

```typescript
await conversation.send({
  type: 'image',
  payload: {
    imageUrl: 'https://example.com/image.png',
  },
})
```

### Audio

Play an audio file.

```typescript
await conversation.send({
  type: 'audio',
  payload: {
    audioUrl: 'https://example.com/audio.mp3',
  },
})
```

### Video

Display a video player.

```typescript
await conversation.send({
  type: 'video',
  payload: {
    videoUrl: 'https://example.com/video.mp4',
  },
})
```

### File

Share a downloadable file with optional metadata.

```typescript
await conversation.send({
  type: 'file',
  payload: {
    fileUrl: 'https://example.com/document.pdf',
    title: 'Invoice', // optional
    metadata: {
      // optional - see Message Metadata section
      fileId: 'file_123',
      uniqueKey: 'invoice-2024-001',
    },
  },
})
```

### Location

Share a geographic location.

```typescript
await conversation.send({
  type: 'location',
  payload: {
    latitude: 40.7128,
    longitude: -74.006,
    address: 'New York, NY', // optional
    title: 'Meeting Location', // optional
  },
})
```

### Card

Rich card with image, title, and action buttons.

```typescript
await conversation.send({
  type: 'card',
  payload: {
    title: 'Product Name',
    subtitle: 'Product description', // optional
    imageUrl: 'https://example.com/product.jpg', // optional
    actions: [
      {
        action: 'postback', // or "url" or "say"
        label: 'Buy Now',
        value: 'buy_product_123',
      },
      {
        action: 'url',
        label: 'Learn More',
        value: 'https://example.com/product',
      },
    ],
  },
})
```

**Action Types**:

- `postback`: Sends a value back to the bot (triggers new message)
- `url`: Opens a URL in browser
- `say`: Makes user "say" text (sends as user message)

### Carousel

Multiple cards in a scrollable carousel.

```typescript
await conversation.send({
  type: 'carousel',
  payload: {
    items: [
      {
        title: 'Product 1',
        subtitle: 'Description 1',
        imageUrl: 'https://example.com/product1.jpg',
        actions: [{ action: 'postback', label: 'Select', value: 'product_1' }],
      },
      {
        title: 'Product 2',
        subtitle: 'Description 2',
        imageUrl: 'https://example.com/product2.jpg',
        actions: [{ action: 'postback', label: 'Select', value: 'product_2' }],
      },
    ],
  },
})
```

### Choice (Buttons)

Quick reply buttons for user selection.

```typescript
await conversation.send({
  type: 'choice',
  payload: {
    text: 'What would you like to do?',
    options: [
      { label: 'Option 1', value: 'opt1' },
      { label: 'Option 2', value: 'opt2' },
      { label: 'Option 3', value: 'opt3' },
    ],
    disableFreeText: false, // optional - prevent typing
  },
})
```

### Dropdown

Dropdown/select menu for user selection.

```typescript
await conversation.send({
  type: 'dropdown',
  payload: {
    text: 'Select your country:',
    options: [
      { label: 'United States', value: 'us' },
      { label: 'Canada', value: 'ca' },
      { label: 'United Kingdom', value: 'uk' },
    ],
    disableFreeText: true, // optional
  },
})
```

### Bloc

Multiple messages grouped together (composite message).

```typescript
await conversation.send({
  type: 'bloc',
  payload: {
    items: [
      {
        type: 'text',
        payload: { text: "Here's your order summary:" },
      },
      {
        type: 'image',
        payload: { imageUrl: 'https://example.com/product.jpg' },
      },
      {
        type: 'text',
        payload: { text: 'Total: $99.99' },
      },
    ],
  },
})
```

**Allowed item types in bloc**:

- `text`, `markdown`, `image`, `audio`, `video`, `file`, `location`

### Custom Component (Webchat)

Send a custom React component in webchat conversations using the `customComponent` message type:

```typescript
import { WelcomeBannerComponent } from '../components'

await conversation.send({
  type: 'customComponent',
  payload: {
    component: WelcomeBannerComponent,
    props: {},
  },
})
```

Components are `.bp.tsx` files registered in `src/components/index.ts` with `new CustomComponent()`. See the component registry reference for the full creation flow.

When components are listed in a `Conversation`'s `components` array, the LLM can also yield them autonomously during `execute()` — no explicit `send()` needed.

**Note**: Custom components only work in webchat channels. For other channels, use agnostic message types like `card` or `carousel`.

## Accessing Messages on the Frontend

Messages (including metadata) are available to frontend clients via the webchat SDK.

### Listening to New Messages

```javascript
// React to new messages as they arrive
window.botpressWebChat.onMessage((message) => {
  console.log('New message:', message)

  if (message.type === 'file') {
    console.log('File URL:', message.payload.fileUrl)
    console.log('File title:', message.payload.title)
    console.log('Metadata:', message.payload.metadata)

    // Access custom metadata
    const { fileId, uniqueKey, customData } = message.payload.metadata || {}

    // Fetch file contents if needed
    fetch(message.payload.fileUrl)
      .then((response) => response.text())
      .then((content) => {
        console.log('File content:', content)
      })
  }
})
```

### Reconstructing State from Message History

On page reload, iterate through conversation history to reconstruct application state:

```javascript
// Get all messages from conversation history
window.botpressWebChat.getMessages().then((messages) => {
  // Filter for file messages with specific metadata
  const componentFiles = messages.filter((msg) => msg.type === 'file' && msg.payload.metadata?.fileType === 'component')

  // Reconstruct state from persisted messages
  componentFiles.forEach(async (msg) => {
    const { fileUrl, metadata } = msg.payload
    const { componentId, stepId } = metadata

    // Fetch and restore component
    const content = await fetch(fileUrl).then((r) => r.text())
    restoreComponent(componentId, stepId, content)
  })
})
```

### Message Persistence Benefits

Messages (unlike events) are:

- ✅ Persisted in conversation history
- ✅ Replayed on page reload
- ✅ Available via `getMessages()` API
- ✅ Include all metadata

This makes messages ideal for:

- State reconstruction after page reload
- File tracking and retrieval
- Workflow progress indicators
- Audit trails

## Sending Messages from Workflows

Workflows can't use `conversation.send()` - they must use `client.createMessage()`:

```typescript
import { Workflow } from '@botpress/runtime'

export const NotifyWorkflow = new Workflow({
  name: 'notify',
  input: z.object({
    conversationId: z.string(), // REQUIRED for messaging!
    message: z.string(),
  }),

  handler: async ({ input, client, step }) => {
    await step('send-notification', async () => {
      await client.createMessage({
        conversationId: input.conversationId,
        type: 'text',
        payload: { text: input.message },
      })
    })
  },
})
```

**CRITICAL**: Always pass `conversationId` to workflows that need to send messages (see Common Mistakes section for details).

## Sending Events (Ephemeral)

Events are **NOT messages** - they don't persist in conversation history. Use integration actions to send ephemeral events (see [Integration Actions for Messages](#integration-actions-for-messages) section for examples).

### When to Use Events vs Messages

**Use Messages** (persistent) when:

- User needs to see it in history
- It's part of the conversation flow
- You want it to survive page reloads
- Examples: chat responses, confirmations, results

**Use Events** (ephemeral) when:

- Real-time notifications (typing indicators, progress)
- UI state changes (show/hide widget, config updates)
- Temporary feedback (loading, processing)
- Examples: "Agent is typing...", "File uploading..."

## Integration Actions for Messages

Some integrations provide actions for special message types and events:

```typescript
// Webchat - Send custom event (ephemeral, not persisted)
await client.callAction({
  type: 'webchat:customEvent',
  input: {
    conversationId: conversation.id,
    event: JSON.stringify({
      type: 'notification',
      message: 'Processing...',
    }),
  },
})

// Webchat - Show/hide widget
await client.callAction({
  type: 'webchat:showWebchat',
  input: { conversationId: conversation.id },
})

await client.callAction({
  type: 'webchat:hideWebchat',
  input: { conversationId: conversation.id },
})

// Webchat - Update configuration
await client.callAction({
  type: 'webchat:configWebchat',
  input: {
    conversationId: conversation.id,
    config: JSON.stringify({
      theme: { primaryColor: '#ff0000' },
    }),
  },
})
```

**Frontend event handling**:

```javascript
window.botpressWebChat.onEvent(
  (event) => {
    if (event.type === 'notification') {
      showToast(event.message)
    }
  },
  ['TRIGGER']
)
```

## Channel Compatibility

Not all message types work in all channels:

| Message Type    | Chat | Webchat           | Slack | WhatsApp | Teams |
| --------------- | ---- | ----------------- | ----- | -------- | ----- |
| text            | ✅   | ✅                | ✅    | ✅       | ✅    |
| markdown        | ✅   | ✅                | ✅    | ❌       | ✅    |
| image           | ✅   | ✅                | ✅    | ✅       | ✅    |
| audio           | ✅   | ✅                | ❌    | ✅       | ❌    |
| video           | ✅   | ✅                | ❌    | ✅       | ❌    |
| file            | ✅   | ✅                | ✅    | ✅       | ✅    |
| location        | ✅   | ✅                | ❌    | ✅       | ❌    |
| card            | ✅   | ✅                | ✅    | ❌       | ✅    |
| carousel        | ✅   | ✅                | ❌    | ❌       | ❌    |
| choice          | ✅   | ✅                | ✅    | ✅       | ✅    |
| dropdown        | ✅   | ✅                | ❌    | ✅       | ❌    |
| bloc            | ✅   | ✅                | ❌    | ❌       | ❌    |
| customComponent | ❌   | ✅ (webchat only) | ❌    | ❌       | ❌    |

**Tip**: Use `text` and `image` for maximum compatibility across channels.

## Common Mistakes

### 1. Using client.createMessage() in Conversations

```typescript
// ❌ WRONG
export const Chat = new Conversation({
  async handler({ client }) {
    await client.createMessage({
      /* ... */
    })
  },
})

// ✅ CORRECT
export const Chat = new Conversation({
  async handler({ conversation }) {
    await conversation.send({
      /* ... */
    })
  },
})
```

### 2. Using client.createEvent() for Messages

```typescript
// ❌ WRONG - Events don't persist!
await client.createEvent({
  conversationId: conversation.id,
  type: 'text',
  payload: { text: 'Hello' },
})

// ✅ CORRECT - Use messages
await conversation.send({
  type: 'text',
  payload: { text: 'Hello' },
})
```

### 3. Missing conversationId in Workflows

```typescript
// ❌ WRONG - Can't send messages without conversationId
export const MyWorkflow = new Workflow({
  handler: async ({ input, client }) => {
    await client.createMessage({
      // Where's conversationId? This will fail!
      type: 'text',
      payload: { text: 'Hello' },
    })
  },
})

// ✅ CORRECT - Pass conversationId in input
export const MyWorkflow = new Workflow({
  input: z.object({
    conversationId: z.string(),
  }),
  handler: async ({ input, client }) => {
    await client.createMessage({
      conversationId: input.conversationId,
      type: 'text',
      payload: { text: 'Hello' },
    })
  },
})
```

### 4. Using Custom Components in Non-Webchat Channels

```typescript
// ❌ WRONG - customComponent only works in webchat
export const SlackChat = new Conversation({
  channel: 'slack.dm',
  async handler({ conversation }) {
    await conversation.send({
      type: 'customComponent', // Will fail in Slack!
      payload: {
        component: TicketCardComponent,
        props: {
          /* ... */
        },
      },
    })
  },
})

// ✅ CORRECT - Use agnostic message types for non-webchat channels
export const SlackChat = new Conversation({
  channel: 'slack.dm',
  async handler({ conversation }) {
    await conversation.send({
      type: 'card', // Works in Slack
      payload: { title: 'Ticket', subtitle: 'Details here', actions: [] },
    })
  },
})
```

## Best Practices

### 1. Type Safety

TypeScript will help you with type-safe payloads:

```typescript
// TypeScript knows the payload structure based on type
await conversation.send({
  type: 'card',
  payload: {
    title: 'Required',
    subtitle: 'Optional',
    // IntelliSense will suggest all valid fields!
  },
})
```

### 2. Graceful Degradation

When supporting multiple channels:

```typescript
import { TicketCardComponent } from '../components'

export const Chat = new Conversation({
  async handler({ conversation }) {
    if (conversation.channel === 'webchat.channel') {
      // Webchat supports custom components
      await conversation.send({
        type: 'customComponent',
        payload: {
          component: TicketCardComponent,
          props: { ticketId: 'TKT-001', title: 'VPN issue', priority: 'high', status: 'open' },
        },
      })
    } else {
      // Fall back to card for other channels
      await conversation.send({
        type: 'card',
        payload: {
          title: 'TKT-001: VPN issue',
          subtitle: 'Priority: high · Status: open',
          actions: [],
        },
      })
    }
  },
})
```

### 3. Error Handling

Always wrap message sending in try-catch:

```typescript
try {
  await conversation.send({
    type: 'image',
    payload: { imageUrl: maybeInvalidUrl },
  })
} catch (error) {
  console.error('Failed to send image:', error)
  // Fall back to text
  await conversation.send({
    type: 'text',
    payload: { text: 'Image unavailable' },
  })
}
```

### 4. Message Composition

Break complex messages into parts:

```typescript
// Instead of one giant text
await conversation.send({
  type: 'text',
  payload: { text: 'Title\n\nBody text here\n\nFooter' },
})

// Use bloc for better structure
await conversation.send({
  type: 'bloc',
  payload: {
    items: [
      { type: 'markdown', payload: { markdown: '**Title**' } },
      { type: 'text', payload: { text: 'Body text here' } },
      { type: 'text', payload: { text: 'Footer' } },
    ],
  },
})
```

## Summary

**In Conversations**: Use `conversation.send()` for messages (persistent, type-safe)

**In Workflows**: Use `client.createMessage()` with `conversationId` in input

**Events**: Use integration actions for ephemeral notifications (don't persist)

**Key Rules**:

1. ✅ Use `conversation.send()` in conversations, `client.createMessage()` in workflows
2. ✅ Always pass `conversationId` to workflows that send messages
3. ✅ Use messages for persistent content, events for ephemeral notifications
4. ✅ In webchat conversations, use `customComponent` message type with a `CustomComponent` reference
5. ❌ Never use `client.createMessage()` in conversations
6. ❌ Check channel compatibility for message types (see table above)
