# ZAI: Complete Developer Guide

ZAI (Zui AI) is Botpress's production-ready LLM utility library that provides a clean, type-safe API for common AI operations. Built on Zod schemas and the Botpress Cognitive API, it makes AI operations simple, intuitive, and scalable.

## Part I: Developer Usage

### 1. Getting Started

#### Installation

```bash
npm install @botpress/zai @botpress/client @bpinternal/zui
```

#### Basic Setup

```typescript
import { Client } from '@botpress/client'
import { Zai } from '@botpress/zai'
import { z } from '@bpinternal/zui'

// Initialize Botpress client
const client = new Client({
  botId: 'YOUR_BOT_ID',
  token: 'YOUR_TOKEN',
})

// Create ZAI instance
const zai = new Zai({ client })
```

#### Configuration Options

```typescript
const zai = new Zai({
  client, // Required: Botpress client or Cognitive instance
  modelId: 'best', // Model selection: 'best' | 'fast' | specific model ID
  userId: 'user-123', // Optional: Track usage per user
  namespace: 'my-app', // Default: 'zai'
  activeLearning: {
    // Enable learning from examples
    enable: true,
    tableName: 'AILearningTable',
    taskId: 'sentiment-analysis',
  },
})
```

### 2. Core Operations

#### 2.1 Extract - Structured Data Extraction

Extract structured data from any input using Zod schemas. Located in `/packages/zai/src/operations/extract.ts`.

**Basic Object Extraction:**

```typescript
const person = await zai.extract(
  'John Doe is 30 years old and lives in New York',
  z.object({
    name: z.string(),
    age: z.number(),
    location: z.string(),
  })
)
// Result: { name: 'John Doe', age: 30, location: 'New York' }
```

**Array Extraction:**

```typescript
const products = await zai.extract(
  productCatalogText,
  z.array(
    z.object({
      name: z.string(),
      price: z.number(),
      inStock: z.boolean(),
    })
  )
)
```

**Advanced Options:**

```typescript
const data = await zai.extract(input, schema, {
  instructions: 'Focus on technical specifications', // Guide extraction
  chunkLength: 8000, // Max tokens per chunk (default: 16000)
  strict: false, // Allow partial matches
})
```

**Large Document Handling:**
ZAI automatically handles documents of any size through intelligent chunking:

- Documents over `chunkLength` are split into chunks
- Each chunk is processed in parallel
- Results are intelligently merged

#### 2.2 Check - Boolean Verification

Verify conditions with natural language. Located in `/packages/zai/src/operations/check.ts`.

**Simple Check:**

```typescript
const isSpam = await zai.check('Win FREE iPhone!!!', 'is spam')
// Result: true
```

**Detailed Results:**

```typescript
const result = await zai.check(email, 'contains personal information')
const { value, explanation } = await result.full()
// value: true
// explanation: "The email contains names, addresses, and phone numbers"
```

**With Examples:**

```typescript
const isValid = await zai.check(code, 'is valid JavaScript', {
  examples: [
    { input: 'const x = 1', check: true, reason: 'Valid const declaration' },
    { input: 'const = 1', check: false, reason: 'Missing variable name' },
  ],
})
```

#### 2.3 Label - Multi-Label Classification

Apply multiple labels simultaneously. Located in `/packages/zai/src/operations/label.ts`.

```typescript
const labels = await zai.label(customerReview, {
  positive: 'expresses positive sentiment',
  technical: 'mentions technical specifications',
  verified: 'from a verified purchaser',
  urgent: 'requires immediate attention',
})
// Result: { positive: true, technical: true, verified: false, urgent: false }
```

Each label gets its own explanation:

```typescript
const result = await zai.label(text, criteria)
const detailed = await result.full()
// detailed.positive = { value: true, explanation: "User says 'excellent product'" }
```

#### 2.4 Rewrite - Text Transformation

Transform text according to instructions. Located in `/packages/zai/src/operations/rewrite.ts`.

**Translation:**

```typescript
const french = await zai.rewrite(englishText, 'translate to French')
```

**Tone Adjustment:**

```typescript
const professional = await zai.rewrite('hey whats up? need that report asap!!', 'make it professional and polite')
// "Good morning, I hope this message finds you well.
//  Could you please provide the report at your earliest convenience?"
```

**Format Conversion:**

```typescript
const markdown = await zai.rewrite(htmlContent, 'convert to Markdown format')
const json = await zai.rewrite(csvData, 'convert to JSON array')
```

#### 2.5 Filter - Array Filtering

Filter arrays using natural language conditions. Located in `/packages/zai/src/operations/filter.ts`.

```typescript
const companies = [
  { name: 'Apple', industry: 'Tech', revenue: 365 },
  { name: 'Ford', industry: 'Auto', revenue: 156 },
  { name: 'Google', industry: 'Tech', revenue: 282 },
]

const techGiants = await zai.filter(companies, 'are technology companies with revenue over 200 billion')
// Result: [Apple, Google]
```

**Complex Filtering:**

```typescript
const eligibleUsers = await zai.filter(
  users,
  `
  - Have verified email
  - Account created more than 30 days ago
  - No recent violations
  - Located in North America
`
)
```

#### 2.6 Text - Content Generation

Generate text from prompts. Located in `/packages/zai/src/operations/text.ts`.

```typescript
const blogPost = await zai.text('Write about the future of AI in healthcare', {
  length: 1000, // Target length in tokens
  temperature: 0.7, // Creativity (0-1)
  stopSequences: ['---'], // Optional stop markers
})
```

**Structured Generation:**

```typescript
const outline = await zai.text(`
  Create a detailed course outline for:
  - Topic: Machine Learning
  - Level: Beginner
  - Duration: 8 weeks
  - Format: Online
`)
```

#### 2.7 Summarize - Document Summarization

Create intelligent summaries. Located in `/packages/zai/src/operations/summarize.ts`.

**Basic Summary:**

```typescript
const summary = await zai.summarize(longArticle)
```

**Custom Summaries:**

```typescript
const technicalSummary = await zai.summarize(researchPaper, {
  length: 500, // Max tokens
  prompt: 'Focus on methodology and results',
  bulletPoints: true, // Format as bullet points
})
```

**Handling Large Documents:**

```typescript
// ZAI automatically handles documents of any size
const bookSummary = await zai.summarize(entireBook, {
  length: 2000,
  prompt: 'Summarize each chapter separately, then provide overall themes',
})
```

#### 2.8 Answer - Question Answering with Citations

Answer questions from documents with citations and intelligent edge case handling. Located in `/packages/zai/src/operations/answer.ts`.

**Basic Usage:**

```typescript
const documents = [
  'Botpress was founded in 2016.',
  'The company is based in Quebec, Canada.',
  'Botpress provides an AI agent platform.',
]

const result = await zai.answer(documents, 'When was Botpress founded?')
if (result.type === 'answer') {
  console.log(result.answer) // "Botpress was founded in 2016."
  console.log(result.citations) // Citations with source references
}
```

**Response Types:**

The answer operation returns different types based on the situation:

```typescript
const result = await zai.answer(documents, question)

switch (result.type) {
  case 'answer':
    // Has answer with citations
    console.log(result.answer)
    console.log(result.citations) // [{ offset, item, snippet }]
    break

  case 'ambiguous':
    // Multiple interpretations exist
    console.log(result.ambiguity) // Why it's ambiguous
    console.log(result.follow_up) // Clarifying question
    console.log(result.answers) // Possible answers
    break

  case 'out_of_topic':
    // Question unrelated to documents
    console.log(result.reason)
    break

  case 'invalid_question':
    // Malformed or unclear question
    console.log(result.reason)
    break

  case 'missing_knowledge':
    // Insufficient information to answer
    console.log(result.reason)
    break
}
```

**With Custom Instructions:**

```typescript
const result = await zai.answer(documents, "What is the pricing?", {
  instructions: "Provide detailed pricing breakdown including all tiers",
  chunkLength: 8000, // Process in smaller chunks
  examples: [...], // Few-shot examples
});
```

**Tracking Citations:**

```typescript
if (result.type === 'answer') {
  result.citations.forEach((citation) => {
    console.log(`At position ${citation.offset}:`)
    console.log(`  Cited: "${citation.snippet}"`)
    console.log(`  From document:`, citation.item)
  })
}
```

#### 2.9 Rate - Array Rating

Rate array items on a 1-5 scale based on criteria. Located in `/packages/zai/src/operations/rate.ts`.

**Single Criterion:**

```typescript
const emails = [
  /* array of emails */
]
const urgencyScores = await zai.rate(emails, 'urgency level')
// Result: [4, 2, 5, 1, 3]  // Numbers 1-5
```

**Multiple Criteria:**

```typescript
const products = [
  /* array of products */
]
const ratings = await zai.rate(products, {
  quality: 'product build quality',
  value: 'price to performance ratio',
  design: 'aesthetic appeal',
})
// Result: [
//   { quality: 5, value: 4, design: 5, total: 14 },
//   { quality: 3, value: 5, design: 4, total: 12 },
//   ...
// ]
```

**With Options:**

```typescript
const rated = await zai.rate(items, instructions, {
  tokensPerItem: 250, // Max tokens per item
  maxItemsPerChunk: 50, // Items per batch
})
```

#### 2.10 Sort - Natural Language Sorting

Sort arrays based on natural language instructions. Located in `/packages/zai/src/operations/sort.ts`.

**Basic Sorting:**

```typescript
const sorted = await zai.sort(tickets, 'from least urgent to most urgent')
const byPrice = await zai.sort(products, 'by price, cheapest first')
```

**Priority-Based Sorting:**

```typescript
const prioritized = await zai.sort(emails, 'prioritize: open old items highest')
// First item = highest priority, last = lowest priority
```

**Complex Sorting:**

```typescript
const sorted = await zai.sort(
  applications,
  `
  Sort by:
  1. Completeness (complete applications first)
  2. Submission date (newer first)
  3. Applicant experience (more experienced first)
`
)
```

**With Options:**

```typescript
const sorted = await zai.sort(items, instructions, {
  tokensPerItem: 250, // Max tokens per item
})
```

#### 2.11 Group - Array Grouping

Group array elements based on natural language criteria. Located in `/packages/zai/src/operations/group.ts`.

**Basic Grouping:**

```typescript
const groups = await zai.group(tickets, {
  instructions: 'group by issue type and priority',
})
// Result: [
//   { id: 'bugs', label: 'Bug Reports', elements: [...] },
//   { id: 'features', label: 'Feature Requests', elements: [...] },
//   { id: 'urgent', label: 'Urgent Issues', elements: [...] }
// ]
```

**With Initial Groups:**

```typescript
const groups = await zai.group(emails, {
  instructions: 'categorize emails',
  initialGroups: [
    { id: 'urgent', label: 'Urgent' },
    { id: 'spam', label: 'Spam' },
    { id: 'normal', label: 'Normal' },
  ],
})
```

**Access Results:**

```typescript
// As groups array
const groups = await zai.group(items, options)
for (const group of groups) {
  console.log(`${group.label}: ${group.elements.length} items`)
}

// As dictionary (using .result())
const { output } = await zai.group(items, options).result()
// output is Record<string, T[]>
```

**With Options:**

```typescript
const groups = await zai.group(items, {
  instructions: "group by category",
  tokensPerElement: 250, // Max tokens per element
  chunkLength: 16000, // Max tokens per chunk
  initialGroups: [...], // Predefined groups
});
```

#### 2.12 Patch - File Patching

Patch code files using natural language instructions with efficient micropatch protocol. Located in `/packages/zai/src/operations/patch.ts`.

**Basic Patching:**

```typescript
const files = [
  {
    path: 'src/hello.ts',
    name: 'hello.ts',
    content: 'console.log("Hello World")',
  },
]

const patched = await zai.patch(files, 'change message to "Hi World"')
// Result: [{
//   path: 'src/hello.ts',
//   name: 'hello.ts',
//   content: 'console.log("Hi World")',
//   patch: '◼︎=1|console.log("Hi World")'
// }]
```

**Multiple Files:**

```typescript
const files = [
  { path: 'package.json', name: 'package.json', content: '...' },
  { path: 'config.json', name: 'config.json', content: '...' },
]

const patched = await zai.patch(files, 'update version to 2.0.0 in all config files')
```

**Common Use Cases:**

```typescript
// Add documentation
await zai.patch(files, 'add JSDoc comments to all exported functions')

// Remove code
await zai.patch(files, 'remove all debug code')

// Refactoring
await zai.patch(files, 'convert to async/await and add error handling')

// Type annotations
await zai.patch(files, 'add TypeScript types to all function parameters')
```

**Inspect Applied Patches:**

```typescript
const patched = await zai.patch(files, instructions)
for (const file of patched) {
  if (file.patch) {
    console.log(`Patches for ${file.path}:`)
    console.log(file.patch) // Micropatch operations
  }
}
```

**With Options:**

```typescript
const patched = await zai.patch(files, instructions, {
  maxTokensPerChunk: 16000, // Max tokens per processing chunk
})
```

### 3. Advanced Features

#### 3.1 Active Learning

Enable learning from examples to improve accuracy over time. Implementation in `/packages/zai/src/zai.ts:106-112`.

**How It Works:**

1. **Example Storage**: When enabled, ZAI stores successful operations as examples with:
   - A unique hash key based on input, instructions, task type, and task ID
   - The input and output data
   - Metadata (tokens, cost, latency, model used)
   - A status field (`'pending'` by default)

2. **Example Retrieval**: On subsequent operations, ZAI:
   - Generates the same hash key for identical inputs
   - Checks for exact matches (returns immediately if found - no LLM call!)
   - Searches for similar examples using Botpress Tables API (first 1024 chars)
   - Includes up to 10 similar examples in the prompt to guide the LLM

3. **Key Generation** (`/packages/zai/src/operations/extract.ts:182-189`):

```typescript
const Key = fastHash(
  JSON.stringify({
    taskType: 'zai.extract',
    taskId: 'product-extraction',
    input: inputAsString,
    instructions: 'Extract product details',
  })
)
```

**Configuration:**

```typescript
// Enable globally
const zai = new Zai({
  client,
  activeLearning: {
    enable: true,
    tableName: 'MyLearningTable', // Must end with "Table"
    taskId: 'my-task', // Namespaced as 'zai/my-task'
  },
})

// Enable for specific task using .learn()
const sentimentZai = zai.learn('sentiment-analysis')
const result = await sentimentZai.check(text, 'is positive')
```

**Important Notes:**

- Examples are saved with `status: 'pending'` by default
- Only examples with `status: 'approved'` are used for learning
- The approval mechanism requires external implementation
- Without approved examples, learning is effectively disabled

**Method: `.learn(taskId)`**

Creates a new ZAI instance with active learning enabled for a specific task:

```typescript
// Enable for specific task
const sentimentZai = zai.learn('sentiment-analysis')

// What actually happens:
// 1. Enables active learning with the given taskId
// 2. Saves all operations as examples (status: 'pending')
// 3. Uses only 'approved' examples to improve prompts
// 4. WITHOUT approval, acts like caching without learning
```

**Note**: The `learn()` method enables the infrastructure but doesn't automatically approve examples. External approval is required for true learning to occur.

#### 3.1.1 Active Learning Limitations & Considerations

**Current Limitations:**

- **Manual Approval Required**: Examples default to `'pending'` status and require external approval
- **Search Scope**: Only first 1024 characters of input used for similarity search
- **Example Limit**: Maximum 10 examples retrieved per operation
- **No Auto-Learning**: Without approval workflow, examples accumulate but aren't used

**Storage Details:**

- Uses Botpress Tables with `'x-studio-readonly': 'true'` (read-only in Studio)
- Table schema includes fields for feedback and ratings (not currently used)
- Similarity scoring handled by Botpress Tables API, not ZAI

**Performance Impact:**

- Exact matches bypass LLM completely (instant response)
- Similar examples improve prompt quality but add tokens
- Failed operations aren't saved as examples

**Best Practices:**

- Use unique task IDs for different contexts to prevent cross-contamination
- Monitor table size - unused pending examples accumulate over time
- Consider implementing custom approval workflow if needed
- Test with MemoryAdapter first before using TableAdapter in production

**Example Isolation:**

```typescript
// Isolate learning contexts
const productSpamZai = zai.learn('spam-detection-products')
const commentSpamZai = zai.learn('spam-detection-comments')

// Each maintains separate example sets
const isProductSpam = await productSpamZai.check(productDesc, 'is spam')
const isCommentSpam = await commentSpamZai.check(userComment, 'is spam')
```

#### 3.2 Progress Tracking

Monitor long-running operations. Implementation in `/packages/zai/src/response.ts`.

```typescript
const response = zai.summarize(veryLongDocument)

// Track progress
response.on('progress', (progress) => {
  console.log(`Processing: ${progress.percent}% complete`)
  console.log(`Chunks: ${progress.completed}/${progress.total}`)
})

const summary = await response
```

**Additional Event Methods:**

```typescript
// One-time event listener
response.once('complete', (result) => {
  console.log('Operation finished:', result)
})

// Remove event listener
const handler = (progress) => console.log(progress)
response.on('progress', handler)
response.off('progress', handler)

// Connect AbortSignal for external cancellation control
const controller = new AbortController()
response.bindSignal(controller.signal)

// Cancel from external controller
setTimeout(() => controller.abort(), 5000)
```

#### 3.3 Usage Monitoring

Track tokens, costs, and performance. Implementation in `/packages/zai/src/context.ts:175-196`.

```typescript
const result = await zai.extract(text, schema)
const usage = await result.usage()

console.log({
  tokens: {
    input: usage.tokens.input,
    output: usage.tokens.output,
    total: usage.tokens.total,
  },
  cost: {
    input: usage.cost.input,
    output: usage.cost.output,
    total: usage.cost.total, // In USD
  },
  requests: usage.requests.requests,
  cached: usage.requests.cached,
  latency: usage.elapsedTime, // Milliseconds
})
```

#### 3.4 Method Chaining

Create specialized instances with different configurations:

```typescript
// Create temperature variant
const creativeZai = zai.with({ temperature: 0.9 })

// Chain multiple configurations
const preciseExtractor = zai.with({ modelId: 'gpt-4-turbo' }).with({ temperature: 0.1 }).learn('invoice-extraction')

const invoice = await preciseExtractor.extract(document, invoiceSchema)
```

#### 3.5 Abort Operations

Cancel long-running operations:

```typescript
const response = zai.summarize(massiveDocument)

// Abort after 5 seconds
setTimeout(() => response.abort(), 5000)

try {
  const summary = await response
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Operation cancelled')
  }
}
```

### 4. Error Handling

#### Common Error Types

```typescript
try {
  const result = await zai.extract(text, schema)
} catch (error) {
  if (error instanceof JsonParsingError) {
    // Schema validation failed
    console.error('Invalid JSON:', error.message)
  } else if (error.name === 'AbortError') {
    // Operation was cancelled
    console.log('Operation aborted')
  } else if (error.code === 'RATE_LIMIT') {
    // API rate limit hit
    await delay(error.retryAfter)
  }
}
```

#### Automatic Retries

ZAI includes built-in retry logic with exponential backoff. You can also wrap ZAI for custom retry behavior:

```typescript
// Example from /packages/llmz/examples/utils/zai.ts:3-33
import { withRetry } from './utils/zai'

const reliableZai = withRetry(zai)
const result = await reliableZai.extract(text, schema) // Retries up to 10 times
```

### 5. Integration Patterns

#### 5.1 With Botpress Bots

```typescript
// In Botpress action or hook
import { Zai } from '@botpress/zai'

export const analyzeSentiment = async ({ client, input }) => {
  const zai = new Zai({ client })

  const sentiment = await zai.label(input.message, {
    positive: 'expresses positive sentiment',
    negative: 'expresses negative sentiment',
    neutral: 'is neutral in tone',
  })

  return { sentiment }
}
```

#### 5.2 With LLMz Framework

Example from `/packages/llmz/examples/07_chat_guardrails/index.ts:33-46`:

```typescript
import { execute, ThinkSignal } from 'llmz'
import { Zai } from '@botpress/zai'

const zai = new Zai({ client })

// Use ZAI for content moderation
const guardrails = {
  violence: 'is free of violence',
  hate: 'is free of hate speech',
  pii: 'does not contain personal data',
}

await execute({
  async onBeforeExecution(iteration) {
    const checks = await zai.label(iteration.code, guardrails)

    const violations = Object.entries(checks)
      .filter(([_, result]) => !result.value)
      .map(([rule, result]) => `${rule}: ${result.explanation}`)

    if (violations.length > 0) {
      throw new ThinkSignal(`Fix violations: ${violations.join(', ')}`)
    }
  },
})
```

#### 5.3 Batch Processing

```typescript
async function processBatch(documents: string[]) {
  // Process in parallel with concurrency limit
  const results = await Promise.all(
    documents.map(async (doc, i) => {
      // Stagger requests to avoid rate limits
      await delay(i * 100)

      return zai.extract(
        doc,
        z.object({
          title: z.string(),
          category: z.string(),
          summary: z.string(),
        })
      )
    })
  )

  return results
}
```

## Part II: Stack Architecture

### 1. Core Architecture

#### 1.1 Package Structure

Located at `/packages/zai/`:

```
packages/zai/
├── src/
│   ├── index.ts                 # Main export
│   ├── zai.ts                   # Core Zai class (79-163)
│   ├── context.ts               # Execution context management
│   ├── response.ts              # Response wrapper with events
│   ├── emitter.ts               # Event emitter implementation
│   ├── tokenizer.ts             # Token counting utilities
│   ├── utils.ts                 # Helper functions
│   ├── operations/              # Operation implementations
│   │   ├── extract.ts           # Data extraction (52-403)
│   │   ├── check.ts             # Boolean checks
│   │   ├── label.ts             # Multi-label classification
│   │   ├── rewrite.ts           # Text transformation
│   │   ├── filter.ts            # Array filtering
│   │   ├── text.ts              # Text generation
│   │   ├── summarize.ts         # Summarization
│   │   ├── constants.ts         # Shared constants
│   │   └── errors.ts            # Custom error types
│   └── adapters/                # Storage adapters
│       ├── adapter.ts           # Base adapter interface
│       ├── botpress-table.ts    # Botpress Tables adapter
│       └── memory.ts            # In-memory adapter
├── e2e/                         # End-to-end tests
├── build.ts                     # Build configuration
└── package.json                 # Dependencies
```

#### 1.2 Dependency Chain

```typescript
// Core dependencies (/packages/zai/package.json:34-39)
{
  "@botpress/cognitive": "0.3.6",     // LLM abstraction layer
  "@bpinternal/zui": "^1.3.2",        // Zod-based schema library
  "@bpinternal/thicktoken": "^1.0.0", // WASM tokenizer
  "json5": "^2.2.3",                  // Flexible JSON parsing
  "jsonrepair": "^3.10.0",            // Fix malformed JSON
  "lodash-es": "^4.17.21"             // Utility functions
}
```

#### 1.3 Class Hierarchy

**Main Class** (`/packages/zai/src/zai.ts:79-163`):

```typescript
export class Zai {
  protected client: Cognitive // LLM client
  protected Model: ModelId // Selected model
  protected namespace: string // Operation namespace
  protected adapter: Adapter // Storage adapter
  protected activeLearning: ActiveLearning

  constructor(config: ZaiConfig)
  with(options: Partial<ZaiConfig>): Zai
  learn(taskId: string): Zai
}
```

**Context Management** (`/packages/zai/src/context.ts:45-197`):

```typescript
export class ZaiContext {
  private _client: Cognitive
  public controller: AbortController

  async generateContent<Out>(props): Promise<{ meta; output; text; extracted }>
  get usage(): Usage
  on<K>(type: K, listener: Function): this
}
```

### 2. Execution Pipeline

#### 2.1 Operation Flow

1. **User calls operation** (e.g., `zai.extract()`)
2. **Create ZaiContext** with client, model, and task info
3. **Prepare prompt** using operation-specific template
4. **Check active learning** for cached examples
5. **Generate content** via Cognitive API
6. **Transform response** based on operation type
7. **Store example** if active learning enabled
8. **Return Response** wrapper with result

#### 2.2 Prompt Engineering

Each operation uses sophisticated prompts. Example from extract (`/packages/zai/src/operations/extract.ts:301-316`):

```typescript
systemPrompt: `
Extract the following information from the input:
${schemaTypescript}
====
${instructions.map((x) => `• ${x}`).join('\n')}
`.trim()
```

Operations include:

- Schema definitions in TypeScript format
- Clear instructions with examples
- Special markers for parsing (e.g., `■json_start■`, `■json_end■`)

#### 2.3 Chunking Strategy

For large documents (`/packages/zai/src/operations/extract.ts:112-149`):

```typescript
if (tokenizer.count(inputAsString) > options.chunkLength) {
  // 1. Split into chunks
  const tokens = tokenizer.split(inputAsString)
  const chunks = chunk(tokens, options.chunkLength)

  // 2. Process in parallel
  const all = await Promise.allSettled(chunks.map((chunk) => extract(chunk, schema, options, ctx)))

  // 3. Merge results recursively
  return extract(mergePrompt, originalSchema, options, ctx)
}
```

### 3. Storage & Learning

#### 3.1 Adapter System

**Base Interface** (`/packages/zai/src/adapters/adapter.ts`):

```typescript
export interface Adapter {
  saveExample(example: Example): Promise<void>
  getExamples<I, O>(params: GetExamplesParams): Promise<Example<I, O>[]>
}
```

**Implementations:**

**MemoryAdapter** (`/packages/zai/src/adapters/memory.ts`):

- In-memory storage, no persistence
- Returns all stored examples (no filtering)
- Useful for testing and development
- No status management or approval workflow

**TableAdapter** (`/packages/zai/src/adapters/botpress-table.ts:82-231`):

- Persistent storage via Botpress Tables
- Filters by status, taskType, and taskId
- Performs similarity search on input field (first 1024 chars)
- Auto-creates table with schema on first use
- Table configuration:
  - Factor: 30 (affects table performance)
  - Frozen: true (schema cannot be modified)
  - Searchable: input field only
  - Tags: `'x-studio-readonly': 'true'` (read-only in Studio)

#### 3.2 Active Learning Flow

When enabled (`/packages/zai/src/operations/extract.ts:362-383`):

```typescript
if (taskId && ctx.adapter && !ctx.controller.signal.aborted) {
  await ctx.adapter.saveExample({
    key: fastHash(JSON.stringify({ taskType, taskId, input, instructions })),
    taskId: `zai/${taskId}`,
    taskType,
    instructions,
    input: inputAsString,
    output: final,
    metadata: { cost, latency, model, tokens },
    status: 'pending', // Default - requires approval
  })
}
```

**Retrieval Process** (`/packages/zai/src/adapters/botpress-table.ts:96-124`):

```typescript
const { rows } = await this._client.findTableRows({
  table: this._tableName,
  search: JSON.stringify({ value: input }).substring(0, 1023),
  limit: 10,
  filter: {
    taskType,
    taskId,
    status: 'approved', // Only approved examples used!
  },
})
```

#### 3.3 Example Matching

Examples are retrieved and ranked by relevance:

1. **Exact key match**: Hash comparison, returns immediately without LLM call
2. **Similarity search**: Botpress Tables API handles similarity (likely embeddings)
3. **Token budget allocation**: Examples included up to token limit
4. **Prompt inclusion**: Up to 10 examples guide the LLM

### 4. Performance Optimization

#### 4.1 Token Management

**Tokenizer Integration** (`/packages/zai/src/zai.ts:125-134`):

```typescript
protected async getTokenizer() {
  Zai.tokenizer ??= await (async () => {
    while (!getWasmTokenizer) {
      await new Promise(resolve => setTimeout(resolve, 25))
    }
    return getWasmTokenizer() as TextTokenizer
  })()
  return Zai.tokenizer
}
```

**Budget Allocation**:

- Input: 50% of available tokens
- Condition/Instructions: 20%
- Examples: 30%

#### 4.2 Parallel Processing

Operations process chunks in parallel:

- Automatic detection of large inputs
- Concurrent chunk processing
- Result aggregation and merging

#### 4.3 Caching Strategy

1. **Model Details Cache**: Model capabilities cached per session
2. **Tokenizer Cache**: Single WASM instance shared
3. **Example Cache**: Active learning examples stored and reused
4. **Response Cache**: Cognitive layer handles HTTP caching

### 5. Error Recovery

#### 5.1 Retry Mechanism

Built into context generation (`/packages/zai/src/context.ts:117-169`):

```typescript
for (let attempt = 0; attempt <= maxRetries; attempt++) {
  try {
    const response = await this._client.generateContent({...})
    return { meta, output, text, extracted }
  } catch (error) {
    if (attempt === maxRetries) throw error

    messages.push({
      role: 'user',
      content: `ERROR: ${error.message}. Please fix and retry.`
    })
  }
}
```

#### 5.2 JSON Repair

For extract operations (`/packages/zai/src/operations/extract.ts:323-339`):

```typescript
try {
  const json = x.slice(0, x.indexOf(END)).trim()
  const repairedJson = jsonrepair(json) // Fix common JSON errors
  const parsedJson = JSON5.parse(repairedJson) // Flexible parsing
  const safe = schema.safeParse(parsedJson) // Validate

  if (safe.success) return safe.data
  if (options.strict) throw new JsonParsingError(x, safe.error)
  return parsedJson // Non-strict mode
} catch (error) {
  throw new JsonParsingError(x, error)
}
```

### 6. Model Management

#### 6.1 Model Selection

Models configured at initialization (`/packages/zai/src/zai.ts:50-68`):

```typescript
modelId: z.custom<ModelId | string>((value) => {
  if (typeof value !== 'string') return false
  if (value !== 'best' && value !== 'fast' && !value.includes(':')) {
    return false
  }
  return true
}).default('best')
```

Options:

- `'best'`: Highest quality model
- `'fast'`: Lower latency model
- Custom model IDs: `'openai:gpt-4-turbo'`

#### 6.2 Model Capabilities

Retrieved dynamically (`/packages/zai/src/zai.ts:136-140`):

```typescript
protected async fetchModelDetails(): Promise<void> {
  if (!this.ModelDetails) {
    this.ModelDetails = await this.client.getModelDetails(this.Model)
  }
}
```

Used for:

- Token limits
- Cost calculation
- Feature availability

## Part III: Troubleshooting

### Common Issues

#### 1. Token Limit Exceeded

**Problem**: Input too large for model
**Solution**: Adjust `chunkLength` parameter

```typescript
const result = await zai.extract(hugeDocument, schema, {
  chunkLength: 4000, // Smaller chunks
})
```

#### 2. Schema Validation Failures

**Problem**: Extracted data doesn't match schema
**Solution**: Use non-strict mode or improve instructions

```typescript
const result = await zai.extract(input, schema, {
  strict: false, // Allow partial matches
  instructions: 'If age is missing, use -1',
})
```

#### 3. Rate Limiting

**Problem**: Too many requests
**Solution**: Implement backoff or reduce concurrency

```typescript
// Stagger requests
for (const [i, doc] of documents.entries()) {
  await delay(i * 200) // 200ms between requests
  await zai.summarize(doc)
}
```

#### 4. Memory Issues with Large Documents

**Problem**: Out of memory with huge inputs
**Solution**: Process in streaming fashion

```typescript
// Split manually before processing
const chunks = splitIntoChunks(document, 10000)
const summaries = await Promise.all(chunks.map((chunk) => zai.summarize(chunk)))
const final = await zai.summarize(summaries.join('\n'))
```

### Performance Tuning

#### 1. Model Selection

- Use `'fast'` model for high-volume, low-complexity tasks
- Use `'best'` model for complex extraction or generation
- Specify exact model for consistency

#### 2. Chunk Size Optimization

- Smaller chunks (2-4k tokens): More parallel processing, potentially less context
- Larger chunks (8-16k tokens): Better context preservation, less parallelism
- Default (16k): Good balance for most use cases

#### 3. Active Learning

Enable for repetitive tasks:

```typescript
const zai = new Zai({
  client,
  activeLearning: {
    enable: true,
    tableName: 'ProductExtractionTable',
    taskId: 'product-catalog',
  },
})
```

Benefits:

- Reduced latency (cached exact matches)
- Improved accuracy (learns from examples)
- Lower costs (fewer API calls)

## Quick Reference

### Essential Methods

| Method        | Purpose                | Example                              |
| ------------- | ---------------------- | ------------------------------------ |
| `extract()`   | Get structured data    | `zai.extract(text, schema)`          |
| `check()`     | Verify conditions      | `zai.check(text, 'is positive')`     |
| `label()`     | Multi-classification   | `zai.label(text, criteria)`          |
| `rewrite()`   | Transform text         | `zai.rewrite(text, 'translate')`     |
| `filter()`    | Filter arrays          | `zai.filter(items, condition)`       |
| `text()`      | Generate content       | `zai.text(prompt, options)`          |
| `summarize()` | Create summaries       | `zai.summarize(document)`            |
| `answer()`    | Answer with citations  | `zai.answer(docs, question)`         |
| `rate()`      | Rate array items (1-5) | `zai.rate(items, criteria)`          |
| `sort()`      | Sort with natural lang | `zai.sort(items, instructions)`      |
| `group()`     | Group array elements   | `zai.group(items, { instructions })` |
| `patch()`     | Patch files with AI    | `zai.patch(files, instructions)`     |

### Configuration Options

| Option                     | Default                 | Description         |
| -------------------------- | ----------------------- | ------------------- |
| `modelId`                  | `'best'`                | Model selection     |
| `namespace`                | `'zai'`                 | Operation namespace |
| `activeLearning.enable`    | `false`                 | Enable learning     |
| `activeLearning.tableName` | `'ActiveLearningTable'` | Storage table       |
| `activeLearning.taskId`    | `'default'`             | Task identifier     |

### Token Limits

| Model Type | Input Tokens | Recommended Chunk Size |
| ---------- | ------------ | ---------------------- |
| Fast       | 8k           | 4000                   |
| Best       | 128k         | 16000                  |
| Custom     | Varies       | Model-specific         |

### Response Methods

| Method                        | Returns         | Usage                  |
| ----------------------------- | --------------- | ---------------------- |
| `await response`              | Simple result   | Quick access to result |
| `await response.full()`       | Detailed result | Includes explanations  |
| `await response.usage()`      | Usage stats     | Tokens, cost, latency  |
| `response.on('progress', fn)` | Event listener  | Track progress         |
| `response.abort()`            | void            | Cancel operation       |

### Error Types

| Error              | Cause               | Solution                     |
| ------------------ | ------------------- | ---------------------------- |
| `JsonParsingError` | Invalid JSON/schema | Check schema, use non-strict |
| `AbortError`       | Operation cancelled | Handle cancellation          |
| `Rate limit`       | Too many requests   | Implement backoff            |
| `Token limit`      | Input too large     | Reduce chunk size            |

### Active Learning States

| Status       | Used for Learning | Description                        |
| ------------ | ----------------- | ---------------------------------- |
| `'pending'`  | ❌ No             | Default status for new examples    |
| `'approved'` | ✅ Yes            | Manually approved, used in prompts |
| `'rejected'` | ❌ No             | Manually rejected, ignored         |

### Active Learning Flow

1. Generate hash key from input → Check exact match
2. If match found → Return cached result (skip LLM)
3. If no match → Search similar examples (max 10)
4. Include examples in prompt → Call LLM
5. Save result with `status: 'pending'`
6. Result needs external approval to be used in future

### Active Learning Configuration

| Setting     | Required | Description                     |
| ----------- | -------- | ------------------------------- |
| `enable`    | Yes      | Set to `true` to activate       |
| `tableName` | Yes      | Must end with "Table"           |
| `taskId`    | Yes      | Unique identifier for task type |

**Example Configuration:**

```typescript
{
  enable: true,
  tableName: 'SpamDetectionTable',  // Must end with "Table"
  taskId: 'email-spam'               // Becomes 'zai/email-spam'
}
```

## Summary

ZAI provides a production-ready, type-safe interface for AI operations with:

- **12 core operations** covering extraction, verification, generation, transformation, analysis, and code patching
- **Automatic handling** of documents of any size through intelligent chunking
- **Active learning** that improves accuracy over time
- **Full observability** with progress tracking and usage monitoring
- **Battle-tested** in production at Botpress, powering millions of AI interactions

The library abstracts complexity while maintaining flexibility, making it ideal for both simple prototypes and production systems requiring scale, reliability, and cost optimization.
