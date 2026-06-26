# Workflows

Workflows are multi-step, resumable processes that maintain state across executions. They're perfect for complex operations, scheduled tasks, and long-running processes that may need to pause for user input or external events.

## Table of Contents

- [Basic Concepts](#basic-concepts)
- [Creating Workflows](#creating-workflows)
- [Managing Instances](#managing-instances)
- [State, Input, and Output](#state-input-and-output)
- [Step Mechanics](#step-mechanics)
- [Communication Patterns](#communication-patterns)
- [AI/LLM Integration](#aillm-integration)
- [Exposing Workflows as Tools (Non-Blocking Pattern)](#exposing-workflows-as-tools-non-blocking-pattern)
- [Scheduled Workflows](#scheduled-workflows)
- [Best Practices](#best-practices)

## Basic Concepts

### What are Workflows?

- **Resumable**: Can pause and resume from where they left off
- **Stateful**: Maintain state across steps and restarts
- **Scheduled**: Can run on cron schedules
- **Interactive**: Can request data from conversations

### File Location

- **Location**: `src/workflows/*.ts`
- **Auto-registration**: Files automatically become available as workflows

## Creating Workflows

### Basic Structure

> ⚠️ **CRITICAL: State Access Pattern**
>
> Workflow state is passed as a **parameter** to the handler, not accessed via `this.state`!
> The handler receives `{ input, state, step, client, execute }` where `state` is a mutable parameter that's automatically tracked and persisted.

```typescript
import { Workflow, z } from '@botpress/runtime'

export const MyWorkflow = new Workflow({
  name: 'myWorkflow',
  description: 'Description of what this workflow does',

  // Optional: Set workflow timeout (default: 5 minutes)
  timeout: '6h', // Can be: "30m", "2h", "1d", etc.

  // Optional: Schedule for automatic execution
  schedule: '0 9 * * *', // Cron format (daily at 9 AM)

  // Input schema - data required to start the workflow
  input: z.object({
    userId: z.string(),
    data: z.string(),
  }),

  // State schema - mutable data that persists across steps
  state: z.object({
    currentStep: z.number().default(0),
    processedItems: z.array(z.string()).default([]),
  }),

  // Output schema - what the workflow returns when complete
  output: z.object({
    result: z.boolean(),
    itemsProcessed: z.number(),
  }),

  // Handler receives state as a parameter
  async handler({ input, state, step, client, execute }) {
    // Access and modify state directly (it's automatically tracked)
    state.currentStep = 1

    // Execute steps
    const data = await step('fetch-data', async () => {
      return await fetchSomething(input.userId)
    })

    state.processedItems.push(data)

    // Return output
    return {
      result: true,
      itemsProcessed: state.processedItems.length,
    }
  },
})
```

### Handler Parameters

The handler receives these parameters:

```typescript
async handler({ input, state, step, client, execute }) {
  // input: z.infer<Input> - Read-only input data
  // state: z.infer<State> - Mutable workflow state (automatically tracked and persisted)
  // step: TypedWorkflowStep - Step execution functions
  // client: BotClient - Botpress API client
  // execute: ExecuteFn - AI execution function for autonomous operations
}
```

#### Using AI Execute in Workflows

The `execute` function enables AI operations within workflows:

```typescript
export const AnalyzeWorkflow = new Workflow({
  name: 'analyze',
  async handler({ input, step, execute }) {
    const result = await step('ai-analysis', async () => {
      return await execute({
        instructions: 'Analyze the provided data',
        model: 'openai:gpt-4o',
        temperature: 0,
        input: { data: input.data },
      })
    })

    return { analysis: result }
  },
})
```

## Managing Instances

### Creating and Retrieving Workflows

```typescript
// 1. Start a new workflow (always creates new instance)
const instance = await MyWorkflow.start({
  userId: user.id,
  data: 'some data',
})
console.log(instance.id) // "wflw_abc123"

// 2. Get or create (idempotent - uses key for deduplication)
const instance = await MyWorkflow.getOrCreate({
  key: user.id, // Unique key prevents duplicates
  input: { userId: user.id, data: 'x' },
})

// 3. Check status via getOrCreate (no standalone get/list methods)
const instance = await MyWorkflow.getOrCreate({
  key: user.id,
  input: { userId: user.id, data: 'x' },
})
console.log(instance.status) // "in_progress" | "completed" | "failed"
```

### Important Notes

- There is NO `create()`, `get()`, or `list()` method - use `start()` or `getOrCreate()`
- `start()`: Always creates a new instance
- `getOrCreate()`: Creates only if no instance exists with the given key

### Instance Properties

```typescript
const instance = await MyWorkflow.getOrCreate({
  key: userId,
  input: {
    /* ... */
  },
})

// Available properties
console.log(instance.id) // "wflw_abc123"
console.log(instance.status) // "in_progress" | "completed" | "failed" | "cancelled"
console.log(instance.input) // Input data
console.log(instance.state) // Current state
console.log(instance.output) // Output (undefined if not complete)
```

### Workflow Control Methods

#### Cancelling Workflows

Cancel a running workflow from outside:

```typescript
const instance = await MyWorkflow.getOrCreate({
  key: userId,
  input: {
    /* ... */
  },
})

if (instance && instance.status === 'in_progress') {
  await instance.cancel()
  console.log(instance.status) // "cancelled"
}
```

Cancellation is also available via the ADK UI (localhost:3001) during development.

#### Completing Workflows Early

Complete a workflow immediately with output (from within the handler):

```typescript
export const MyWorkflow = new Workflow({
  name: 'myWorkflow',
  output: z.object({
    result: z.string(),
    skipped: z.boolean(),
  }),

  async handler({ input, workflow, step }) {
    // Check condition and complete early
    if (input.skipProcessing) {
      workflow.complete({
        result: 'Skipped',
        skipped: true,
      })
      // Code after complete() is never reached
    }

    // Normal processing continues if not completed early
    const data = await step('process', async () => {
      return await processData(input)
    })

    return { result: data, skipped: false }
  },
})
```

**Note:** `workflow.complete()` can only be called from within the workflow handler. It immediately interrupts execution.

#### Failing Workflows

Fail a workflow with an error reason (from within the handler):

```typescript
export const MyWorkflow = new Workflow({
  name: 'myWorkflow',

  async handler({ input, workflow, step }) {
    // Validate input
    if (!input.data || input.data.length === 0) {
      workflow.fail('Invalid input: data cannot be empty')
      // Code after fail() is never reached
    }

    // Check external conditions
    const isAvailable = await step('check-service', async () => {
      return await checkServiceAvailability()
    })

    if (!isAvailable) {
      workflow.fail('External service unavailable')
    }

    // Continue normal processing
    return { success: true }
  },
})
```

**Note:** `workflow.fail()` can only be called from within the workflow handler. It immediately interrupts execution and marks the workflow as failed.

#### Extending Workflow Timeouts

Extend or set a new timeout for long-running workflows:

```typescript
export const LongRunningWorkflow = new Workflow({
  name: 'longRunning',
  timeout: '1h', // Initial timeout

  async handler({ input, workflow, step }) {
    // Extend timeout before a long operation
    workflow.setTimeout({ in: '6h' }) // Relative: 6 hours from now

    // Or set an absolute deadline
    workflow.setTimeout({ at: '2025-12-31T23:59:59Z' })

    // Long-running operation
    for (const batch of batches) {
      await step(`process-batch-${batch.id}`, async () => {
        // Extend timeout for each batch if needed
        workflow.setTimeout({ in: '30m' })
        return await processBatch(batch)
      })
    }

    return { completed: true }
  },
})
```

**Duration formats:** `"30m"`, `"1h"`, `"6 hours"`, `"1d"`, etc.

#### Control Methods Summary

| Method                        | Location        | Purpose                      |
| ----------------------------- | --------------- | ---------------------------- |
| `instance.cancel()`           | Outside handler | Cancel a workflow externally |
| `workflow.complete(output)`   | Inside handler  | Complete early with output   |
| `workflow.fail(reason)`       | Inside handler  | Fail with error message      |
| `workflow.setTimeout({ in })` | Inside handler  | Extend timeout (relative)    |
| `workflow.setTimeout({ at })` | Inside handler  | Set absolute deadline        |

## State, Input, and Output

### Understanding the Three Data Types

```typescript
export const DataWorkflow = new Workflow({
  name: 'dataWorkflow',

  // INPUT: Read-only data passed at creation
  input: z.object({
    userId: z.string(),
    config: z.object({ mode: z.string() }),
  }),

  // STATE: Mutable data persisted across steps
  state: z.object({
    currentStep: z.number().default(0),
    items: z.array(z.string()).default([]),
    error: z.string().optional(),
  }),

  // OUTPUT: Final result returned on completion
  output: z.object({
    success: z.boolean(),
    totalProcessed: z.number(),
  }),

  async handler({ input, state, step }) {
    // INPUT is read-only
    console.log(input.userId) // ✅ Read
    // input.userId = "new"; // ❌ TypeScript error

    // STATE is mutable via the state parameter
    state.currentStep = 1 // ✅ Automatically persisted
    state.items.push('item1')

    // Steps automatically persist state
    await step('process', async () => {
      state.currentStep = 2 // Saved even if workflow crashes
    })

    // OUTPUT is returned at the end
    return {
      success: true,
      totalProcessed: state.items.length,
    }
  },
})
```

## Step Mechanics

### Basic Steps

Steps are the fundamental unit of workflow execution with automatic persistence:

```typescript
async handler({ input, state, step }) {
  // Basic step - returns and caches the value
  const userData = await step("fetch-user", async () => {
    const data = await api.getUser(input.userId);
    return data; // This value is cached and returned
  });

  // Use the returned value
  console.log(userData.name);

  // Nested steps with return values
  const processedData = await step("process-data", async () => {
    // Steps can contain other steps
    const enriched = await step("enrich", async () => {
      return await enrichData(userData);
    });

    const validated = await step("validate", async () => {
      return await validateData(enriched);
    });

    return { enriched, validated }; // Return multiple values
  });

  // Step with retry logic
  const result = await step("risky-op", async ({ attempt }) => {
    console.log(`Attempt ${attempt}`);
    if (attempt < 3) {
      throw new Error("Retry me");
    }
    return "success";
  }, {
    maxAttempts: 5,  // Retry up to 5 times
    timeout: 10000   // 10 second timeout
  });

  // Accessing state inside steps
  await step("update-state", async () => {
    state.userData = userData; // State is accessible in the closure
    state.processedData = processedData;
    // No need to return if just updating state
  });

  // Progress logging in steps (production pattern)
  await step("final-processing", async () => {
    console.log(`✓ Processing user ${userData.id}`);
    const result = await finalProcess(processedData);
    console.log(`✓ Completed: ${result.status}`);
    return result;
  });
}
```

### Available Step Methods

```typescript
// Sleep for specified milliseconds
await step.sleep('wait-5s', 5000)

// Sleep until specific time
await step.sleepUntil('wait-until', new Date('2025-12-31'))

// Update progress message
await step.progress('Processing items...')

// Execute child workflow
const result = await step.executeWorkflow('child', ChildWorkflow, { input: data })

// Wait for workflow completion
await step.waitForWorkflow('wait-child', childWorkflowId)

// Request data from conversation (pauses workflow)
const answer = await step.request('confirmation', 'Do you want to proceed?')

// Process array in batches
await step.batch(
  'batch-urls',
  urls,
  async (batch) => {
    // Process batch
  },
  { batchSize: 20 }
)

// Map over array with parallel processing and retry logic
const results = await step.map(
  'map-items',
  items,
  async (item) => {
    return processItem(item)
  },
  {
    concurrency: 10, // Process 10 items at a time
    maxAttempts: 3, // Retry failed items up to 3 times
  }
)

// ForEach with concurrency
await step.forEach(
  'foreach-items',
  items,
  async (item) => {
    await processItem(item)
  },
  { concurrency: 5 }
)

// Listen for events (pauses until event)
await step.listen('wait-for-event')

// Fail workflow with message
await step.fail('Workflow failed due to X')

// Abort workflow (no args, synchronous, does not mark as failed)
step.abort()
```

### Step Rules

1. **Step names must be unique** within a workflow
2. **Step names must be stable** (don't use dynamic names)
3. **Steps execute sequentially**
4. **Completed steps are cached** and skipped on resume
5. **Step results are persisted**

```typescript
// ❌ BAD: Dynamic step names break resume
for (let i = 0; i < items.length; i++) {
  await step(`process-${i}`, async () => {
    /* ... */
  })
}

// ✅ GOOD: Single step for batch operations
await step('process-all-items', async () => {
  for (const item of items) {
    await processItem(item)
  }
})
```

## Communication Patterns

> **For simple turn-by-turn chat (quizzes, multi-step prompts within one conversation), don't use a Workflow.** Keep the sequence in the Conversation handler with per-conversation `state`. Request/provide workflows are for pausing on external or async input — overkill and hard to resume for linear chat.

### 1. Requesting User Input (Blocking)

Workflows can pause and request data from conversations:

```typescript
// In Workflow
export const InteractiveWorkflow = new Workflow({
  name: 'interactive',

  // Define expected request types
  requests: {
    email: z.object({ email: z.string().email() }),
    confirmation: z.object({ confirmed: z.boolean() }),
  },

  async handler({ state, step }) {
    // Request email (workflow pauses here)
    const { email } = await step.request('email', 'Please enter your email address:')

    // Request confirmation
    const { confirmed } = await step.request('confirmation', 'Do you want to proceed?')

    if (confirmed) {
      // Continue processing
    }
  },
})

// In Conversation - handle the request
export const Chat = new Conversation({
  channel: 'chat.channel',

  async handler({ type, request, conversation }) {
    if (type === 'workflow_request') {
      // Send prompt to user
      await conversation.send({
        type: 'text',
        payload: { text: request.workflow.prompt },
      })

      // Later, provide data back
      await request.workflow.provide('email', {
        email: userInput,
      })
    }
  },
})
```

### 2. Sending Progress Updates (Non-blocking)

Send messages without pausing execution:

```typescript
export const NotificationWorkflow = new Workflow({
  name: 'notification',
  input: z.object({
    conversationId: z.string(), // CRITICAL: Required for messaging
    userId: z.string(),
  }),

  async handler({ input, state, client, step }) {
    // Send progress update
    await step('notify-start', async () => {
      await client.createMessage({
        conversationId: input.conversationId,
        type: 'text',
        payload: { text: '🚀 Processing started...' },
      })
    })

    // Do work
    const result = await step('process', async () => {
      return await processData()
    })

    // Send completion
    await step('notify-complete', async () => {
      await client.createMessage({
        conversationId: input.conversationId,
        type: 'text',
        payload: { text: `✅ Complete: ${result}` },
      })
    })
  },
})
```

### 3. Starting Workflows from Conversations

**CRITICAL**: Always pass `conversationId` for communication:

```typescript
// In Conversation handler
async handler({ state, conversation, message }) {
  const instance = await MyWorkflow.start({
    conversationId: conversation.id,  // ← Essential!
    userId: user.id,
    data: message.payload.text
  });

  // Store workflow ID for tracking
  state.activeWorkflowId = instance.id;
}
```

### 4. Handling Workflow Completion in Conversations

When a workflow completes, fails, is canceled, or times out, the associated conversation handler receives a `workflow_callback` event with a typed `completion` object:

```typescript
// In Conversation - handle workflow completion
export const Chat = new Conversation({
  channel: 'chat.channel',

  async handler({ type, completion, conversation }) {
    if (type === 'workflow_callback') {
      // completion.type — workflow name (e.g., "processOrder")
      // completion.workflow — workflow instance
      // completion.status — "completed" | "failed" | "canceled" | "timed_out"
      // completion.output — workflow output (when completed)
      // completion.error — error message (when failed)

      if (completion.status === 'completed') {
        await conversation.send({
          type: 'text',
          payload: {
            text: `Processing finished! Result: ${JSON.stringify(completion.output)}`,
          },
        })
      } else if (completion.status === 'failed') {
        await conversation.send({
          type: 'text',
          payload: { text: `Processing failed: ${completion.error}` },
        })
      }
    }
  },
})
```

This replaces the need to poll workflow status or use raw event type guards. See **[Conversations — Handling Workflow Callbacks](./conversations.md#handling-workflow-callbacks-completion-events)** for full examples.

### Communication Best Practices

1. **Always pass conversationId** for workflows that need to communicate
2. **Wrap client calls in steps** for persistence and retry
3. **Choose the right pattern**:
   - `step.request()` for required user input
   - `type === "workflow_callback"` for reacting to workflow completion/failure
   - `client.createMessage()` for status updates
   - Events for decoupled notifications

## Inter-Workflow Communication

### Calling and Waiting for Other Workflows

Workflows can start and wait for other workflows to complete:

```typescript
import { Workflow, WorkflowDefinitions } from '@botpress/runtime'

export const ParentWorkflow = new Workflow({
  name: 'parent',
  input: z.object({
    conversationId: z.string(),
    uniqueKey: z.string(),
  }),
  output: z.object({
    childResult: z.any(),
  }),

  async handler({ step, input }) {
    // Start another workflow and wait for it
    const { output } = await step('call-child', async () => {
      const { id } = await ChildWorkflow.getOrCreate({
        input: { data: 'some data' },
        statuses: ['pending', 'in_progress', 'completed'],
        key: `child_${input.uniqueKey}`,
      })

      // Wait for the workflow to complete
      const result = await step.waitForWorkflow('ChildWorkflow', id)

      return result.output as WorkflowDefinitions['child']['output']
    })

    return { childResult: output }
  },
})
```

### Workflow Coordination Pattern

Use getOrCreate with unique keys to prevent duplicate workflows:

```typescript
export const ExtractTopicsWorkflow = new Workflow({
  name: 'topics',
  input: z.object({
    conversationId: z.string(),
  }),

  async handler({ step, input }) {
    // Get or create ensures only one workflow per conversation
    const { id } = await InsightsWorkflow.getOrCreate({
      input: { conversationId: input.conversationId },
      statuses: ['pending', 'in_progress', 'completed'],
      key: `insights_conversation_${input.conversationId}`, // Unique key
    })

    // If workflow already exists with key, returns existing instance
    const { output } = await step.waitForWorkflow('InsightsWorkflow', id)

    return output
  },
})
```

### Workflow Synchronization Pattern

When you need to ensure certain operations complete before others:

```typescript
export const SyncWorkflow = new Workflow({
  name: 'sync',

  async handler({ step, input }) {
    // Step 1: Get or create dependent workflow
    const topics = await step('find topics', async () => {
      const { id } = await InsightsTopicsWorkflow.getOrCreate({
        input: { conversationId: input.conversationId },
        statuses: ['pending', 'in_progress', 'completed'],
        key: `topics_conversation_${input.conversationId}`,
      })

      const { output } = await step.waitForWorkflow('InsightsTopicsWorkflow', id)

      return output as WorkflowDefinitions['insights_topics']['output']
    })

    // Step 2: Use the topics in the main processing
    const insights = await step('process insights', async () => {
      // Use topics data from the dependent workflow
      return processWithTopics(topics)
    })

    return { insights }
  },
})
```

## AI/LLM Integration

Workflows have full access to AI capabilities through multiple approaches:

### 1. Using execute() Function (Autonomous Agent)

```typescript
import { Workflow, z, Autonomous } from '@botpress/runtime'
import { actions } from '@botpress/runtime'

export const AIWorkflow = new Workflow({
  name: 'aiWorkflow',
  input: z.object({ question: z.string() }),
  output: z.object({ answer: z.string() }),

  handler: async ({ input, state, execute, step }) => {
    // Define exits for structured responses
    const AnswerExit = new Autonomous.Exit({
      name: 'Answer',
      description: 'Provide answer',
      schema: z.object({
        answer: z.string(),
        confidence: z.number(),
      }),
    })

    // Define tools for AI
    const SearchTool = new Autonomous.Tool({
      name: 'Search',
      description: 'Search for info',
      input: z.object({ query: z.string() }),
      output: z.string(),
      handler: async ({ query }) => {
        return await actions.browser.webSearch({ query })
      },
    })

    // Execute AI with tools
    const result = await execute({
      instructions: `Answer: "${input.question}"`,
      tools: [SearchTool],
      exits: [AnswerExit],
      model: 'openai:gpt-4o',
      temperature: 0.7,
      iterations: 10,
    })

    if (result.is(AnswerExit)) {
      return { answer: result.output.answer }
    }

    return { answer: 'No answer found' }
  },
})
```

### 2. Using execute() with Knowledge Bases

Provide knowledge bases directly to the AI for RAG-powered responses:

```typescript
import { Workflow, z, Autonomous } from '@botpress/runtime'
import { KnowledgeDocs } from '../knowledge/docs' // Your knowledge base

export const KnowledgeWorkflow = new Workflow({
  name: 'answerFromKnowledge',
  input: z.object({ question: z.string() }),

  handler: async ({ input, execute }) => {
    const AnswerExit = new Autonomous.Exit({
      name: 'Answer',
      description: 'Found answer in knowledge base',
      schema: z.object({
        answer: z.string(),
        sources: z.array(z.string()),
      }),
    })

    const NoAnswerExit = new Autonomous.Exit({
      name: 'NoAnswer',
      description: 'No relevant information found',
    })

    const result = await execute({
      instructions: `Find answer to: "${input.question}"
        Search the knowledge base and provide accurate information.
        If no relevant information exists, use NoAnswer exit.`,
      knowledge: [KnowledgeDocs], // Pass knowledge bases directly
      exits: [AnswerExit, NoAnswerExit],
      model: 'openai:gpt-4o',
      temperature: 0,
      iterations: 5,
    })

    if (result.is(AnswerExit)) {
      // Access citations if needed
      const citations = context.get('citations')
      const [cleaned, found] = citations.removeCitationsFromObject(result.output.answer)

      return {
        answer: cleaned,
        hasSources: found.length > 0,
      }
    }

    return { answer: 'No information found', hasSources: false }
  },
})
```

### 3. Using Cognitive Client (Raw LLM)

```typescript
import { Workflow, z, context } from '@botpress/runtime'

export const DirectLLMWorkflow = new Workflow({
  name: 'directLLM',

  handler: async ({ input, state, step }) => {
    const cognitive = context.get('cognitive')

    const result = await step('generate', async () => {
      const response = await cognitive.generateContent({
        model: 'openai:gpt-4o',
        systemPrompt: 'You are helpful',
        messages: [{ role: 'user', content: input.prompt }],
        temperature: 0.7,
        maxTokens: 1000,
      })

      return response.choices[0].message.content
    })

    return { response: result }
  },
})
```

### 3. Using Zai (Structured Operations)

Use `adk.zai` for structured AI operations (extract, check, summarize, etc.) inside workflows. Always wrap Zai calls in `step()` for persistence.

```typescript
import { Workflow, z, adk } from '@botpress/runtime'

export const ZaiWorkflow = new Workflow({
  name: 'zaiWorkflow',
  handler: async ({ input, state, step }) => {
    const insights = await step('extract insights', async () =>
      adk.zai.extract(
        input.text,
        z.array(
          z.object({
            type: z.enum(['bug', 'feature_request', 'question']),
            description: z.string(),
            priority: z.enum(['low', 'medium', 'high']),
          })
        )
      )
    )
    const hasBugs = await step('check for bugs', async () => adk.zai.check(insights, 'Are there any bug reports?'))
    return { insights, hasBugs }
  },
})
```

### AI Approach Comparison

| Approach                | Best For                       | Example Use Case         |
| ----------------------- | ------------------------------ | ------------------------ |
| **execute()**           | Multi-step AI tasks with tools | Research, support agents |
| **Cognitive Client**    | Simple text generation         | Content generation       |
| **Zai**                 | Structured data extraction     | Entity extraction        |
| **Integration Actions** | Provider-specific features     | Vision models            |

### Important AI Notes

1. **Always wrap AI calls in step()** for persistence
2. **Model format**: Use `"provider:model"` (e.g., `"openai:gpt-4o"`)
3. **Cost awareness**: AI calls consume tokens
4. **Error handling**: AI calls can fail, use retries

> For the full list of Zai operations, everyday use cases, and edge cases, see [zai-agent-reference.md](./zai-agent-reference.md).

## Exposing Workflows as Tools (Non-Blocking Pattern)

Workflows can be converted to tools using `.asTool()`. This is useful when you want AI to start a long-running workflow without blocking on its completion.

### Direct Workflow Tool Pattern

```typescript
// Starts the workflow and returns immediately
await execute({
  tools: [MyWorkflow.asTool()],
})
```

When a workflow is exposed this way, the tool starts the workflow and returns a lightweight result such as the workflow ID and current status.

### When to Still Use an Action Wrapper

An Action wrapper is still useful when you want to rename the tool, constrain inputs, add business rules, or hide workflow details from the AI:

```typescript
// File: /actions/start-processing.ts
import { Action, z } from '@botpress/runtime'
import { DataProcessingWorkflow } from '../workflows/data-processing'

export default new Action({
  name: 'startDataProcessing',
  description: 'Start data processing workflow',

  input: z.object({
    datasetId: z.string(),
    options: z
      .object({
        fullScan: z.boolean().default(false),
      })
      .optional(),
  }),

  output: z.object({
    workflowId: z.string(),
  }),

  async handler({ input }) {
    // Calls workflow.start() - returns immediately
    const instance = await DataProcessingWorkflow.start({
      datasetId: input.datasetId,
      options: input.options || { fullScan: false },
    })

    return { workflowId: instance.id }
  },
})
```

Use the Action wrapper as a tool:

```typescript
import { Conversation, actions } from '@botpress/runtime'

export default new Conversation({
  channel: '*',
  handler: async ({ execute }) => {
    await execute({
      instructions: 'Help the user',
      tools: [actions.startDataProcessing.asTool()],
    })
  },
})
```

### Tracking Workflow Status

#### 1. Status Check Action

```typescript
import { Action, z, context } from '@botpress/runtime'

export default new Action({
  name: 'checkProcessingStatus',
  description: 'Check workflow status',

  input: z.object({
    workflowId: z.string(),
  }),

  output: z.object({
    status: z.string(),
    progress: z.number(),
  }),

  async handler({ workflowId }) {
    const client = context.get('client')
    const { workflow } = await client.getWorkflow({ id: workflowId })

    const { state } = await client
      .getState({
        name: 'workflowSteps',
        id: workflowId,
        type: 'workflow',
      })
      .catch(() => ({ state: { payload: { steps: {} } } }))

    const steps = state.payload.steps || {}
    const stepArray = Object.values(steps)
    const completed = stepArray.filter((s: any) => s.finishedAt).length
    const progress = stepArray.length > 0 ? Math.round((completed / stepArray.length) * 100) : 0

    return {
      status: workflow.status,
      progress,
    }
  },
})
```

#### 2. Progress Events

Send progress events from workflow:

```typescript
import { context } from '@botpress/runtime'

export const DataProcessingWorkflow = new Workflow({
  name: 'dataProcessing',

  async handler({ input, state, step, client }) {
    const workflow = context.get('workflow')
    const conversationId = workflow.conversationId

    if (conversationId) {
      await client.createEvent({
        type: 'workflowProgress',
        conversationId,
        payload: {
          workflowId: workflow.id,
          stage: 'processing',
          progress: 50,
        },
      })
    }

    return { itemsProcessed: 0 }
  },
})
```

### Key Differences

| Aspect        | Action        | Workflow Wrapper  |
| ------------- | ------------- | ----------------- |
| **Returns**   | Final result  | Workflow ID       |
| **Execution** | Synchronous   | Asynchronous      |
| **Example**   | `fetchUser()` | `startIndexing()` |

> **See Also:** [Converting Actions to Tools](./actions.md#converting-actions-to-tools) for more details on using `.asTool()` with different action patterns.

## Scheduled Workflows

Run workflows automatically on a schedule:

```typescript
import { bot, Workflow, z } from '@botpress/runtime'

export const DailySync = new Workflow({
  name: 'dailySync',
  description: 'Syncs data daily with incremental updates',

  // Cron schedule (runs at 8 AM every day)
  schedule: '0 8 * * *',

  // Long timeout for large sync operations
  timeout: '6h',

  // Scheduled workflows can have optional input for manual triggering
  input: z.object({
    fullSync: z.boolean().default(false).describe('Force full sync'),
  }),

  // Track sync progress
  state: z.object({
    lastSyncDate: z.string().optional(),
    itemsProcessed: z.number().default(0),
  }),

  async handler({ input, state, step }) {
    // Access global bot state to check if initial sync is done
    bot.state.syncStatus ??= { initialized: false }

    const isInitialSync = input.fullSync || !bot.state.syncStatus.initialized

    const report = await step('generate', async () => {
      return await generateDailyReport(isInitialSync)
    })

    await step('send', async () => {
      await sendReportToTeam(report)
    })

    // Mark initial sync as complete in global state
    if (isInitialSync) {
      bot.state.syncStatus.initialized = true
    }

    return { sent: true }
  },
})
```

### Cron Syntax Reference

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

### Common Patterns

```typescript
const schedulePatterns = {
  everyMinute: '* * * * *',
  every5Minutes: '*/5 * * * *',
  everyHour: '0 * * * *',
  daily9AM: '0 9 * * *',
  weekdaysMorning: '0 9 * * 1-5', // Mon-Fri at 9am
  firstOfMonth: '0 0 1 * *',
}
```

## Accessing Global Bot State

Workflows can also access and modify global bot state (not just workflow-specific state):

```typescript
import { bot, Workflow, z } from '@botpress/runtime'

export const AnalysisWorkflow = new Workflow({
  name: 'analysis',
  schedule: '0 8 * * *', // Daily at 8 AM

  async handler({ state, step }) {
    // Perform analysis
    const results = await step('analyze', async () => {
      return await performAnalysis()
    })

    // Store results in global bot state
    bot.state.analysisResults = results
    bot.state.lastAnalysisDate = new Date().toISOString()

    // Access existing bot state
    console.log(`Previous analysis: ${bot.state.lastAnalysisDate}`)

    return { completed: true }
  },
})
```

This is useful for:

- Storing cross-workflow shared data
- Maintaining global configuration
- Tracking system-wide metrics
- Sharing state between workflows and conversations

## Best Practices

### 1. Use Meaningful Keys

```typescript
// Prevent duplicate workflows for same user
await MyWorkflow.getOrCreate({
  key: userId, // Or composite: `${userId}-${date}`
  input: { userId },
})
```

### 2. Keep Step Names Stable

```typescript
// ✅ GOOD: Stable step names
await step('process-batch', async () => {
  for (const item of items) {
    await processItem(item)
  }
})

// ❌ BAD: Dynamic step names
for (let i = 0; i < items.length; i++) {
  await step(`process-${i}`, async () => {})
}
```

### 3. Store Progress in State

```typescript
// Access state via the state parameter in workflow handlers
state.progress = 'Processing item 5 of 10'
state.percentComplete = 50
// External systems can poll this state via workflow instance
```

### 4. Pass State Values, Not References

```typescript
// ❌ BAD - Passing state reference
async handler({ state, step }) {
  const result = await processItems(state.items);
  // If state.items changes, processItems might see it!
}

// ✅ GOOD - Pass a copy
async handler({ state, step }) {
  const itemsCopy = [...state.items];
  const result = await processItems(itemsCopy);
  // Safe - function has its own copy
}

// ✅ GOOD - Extract primitives directly
async handler({ state, step }) {
  const count = state.count;  // Primitives are safe
  const items = [...state.items];  // Arrays need copying
  const config = { ...state.config };  // Objects need copying

  await step("process", async () => {
    return await processData(count, items, config);
  });
}
```

### 5. Handle Errors Gracefully

```typescript
await step(
  'risky-op',
  async () => {
    try {
      return await riskyOperation()
    } catch (error) {
      state.lastError = error.message // Store error in state
      throw error // Re-throw to mark step as failed
    }
  },
  { maxAttempts: 3 }
)
```

### 6. Use Appropriate Timeouts

```typescript
export const MyWorkflow = new Workflow({
  timeout: '5m', // Balance completion time and resources
  // ...
})
```

## Complete Example: Research Workflow

```typescript
import { Workflow, z, Autonomous } from '@botpress/runtime'
import { actions } from '@botpress/runtime'

export const ResearchWorkflow = new Workflow({
  name: 'research',
  description: 'Research a topic using web searches',

  input: z.object({
    topic: z.string(),
    conversationId: z.string(),
  }),

  state: z.object({
    sources: z.array(z.string()).default([]),
    progress: z.string().default('Starting...'),
  }),

  output: z.object({
    report: z.string(),
  }),

  async handler({ input, state, execute, step, client }) {
    // Notify start
    await step('notify-start', async () => {
      await client.createMessage({
        conversationId: input.conversationId,
        type: 'text',
        payload: { text: `🔍 Researching "${input.topic}"...` },
      })
    })

    // Define search tool
    const SearchTool = new Autonomous.Tool({
      name: 'webSearch',
      description: 'Search the web',
      input: z.object({ query: z.string() }),
      output: z.string(),
      async handler({ query }) {
        const results = await actions.browser.webSearch({
          query,
          count: 5,
        })
        state.sources.push(...results.urls) // State accessible in closure
        throw new Autonomous.ThinkSignal('Found sources', results)
      },
    })

    // Define report exit
    const ReportExit = new Autonomous.Exit({
      name: 'Report',
      description: 'Final research report',
      schema: z.string(),
    })

    // Execute research
    const report = await step('research', async () => {
      state.progress = 'Researching...' // Update state

      const result = await execute({
        instructions: `Research "${input.topic}".
          Use web searches to gather information.
          Compile findings into a comprehensive report.`,
        tools: [SearchTool],
        exits: [ReportExit],
        iterations: 15,
      })

      if (result.is(ReportExit)) {
        return result.output
      }
      return 'Research incomplete'
    })

    // Send report
    await step('send-report', async () => {
      await client.createMessage({
        conversationId: input.conversationId,
        type: 'text',
        payload: { text: `📄 Research Report:\n\n${report}` },
      })
    })

    return { report }
  },
})
```

## Workflow Lifecycle

### Status Values

- `pending`: Created but not started
- `in_progress`: Currently executing
- `completed`: Finished successfully
- `failed`: Terminated due to error
- `cancelled`: Manually cancelled
- `timedout`: Exceeded timeout limit

When a workflow reaches a terminal status (`completed`, `failed`, `cancelled`, `timedout`), the associated conversation handler receives a `workflow_callback` event. Use `type === "workflow_callback"` in the conversation handler to react to these transitions — see [Handling Workflow Completion in Conversations](#4-handling-workflow-completion-in-conversations).

### Managing Lifecycle

```typescript
// Check status
const instance = await MyWorkflow.getOrCreate({ key: userId, input: { /* ... */ } });
if (instance?.status === "failed") {
  // Retry by starting new instance
  await MyWorkflow.start(instance.input);
}

// Handle cancellation in handler
async handler({ state, step }) {
  if (state.shouldCancel) {
    return { cancelled: true };
  }
}
```
