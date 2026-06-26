# Conversation Lifecycle (Nudge / Expiration)

The lifecycle system lets conversations re-engage idle users (nudge) and clean up stale sessions (expiration). It is an opt-in feature configured per conversation via the `lifecycle` property.

For basic conversation setup, channel routing, and handler parameters, see **[conversations.md](./conversations.md)**.

## Enabling Lifecycle

Add a `lifecycle` object to any Conversation definition. Durations use `ms`-compatible strings (`"30s"`, `"5m"`, `"1h"`, `"1d"`).

```typescript
import { Conversation, z } from '@botpress/runtime'

export const Chat = new Conversation({
  channel: 'webchat.channel',

  lifecycle: {
    nudge: {
      after: '5m', // First nudge fires 5 min after last user message
      interval: '10m', // Subsequent nudges fire every 10 min
      max: 3, // Stop after 3 nudges (omit for unlimited)
    },
    expire: {
      after: '1h', // Session expires 1 hour after last user message
    },
  },

  state: z.object({
    topic: z.string().optional(),
  }),

  handler: async (props) => {
    // handler receives nudge and expire events alongside regular messages
  },
})
```

### Configuration Fields

| Field            | Type     | Required        | Description                                                            |
| ---------------- | -------- | --------------- | ---------------------------------------------------------------------- |
| `nudge.after`    | `string` | Yes (if nudge)  | Duration of silence before the first nudge fires                       |
| `nudge.interval` | `string` | No              | Duration between subsequent nudges. Defaults to `nudge.after`          |
| `nudge.max`      | `number` | No              | Max nudges per session. Must be a positive integer. Omit for unlimited |
| `expire.after`   | `string` | Yes (if expire) | Duration of silence before the session expires                         |

Nudge and expire are independent -- you can configure either or both.

## Handler Types

When lifecycle is enabled, the conversation handler receives two additional event types: `"nudge"` and `"expire"`. Discriminate using the `type` parameter.

```typescript
handler: async ({ type, conversation, state, execute }) => {
  if (type === 'nudge') {
    // User has been silent -- send a re-engagement message
    await conversation.send({
      type: 'text',
      payload: { text: 'Still there? Let me know if you need anything.' },
    })
    return
  }

  if (type === 'expire') {
    // Session is about to be torn down -- send a farewell
    await conversation.send({
      type: 'text',
      payload: { text: 'This session has expired. Send a new message to start fresh.' },
    })
    // After the handler returns, the runtime automatically:
    //   1. Cancels all active workflows on the conversation
    //   2. Tags the conversation with sessionExpired = "true"
    //   3. Resets conversation state to defaults
    //   4. Clears the transcript
    //   5. Sets lifecycle status to "expired"
    return
  }

  if (type === 'message') {
    // Normal message handling
    await execute({
      instructions: 'You are a helpful assistant',
    })
  }
}
```

### Handler Props by Type

When `type === "nudge"`:

- `event` is typed as `LifecycleNudgeEventType` with payload `{ conversationId, sessionId, scheduledAt }`
- `message` is `undefined`

When `type === "expire"`:

- `event` is typed as `LifecycleExpireEventType` with payload `{ conversationId, sessionId, scheduledAt }`
- `message` is `undefined`

All other handler props (`conversation`, `state`, `execute`, `client`, `chat`) are available as normal. The `chat` prop provides access to transcript and message operations within the conversation (e.g., `chat.fetchTranscript()`, `chat.clearTranscript()`, `chat.saveTranscript()`).

## Session Object

Lifecycle-enabled conversations expose a read-only `conversation.session` property:

```typescript
handler: async ({ type, conversation }) => {
  const session = conversation.session
  if (!session) return // undefined when lifecycle is not configured

  console.log(session.id) // ULID identifying the current session
  console.log(session.number) // Monotonically increasing (1, 2, 3...)
  console.log(session.status) // "active" or "expired"
  console.log(session.startedAt) // ISO timestamp
  console.log(session.lastActivityAt) // ISO timestamp of last user message
  console.log(session.nudgeCount) // Number of nudges fired this session
}
```

### Session Fields

| Field            | Type                    | Description                                                  |
| ---------------- | ----------------------- | ------------------------------------------------------------ |
| `id`             | `string`                | ULID unique to the current session                           |
| `number`         | `number`                | Session counter, increments on each expiration (starts at 1) |
| `status`         | `"active" \| "expired"` | Current session status                                       |
| `startedAt`      | `string`                | ISO timestamp when this session began                        |
| `lastActivityAt` | `string`                | ISO timestamp of the last user message                       |
| `nudgeCount`     | `number`                | Number of nudges delivered in this session                   |

## How Timers Work

Understanding the timer lifecycle is important for building correct nudge/expire logic.

### On Every User Message

1. `lastActivityAt` is updated to now
2. `nudgeCount` resets to 0
3. Any pending nudge and expire scheduled events are cancelled
4. New nudge and expire events are scheduled based on the configured delays

This means every user message resets the clock. Timers always measure silence from the most recent message.

### On Nudge Event

1. **Race guard**: If `lastActivityAt > scheduledAt`, the nudge is silently dropped (a message arrived after the nudge was scheduled)
2. **Workflow suppression**: If any active workflows exist on the conversation (`pending`, `in_progress`, `listening`, `paused`), the nudge is silently rescheduled at `intervalMs` and skipped
3. `nudgeCount` increments
4. The user's handler runs
5. If `nudgeCount < max` (or no max), the next nudge is scheduled at `intervalMs`

### On Expire Event

1. **Race guard**: If `lastActivityAt > scheduledAt`, the expire is silently dropped
2. The user's handler runs (errors are caught -- expiration cleanup always proceeds)
3. **Hard-kill expiration sequence** (strict ordering):
   - Cancel all active workflows on the conversation
   - Tag conversation with `sessionExpired = "true"`
   - Reset conversation state to defaults (empty object)
   - Clear the transcript
   - Set lifecycle status to `"expired"`

### Session Renewal

When a message arrives on an expired session:

1. A new `sessionId` (ULID) is generated
2. `sessionNumber` increments
3. `nudgeCount` resets to 0
4. `status` becomes `"active"`
5. `startedAt` and `lastActivityAt` update to now
6. The `sessionExpired` conversation tag is cleared
7. New timers are scheduled

## Built-in Tags

Lifecycle automatically manages these tags without any user configuration:

### Conversation Tags

| Tag              | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `sessionExpired` | Set to `"true"` when a session expires. Cleared on renewal |

### Message Tags

| Tag             | Description                                              |
| --------------- | -------------------------------------------------------- |
| `sessionId`     | ULID of the session this message belongs to              |
| `sessionNumber` | Session sequence number at the time the message was sent |

Message tags are applied automatically to both incoming user messages and outgoing bot messages. They enable grouping messages by session.

## Internal State Namespace

Lifecycle state is managed by the runtime in a separate internal state namespace, not in the user-facing conversation state. This means:

- Lifecycle state survives conversation state resets (which happen on expiration)
- You cannot accidentally overwrite lifecycle fields by mutating `state`
- The `conversation.session` property is the intended read-only interface for accessing lifecycle data -- use it instead of attempting to access internal state directly

## Common Patterns

### Escalating Nudge Messages

Use `conversation.session.nudgeCount` to vary the message urgency:

```typescript
handler: async ({ type, conversation }) => {
  if (type === 'nudge') {
    const count = conversation.session?.nudgeCount ?? 0

    if (count === 1) {
      await conversation.send({
        type: 'text',
        payload: { text: 'Just checking in -- do you still need help?' },
      })
    } else if (count === 2) {
      await conversation.send({
        type: 'text',
        payload: { text: "I'm still here if you need me." },
      })
    } else {
      await conversation.send({
        type: 'text',
        payload: { text: "This conversation will expire soon if there's no activity." },
      })
    }
    return
  }
  // ... handle messages
}
```

### Expire with Summary

Send a session summary before the session is torn down:

```typescript
handler: async ({ type, conversation, state, execute }) => {
  if (type === 'expire') {
    if (state.topic) {
      await conversation.send({
        type: 'text',
        payload: {
          text: `Session expired. You were working on: ${state.topic}. Send a message to start a new session.`,
        },
      })
    }
    // State will be reset after this handler returns
    return
  }
  // ... handle messages
}
```

### Nudge-Only (No Expiration)

You can configure nudges without expiration:

```typescript
lifecycle: {
  nudge: {
    after: "3m",
    max: 2,
  },
  // no expire -- sessions stay active indefinitely
},
```

### Expire-Only (No Nudges)

You can configure expiration without nudges:

```typescript
lifecycle: {
  // no nudge -- no re-engagement messages
  expire: {
    after: "30m",
  },
},
```

## Pitfalls

### Nudges Do Not Fire During Active Workflows

If a workflow is running on the conversation (status `pending`, `in_progress`, `listening`, or `paused`), nudges are silently suppressed and rescheduled. This prevents the bot from sending "Are you still there?" while a workflow is actively processing. The check is fail-closed: if the workflow status query fails, the nudge is suppressed. See [workflow-steps.md](./workflow-steps.md) for the step methods that put workflows into these statuses.

### Expire Handler Errors Do Not Block Cleanup

If the expire handler throws, the error is caught and the expiration sequence still runs (workflow cancellation, state reset, transcript clear). The error is re-thrown after cleanup completes. Do not rely on throwing in the expire handler to prevent expiration.

### State Is Reset on Expiration

After expiration, conversation state is reset to defaults (the empty object triggers schema defaults on the next load). Any data you need to survive across sessions must be stored elsewhere (user state, bot state, or tables).

### Typing Indicators Are Suppressed for Lifecycle Events

The runtime does not show typing indicators for nudge or expire events. This is intentional -- lifecycle events should feel automatic, not like the bot is "thinking."

### Timer Scheduling Failures Are Non-Fatal

If the runtime fails to schedule a nudge or expire event (e.g., API error), it logs a warning but does not crash the handler. The next user message will attempt to schedule new timers.

### Race Guards Prevent Stale Events

Both nudge and expire events carry a `scheduledAt` timestamp. If a user message arrived after the event was scheduled (i.e., `lastActivityAt > scheduledAt`), the event is silently dropped. This prevents stale timers from firing after the user has already re-engaged.

## See Also

- [Conversations](./conversations.md) — Conversation setup, channel routing, and handler parameters
- [Workflows](./workflows.md) — Workflow basics and how workflows interact with conversations
- [Workflow Steps](./workflow-steps.md) — Step methods whose statuses affect nudge suppression
