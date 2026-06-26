# ZAI Reference for AI Agents

ZAI is pre-configured in your ADK environment. Use `adk.zai.*` to access LLM operations with automatic type safety. Import `adk` from `@botpress/runtime`.

## Core Operations

### `zai.extract(input, schema)`

Extract structured data from any input using Zod schema. Auto-handles large documents via chunking.

```typescript
await zai.extract('John is 30', z.object({ name: z.string(), age: z.number() }))
// → { name: 'John', age: 30 }

await zai.extract(emails, z.array(z.object({ from: z.string(), subject: z.string() })))
// → [{ from: 'alice@example.com', subject: 'Meeting' }, ...]
```

### `zai.check(input, condition)`

Boolean verification using natural language.

```typescript
await zai.check('Buy cheap pills!', 'is spam') // → true
await zai.check(code, 'contains SQL injection vulnerability') // → boolean
```

### `zai.label(input, criteria)`

Apply multiple boolean labels simultaneously.

```typescript
await zai.label(customerEmail, {
  spam: 'is spam',
  urgent: 'requires immediate response',
  complaint: 'expresses dissatisfaction',
})
// → { spam: false, urgent: true, complaint: true }
```

### `zai.rewrite(input, instruction)`

Transform text per instruction.

```typescript
await zai.rewrite('hey wassup', 'make professional') // → 'Hello, how are you?'
await zai.rewrite(html, 'convert to markdown')
await zai.rewrite(text, 'translate to French')
```

### `zai.filter(array, condition)`

Filter arrays with natural language.

```typescript
await zai.filter(users, 'have purchased in last 30 days')
await zai.filter([1, 2, 3, 4, 5], 'are prime numbers') // → [2,3,5]
```

### `zai.text(prompt)`

Generate text from prompt.

```typescript
await zai.text('Write a regex for email validation')
await zai.text('SQL query to find duplicate records')
```

### `zai.summarize(input)`

Create intelligent summary. Handles any size via auto-chunking.

```typescript
await zai.summarize(longDocument)
await zai.summarize(chatHistory, {
  length: 200,
  prompt: 'focus on decisions made',
})
```

### `zai.answer(documents, question)`

Answer questions from documents with citations and intelligent edge case handling. Returns different response types based on question quality and available information.

```typescript
const docs = [
  'Botpress was founded in 2016.',
  'The company is based in Quebec, Canada.',
  'Botpress provides an AI agent platform.',
]

const result = await zai.answer(docs, 'When was Botpress founded?')
if (result.type === 'answer') {
  console.log(result.answer) // "Botpress was founded in 2016."
  console.log(result.citations) // [{ offset: 30, item: docs[0], snippet: '...' }]
}

// Handle different response types
switch (result.type) {
  case 'answer': // Has answer and citations
  case 'ambiguous': // Multiple interpretations, has follow_up question
  case 'out_of_topic': // Question unrelated to documents
  case 'invalid_question': // Malformed or unclear question
  case 'missing_knowledge': // Insufficient information
}
```

### `zai.rate(items, instructions)`

Rate array items on a 1-5 scale. Returns single score or multiple criteria scores.

```typescript
// Single criterion (returns number 1-5)
await zai.rate(customerEmails, 'urgency level')
// → [4, 2, 5, 1, 3]

// Multiple criteria (returns scores object)
await zai.rate(products, {
  quality: 'product build quality',
  value: 'price to performance ratio',
  design: 'aesthetic appeal',
})
// → [{ quality: 5, value: 4, design: 5, total: 14 }, ...]
```

### `zai.sort(items, instructions)`

Sort array based on natural language instructions.

```typescript
await zai.sort(tickets, 'from least urgent to most urgent')
await zai.sort(products, 'by price, cheapest first')
await zai.sort(emails, 'prioritize: open old items highest')
// Returns sorted array directly
```

### `zai.group(items, options)`

Group array elements based on natural language criteria.

```typescript
await zai.group(tickets, {
  instructions: 'group by issue type and priority',
})
// → [
//   { id: 'bugs', label: 'Bug Reports', elements: [...] },
//   { id: 'features', label: 'Feature Requests', elements: [...] }
// ]

// With initial groups
await zai.group(emails, {
  instructions: 'categorize emails',
  initialGroups: [
    { id: 'urgent', label: 'Urgent' },
    { id: 'spam', label: 'Spam' },
  ],
})
```

### `zai.patch(files, instructions)`

Patch code files using natural language instructions. Uses efficient micropatch protocol.

```typescript
const files = [
  {
    path: 'src/hello.ts',
    name: 'hello.ts',
    content: 'console.log("Hello World")',
  },
]

const patched = await zai.patch(files, 'change message to "Hi World"')
// → [{ path: 'src/hello.ts', content: 'console.log("Hi World")', patch: '...' }]

// Works with multiple files
await zai.patch(files, 'add JSDoc comments to all functions')
await zai.patch(files, 'remove all debug code')
await zai.patch(files, 'update version to 2.0.0 in all config files')
```

## Advanced Usage

### `zai.with(options)`

Create a new instance with modified configuration.

```typescript
const creativeZai = zai.with({ temperature: 0.9 })
const fastZai = zai.with({ modelId: 'fast' })
const preciseZai = zai.with({ modelId: 'best' }).learn('extraction-task')
```

### `zai.learn(taskId)`

Enable learning for repetitive tasks. Caches exact matches, uses approved examples.

```typescript
const smartZai = zai.learn('invoice-parsing')
await smartZai.extract(invoice, invoiceSchema) // Learns patterns over time
```

### Response Methods

All operations return a Response object:

```typescript
const result = await zai.check(text, 'is positive') // Simple boolean
const { value, explanation } = await result.full() // Detailed result
const { tokens, cost } = await result.usage() // Usage metrics
```

### Options (all operations)

```typescript
await zai.extract(input, schema, {
  instructions: 'Focus on financial data only',
  strict: false, // Allow partial matches
  chunkLength: 8000, // For large docs
})
```

## Quick Patterns

```typescript
// Validate and extract
if (await zai.check(input, 'is valid JSON')) {
  const data = await zai.extract(input, schema)
}

// Multi-step processing
const clean = await zai.rewrite(userInput, 'remove profanity')
const translated = await zai.rewrite(clean, 'translate to Spanish')

// Conditional filtering
const urgentTickets = await zai.filter(tickets, 'require response within 1 hour')

// Smart extraction with learning
const parser = zai.learn('resume-parser')
const candidate = await parser.extract(resume, candidateSchema)

// Question answering with citations
const result = await zai.answer(knowledgeBase, userQuestion)
if (result.type === 'answer') {
  return { answer: result.answer, sources: result.citations }
}

// Rate and sort workflow
const rated = await zai.rate(items, 'quality score')
const sorted = await zai.sort(items, 'by quality, best first')

// Group and process
const groups = await zai.group(tickets, {
  instructions: 'by priority and category',
})
for (const group of groups) {
  await processGroup(group.label, group.elements)
}

// Automated code modifications
const updatedFiles = await zai.patch(sourceFiles, 'add TypeScript types')
```

## Everyday Problems Zai Solves

### Parsing Unstructured Input into Structured Data

A user sends "I'm Jane, I work at Acme Corp, my email is jane@acme.com and I need help with billing". Instead of regex or manual parsing:

```typescript
const contact = await zai.extract(
  message,
  z.object({
    name: z.string(),
    company: z.string(),
    email: z.string(),
    topic: z.string(),
  })
)
// → { name: 'Jane', company: 'Acme Corp', email: 'jane@acme.com', topic: 'billing' }
```

### Triaging Support Messages

Incoming messages need routing to the right team without building a classifier from scratch:

```typescript
const triage = await zai.label(message, {
  urgent: 'needs response within 1 hour',
  billing: 'related to payments or invoices',
  technical: 'related to bugs or technical issues',
  churn_risk: 'user is frustrated or threatening to leave',
})
// → { urgent: true, billing: true, technical: false, churn_risk: true }
```

### Making User Content Presentable

User-generated text needs to go into a report or external system:

```typescript
const cleaned = await zai.rewrite(userMessage, 'fix grammar and spelling, keep the meaning')
const translated = await zai.rewrite(userMessage, 'translate to French, keep a professional tone')
```

### Answering Questions from a Knowledge Base

A user asks a question and you have docs to search through — but you need citations and graceful handling when the answer isn't there:

```typescript
const result = await zai.answer(kbDocuments, userQuestion)
if (result.type === 'answer') {
  return `${result.answer}\n\nSources: ${result.citations.map((c) => c.snippet).join(', ')}`
} else if (result.type === 'missing_knowledge') {
  return "I don't have enough information to answer that. Let me connect you with a human."
}
```

### Prioritizing a Queue

A support queue has 50 tickets and the agent needs to work the most urgent ones first:

```typescript
// Score tickets, then sort by those scores
const scored = await zai.rate(tickets, 'customer impact and time sensitivity')
// scored: [4, 2, 5, 1, 3] — one score per ticket

// Or sort directly when you only need ordering
const sorted = await zai.sort(tickets, 'most urgent and highest impact first')
```

### Pre-screening Before Human Review

Filter out irrelevant items before a human sees them:

```typescript
const relevant = await zai.filter(applications, 'meet minimum requirements: 3+ years experience, relevant degree')
```

### Summarizing Long Conversations for Handoff

A conversation has been going for 30 messages and needs to be handed to a human agent:

```typescript
const summary = await zai.summarize(conversationHistory, {
  prompt: "focus on the customer's problem, what has been tried, and current status",
  length: 200,
})
```

### Grouping Feedback for Product Review

Hundreds of user feedback messages need to be organized into themes:

```typescript
const themes = await zai.group(feedbackMessages, {
  instructions: 'group by product area and sentiment',
})
// → [{ id: 'onboarding', label: 'Onboarding Issues', elements: [...] }, ...]
```

## Edge Cases & Gotchas

### Ambiguous Input

When `check()` gives inconsistent results on borderline inputs, add examples to guide it:

```typescript
await zai.check(text, 'is a complaint', {
  examples: [
    { input: 'This is taking too long', check: true, reason: 'Expresses frustration with wait time' },
    { input: 'How long does shipping take?', check: false, reason: 'Neutral question, not a complaint' },
  ],
})
```

### Very Large Documents

Zai auto-chunks, but default `chunkLength` (16000 tokens) may lose context across chunks. For documents where cross-chunk context matters (e.g., a contract where definitions appear at the top):

```typescript
await zai.extract(contract, schema, {
  chunkLength: 32000, // Larger chunks to keep definitions in context
  instructions: "Definitions from the 'Definitions' section apply throughout",
})
```

### extract() Returns Hallucinated Fields

When the input doesn't contain the requested data, the LLM may invent values. Use `.describe()` on schema fields and strict mode:

```typescript
const data = await zai.extract(
  text,
  z.object({
    revenue: z.number().describe('Annual revenue in USD. Use -1 if not mentioned.'),
    founded: z.number().describe('Year founded. Use 0 if not mentioned.'),
  }),
  { strict: true }
)
```

### answer() Returns "missing_knowledge" Despite Relevant Docs

This usually means the docs are too long and the relevant passage fell outside the chunk window, or the question phrasing doesn't match the document language. Reduce chunk size and add instructions:

```typescript
await zai.answer(docs, question, {
  chunkLength: 4000,
  instructions: 'The documents use technical terminology. Match concepts, not exact wording.',
})
```

### Mixed-Language Content

Zai handles multilingual input natively — no special config needed. But be explicit when you want output in a specific language:

```typescript
await zai.extract(mixedLanguageText, schema, {
  instructions: 'Input may be in any language. Always return field values in English.',
})
```

### Empty or Minimal Input

Zai doesn't error on empty strings but results will be empty/default. Guard at the call site:

```typescript
if (input.trim().length > 0) {
  const result = await zai.extract(input, schema)
}
```

### Rate Limiting Under Load

When processing batches, stagger requests to avoid hitting API limits:

```typescript
const results = []
for (const [i, item] of items.entries()) {
  if (i > 0) await new Promise((r) => setTimeout(r, 200))
  results.push(await zai.extract(item, schema))
}
```

## Notes

- All operations handle any input size via automatic chunking
- `.learn()` creates persistent cache - use unique taskIds
- Exact input matches skip LLM entirely when using `.learn()`
- All methods are async - use `await`
- For the full developer guide including architecture, storage, and performance tuning, see [zai-complete-guide.md](./zai-complete-guide.md)
