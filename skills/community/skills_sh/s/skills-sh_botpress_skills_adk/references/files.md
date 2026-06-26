# Files API

The Files API provides structured file storage with automatic indexing, semantic search capabilities, and CDN-backed content delivery.

## Accessing the Files API

All file operations use the Botpress client. Get the client using the Context API:

```typescript
import { context } from '@botpress/runtime'

const client = context.get('client')
```

This pattern is used in all examples below. See **[Context API](./context-api.md)** for more details.

## Basic Concepts

### What is the Files API?

- **Persistent storage**: Upload and manage files for your bot
- **Semantic search**: Optional vector indexing for searchable content
- **CDN delivery**: Fast file access through CloudFront
- **Access control**: Fine-grained permissions and policies
- **Metadata & tags**: Organize files with custom attributes

### File Properties

Files have the following core properties:

- **id**: Unique file identifier
- **key**: User-defined unique key per bot
- **url**: CDN URL for file content access
- **size**: File size in bytes
- **contentType**: MIME type (e.g., "application/pdf")
- **tags**: Key-value pairs for organization
- **metadata**: Custom JSON metadata
- **accessPolicies**: Array of access control policies
- **status**: Upload/indexing status
- **createdAt/updatedAt**: Timestamps

## Creating and Uploading Files

### Basic File Upload

```typescript
const { file } = await client.uploadFile({
  key: 'documents/report-2024.pdf', // Unique key
  content: fileBuffer, // File content (Buffer/ArrayBuffer/Blob/string)
  contentType: 'application/pdf', // MIME type
  tags: {
    category: 'reports',
    year: '2024',
  },
  index: true, // Enable semantic search
  accessPolicies: ['public_content'], // Make publicly accessible
})

console.log('File ID:', file.id)
console.log('File URL:', file.url)
```

### Upload Options

```typescript
await client.uploadFile({
  key: 'unique-file-key', // Required: Unique identifier
  content: fileBuffer, // Required: File content
  contentType: 'text/plain', // Optional: MIME type

  // Indexing options
  index: true, // Enable semantic search
  indexing: {
    configuration: {
      vision: {
        transcribePages: true, // OCR for images/PDFs
        indexPages: 'all', // Index all pages
      },
    },
  },

  // Access control
  accessPolicies: [
    'public_content', // Public URL access
    'integrations', // Integration access
  ],

  // Organization
  tags: {
    category: 'documents',
    department: 'sales',
  },

  // Custom metadata
  metadata: {
    author: 'John Doe',
    version: '1.0',
  },

  // Expiry (max 90 days)
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),

  // Immediate public access (requires public_content policy)
  publicContentImmediatelyAccessible: true,
})
```

### Uploading Text Content

For simple text/JSON content:

```typescript
const { file } = await client.uploadFile({
  key: 'config/settings.json',
  content: jsonContent, // String content
  contentType: 'application/json',
  index: false,
})
```

### Uploading from URL

To upload from an external URL:

```typescript
const { file } = await client.uploadFile({
  key: 'imported/image.jpg',
  url: 'https://example.com/image.jpg', // Fetch from URL
  contentType: 'image/jpeg',
  index: false,
})
```

## Retrieving Files

### Get File Metadata

```typescript
// Get by ID
const { file } = await client.getFile({
  id: 'file_abc123',
})

// Get by key
const { file } = await client.getFile({
  id: 'documents/report-2024.pdf', // Can use key as ID
})

console.log('File URL:', file.url)
console.log('File size:', file.size)
console.log('Status:', file.status)
```

### Access File Content

Files are accessed via URL. The URL type depends on access policies:

```typescript
const { file } = await client.getFile({ id: fileId })

// For public files: permanent CDN URL
// For private files: temporary presigned S3 URL

const response = await fetch(file.url)
const content = await response.text()

// For JSON files
const data = await response.json()

// For binary files
const buffer = await response.arrayBuffer()
```

### File Status States

```typescript
type FileStatus =
  | 'upload_pending' // Awaiting content upload
  | 'upload_completed' // Upload successful
  | 'upload_failed' // Upload failed
  | 'indexing_pending' // Queued for indexing
  | 'indexing_completed' // Indexed and searchable
  | 'indexing_failed' // Indexing failed

// Check file status
const { file } = await client.getFile({ id: fileId })
if (file.status === 'indexing_completed') {
  console.log('File is indexed and searchable')
}
```

## Listing Files

### Basic Listing

```typescript
const { files, meta } = await client.listFiles({
  limit: 20,
  offset: 0,
})

files.forEach((file) => {
  console.log(file.key, file.size, file.status)
})

// Pagination
if (meta.nextToken) {
  const nextPage = await client.listFiles({
    nextToken: meta.nextToken,
  })
}
```

### Filtering by Tags

```typescript
// Single tag filter
const { files } = await client.listFiles({
  tags: { category: 'reports' },
})

// Multiple values (OR condition)
const { files } = await client.listFiles({
  tags: {
    category: ['reports', 'documents'],
  },
})

// Exclude values
const { files } = await client.listFiles({
  tags: {
    category: {
      not: 'archived',
    },
  },
})
```

### Filtering by IDs

```typescript
const { files } = await client.listFiles({
  ids: ['file_123', 'file_456', 'file_789'],
})
```

### Sorting

```typescript
const { files } = await client.listFiles({
  sortBy: 'createdAt',
  sortOrder: 'desc',
  limit: 10,
})

// Available sort fields:
// - key
// - size
// - createdAt
// - updatedAt
// - status
```

## Semantic Search

### Searching File Content

```typescript
const { passages } = await client.searchFiles({
  query: 'machine learning algorithms',
  limit: 5,
})

passages.forEach((passage) => {
  console.log('File:', passage.file.key)
  console.log('Content:', passage.content)
  console.log('Similarity:', passage.score)
  console.log('Page:', passage.meta.pageNumber)
})
```

### Search Options

```typescript
const { passages } = await client.searchFiles({
  query: 'customer feedback',

  // Filtering
  tags: { category: 'support' },

  // Context
  contextDepth: 2, // Include 2 surrounding passages
  includeBreadcrumb: true, // Include document structure
  withContext: true, // Return detailed context

  // Consolidation
  consolidate: true, // Group by file, sort by position

  // Pagination
  limit: 10,
})
```

### Search Result Structure

```typescript
{
  passages: [
    {
      content: 'The matched text passage...',
      score: 0.89, // Similarity score (0-1)
      meta: {
        type: 'paragraph', // passage | title | subtitle | etc.
        subtype: 'text',
        pageNumber: 5,
        position: 12,
        sourceUrl: 'https://...',
      },
      file: {
        id: 'file_abc123',
        key: 'documents/report.pdf',
        contentType: 'application/pdf',
        tags: { category: 'reports' },
        createdAt: '2024-01-15T10:30:00Z',
        updatedAt: '2024-01-15T10:30:00Z',
      },
      context: [
        // Only if withContext: true
        {
          type: 'preceding',
          content: 'Previous passage...',
        },
        {
          type: 'current',
          content: 'The matched text passage...',
        },
        {
          type: 'subsequent',
          content: 'Next passage...',
        },
      ],
    },
  ]
}
```

## Updating Files

### Update File Metadata

```typescript
// Update without changing content
const { file } = await client.updateFileMetadata({
  id: fileId,

  metadata: {
    version: '2.0',
    updatedBy: 'Jane Doe',
  },

  tags: {
    status: 'reviewed',
    newTag: 'value',
  },

  accessPolicies: ['public_content'],

  expiresAt: new Date('2024-12-31').toISOString(),
})
```

### Metadata Update Behavior

```typescript
// Partial updates - existing keys preserved
await client.updateFileMetadata({
  id: fileId,
  metadata: {
    newKey: 'newValue',
    // Other metadata keys remain unchanged
  },
})

// Delete metadata key
await client.updateFileMetadata({
  id: fileId,
  metadata: {
    oldKey: null, // Removes this key
  },
})

// Delete tag
await client.updateFileMetadata({
  id: fileId,
  tags: {
    oldTag: null, // Removes this tag
  },
})
```

### Replace File Content

```typescript
// Upload new content with same key (replaces old content)
const { file } = await client.uploadFile({
  key: existingFileKey,
  content: newContent,
  contentType: 'text/plain',
})
```

## Managing File Passages

### List File Passages

```typescript
const { passages, meta } = await client.listFilePassages({
  id: fileId,
  limit: 20,
})

passages.forEach((passage) => {
  console.log('Passage ID:', passage.id)
  console.log('Content:', passage.content)
  console.log('Type:', passage.meta.type)
  console.log('Page:', passage.meta.pageNumber)
})
```

### Set Custom Passages

```typescript
// Replace all passages with custom content
await client.setFilePassages({
  id: fileId,
  passages: [
    {
      content: '# Introduction\n\nThis is the first section...',
      type: 'title',
    },
    {
      content: 'Main content paragraph here.',
      type: 'paragraph',
      pageNumber: 1,
    },
    {
      content: '## Subsection\n\nMore details...',
      type: 'subtitle',
    },
  ],
})

// File status becomes "indexing_pending"
// Check status later to confirm completion
```

## Deleting Files

### Delete Single File

```typescript
// Delete by ID
await client.deleteFile({ id: 'file_abc123' })

// Delete by key
await client.deleteFile({ id: 'documents/report.pdf' })
```

### Cleanup

When a file is deleted:

- File metadata removed from database
- File content removed from S3
- Vector embeddings removed (if indexed)
- All passages deleted

## Knowledge Bases

For high-level RAG implementation with automatic indexing and search integration, see **[Knowledge Bases](./knowledge-bases.md)**.

The Files API provides low-level file management. Knowledge Bases use the Files API internally but provide a simpler interface for document indexing and semantic search in AI responses.

## Copying Files

### Copy Within Bot

```typescript
const { file } = await client.copyFile({
  idOrKey: sourceFileId,
  destinationKey: 'backups/report-copy.pdf',
  overwrite: false, // Fail if destination exists
})
```

### Copy Across Bots

```typescript
const { file } = await client.copyFile({
  idOrKey: sourceFileId,
  destinationKey: 'imported/report.pdf',
  destinationBotId: targetBotId,
  overwrite: true,
})
```

## Supported File Types

### Indexable Formats

These file types support semantic search indexing:

```typescript
const INDEXABLE_TYPES = {
  // Documents
  pdf: 'application/pdf',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

  // Text
  txt: 'text/plain',
  md: 'text/markdown',
  html: 'text/html',

  // Images (with vision processing)
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  png: 'image/png',
}
```

### Vision Processing

For images and PDFs with vision enabled:

```typescript
await client.uploadFile({
  key: 'documents/invoice.pdf',
  content: pdfBuffer,
  contentType: 'application/pdf',
  index: true,
  indexing: {
    configuration: {
      vision: {
        transcribePages: true, // OCR text extraction
        indexPages: 'all', // or [1, 2, 3] for specific pages
      },
    },
  },
})
```

## Usage in Actions/Workflows

### In Actions

```typescript
import { Action, z, context } from '@botpress/runtime'

export const uploadDocument = new Action({
  name: 'uploadDocument',
  input: z.object({
    content: z.string(),
    filename: z.string(),
  }),
  output: z.object({
    fileId: z.string(),
    fileUrl: z.string(),
  }),

  async handler({ input }) {
    const client = context.get('client')

    // Upload file
    const { file } = await client.uploadFile({
      key: `uploads/${input.filename}`,
      content: input.content,
      contentType: 'text/plain',
      index: true,
      tags: {
        source: 'action',
        type: 'user-upload',
      },
    })

    return {
      fileId: file.id,
      fileUrl: file.url,
    }
  },
})
```

### In Workflows

```typescript
import { Workflow, z, context } from '@botpress/runtime'

export const ProcessDocumentWorkflow = new Workflow({
  name: 'processDocument',
  input: z.object({ documentKey: z.string() }),

  async handler({ input, step }) {
    const client = context.get('client')

    // Get file
    const file = await step('get-file', async () => {
      const { file } = await client.getFile({
        id: input.documentKey,
      })
      return file
    })

    // Wait for indexing
    await step('wait-indexing', async () => {
      let status = file.status
      while (status === 'INDEXING_PENDING') {
        await new Promise((resolve) => setTimeout(resolve, 1000))
        const { file: updated } = await client.getFile({
          id: file.id,
        })
        status = updated.status
      }
      return status
    })

    // Search content
    const results = await step('search', async () => {
      const { passages } = await client.searchFiles({
        query: 'important findings',
        tags: { key: input.documentKey },
      })
      return passages
    })

    return {
      processed: true,
      findings: results.length,
    }
  },
})
```

## Best Practices

### 1. Use Meaningful Keys

```typescript
// ✅ Good - Clear, hierarchical structure
await client.uploadFile({
  key: 'documents/2024/reports/q1-sales.pdf',
})

// ❌ Bad - Unclear, no structure
await client.uploadFile({
  key: 'file123.pdf',
})
```

### 2. Tag Appropriately

```typescript
// ✅ Good - Useful, queryable tags
tags: {
  category: "reports",
  year: "2024",
  quarter: "Q1",
  department: "sales"
}

// ❌ Bad - Too specific or redundant
tags: {
  filename: "q1-sales.pdf",  // Already in key
  timestamp: "1234567890"     // Use createdAt instead
}
```

### 3. Handle File Status

```typescript
// ✅ Good - Check and handle status
const { file } = await client.getFile({ id: fileId })

switch (file.status) {
  case 'UPLOAD_PENDING':
    console.log('Waiting for upload...')
    break
  case 'INDEXING_PENDING':
    console.log('Indexing in progress...')
    break
  case 'INDEXING_COMPLETED':
    // File is searchable
    break
  case 'INDEXING_FAILED':
    console.error('Indexing failed:', file.failedStatusReason)
    break
}
```

### 4. Set Appropriate Expiry

```typescript
// ✅ Good - Reasonable expiry for temporary files
await client.uploadFile({
  key: 'temp/cache-data.json',
  expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 1 day
})

// For permanent files, omit expiresAt
await client.uploadFile({
  key: 'documents/permanent-record.pdf',
  // No expiresAt = never expires
})
```

### 5. Optimize Indexing

```typescript
// ✅ Good - Index only searchable content
await client.uploadFile({
  key: 'documents/report.pdf',
  content: pdfBuffer,
  index: true, // Searchable document
})

await client.uploadFile({
  key: 'images/logo.png',
  content: imageBuffer,
  index: false, // Not searchable, save quota
})

// ✅ Good - Use vision only when needed
await client.uploadFile({
  key: 'documents/scanned-invoice.pdf',
  content: pdfBuffer,
  index: true,
  indexing: {
    configuration: {
      vision: {
        transcribePages: true, // OCR needed
      },
    },
  },
})
```

## Common Patterns

### File Upload with Validation

```typescript
export const uploadWithValidation = async (fileContent: Buffer, filename: string) => {
  const client = context.get('client')

  // Validate file size (max 100MB)
  const MAX_SIZE = 100 * 1024 * 1024
  if (fileContent.length > MAX_SIZE) {
    throw new Error('File too large')
  }

  // Validate file type
  const contentType = getContentType(filename)
  if (!ALLOWED_TYPES.includes(contentType)) {
    throw new Error('File type not allowed')
  }

  // Upload
  const { file } = await client.uploadFile({
    key: `uploads/${Date.now()}-${filename}`,
    content: fileContent,
    contentType,
    index: true,
    tags: {
      originalName: filename,
      uploadedAt: new Date().toISOString(),
    },
  })

  return file
}
```

### Search with Context

```typescript
export const searchWithContext = async (query: string, category?: string) => {
  const client = context.get('client')

  const { passages } = await client.searchFiles({
    query,
    tags: category ? { category } : undefined,
    contextDepth: 2,
    includeBreadcrumb: true,
    limit: 5,
  })

  return passages.map((p) => ({
    content: p.content,
    source: p.file.key,
    relevance: p.score,
    location: `Page ${p.meta.pageNumber || 'N/A'}`,
  }))
}
```

### Bulk File Operations

```typescript
export const bulkUpload = async (files: FileData[]) => {
  const client = context.get('client')

  const results = await Promise.allSettled(
    files.map(async (fileData) => {
      const { file } = await client.uploadFile({
        key: fileData.key,
        content: fileData.content,
        contentType: fileData.contentType,
        index: true,
      })

      return file
    })
  )

  const successful = results.filter((r) => r.status === 'fulfilled').map((r) => r.value)

  const failed = results.filter((r) => r.status === 'rejected').map((r) => r.reason)

  return { successful, failed }
}
```

## Troubleshooting

### Common Issues

1. **Upload fails with 403 error**
   - Ensure you have proper access policies set
   - Check that the bot token has file upload permissions
   - Verify the file size is within limits

2. **File not searchable**
   - Check `file.status` is `INDEXING_COMPLETED`
   - Verify `index: true` was set during upload
   - Ensure file type is in supported indexable formats
   - Check billing plan supports indexing features

3. **Search returns no results**
   - Verify files are indexed (`status: "INDEXING_COMPLETED"`)
   - Check tag filters aren't too restrictive
   - Try broader search queries
   - Ensure files have searchable content

4. **File access denied**
   - Verify access policies are correctly set
   - Check workspace member permissions
   - For integration files, ensure proper namespace

5. **Quota exceeded**
   - Check storage usage in workspace settings
   - Delete unused files or increase quota
   - Consider file expiry policies for temporary files

## Limits and Quotas

- **Maximum file size**: 100 MB
- **Maximum expiry**: 90 days from upload
- **Maximum tags per file**: 50
- **Maximum indexable file size**: varies by file type
- **Search result limit**: Configurable, recommended max 100

## Migration Notes

### Current API (ADK 1.13+)

The current Files API uses direct content upload:

```typescript
// ✅ CURRENT - Direct content parameter
await client.uploadFile({
  key: 'unique-key',
  content: fileBuffer, // Direct upload
  contentType: 'application/pdf',
  tags: { category: 'docs' },
})

// Alternative: Upload from URL
await client.uploadFile({
  key: 'unique-key',
  url: 'https://example.com/file.pdf', // Fetch from URL
  tags: { category: 'docs' },
})
```

### Retrieving File Content

Files are accessed via their URL:

```typescript
const { file } = await client.getFile({ id: fileId })

// Fetch file content
const response = await fetch(file.url)
const content = await response.arrayBuffer()

// For text/JSON
const text = await response.text()
const json = await response.json()
```

**URL Types:**

- **Public files** (`public_content` policy): Permanent CDN URL
- **Private files**: Temporary presigned URL (use shortly after retrieval)
