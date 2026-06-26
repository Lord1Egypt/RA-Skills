# Integration Actions

Call actions from installed integrations using a simple, type-safe API.

## Quick Start

```typescript
import { actions } from '@botpress/runtime'

// Call integration action
const { items } = await actions.linear.issueList({
  first: 10,
  filter: { state: { name: { eq: 'In Progress' } } },
})
```

## Overview

Integration actions allow you to call functionality from installed integrations (Slack, Linear, GitHub, etc.) using a unified, type-safe API. Each integration exposes actions that map to its capabilities.

**Pattern:**

```typescript
await actions.{integration}.{actionName}(params);
```

**Available in:**

- Actions
- Tools
- Workflows
- Conversations
- Triggers

## Installation

Before using integration actions, add the integration to your project:

```bash
# Add integration
adk integrations add slack@2.5.5

# Or with custom alias
adk integrations add linear@2.0.0 --alias my-linear

# Start dev to configure
adk dev
```

Then configure the integration in the Dev Console at `localhost:3001` or via `adk integrations configure`.

## Basic Usage

### Importing Actions

```typescript
import { actions } from '@botpress/runtime'
```

### Calling Actions

```typescript
// Slack - Send message
await actions.slack.sendMessage({
  channel: '#general',
  text: 'Hello from bot!',
})

// Linear - List issues
const { items } = await actions.linear.issueList({
  first: 10,
  filter: { state: { name: { eq: 'In Progress' } } },
})

// GitHub - Create issue
await actions.github.createIssue({
  owner: 'myorg',
  repo: 'myrepo',
  title: 'Bug report',
  body: 'Issue description',
})
```

### Alternative: Bracket Notation

Use bracket notation when integration names contain special characters or when accessing them dynamically:

```typescript
// Useful for dynamic integration names
const integrationName = 'intercom'
await actions[integrationName].getConversation({
  intercomConversationId: 'conv_123',
})

// Or when the integration name has special characters
await actions['my-integration'].someAction({
  param: 'value',
})
```

### Type Safety

All integration actions are fully typed with TypeScript:

```typescript
type LinearIssue = Awaited<ReturnType<typeof actions.linear.getIssue>>

// TypeScript knows the exact shape of the result
const issue = await actions.linear.getIssue({ id: 'ISS-123' })
// issue.title, issue.description, issue.state, etc. are all typed
```

## Converting to AI Tools

Integration actions can be converted to AI-callable tools using `.asTool()`:

```typescript
await execute({
  instructions: 'Help the user browse the web',
  tools: [
    // Convert integration action to tool
    actions.browser.captureScreenshot.asTool(),

    // Mix with custom tools
    customSearchTool,
  ],
})
```

**How it works:**

- The action's input/output schemas become the tool's parameters
- The action's description (if any) helps the AI understand when to use it
- The AI can call the tool during autonomous execution

## Common Integration Actions

### Slack Integration

```typescript
// Send message
await actions.slack.sendMessage({
  channel: '#general',
  text: 'Hello!',
  blocks: [
    {
      type: 'section',
      text: { type: 'mrkdwn', text: '*Hello* from bot!' },
    },
  ],
})

// Add reaction
await actions.slack.addReaction({
  channel: 'C123456',
  timestamp: '1234567890.123456',
  name: 'thumbsup',
})

// Upload file
await actions.slack.uploadFile({
  channels: ['#general'],
  file: fileBuffer,
  filename: 'report.pdf',
  title: 'Monthly Report',
})
```

### Linear Integration

```typescript
// List issues with filters
const { items, meta } = await actions.linear.issueList({
  first: 50,
  filter: {
    state: { name: { eq: 'In Progress' } },
    assignee: { email: { eq: 'user@example.com' } },
  },
  orderBy: { createdAt: 'desc' },
})

// Get specific issue
const issue = await actions.linear.getIssue({
  id: 'ISS-123',
})

// Create issue
await actions.linear.issueCreate({
  teamId: 'team_123',
  title: 'New feature request',
  description: 'Detailed description',
  priority: 1,
  assigneeId: 'user_456',
})

// Update issue
await actions.linear.issueUpdate({
  id: 'ISS-123',
  stateId: 'state_done',
})
```

### Browser Integration

```typescript
// Browse pages (web scraping)
const { results } = await actions.browser.browsePages({
  urls: ['https://docs.example.com'],
  extractType: 'markdown',
  maxPages: 10,
})

// Web search
const output = await actions.browser.webSearch({
  query: 'Botpress ADK documentation',
  maxResults: 5,
})

// Capture screenshot
const screenshot = await actions.browser.captureScreenshot({
  url: 'https://example.com',
  fullPage: true,
  format: 'png',
})
```

### GitHub Integration

```typescript
// Create issue
await actions.github.createIssue({
  owner: 'myorg',
  repo: 'myrepo',
  title: 'Bug: Login not working',
  body: 'Steps to reproduce:\n1. ...',
  labels: ['bug', 'priority-high'],
})

// Get repository
const repo = await actions.github.getRepository({
  owner: 'myorg',
  repo: 'myrepo',
})

// Create pull request
await actions.github.createPullRequest({
  owner: 'myorg',
  repo: 'myrepo',
  title: 'Fix login issue',
  head: 'feature-branch',
  base: 'main',
  body: 'This PR fixes the login issue',
})
```

### Discord Integration

```typescript
// Send message
await actions.discord.sendMessage({
  channelId: '123456789',
  content: 'Hello from bot!',
  embeds: [
    {
      title: 'Notification',
      description: 'Your task is complete',
      color: 0x00ff00,
    },
  ],
})

// Add reaction
await actions.discord.addReaction({
  channelId: '123456789',
  messageId: '987654321',
  emoji: '✅',
})
```

### WhatsApp Integration

```typescript
// Send text message
await actions.whatsapp.sendMessage({
  to: '+1234567890',
  type: 'text',
  text: { body: 'Hello from bot!' },
})

// Send template message
await actions.whatsapp.sendTemplate({
  to: '+1234567890',
  template: {
    name: 'order_confirmation',
    language: { code: 'en' },
    components: [
      {
        type: 'body',
        parameters: [{ type: 'text', text: '12345' }],
      },
    ],
  },
})
```

### Intercom Integration

```typescript
// Send admin message with attachments
await actions.intercom.sendAdminMessage({
  adminId: 'admin_123',
  intercomConversationId: 'conv_456',
  messageType: 'comment',
  body: 'Thank you for contacting us!',
  attachment_urls: ['https://example.com/image.png'],
})

// Close/open conversation
await actions.intercom.closeConversation({
  intercomConversationId: 'conv_456',
  adminId: 'admin_123',
})

// Manage tags
await actions.intercom.updateConversationTags({
  intercomConversationId: 'conv_456',
  adminId: 'admin_123',
  tagsToAdd: ['priority'],
  tagsToRemove: ['pending'],
})
```

## Advanced: Building Custom Integration Actions

> **Note**: This section is for integration developers building custom integrations. If you're building a bot and using existing integrations (Slack, Linear, etc.), you can skip this section.

When building a custom integration, you define actions that bot developers can call via `actions.{yourIntegration}.{actionName}()`.

### Integration Action Structure

Here's how integration actions are implemented (example from Intercom integration):

```typescript
// In integrations/intercom/src/actions/send-admin-message.ts
import { RuntimeError } from '@botpress/client'
import * as bp from '../../.botpress'

export const sendAdminMessage: bp.IntegrationProps['actions']['sendAdminMessage'] = async ({ input }) => {
  const url = new URL(`https://api.intercom.io/conversations/${input.intercomConversationId}/reply`)

  const requestBody: Record<string, unknown> = {
    message_type: input.messageType ?? 'comment',
    type: 'admin',
    body: input.body,
    admin_id: input.adminId,
  }

  // Add optional parameters
  if (input.attachment_urls && input.attachment_urls.length > 0) {
    requestBody.attachment_urls = input.attachment_urls
  }

  // Call external API
  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${bp.secrets.TOKEN}`,
      'Intercom-Version': '2.14',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  })

  // Error handling
  if (!response.ok) {
    const errorText = await response.text()
    throw new RuntimeError(`Failed to send admin message: ${response.status} - ${errorText}`)
  }

  return await response.json()
}
```

### Integration Action Definition

Actions are defined in the integration's definition file:

```typescript
// In integrations/intercom/integration.definition.ts
import { Integration, z } from '@botpress/sdk'

export default new Integration({
  actions: {
    sendAdminMessage: {
      title: 'Send Admin Message',
      description: 'Send a message as an admin with optional attachments',
      input: {
        schema: z.object({
          adminId: z.string(),
          intercomConversationId: z.string(),
          body: z.string(),
          messageType: z.enum(['comment', 'note']).optional(),
          attachment_urls: z.array(z.string().url()).max(10).optional(),
        }),
      },
      output: {
        schema: z.object({
          id: z.string(),
          body: z.string(),
          createdAt: z.string(),
        }),
      },
    },
    // ... more actions
  },
})
```

### Key Integration Action Patterns

1. **Use RuntimeError for failures** - Provides better error context to bot developers
2. **Validate external API responses** - Always check `response.ok` and handle errors
3. **Transform external data** - Map external API schemas to your action output schema
4. **Use bp.secrets for credentials** - Never hardcode tokens or API keys
5. **Handle optional parameters** - Check before adding to request body
6. **Type external API responses** - Use TypeScript types from SDK if available

## Using Integration Actions

### Composing Actions

```typescript
// In a workflow step
await step('sync-to-slack', async () => {
  // Get data from Linear
  const { items } = await actions.linear.issueList({
    first: 10,
    filter: { state: { name: { eq: 'Done' } } },
  })

  // Send to Slack
  for (const issue of items) {
    await actions.slack.sendMessage({
      channel: '#updates',
      text: `✅ Completed: ${issue.title}`,
    })
  }
})
```

### Using in Workflows

```typescript
export const SyncLinearWorkflow = new Workflow({
  name: 'syncLinear',
  async handler({ step }) {
    // Step 1: Fetch from Linear
    const issues = await step('fetch-issues', async () => {
      const { items } = await actions.linear.issueList({
        first: 50,
        orderBy: { updatedAt: 'desc' },
      })
      return items
    })

    // Step 2: Process and update
    await step('update-database', async () => {
      for (const issue of issues) {
        await updateDatabase(issue)
      }
    })
  },
})
```

### Using in Tools

```typescript
import { Autonomous, z } from '@botpress/runtime'

export const searchWebTool = new Autonomous.Tool({
  name: 'searchWeb',
  description: 'Search the web for information',
  input: z.object({
    query: z.string().describe('Search query'),
  }),
  output: z.string(),
  handler: async ({ query }) => {
    const results = await actions.browser.webSearch({
      query,
      maxResults: 5,
    })

    return results.map((r, i) => `${i + 1}. ${r.title}\n${r.snippet}`).join('\n\n')
  },
})
```

## Type Inference

TypeScript automatically infers types from integration actions:

```typescript
// Infer return type
type SearchResult = Awaited<ReturnType<typeof actions.browser.webSearch>>
// SearchResult is { title: string; url: string; snippet: string }[]

// Infer parameter type
type IssueListParams = Parameters<typeof actions.linear.issueList>[0]
// IssueListParams is { first?: number; filter?: {...}; ... }

// Use in function signatures
async function processIssues(params: Parameters<typeof actions.linear.issueList>[0]) {
  const { items } = await actions.linear.issueList(params)
  // ...
}
```

## Bot Actions vs Integration Actions

The `actions` proxy handles both:

**Bot Actions** (from `src/actions/*.ts`):

```typescript
// Direct access to your bot's actions
await actions.myCustomAction({ param: 'value' })
```

**Integration Actions** (from installed integrations):

```typescript
// Nested under integration name
await actions.slack.sendMessage({ channel: '#general', text: 'Hi' })
```

The actions proxy automatically determines whether you're calling a bot action (top-level) or an integration action (nested under integration name).

## Troubleshooting

### Integration Not Found

```typescript
// Error: Could not find integration "slack" and action "sendMessage"
```

**Solutions:**

1. Add integration: `adk integrations add slack@2.5.5`
2. Enable: `adk integrations enable slack`
3. Configure credentials in Dev Console (localhost:3001) or via `adk integrations configure`
4. Restart dev server: `adk dev`

### Action Not Found

```typescript
// Error: Action "nonexistentAction" not found in integration "slack"
```

**Solutions:**

1. Check integration documentation for available actions
2. Verify integration version supports the action
3. Check for typos in action name

### Type Errors

```typescript
// Error: Property 'wrongParam' does not exist on type ...
```

**Solutions:**

1. Check IntelliSense for correct parameter names
2. Verify integration version matches your usage
3. Run `adk dev` to regenerate types

### Authentication Errors

```typescript
// Error: Integration not authenticated
```

**Solutions:**

1. Configure credentials in Dev Console (localhost:3001 during dev)
2. Set credentials via `adk integrations configure <alias> --set key=value`
3. Check environment variables are set
4. Verify API keys/tokens are valid

## Best Practices

### 1. Handle Errors Gracefully

```typescript
try {
  await actions.slack.sendMessage({ channel: '#general', text: 'Hi' })
} catch (error) {
  console.error('Failed to send Slack message:', error)
  // Fallback or retry logic
}
```

### 2. Use Type Inference

```typescript
// ✅ Good - Let TypeScript infer types
const issue = await actions.linear.getIssue({ id: "ISS-123" });

// ❌ Bad - Manual typing (can get out of sync)
const issue: { id: string; title: string } = await actions.linear.getIssue(...);
```

### 3. Check Integration Availability

```typescript
// For optional integrations
const slack = adk.project.integrations.get("slack");
if (slack) {
  await actions.slack.sendMessage(...);
} else {
  console.log("Slack not configured, skipping notification");
}
```

### 4. Batch When Possible

```typescript
// ✅ Good - Parallel requests
await Promise.all([
  actions.slack.sendMessage({ channel: '#team1', text: 'Update' }),
  actions.slack.sendMessage({ channel: '#team2', text: 'Update' }),
])

// ❌ Bad - Sequential (slower)
await actions.slack.sendMessage({ channel: '#team1', text: 'Update' })
await actions.slack.sendMessage({ channel: '#team2', text: 'Update' })
```

### 5. Use .asTool() for AI

```typescript
// Make integration actions available to AI
await execute({
  instructions: 'Help the user',
  tools: [actions.linear.issueCreate.asTool(), actions.slack.sendMessage.asTool()],
})
```

## See Also

- **[Agent Configuration](./agent-config.md)** - Installing and configuring integrations
- **[Actions](./actions.md)** - Creating custom actions
- **[Tools](./tools.md)** - Creating AI-callable tools
- **[Workflows](./workflows.md)** - Using actions in workflows
- **[Context API](./context-api.md)** - Accessing integrations via context
