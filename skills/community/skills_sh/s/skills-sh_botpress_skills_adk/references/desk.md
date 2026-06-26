# Desk Integration

Desk is Botpress's AI-augmented support workspace where human agents and AI bots collaborate on customer tickets. This guide covers how to build ADK agents that participate in the Desk support workflow.

## Quick Start

Minimal working example for a Desk support bot:

```typescript
// src/conversations/desk.ts
import { Autonomous, context, Conversation, z } from '@botpress/runtime'
import { actions, joinMarkdownChildren } from '@botpress/runtime/runtime'

export default new Conversation({
  channel: 'desk.ticket',
  state: z.object({
    lastSync: z.string().default(''),
  }),
  events: ['desk:ticketActivity'],
  handler: async ({ conversation, execute, send }) => {
    // CRITICAL: Only process tickets assigned to this bot
    if (conversation.tags['desk:dassignedself'] !== 'true') {
      console.log('Ticket not assigned to bot, ignoring...')
      return
    }

    await execute({
      tools: [],
      instructions: 'You are a helpful support agent...',
    })
  },
})
```

### Configuration (agent.config.ts)

```typescript
import { defineConfig } from '@botpress/runtime'

export default defineConfig({
  name: 'support-bot',

  dependencies: {
    integrations: {
      desk: {
        enabled: true,
        configuration: {
          displayName: 'Support Bot',
          botHandle: 'SupportBot',
          canBeAssigned: true,
        },
      },
    },
  },
})
```

---

## Overview

### What is Desk?

Desk is a unified support workspace that:

- Aggregates tickets from multiple sources (Intercom, Zendesk, native)
- Enables human agents and AI bots to collaborate on customer tickets
- Provides real-time activity feeds and assignment management
- Supports internal notes (staff-only) and customer-visible replies

### Bot Participation Modes

| Mode          | `canBeAssigned` | Description                                            |
| ------------- | --------------- | ------------------------------------------------------ |
| **Assigned**  | `true`          | Bot owns tickets and replies directly to customers     |
| **Assisting** | `false`         | Bot helps human agents with suggestions and automation |

### Multi-Bot Teams

Multiple bots can be registered with Desk, each with different capabilities:

- A triage bot that classifies and routes tickets
- A knowledge bot that searches documentation
- A specialist bot for specific product areas

Each bot is identified by its `botHandle` (e.g., "@SupportBot", "@TriageBot").

---

## Configuration

All Desk configuration lives in `agent.config.ts` inside the `dependencies.integrations.desk` block:

```typescript
import { defineConfig } from '@botpress/runtime'

export default defineConfig({
  name: 'my-agent',

  dependencies: {
    integrations: {
      desk: {
        enabled: true,
        configuration: {
          displayName: 'My Support Bot',
          botHandle: 'MySupportBot',
          displayAvatarUrl: 'https://example.com/bot-avatar.png',
          canBeAssigned: true,
        },
      },
    },
  },
})
```

### Configuration Options

| Option             | Type    | Required | Description                                                                       |
| ------------------ | ------- | -------- | --------------------------------------------------------------------------------- |
| `displayName`      | string  | Yes      | Name shown in Desk UI                                                             |
| `botHandle`        | string  | Yes      | Handle for @mentions (3-20 chars, starts with letter, alphanumeric + underscores) |
| `displayAvatarUrl` | string  | No       | URL of avatar image                                                               |
| `canBeAssigned`    | boolean | No       | Whether bot can be assigned to tickets (default: `false`)                         |

### Handle Rules

The `botHandle` must:

- Be 3-20 characters
- Start with a letter
- Contain only letters, numbers, and underscores

Examples:

- `SupportBot`, `Triage_Bot`, `KB123`
- ❌ `Bot`, `123Bot`, `support-bot`

---

## Channel & Events

### Channel: desk.ticket

The Desk integration exposes a single channel: `desk.ticket`. All ticket interactions flow through this channel.

```typescript
export default new Conversation({
  channel: 'desk.ticket',
  // ...
})
```

### Event: desk:ticketActivity

Emitted when new activities (comments, notes, or system activities) are added to a ticket the bot is assigned to.

```typescript
export default new Conversation({
  channel: 'desk.ticket',
  events: ['desk:ticketActivity'],
  handler: async ({ event }) => {
    // event.payload contains:
    // - ticketId: string
    // - activityCount: number
  },
})
```

**Important:** The event does NOT include activities created by the bot itself (prevents infinite loops).

### Conversation Tags

| Tag                    | Description                 | Example                         |
| ---------------------- | --------------------------- | ------------------------------- |
| `desk:did`             | Desk ticket ID              | `tkt_abc123`                    |
| `desk:status`          | Ticket status               | `open`, `closed`, `snoozed`     |
| `desk:title`           | Ticket title                | `"Login issue"`                 |
| `desk:system`          | Source system               | `intercom`, `zendesk`, `native` |
| `desk:url`             | URL to view in Desk         | `https://desk.botpress.com/...` |
| `desk:snoozeduntil`    | Wake time if snoozed        | ISO timestamp                   |
| `desk:dtags`           | Desk tags (comma-separated) | `urgent,billing`                |
| `desk:dcustomerid`     | Customer ID                 | `cus_xyz789`                    |
| `desk:dassignedid`     | Assigned admin/bot ID       | `adm_123`, `ibot_456`           |
| `desk:dassignedself`   | **Is this bot assigned?**   | `"true"` or `"false"`           |
| `desk:dsyncactivityid` | Last synced activity ID     | `tka_abc123`                    |

### Message Tags

| Tag                | Description                |
| ------------------ | -------------------------- |
| `desk:did`         | Activity ID (`tka_...`)    |
| `desk:dassignedid` | Who was assigned when sent |
| `desk:dstatus`     | Ticket status when sent    |

---

## Message Types

The Desk channel supports three message types:

### 1. Reply (text) — Customer-Visible

Replies are visible to the customer and may be sent via email.

```typescript
await send({
  type: 'text',
  payload: {
    format: 'markdown',
    text: 'Hello! How can I help you today?',
  },
})
```

**Schema:**

```typescript
{
  format: "plain" | "html" | "markdown",
  text: string,
  attachments?: Array<{
    id: string,
    url: string,
    name: string,
    contentType: string,
    size: number,
    width?: number,
    height?: number,
  }>
}
```

### 2. Note — Internal Staff-Only

Notes are only visible to support staff (admins and bots), never to customers.

```typescript
await send({
  type: 'note',
  payload: {
    format: 'markdown',
    text: 'Internal note: Customer has billing issues in CRM',
  },
})
```

**Schema:**

```typescript
{
  format: "plain" | "html" | "markdown",
  text: string,
  mentions?: Array<{
    id: string,
    type: "admin" | "bot",
    name: string,
  }>
}
```

### 3. Activity — System Events

Activities represent system events like assignment changes, status changes, etc.

```typescript
await send({
  type: 'activity',
  payload: {
    type: 'ticket.activity',
    private: true,
    activity: {
      type: 'ticket.assigned',
      assignedTo: {
        type: 'bot',
        id: 'ibot_abc123',
        reply_as: 'SupportBot',
      },
    },
  },
})
```

**Activity Types:** `ticket.snoozed`, `ticket.unsnoozed`, `ticket.assigned`, `ticket.unassigned`, `ticket.closed`, `ticket.reopened`, `ticket.renamed`, `ticket.tags_updated`

---

## Conversation Handler Pattern

### Complete Handler Structure

```typescript
import { Autonomous, context, Conversation, z } from '@botpress/runtime'
import { actions, joinMarkdownChildren, TranscriptItem } from '@botpress/runtime/runtime'

export default new Conversation({
  channel: 'desk.ticket',
  state: z.object({
    customer: z.object({
      id: z.string(),
      name: z.string(),
      email: z.string().optional(),
    }),
    admins: z.array(z.object({ id: z.string(), name: z.string(), email: z.string().optional() })),
    ticket: z.object({
      id: z.string(),
      title: z.string(),
      status: z.string(),
      priority: z.string().optional(),
      assignedTo: z.string().optional(),
      createdAt: z.string(),
    }),
    lastSync: z.string().default(''),
  }),
  events: ['desk:ticketActivity'],
  handler: async ({ type, conversation, message, state, event, execute, client }) => {
    // ... handler logic
  },
})
```

### Assignment Check Pattern (CRITICAL)

**This is the most important pattern.** Without this check, your bot will process ALL tickets in the workspace.

```typescript
handler: async ({ conversation }) => {
  if (conversation.tags['desk:dassignedself'] !== 'true') {
    console.log('Ticket not assigned to bot, ignoring...')
    return
  }
  // Only process assigned tickets below this line
}
```

**Why?** The Desk integration fires events for ALL ticket activity. Without the assignment check:

- Your bot processes every ticket in the workspace
- Customers receive confusing or duplicate responses
- Unnecessary resource and API consumption

### Transcript Management

Sync messages to maintain conversation context:

```typescript
handler: async ({ conversation, state, client }) => {
  // Check assignment first...

  const chat = context.get('chat')
  const transcript = await chat.fetchTranscript()

  const messages = await client._inner.list
    .messages({
      conversationId: conversation.id,
      afterDate: state.lastSync,
    })
    .collect({})
    .then((messages) => messages.sort((a, b) => (a.createdAt < b.createdAt ? -1 : 1)))

  const newMessages = [
    ...transcript,
    ...messages.map(
      (m) =>
        ({
          id: m.id,
          content: JSON.stringify(m.payload),
          createdAt: m.createdAt,
          role: m.direction === 'incoming' ? 'user' : 'assistant',
          attachments: [],
          name: m.userId,
        }) satisfies TranscriptItem
    ),
  ]

  chat.setTranscript(newMessages)

  state.lastSync = newMessages.filter((x) => x.role === 'user' || x.role === 'assistant').slice(-1)[0]?.createdAt
}
```

> **Note:** Use `context.enterWith()` when reassigning context in async operations. Do not use `context.set("chat", ...)` for full context reassignment.

---

## Reply and Note Components

For AI-driven responses, register custom components that map to Desk message types.

### Reply Component

```typescript
const Reply = new Autonomous.Component({
  name: 'Reply',
  description: 'Sends a reply to the customer, visible to them and via email.',
  type: 'leaf',
  leaf: { props: z.object({}) },
  aliases: [],
  examples: [
    {
      name: 'Reply',
      description: 'Sends a reply to the customer',
      code: `
yield <Message><Reply>
  Some **markdown** reply to the customer!
</Reply></Message>`,
    },
  ],
})
```

### Note Component

```typescript
const Note = new Autonomous.Component({
  name: 'Note',
  description: 'Adds an internal note to the ticket. Not visible to the customer.',
  type: 'leaf',
  leaf: { props: z.object({}) },
  aliases: [],
  examples: [
    {
      name: 'Note',
      description: 'Adds an internal note to the ticket',
      code: `yield <Message><Note>This is a **note** with markdown!</Note></Message>`,
    },
  ],
})
```

### Component Registration

```typescript
handler: async ({ conversation }) => {
  // ... assignment check ...

  const chat = context.get('chat')

  // Remove default message components
  chat.removeComponent('MESSAGE')
  chat.removeComponent('Text')
  chat.removeComponent('TEXT')

  // Register Reply component
  chat.registerComponent({
    component: Reply as any,
    handler: async ({ props, children }) => {
      await conversation.send({
        type: 'text',
        payload: { format: 'markdown', text: joinMarkdownChildren(children) },
      })
    },
  })

  // Register Note component
  chat.registerComponent({
    component: Note as any,
    handler: async ({ props, children }) => {
      await conversation.send({
        type: 'note',
        payload: { format: 'markdown', text: joinMarkdownChildren(children) },
      })
    },
  })

  // Update chat context with new components
  const newChat = Object.assign(chat, {
    getComponents: async () => [Reply, Note],
  } satisfies Partial<typeof chat>)

  context.enterWith({ ...context.getAll(), chat: newChat })
}
```

---

## Available Actions

The Desk integration provides 11 actions for ticket management.

### Ticket Queries

```typescript
// listTickets - List tickets with pagination
const result = await actions.desk.listTickets({
  orderBy: 'updatedAt',
  orderDirection: 'desc',
  limit: 50,
  cursor: undefined,
})
// Returns: { tickets: Ticket[], hasMore: boolean, nextCursor?: string }

// getTicket - Get a single ticket by ID
const result = await actions.desk.getTicket({ id: 'tkt_abc123' })

// listTicketActivities - List activities for a ticket
const result = await actions.desk.listTicketActivities({
  ticketId: 'tkt_abc123',
  limit: 50,
  cursor: undefined,
})
```

### Assignment Actions

```typescript
// assignTicket - Assign to admin or bot
await actions.desk.assignTicket({
  ticketId: 'tkt_abc123',
  assigneeId: 'adm_xyz789', // or "ibot_..." for a bot
})

// unassignTicket - Remove assignment
await actions.desk.unassignTicket({ ticketId: 'tkt_abc123' })
```

### Lifecycle Actions

```typescript
// closeTicket
await actions.desk.closeTicket({ ticketId: 'tkt_abc123' })

// reopenTicket
await actions.desk.reopenTicket({ ticketId: 'tkt_abc123' })

// snoozeTicket
await actions.desk.snoozeTicket({
  ticketId: 'tkt_abc123',
  snoozedUntil: '2025-01-21T09:00:00Z',
})

// unsnoozeTicket
await actions.desk.unsnoozeTicket({ ticketId: 'tkt_abc123' })
```

### Metadata Actions

```typescript
// renameTicket
await actions.desk.renameTicket({
  ticketId: 'tkt_abc123',
  title: 'Updated: Login Issue with 2FA',
})

// addTags
await actions.desk.addTags({
  ticketId: 'tkt_abc123',
  tags: ['urgent', 'billing', 'enterprise'],
})

// removeTags
await actions.desk.removeTags({
  ticketId: 'tkt_abc123',
  tags: ['low-priority'],
})
```

---

## Converting Actions to Tools

Convert Desk actions to AI-callable tools using `asTool()` and `setStaticInputValues()`:

```typescript
handler: async ({ conversation, execute }) => {
  // Check assignment...

  const ticketId = conversation.tags['desk:did']

  // Create tools with bound ticketId
  const tools = [
    actions.desk.unassignTicket.asTool().setStaticInputValues({ ticketId }),
    actions.desk.closeTicket.asTool().setStaticInputValues({ ticketId }),
    actions.desk.snoozeTicket.asTool().setStaticInputValues({ ticketId }),
    actions.desk.addTags.asTool().setStaticInputValues({ ticketId }),
    actions.desk.removeTags.asTool().setStaticInputValues({ ticketId }),
  ]

  await execute({
    tools,
    instructions: 'You are a helpful support agent...',
  })
}
```

---

## AI Execution with Desk

### Execute with Instructions

```typescript
handler: async ({ conversation, execute }) => {
  if (conversation.tags['desk:dassignedself'] !== 'true') return

  const ticketId = conversation.tags['desk:did']

  const UnassignTool = actions.desk.unassignTicket.asTool().setStaticInputValues({ ticketId })

  await execute({
    iterations: 5,
    tools: [UnassignTool],
    model: 'anthropic:claude-sonnet-4-20250514',
    instructions: `You are a helpful assistant for customer support tickets.

You can choose to:
- Reply to the customer using <Reply>
- Add an internal note using <Note>
- Take no action

## Rules
- Always use <Reply> for customer-visible messages
- Always use <Note> for internal staff communication
- Be polite, concise, and don't make up information
- Ask for human help if unsure

## Current Ticket
${JSON.stringify(conversation.tags, null, 2)}
`,
  })
}
```

### System Prompt Guidelines

**DO:**

- Explain when to use Reply vs Note
- Set clear escalation criteria
- Include ticket context via tags
- Define what "taking no action" means

**DON'T:**

- Allow direct customer replies without components
- Let the bot make up information
- Process messages the bot sent itself
- Reply to every message (e.g., "thank you")

---

## Escalation Pattern

When a bot needs to hand off to a human agent, follow this 4-step pattern:

```typescript
async function escalateToHuman(conversation: any, reason: string): Promise<void> {
  // Step 1: Internal note explaining why
  await conversation.send({
    type: 'note',
    payload: {
      format: 'markdown',
      text: `Escalating to human: ${reason}`,
    },
  })

  // Step 2: Customer reply
  await conversation.send({
    type: 'text',
    payload: {
      format: 'markdown',
      text: "I've connected you with a member of our team who can help. They'll be with you shortly!",
    },
  })

  // Step 3: Unassign bot
  await actions.desk.unassignTicket({
    ticketId: conversation.tags['desk:did'],
  })
}

// In handler:
handler: async ({ conversation }) => {
  if (conversation.tags['desk:dassignedself'] !== 'true') return

  if (needsEscalation) {
    await escalateToHuman(conversation, 'Complex billing issue')
    return // Step 4: Stop processing
  }
  // ... continue normal processing
}
```

### When to Escalate

- Technical issues beyond basic troubleshooting
- Billing or account access issues
- Angry or frustrated customers
- Any uncertainty about the correct answer

---

## Data Schemas

### Ticket

```typescript
interface Ticket {
  id: string // "tkt_abc123"
  title: string
  customer: Customer
  priority: 'low' | 'medium' | 'high' | 'urgent'
  system: 'native' | 'intercom' | 'zendesk'
  systemTicketId: string
  assignedTo?: Admin | Bot
  status: 'open' | 'closed' | 'snoozed'
  createdAt: string
  updatedAt: string
  closedAt?: string
  snoozedUntil?: string
  tags: string[]
  metadata?: Record<string, any>
}
```

### Customer

```typescript
interface Customer {
  id: string // "cus_xyz789"
  name?: string
  email?: string
  phone?: string
  avatarUrl?: string
}
```

### Admin

```typescript
interface Admin {
  id: string // "adm_abc123"
  name: string
  email: string
  avatarUrl?: string
}
```

### Bot

```typescript
interface Bot {
  id: string // "ibot_def456"
  displayName: string
  displayAvatarUrl?: string
  botHandle: string
  canBeAssigned: boolean
}
```

### Activity

```typescript
interface Activity {
  id: string // "tka_abc123"
  ticketId: string
  activityType: 'comment' | 'note' | 'system_public' | 'system_internal'
  authorType: 'admin' | 'customer' | 'bot' | 'user'
  authorId: string
  body: string
  bodyFormat: 'plain' | 'html' | 'markdown' | 'json'
  isRedacted: boolean
  createdAt: string
  updatedAt: string
}
```

### Activity Event Types

```typescript
type TicketActivityType =
  | { type: 'ticket.snoozed'; author: Author }
  | { type: 'ticket.unsnoozed'; author: Author }
  | { type: 'ticket.assigned'; assignedTo: { type: 'admin' | 'bot'; id: string; reply_as?: string } }
  | { type: 'ticket.unassigned'; author: Author }
  | { type: 'ticket.closed'; author: Author }
  | { type: 'ticket.reopened'; author: Author }
  | { type: 'ticket.renamed'; title: string }
  | { type: 'ticket.tags_updated'; author: Author; added: string[]; removed: string[] }
```

---

## Common Mistakes

### Missing Assignment Check

```typescript
// ❌ WRONG - Processes ALL tickets
handler: async ({ conversation, execute }) => {
  await execute({ ... });
}

// ✅ CORRECT - Check assignment first
handler: async ({ conversation, execute }) => {
  if (conversation.tags["desk:dassignedself"] !== "true") return;
  await execute({ ... });
}
```

### Using Reply When Should Use Note

```typescript
// ❌ WRONG - Customer sees internal info
await send({ type: 'text', payload: { text: 'Customer has overdue invoices in CRM' } })

// ✅ CORRECT - Note for internal communication
await send({ type: 'note', payload: { text: 'Customer has overdue invoices in CRM' } })
```

### Not Extracting ticketId for Tools

```typescript
// ❌ WRONG - Tool has no ticketId
const UnassignTool = actions.desk.unassignTicket.asTool()

// ✅ CORRECT - Bind ticketId
const ticketId = conversation.tags['desk:did']
const UnassignTool = actions.desk.unassignTicket.asTool().setStaticInputValues({ ticketId })
```

### Using Wrong Tag Names

```typescript
// ❌ WRONG
conversation.tags['deskId']
conversation.tags['desk:assignedSelf'] // wrong case

// ✅ CORRECT
conversation.tags['desk:did']
conversation.tags['desk:dassignedself'] // lowercase
```

### Replying to Every Message

```typescript
// ❌ WRONG
instructions: 'Always reply to every message from the customer'

// ✅ CORRECT
instructions: `You DON'T have to reply to every message.
If the customer says "thanks" or "got it", take no action.
Only reply when you have something meaningful to add.`
```

---

## See Also

- [./conversations.md](./conversations.md) — General conversation handling
- [./integration-actions.md](./integration-actions.md) — Using integration actions
- [./actions.md](./actions.md) — Actions and Tools reference
- [./tags.md](./tags.md) — Tags reference
- [./patterns-mistakes.md](./patterns-mistakes.md) — General best practices
- [./agent-config.md](./agent-config.md) — Configuration reference
