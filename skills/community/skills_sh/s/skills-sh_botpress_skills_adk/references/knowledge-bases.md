# Knowledge Bases

Knowledge Bases enable RAG (Retrieval Augmented Generation) by indexing documents, websites, and structured data for semantic search and AI-powered responses.

## Basic Concepts

### What are Knowledge Bases?

- **RAG implementation**: Enhance AI responses with relevant context
- **Multiple sources**: Index local files, websites, or table data
- **Semantic search**: Find relevant information based on meaning
- **Auto-chunking**: Documents are automatically split for optimal retrieval

### File Location

- **Location**: `src/knowledge/*.ts`
- **Auto-registration**: Knowledge bases are automatically available to AI

## Creating Knowledge Bases

### Basic Structure

```typescript
import { Knowledge, DataSource } from '@botpress/runtime'

// Define a data source
const docsSource = DataSource.Directory.fromPath('src/knowledge/docs', {
  id: 'docs',
  filter: (path) => path.endsWith('.md') || path.endsWith('.pdf'),
})

// Create knowledge base
export const DocsKnowledgeBase = new Knowledge({
  name: 'docsKB',
  description: 'Documentation knowledge base',
  sources: [docsSource],
})
```

## Data Source Types

### 1. Local Files (Directory)

Index local markdown, PDF, and text files:

```typescript
const docsSource = DataSource.Directory.fromPath('src/knowledge', {
  id: 'docs',

  // Filter specific file types
  filter: (path) => {
    return path.endsWith('.md') || path.endsWith('.pdf') || path.endsWith('.txt')
  },
})
```

**Note**: Local file sources are for development only and won't work in production.

### 2. Website Crawling

Index websites via sitemap or direct URLs:

```typescript
// From sitemap
const websiteSource = DataSource.Website.fromSitemap('https://docs.example.com/sitemap.xml', {
  id: 'website',
  maxPages: 500, // Maximum pages to crawl (1-50000)
  maxDepth: 3, // Maximum crawl depth (1-20)
  fetch: 'node:fetch', // Optional: 'node:fetch' or 'integration:browser'

  // Filter pages
  filter: (context) => {
    // Skip archive pages
    if (context.url.includes('/archive/')) {
      return false
    }
    // Only include documentation pages
    return context.url.includes('/docs/')
  },
})

// From direct URLs
const urlsSource = DataSource.Website.fromUrls(
  ['https://example.com/page1', 'https://example.com/page2', 'https://example.com/page3'],
  {
    id: 'specific_pages',
  }
)

// From llms.txt (AI-friendly site manifest)
const llmsTxtSource = DataSource.Website.fromLlmsTxt('https://example.com/llms.txt', {
  id: 'llms_txt',
  maxPages: 100,
})
```

### 3. Table-Based

Table-backed knowledge sources are not fully implemented yet. The shape below is useful as a forward-looking pattern, but today you should treat it as experimental and prefer directory- or website-backed sources for production workflows.

```typescript
import { FAQTable } from '../tables/FAQ'

const tableSource = DataSource.Table.fromTable(FAQTable, {
  id: 'faq_kb',

  // Transform row data into searchable text
  transform: ({ row }) => {
    return `Question: ${row.question}

Answer: ${row.answer}

Category: ${row.category}
Tags: ${row.tags.join(', ')}`
  },

  // Optional: Filter rows
  filter: ({ row }) => {
    return row.published === true
  },
})
```

### 4. Multiple Sources

Combine different source types:

```typescript
export const CombinedKnowledgeBase = new Knowledge({
  name: 'combinedKB',
  description: 'Knowledge from multiple sources',
  sources: [
    // Local documentation
    DataSource.Directory.fromPath('src/knowledge/docs', {
      id: 'local_docs',
    }),

    // Website documentation
    DataSource.Website.fromSitemap('https://docs.example.com/sitemap.xml', {
      id: 'online_docs',
      maxPages: 100,
    }),

    // FAQ from database
    DataSource.Table.fromTable(FAQTable, {
      id: 'faq',
      transform: ({ row }) => `Q: ${row.question}\nA: ${row.answer}`,
    }),
  ],
})
```

## Using Knowledge Bases

### In Conversations

Provide knowledge bases to AI during execution:

```typescript
import { Conversation } from '@botpress/runtime'
import { DocsKnowledgeBase, FAQKnowledgeBase } from '../knowledge'

export const Chat = new Conversation({
  channel: 'chat.channel',

  async handler({ execute }) {
    await execute({
      instructions: 'You are a helpful assistant. Use the provided knowledge to answer questions accurately.',

      // Add knowledge bases
      knowledge: [DocsKnowledgeBase, FAQKnowledgeBase],

      // Optional: Add tools that can search knowledge
      tools: [searchTool],
    })
  },
})
```

### In Workflows

Knowledge bases work the same in workflows:

```typescript
import { Workflow } from '@botpress/runtime'
import { DocsKnowledgeBase } from '../knowledge'

export const ResearchWorkflow = new Workflow({
  name: 'research',

  handler: async ({ input, execute }) => {
    const result = await execute({
      instructions: `Research the topic: ${input.topic}`,
      knowledge: [DocsKnowledgeBase],
      model: 'openai:gpt-4o',
    })

    return { research: result }
  },
})
```

### Manual Search

Search knowledge bases programmatically:

```typescript
import { context } from '@botpress/runtime'
import { DocsKnowledgeBase } from '../knowledge'

export const searchAction = new Action({
  name: 'searchDocs',
  input: z.object({ query: z.string() }),

  async handler({ input }) {
    const client = context.get('client')

    // Search knowledge base
    const { passages } = await client.searchFiles({
      query: input.query,
      tags: {
        source: 'knowledge-base',
        kbName: [DocsKnowledgeBase.name],
      },
      limit: 5,
    })

    return {
      results: passages.map((p) => ({
        content: p.content,
        score: p.score,
        source: p.file.key,
      })),
    }
  },
})
```

## Syncing Knowledge Bases

As of ADK 1.9+, knowledge bases are synced using the `adk kb` command, which runs automatically during `adk dev` and `adk deploy`.

### CLI Sync (Recommended)

```bash
# Interactive KB management
adk kb

# Non-interactive sync (dev; use --prod for production)
adk kb sync --dev -y

# Force a full re-sync, ignoring change detection
adk kb sync --dev --force -y
```

The KB sync:

1. Detects all knowledge bases in your project
2. Identifies sources (directories, websites, tables)
3. Computes file hashes to detect changes
4. Syncs only changed content to Botpress Cloud
5. Handles orphaned sources (sources removed from code)

### Automatic Sync

KB sync runs automatically during:

- `adk dev` - Syncs on startup and file changes
- `adk deploy` - Syncs before deployment

## Refreshing Knowledge Bases

Refresh knowledge bases programmatically:

```typescript
// Smart refresh - only changed files (uses SHA256 hashing)
await MyKnowledgeBase.refresh()

// Force refresh - re-indexes everything
await MyKnowledgeBase.refresh({ force: true })

// Refresh specific source
await MyKnowledgeBase.refreshSource('docs')
```

For scheduled or triggered refresh, use the same refresh methods in workflows, actions, or conversation handlers.

## Citations and References

Track knowledge sources used in responses:

```typescript
const citations = context.get('citations')

// Register source when using knowledge passage
const { tag } = citations.registerSource({
  file: passage.file.key,
  title: passage.file.tags.title,
  url: passage.file.tags.url,
})

// Include citation tag in content
const citedContent = `<${tag}>${passage.content}</${tag}>`
```

For complete citation implementation examples, see the autonomous execution documentation.

## Advanced Patterns

### Dynamic Knowledge Sources

Select knowledge bases based on user context:

```typescript
// Select knowledge based on user department
const knowledgeBases = [GeneralKB]

if (user.department === 'engineering') {
  knowledgeBases.push(EngineeringKB, TechnicalDocsKB)
} else if (user.department === 'sales') {
  knowledgeBases.push(SalesKB, ProductKB)
}

// Pass to execute()
await execute({
  instructions: 'Answer based on department-specific knowledge',
  knowledge: knowledgeBases,
})
```

### Content Transformation

Enhance content with metadata before indexing (Table and Website sources support transform):

```typescript
// Table source with transformation
const docsTableSource = DataSource.Table.fromTable(DocsTable, {
  id: 'docs_table',

  // Filter specific rows
  filter: ({ row }) => {
    return row.status === 'published' && !row.deprecated
  },

  // Transform row data into searchable text with metadata
  transform: ({ row }) => {
    return `
Title: ${row.title}
Category: ${row.category}
Tags: ${row.tags.join(', ')}
Author: ${row.author}

${row.content}`
  },
})
```

**Note**: Directory sources only support `filter`, not `transform`. Use Table or Website sources for content transformation.

### Multi-Language Support

Create separate knowledge bases per language:

```typescript
export const EnglishKB = new Knowledge({
  name: 'englishKB',
  sources: [DataSource.Directory.fromPath('src/knowledge/en', { id: 'docs_en' })],
})

export const SpanishKB = new Knowledge({
  name: 'spanishKB',
  sources: [DataSource.Directory.fromPath('src/knowledge/es', { id: 'docs_es' })],
})

// Select based on user language
const kb = userLanguage === 'es' ? SpanishKB : EnglishKB
```

## Best Practices

### 1. Organize Content Logically

```
src/knowledge/
├── docs/
│   ├── getting-started/
│   ├── api-reference/
│   └── tutorials/
├── policies/
│   ├── privacy.md
│   └── terms.md
└── faqs/
    ├── technical.md
    └── billing.md
```

### 2. Use Clear Naming

```typescript
// ✅ Good
export const TechnicalDocsKB = new Knowledge({ name: 'technicalDocs' })
export const CustomerFAQKB = new Knowledge({ name: 'customerFAQ' })

// ❌ Bad
export const KB1 = new Knowledge({ name: 'kb1' })
export const Stuff = new Knowledge({ name: 'stuff' })
```

### 3. Refresh Frequently-Changing Content

Use `adk kb sync` during development, or call `refresh()` programmatically for dynamic content.

### 4. Structure Content for Search

Add summaries, keywords, and clear headings to improve retrieval quality.

### 5. Monitor Search Performance

Track search metrics (query, result count, duration) to identify slow queries or poor results.

## Troubleshooting

### Common Issues

1. **Knowledge not found by AI**
   - Verify knowledge base is included in `execute()` call
   - Check that content has been indexed (`refresh()`)
   - Ensure file types are supported

2. **Poor search results**
   - Review content structure and formatting
   - Add metadata and keywords
   - Adjust the `factor` parameter for ranking

3. **Refresh not working**
   - Check file permissions
   - Verify source paths are correct
   - Look for errors in transform functions

4. **Large files causing issues**
   - Files are automatically chunked, but very large files may need manual splitting
   - Consider breaking into smaller documents
   - Use filtering to exclude unnecessary content
