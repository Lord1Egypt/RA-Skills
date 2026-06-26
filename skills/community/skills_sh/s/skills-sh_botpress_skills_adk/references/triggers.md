# Triggers

Triggers allow your bot to react to events from the bot itself or integrated services. They enable event-driven automation and workflow orchestration.

> **⚠️ IMPORTANT:** Always verify integration events exist before using them! Use `adk integrations info <integration> --format json` and inspect the returned event spec. Integration events change between versions.
>
> **⚠️ Dev-mode limitation:** `adk dev` is not a perfect mirror of production for every integration event flow. Some private or custom integration events may not register or route locally even when the event name is valid. If an event-driven flow works in docs but not in local dev, verify the event first, then test against a deployed bot before assuming your trigger code is wrong.
>
> **⚠️ To _receive_ a pushed event, subscribe to `chat:custom` — not a custom name.** An event pushed into a chat conversation (e.g. an order shipped, a status update relayed in) arrives as `chat:custom`. Subscribe the `Conversation` to `events: ['chat:custom']` and branch on `type === 'event'`; a handler on a made-up name like `orderShipped` never fires. See [Conversations → Custom & Proactive Events](./conversations.md#custom--proactive-events). The camelCase rule below applies only to events you _define/emit_, not to receiving.
>
> **⚠️ Events you define must be camelCase** — `orderShipped`, not `order_shipped`; `adk build` rejects snake_case names.

## Basic Concepts

### What are Triggers?

- **Event handlers**: React to bot or integration events
- **Automated**: Execute automatically when events occur
- **Flexible**: Can start workflows, update tables, or perform any action

### File Location

- **Location**: `src/triggers/*.ts`
- **Auto-registration**: Files automatically subscribe to specified events

## Creating Triggers

### Basic Structure

```typescript
import { Trigger } from '@botpress/runtime'

export default new Trigger({
  name: 'myTrigger',
  description: 'Handles user creation events',
  events: ['user.created'], // Events to subscribe to

  handler: async ({ event }) => {
    console.log(event.type) // "user.created"
    console.log(event.payload) // Event data

    // React to the event
    await handleUserCreated(event.payload)
  },
})
```

### Multiple Events

Subscribe to multiple events in one trigger:

```typescript
export default new Trigger({
  name: 'userEvents',
  description: 'Handles all user-related events',
  events: ['user.created', 'user.updated', 'user.deleted'],

  handler: async ({ event }) => {
    switch (event.type) {
      case 'user.created':
        await handleUserCreated(event.payload)
        break
      case 'user.updated':
        await handleUserUpdated(event.payload)
        break
      case 'user.deleted':
        await handleUserDeleted(event.payload)
        break
    }
  },
})
```

## Event Types

### Bot Events

Standard events emitted by the bot:

```typescript
// User events
'user.created' // New user created
'user.updated' // User information updated
'user.deleted' // User deleted

// Conversation events
'conversation.started' // New conversation started
'conversation.ended' // Conversation ended
'message.created' // New message in conversation

// Workflow events
'workflow.started' // Workflow instance started
'workflow.completed' // Workflow completed successfully
'workflow.failed' // Workflow failed

// Bot lifecycle events
'bot.started' // Bot started
'bot.stopped' // Bot stopped
```

### Integration Events

Events from integrated services use the pattern `integrationName:eventName`.

**IMPORTANT:** Always verify events exist using `adk integrations info <integration> --format json` before using them.

```typescript
// Intercom events (real events from vertical-one)
'intercom:conversationEvent' // Fires on create/update/delete
'intercom:contactEvent' // Contact created/updated
'intercom:adminEvent' // Admin changes

// Slack events (verified with adk integrations info slack --format json)
'slack:reactionAdded'
'slack:reactionRemoved'
'slack:memberJoinedChannel'
'slack:memberJoinedWorkspace'
'slack:memberLeftChannel'
'slack:workflowWebhook'

// Linear events (verified with adk integrations info linear --format json)
'linear:issueCreated'
'linear:issueUpdated'
'linear:issueDeleted'

// GitHub events (verified with adk integrations info github --format json)
'github:issueOpened'
'github:pullRequestOpened'
'github:pullRequestMerged'
'github:pullRequestReviewSubmitted'

// Webchat events (verified with adk integrations info webchat --format json)
'webchat:conversationStarted'
'webchat:trigger'
```

**How to discover events:**

```bash
# Search for an integration
adk integrations search email

# Get all events for an integration
adk integrations info slack --format json
adk integrations info linear --format json
adk integrations info github --format json
```

Checking `adk integrations info <integration> --format json` confirms the event exists, but it does not guarantee that every event source behaves the same in `adk dev` as it does after deployment.

## Trigger Handlers

### Starting Workflows

Common pattern: Start a workflow when an event occurs:

```typescript
import { Trigger } from '@botpress/runtime'
import { OnboardingWorkflow } from '../workflows/onboarding'

export default new Trigger({
  name: 'userOnboarding',
  description: 'Start onboarding when user is created',
  events: ['user.created'],

  handler: async ({ event }) => {
    const { userId, email, name } = event.payload

    // Start onboarding workflow
    const instance = await OnboardingWorkflow.start({
      userId,
      email,
      name,
      createdAt: new Date(),
    })

    console.log(`Started onboarding for ${userId}: ${instance.id}`)
  },
})
```

### Updating Tables

Store event data in tables:

```typescript
import { Trigger } from '@botpress/runtime'
import { EventLogTable } from '../tables/EventLog'

export default new Trigger({
  name: 'eventLogger',
  description: 'Log all events to database',
  events: ['user.created', 'user.updated', 'conversation.started', 'workflow.completed'],

  handler: async ({ event }) => {
    // Store event in table
    await EventLogTable.createRows({
      rows: [
        {
          type: event.type,
          payload: event.payload,
          timestamp: new Date(),
          metadata: {
            source: event.source || 'bot',
            version: event.version || '1.0',
          },
        },
      ],
    })
  },
})
```

### Calling Actions

Execute bot actions or integration actions in response to events:

```typescript
import { Trigger } from '@botpress/runtime'
import { actions } from '@botpress/runtime'

export default new Trigger({
  name: 'notificationSender',
  description: 'Send email notifications for important events',
  events: ['workflow.failed', 'user.deleted'],

  handler: async ({ event }) => {
    // Call integration action (e.g., SendGrid)
    // First add the integration: adk integrations add sendgrid@<version>
    await actions.sendgrid.sendEmail({
      to: 'admin@example.com',
      from: 'bot@example.com',
      subject: `Alert: ${event.type}`,
      content: `Event occurred: ${JSON.stringify(event.payload)}`,
    })
  },
})
```

**Note:** The `actions` object provides access to:

- **Bot actions**: `actions.myAction()` - your custom actions from `src/actions/`
- **Integration actions**: `actions.integrationName.actionName()` - actions from installed integrations

## Integration Event Examples

### Intercom Integration

Real-world example from vertical-one bot:

```typescript
import { Trigger } from '@botpress/runtime'
import { syncSingleConversation, deleteConversation } from '../utils/syncConversation'

export default new Trigger({
  name: 'onIntercomUpdate',
  description: 'Updates the Intercom tables in realtime when conversations are created or messages are sent',
  events: ['intercom:conversationEvent'],

  handler: async ({ event }) => {
    const { eventType, conversationId } = event.payload

    console.log(`Intercom event: ${eventType} for conversation ${conversationId}`)

    try {
      if (eventType === 'deleted') {
        // Delete the conversation and its messages
        await deleteConversation(conversationId)
      } else {
        // Sync the conversation with all its data
        await syncSingleConversation(conversationId)
      }
    } catch (error) {
      console.error(`Failed to handle ${eventType} event for conversation ${conversationId}:`, error)
      throw error
    }
  },
})
```

### Linear Integration

Real example from ADK source code:

```typescript
import { Trigger } from '@botpress/runtime'
import { LinearIssueTable } from '../tables/LinearIssues'

export default new Trigger({
  name: 'onLinearIssueUpdate',
  description: 'Updates the Linear Issue Table when issues change',
  events: ['linear:issueCreated', 'linear:issueUpdated', 'linear:issueDeleted'],

  handler: async ({ event }) => {
    if (event.type === 'linear:issueDeleted') {
      await LinearIssueTable.deleteRows({
        linearId: event.payload.id,
      })
    } else if (event.type === 'linear:issueCreated') {
      await LinearIssueTable.createRows({
        rows: [
          {
            linearId: event.payload.linearIds?.issueId,
            content: `# ${event.payload.title}\n\n${event.payload.description}`,
            issue: event.payload,
            linearUpdatedAt: event.payload.updatedAt,
          },
        ],
      })
    } else if (event.type === 'linear:issueUpdated') {
      await LinearIssueTable.upsertRows({
        rows: [
          {
            linearId: event.payload.linearIds?.issueId,
            content: `# ${event.payload.title}\n\n${event.payload.description}`,
            issue: event.payload,
            linearUpdatedAt: event.payload.updatedAt,
          },
        ],
        keyColumn: 'linearId',
      })
    }
  },
})
```

### Slack Integration

```typescript
import { Trigger } from '@botpress/runtime'
import { SlackActivityTable } from '../tables/SlackActivity'

export default new Trigger({
  name: 'slackActivityMonitor',
  description: 'Monitor Slack reactions and member activity',
  events: ['slack:reactionAdded', 'slack:memberJoinedChannel'],

  handler: async ({ event }) => {
    if (event.type === 'slack:reactionAdded') {
      const { reaction, user, item } = event.payload

      // Log important reactions to table
      if (reaction === 'fire' || reaction === 'star' || reaction === 'eyes') {
        await SlackActivityTable.createRows({
          rows: [
            {
              type: 'reaction',
              reaction: reaction,
              user: user,
              messageId: item.ts,
              channelId: item.channel,
              timestamp: new Date(),
            },
          ],
        })
      }
    }

    if (event.type === 'slack:memberJoinedChannel') {
      const { user, channel } = event.payload

      // Log new member joins
      await SlackActivityTable.createRows({
        rows: [
          {
            type: 'member_join',
            user: user,
            channelId: channel,
            timestamp: new Date(),
          },
        ],
      })
    }
  },
})
```

## Advanced Patterns

### Conditional Processing

Process events based on conditions:

```typescript
export default new Trigger({
  name: 'conditionalProcessor',
  events: ['user.created'],

  handler: async ({ event }) => {
    const { email, source, metadata } = event.payload

    // Only process certain users
    if (!email.endsWith('@company.com')) {
      console.log('Skipping external user')
      return
    }

    // Different handling based on source
    if (source === 'api') {
      await handleApiUser(event.payload)
    } else if (source === 'signup') {
      await handleSignupUser(event.payload)
    }

    // Check metadata flags
    if (metadata?.requiresApproval) {
      await startApprovalWorkflow(event.payload)
    }
  },
})
```

### Event Aggregation

Collect and batch process events:

```typescript
import { Trigger } from '@botpress/runtime'
import { EventBatchTable } from '../tables/EventBatch'

export default new Trigger({
  name: 'eventAggregator',
  events: ['metrics.recorded'],

  handler: async ({ event }) => {
    // Store event for batching
    await EventBatchTable.createRows({
      rows: [
        {
          type: event.type,
          data: event.payload,
          processed: false,
          timestamp: new Date(),
        },
      ],
    })

    // Check if we should process batch
    const { rows } = await EventBatchTable.findRows({
      where: { processed: false },
      limit: 100,
    })

    if (rows.length >= 100) {
      // Process batch
      await processBatch(rows)

      // Mark as processed
      const ids = rows.map((r) => r.id)
      await EventBatchTable.updateRows({
        where: { id: { $in: ids } },
        updates: { processed: true },
      })
    }
  },
})
```

### Workflow Orchestration

Chain workflows based on events:

```typescript
export default new Trigger({
  name: 'workflowOrchestrator',
  events: ['workflow.completed'],

  handler: async ({ event }) => {
    const { workflowName, output } = event.payload

    // Chain workflows based on completion
    switch (workflowName) {
      case 'dataCollection':
        // Start processing workflow
        await ProcessingWorkflow.start({
          data: output.collectedData,
        })
        break

      case 'processing':
        // Start validation workflow
        await ValidationWorkflow.start({
          processedData: output.result,
        })
        break

      case 'validation':
        // Start final reporting workflow
        if (output.isValid) {
          await ReportingWorkflow.start({
            data: output.validatedData,
          })
        }
        break
    }
  },
})
```

### Error Recovery

Handle failed events:

```typescript
export default new Trigger({
  name: 'errorRecovery',
  events: ['workflow.failed', 'integration:error'],

  handler: async ({ event }) => {
    const { error, context, retryCount = 0 } = event.payload

    // Log error
    await ErrorLogTable.createRows({
      rows: [
        {
          type: event.type,
          error: error.message,
          stack: error.stack,
          context,
          timestamp: new Date(),
        },
      ],
    })

    // Attempt recovery
    if (retryCount < 3) {
      // Retry with backoff
      setTimeout(
        async () => {
          await RetryWorkflow.start({
            originalEvent: event,
            retryCount: retryCount + 1,
          })
        },
        Math.pow(2, retryCount) * 1000
      )
    } else {
      // Send alert after max retries
      await actions.sendAlert({
        severity: 'critical',
        title: 'Max retries exceeded',
        details: { event, error },
      })
    }
  },
})
```

## Best Practices

### 1. Use Descriptive Names

```typescript
// ✅ Good
export default new Trigger({
  name: 'linearIssueSync',
  description: 'Syncs Linear issues to internal tracking',
})

// ❌ Bad
export default new Trigger({
  name: 'trigger1',
  description: 'Does stuff',
})
```

### 2. Handle Errors Gracefully

```typescript
handler: async ({ event }) => {
  try {
    await processEvent(event)
  } catch (error) {
    console.error(`Failed to process ${event.type}:`, error)

    // Store error for debugging
    await ErrorTable.createRows({
      rows: [
        {
          trigger: 'myTrigger',
          event: event.type,
          error: error.message,
          timestamp: new Date(),
        },
      ],
    })

    // Don't re-throw unless you want to retry
  }
}
```

### 3. Avoid Heavy Processing

```typescript
handler: async ({ event }) => {
  // ✅ Good: Start async workflow
  await HeavyProcessingWorkflow.start({
    eventData: event.payload,
  })

  // ❌ Bad: Long-running synchronous processing
  // const result = await performHeavyComputation(event.payload);
}
```

### 4. Use Event Patterns

```typescript
// Group related events from multiple integrations
export default new Trigger({
  name: 'issueTracker',
  events: ['linear:issueCreated', 'linear:issueUpdated', 'github:issueOpened', 'github:pullRequestOpened'],

  handler: async ({ event }) => {
    const [integration, action] = event.type.split(':')

    // Common processing for all issue-related events
    await IssueTrackingTable.createRows({
      rows: [
        {
          source: integration,
          eventType: action,
          data: event.payload,
          timestamp: new Date(),
        },
      ],
    })
  },
})
```

### 5. Document Event Payloads

```typescript
/**
 * Handles user creation events
 *
 * Expected payload:
 * {
 *   userId: string
 *   email: string
 *   name: string
 *   source: "signup" | "api" | "admin"
 *   metadata?: Record<string, any>
 * }
 */
export default new Trigger({
  name: 'userCreatedHandler',
  events: ['user.created'],

  handler: async ({ event }) => {
    const { userId, email, name, source } = event.payload
    // Process with confidence in payload structure
  },
})
```

## Common Patterns

### Audit Trail

```typescript
export default new Trigger({
  name: 'auditTrail',
  events: ['user.created', 'user.updated', 'user.deleted', 'conversation.started'],

  handler: async ({ event }) => {
    await AuditTable.createRows({
      rows: [
        {
          eventType: event.type,
          payload: event.payload,
          userId: event.payload.userId || event.userId,
          timestamp: new Date(),
        },
      ],
    })
  },
})
```

### Notification System

```typescript
export default new Trigger({
  name: 'notifications',
  events: ['workflow.failed', 'user.deleted', 'integration:error'],

  handler: async ({ event }) => {
    const notifications = {
      'workflow.failed': {
        channel: 'slack',
        priority: 'high',
        template: 'workflow-failure',
      },
      'user.deleted': {
        channel: 'email',
        priority: 'normal',
        template: 'user-deleted',
      },
      'integration:error': {
        channel: 'pagerduty',
        priority: 'critical',
        template: 'integration-error',
      },
    }

    const config = notifications[event.type]
    if (config) {
      await actions.sendNotification({
        ...config,
        data: event.payload,
      })
    }
  },
})
```
