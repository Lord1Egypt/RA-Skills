# Tables

Tables provide structured data storage with automatic schema management, CRUD operations, and optional semantic search capabilities.

> **Use `state`, not a Table, for simple memory.** For per-user or per-bot values (names, preferences, counters), use `user.state` / `bot.state` (see [Context API](./context-api.md)). Reach for a Table only for collections of rows you list, query, or search.

## Basic Concepts

### What are Tables?

- **Structured storage**: Define schemas with Zod validation
- **Auto-created**: Tables are automatically created from your schema
- **Searchable**: Optional semantic search on specified columns
- **Type-safe**: Full TypeScript support for all operations

### File Location

- **Location**: `src/tables/*.ts`
- **Auto-registration**: Files automatically create database tables

## Creating Tables

### ⚠️ CRITICAL REQUIREMENTS

**Before creating any table, you MUST follow these two rules or table creation will fail:**

1. **DO NOT define `id`, `createdAt`, or `updatedAt` columns in schema** - all three are RESERVED and automatically managed. Defining any of them in `columns` throws an error.
   - ❌ Don't define them: `columns: { id: ..., createdAt: ..., updatedAt: ... }`
   - ✅ Every row automatically has `id` (`number`), `createdAt`, and `updatedAt` — read them off the row (e.g. `row.createdAt`). Never write `createdAt`/`updatedAt` in any payload; they are always system-managed.
   - ✅ `id` is auto-assigned by `createRows()` (don't pass it). You may pass `id` (as `number`) to `upsertRows()` — there it is the **match key** that locates the row to update, not a column value you set.

2. **Table names MUST end with "Table" suffix** - The `name` property passed to `new Table()` must end with "Table" (e.g., `"UsersTable"`, `"OrdersTable"`). This is enforced by runtime validation.

```typescript
// ✅ CORRECT
export const UsersTable = new Table({
  name: 'UsersTable',
  columns: {
    // No id field - it's automatic!
    name: z.string(),
    email: z.string(),
  },
})

// ❌ WRONG - id is defined (will fail!)
export const Users = new Table({
  // Also missing "Table" suffix on variable name
  name: 'UsersTable',
  columns: {
    id: z.string(), // ❌ Don't define id!
    name: z.string(),
  },
})
```

### Basic Table Structure

```typescript
import { Table, z } from '@botpress/runtime'

export const UsersTable = new Table({
  name: 'UsersTable',
  description: 'Stores user information',

  columns: {
    // Note: id, createdAt, updatedAt are NOT defined - they're automatic!
    name: z.string(),
    email: z.string().email(),
    role: z.enum(['admin', 'user', 'guest']),
    metadata: z.object({}).passthrough(), // Flexible object
  },
})
```

### Table with Key Column and Tags

Use `keyColumn` to document the logical key for the table and `tags` for table metadata:

```typescript
import { Table, z } from '@botpress/runtime'

export const ExternalUsersTable = new Table({
  name: 'ExternalUsersTable',
  description: 'Users synced from external system',

  // Key column for upsert operations - must be a column name
  keyColumn: 'externalId',

  // Tags for table metadata (key-value pairs)
  tags: {
    source: 'salesforce',
    syncType: 'incremental',
    version: '2.0',
  },

  columns: {
    externalId: z.string(), // This is the key column
    name: z.string(),
    email: z.string().email(),
    lastSyncedAt: z.date(),
  },
})
```

**Key Column Notes:**

- `keyColumn` documents the intended unique key for the table.
- Current runtime upsert helpers may still require `keyColumn` to be passed explicitly per `upsertRows()` call.
- Do not assume table-level `keyColumn` is automatically applied everywhere.

**Tags Use Cases:**

- Track data source/origin
- Version control for schemas
- Environment markers (staging, production)
- Sync metadata (last sync, sync type)

### Complex Schema Patterns

Tables support complex nested structures and flexible schemas:

```typescript
export const ConversationsTable = new Table({
  name: 'ConversationsTable',
  description: 'Store conversation data with complex metadata',

  columns: {
    // id, createdAt, updatedAt are automatic — don't define them.

    // Optional fields
    waitingSince: z.string().optional(),
    snoozedUntil: z.string().optional(),

    // Nested objects with specific structure
    source: z
      .object({
        type: z.string(),
        id: z.string().optional(),
        deliveredAs: z.string().optional(),
        subject: z.string().optional(),
        body: z.string().optional(),
        author: z
          .object({
            type: z.string(),
            id: z.string().optional(),
          })
          .optional(),
      })
      .optional(),

    // Array fields
    contactIds: z.array(z.string()).optional(),
    admins: z
      .array(
        z.object({
          type: z.string(),
          id: z.string(),
          name: z.string().optional(),
          email: z.string().optional(),
        })
      )
      .optional(),

    // Flexible objects with passthrough
    metadata: z.object({}).passthrough(),

    // Discriminated unions for type safety
    status: z.discriminatedUnion('type', [
      z.object({ type: z.literal('active'), reason: z.string() }),
      z.object({ type: z.literal('snoozed'), until: z.string() }),
      z.object({ type: z.literal('closed'), closedAt: z.string() }),
    ]),
  },
})
```

### Searchable Columns

Enable semantic search on specific columns:

```typescript
export const DocumentsTable = new Table({
  name: 'DocumentsTable',
  description: 'Document storage with search',

  columns: {
    // Searchable field with shorthand syntax
    title: {
      searchable: true,
      schema: z.string().describe('Document title'),
    },

    // Enable semantic search on content
    content: {
      schema: z.string(),
      searchable: true,
    },

    // Another searchable field
    summary: {
      schema: z.string(),
      searchable: true,
    },

    tags: z.array(z.string()),
  },

  // Optional: Search optimization factor
  // factor controls the relative importance of this table in search results
  // Higher values (e.g., 5, 10, 20) give this table higher priority in search
  // Default is 1 if not specified
  factor: 5,
})
```

### Important Column Syntax

For searchable columns, use object notation:

```typescript
// ✅ CORRECT - Object with schema and searchable
columns: {
  searchableField: {
    schema: z.string(),
    searchable: true
  }
}

// ❌ WRONG - Chain notation doesn't work
columns: {
  searchableField: z.string().searchable() // This doesn't exist!
}
```

## CRUD Operations

### Creating Rows

```typescript
import { UsersTable } from './tables/Users'

// Create single row (id is auto-assigned)
await UsersTable.createRows({
  rows: [
    {
      name: 'John Doe',
      email: 'john@example.com',
      role: 'user',
      metadata: { source: 'signup' },
    },
  ],
})

// Create multiple rows (ids are auto-assigned)
await UsersTable.createRows({
  rows: [
    {
      name: 'Alice',
      email: 'alice@example.com',
      role: 'admin',
    },
    {
      name: 'Bob',
      email: 'bob@example.com',
      role: 'user',
    },
  ],
})
```

### Finding Rows

```typescript
// Find by condition
const { rows } = await UsersTable.findRows({
  filter: { role: 'admin' },
  orderBy: 'createdAt',
  orderDirection: 'desc',
  limit: 10,
  offset: 0,
})

// Find by multiple conditions
const { rows } = await UsersTable.findRows({
  filter: {
    role: 'user',
    email: 'john@example.com',
  },
})

// Find with complex conditions
const { rows } = await UsersTable.findRows({
  filter: {
    createdAt: { $gte: new Date('2024-01-01') },
  },
  orderBy: 'name',
  orderDirection: 'asc',
})

// Complex filters with logical operators
const { rows } = await UsersTable.findRows({
  filter: {
    $and: [{ role: 'user' }, { createdAt: { $gte: new Date('2024-01-01') } }],
  },
})
```

### Getting Single Row

Get a specific row by its id:

```typescript
// Get row by id
const row = await UsersTable.getRow({ id: 123 })

console.log(row.id) // 123
console.log(row.name) // Access row properties
console.log(row.createdAt) // Auto-generated timestamp
```

### Semantic Search

Search across searchable columns using the `search` parameter:

```typescript
// Search documents
const { rows } = await DocumentsTable.findRows({
  search: 'machine learning algorithms',
  limit: 5,
})

// Results are ranked by semantic similarity
rows.forEach((doc) => {
  console.log(doc.title, doc.content)
})

// Combine search with filters
const { rows } = await DocumentsTable.findRows({
  search: 'machine learning',
  filter: { tags: { $in: ['ai', 'ml'] } },
  limit: 10,
})
```

### Upsert Operations

Upsert allows inserting or updating rows based on a key column:

```typescript
// Upsert based on a unique column
await MessagesTable.upsertRows({
  rows: [
    {
      messageId: 'msg-123', // Key column
      content: 'Updated content',
      timestamp: new Date(),
    },
  ],
  keyColumn: 'messageId', // Updates if messageId exists, inserts if not
})

// Upsert with id (optional, as number)
await UsersTable.upsertRows({
  rows: [
    {
      id: 123, // Optional: provide id to update specific row
      name: 'Jane Doe',
      email: 'jane@example.com',
    },
  ],
  keyColumn: 'id',
})

// Bulk upsert with multiple rows
await ContactsTable.upsertRows({
  rows: contacts.map((contact) => ({
    contactId: contact.id,
    name: contact.name,
    email: contact.email,
  })),
  keyColumn: 'contactId',
})
```

### Updating Rows

Update existing rows by ID:

```typescript
// Update specific row by ID
await UsersTable.updateRows({
  rows: [
    {
      id: 123, // Row ID (required)
      role: 'admin',
      metadata: { promoted: true },
    },
  ],
})

// Update multiple rows
await UsersTable.updateRows({
  rows: [
    { id: 123, role: 'admin' },
    { id: 456, role: 'user' },
  ],
})
```

**Note:** For tables with computed columns, see "Computed Columns" section below for the `waitComputed` option.

### Deleting Rows

```typescript
// Delete by filter condition
await UsersTable.deleteRows({
  role: 'guest',
})

// Delete with complex filter
await UsersTable.deleteRows({
  $and: [{ role: 'guest' }, { createdAt: { $lt: new Date('2024-01-01') } }],
})

// Delete by specific IDs
await UsersTable.deleteRowIds([123, 456, 789])

// Delete all rows (use with caution!)
await UsersTable.deleteAllRows()
```

### Advanced: Direct Table Operations

In workflows, you can also use the client for low-level table operations:

```typescript
import { Workflow } from '@botpress/runtime'

export const ResetTablesWorkflow = new Workflow({
  name: 'resetTables',
  description: 'Resets specific tables',
  async handler({ client }) {
    // Delete entire table (drops and recreates)
    await client._inner.deleteTable({ table: 'MyTable' })

    // Other low-level operations available via client._inner
    // Use with caution as these bypass type safety
  },
})
```

## Complex Schemas

### Nested Objects

```typescript
export const OrdersTable = new Table({
  name: 'OrdersTable',

  columns: {
    customer: z.object({
      id: z.string(),
      name: z.string(),
      email: z.string().email(),
    }),
    items: z.array(
      z.object({
        productId: z.string(),
        quantity: z.number().int().positive(),
        price: z.number().positive(),
      })
    ),
    shipping: z.object({
      address: z.string(),
      city: z.string(),
      country: z.string(),
      postalCode: z.string(),
    }),
    status: z.enum(['pending', 'processing', 'shipped', 'delivered']),
    total: z.number().positive(),
  },
})
```

### Optional and Default Values

```typescript
export const ProductsTable = new Table({
  name: 'ProductsTable',

  columns: {
    name: z.string(),
    description: z.string().optional(), // Optional field

    // With default value
    price: z.number().positive().default(0),
    inStock: z.boolean().default(true),

    // Optional with default
    category: z.string().optional().default('uncategorized'),

    // Nullable field
    discountPrice: z.number().positive().nullable(),

    metadata: z.object({}).passthrough().optional(),
  },
})
```

### Computed Columns

Computed columns are automatically calculated based on other column values. They support dependencies and are recomputed when their dependencies change.

```typescript
import { Table, z } from '@botpress/runtime'

export const ProfilesTable = new Table({
  name: 'ProfilesTable',

  columns: {
    firstName: z.string(),
    lastName: z.string(),

    // Computed column - automatically generated
    fullName: {
      computed: true,
      schema: z.string(),
      dependencies: ['firstName', 'lastName'],
      value: async (row) => {
        return `${row.firstName} ${row.lastName}`
      },
    },

    age: z.number(),

    // Computed with single dependency
    ageInMonths: {
      computed: true,
      schema: z.number(),
      dependencies: ['age'],
      value: async (row) => {
        return row.age * 12
      },
    },
  },
})
```

#### Using Computed Columns

Computed columns are calculated automatically when rows are created or updated:

```typescript
// Create row - computed columns calculated automatically
await ProfilesTable.createRows({
  rows: [
    {
      firstName: 'John',
      lastName: 'Doe',
      age: 30,
      // fullName and ageInMonths will be computed automatically
      // id is auto-assigned by server
    },
  ],
})

// The created row will have: id (number), fullName = "John Doe", ageInMonths = 360
```

#### Waiting for Computed Values

By default, computed columns run asynchronously. Use `waitComputed: true` to ensure computed values finish processing before the operation returns:

```typescript
// Update with waitComputed - blocks until computed columns finish
await ProfilesTable.updateRows({
  rows: [
    {
      id: 123, // Row id as number
      firstName: 'Jane', // fullName will be recomputed
    },
  ],
  waitComputed: true, // Wait for fullName to finish computing
})

// Without waitComputed, computed columns update eventually
await ProfilesTable.updateRows({
  rows: [{ id: 123, firstName: 'Jane' }],
  // Returns immediately, computed columns update in background
})
```

#### Complex Dependencies

Computed columns can have multiple dependencies and form dependency chains:

```typescript
export const OrdersTable = new Table({
  name: 'OrdersTable',

  columns: {
    price: z.number(),
    quantity: z.number(),
    taxRate: z.number(),

    // First level: subtotal
    subtotal: {
      computed: true,
      schema: z.number(),
      dependencies: ['price', 'quantity'],
      value: async (row) => row.price * row.quantity,
    },

    // Second level: tax (depends on computed column)
    tax: {
      computed: true,
      schema: z.number(),
      dependencies: ['subtotal', 'taxRate'],
      value: async (row) => row.subtotal * row.taxRate,
    },

    // Third level: total (depends on two computed columns)
    total: {
      computed: true,
      schema: z.number(),
      dependencies: ['subtotal', 'tax'],
      value: async (row) => row.subtotal + row.tax,
    },
  },
})
```

#### Computed Column Use Cases

**Dynamic Summaries:**

```typescript
export const UsersTable = new Table({
  name: 'UsersTable',
  columns: {
    firstName: z.string(),
    lastName: z.string(),
    email: z.string(),
    age: z.number(),

    // Generate user bio automatically
    bio: {
      computed: true,
      schema: z.string(),
      dependencies: ['firstName', 'lastName', 'age'],
      value: async (row) => {
        return `Name: ${row.firstName} ${row.lastName}, Age: ${row.age}`
      },
    },
  },
})
```

**Calculations:**

```typescript
export const ProductsTable = new Table({
  name: 'ProductsTable',
  columns: {
    price: z.number(),
    cost: z.number(),

    // Calculate profit margin
    profitMargin: {
      computed: true,
      schema: z.number(),
      dependencies: ['price', 'cost'],
      value: async (row) => {
        return ((row.price - row.cost) / row.price) * 100
      },
    },
  },
})
```

**Data Transformations:**

```typescript
export const ContactsTable = new Table({
  name: 'ContactsTable',
  columns: {
    phone: z.string(),

    // Normalize phone format
    phoneNormalized: {
      computed: true,
      schema: z.string(),
      dependencies: ['phone'],
      value: async (row) => {
        // Remove all non-digit characters
        return row.phone.replace(/\D/g, '')
      },
    },
  },
})
```

#### Important Notes

- **Not Stored in Schema**: Computed columns are calculated, not stored in the base schema definition
- **Automatic Resolution**: Dependencies are automatically resolved in the correct order
- **No Circular Dependencies**: The system prevents circular dependency chains
- **Async Support**: The `value` function is async, allowing API calls or complex computations
- **Use `waitComputed`**: When you need computed values immediately after an operation
- **Performance**: Computed columns add processing time - use sparingly for expensive operations

## Usage in Actions/Workflows

### In Actions

```typescript
import { Action, z } from '@botpress/runtime'
import { UsersTable } from '../tables/Users'

export const createUser = new Action({
  name: 'createUser',
  input: z.object({
    name: z.string(),
    email: z.string().email(),
    role: z.enum(['admin', 'user', 'guest']),
  }),
  output: z.object({
    userId: z.string(),
    created: z.boolean(),
  }),

  async handler({ input }) {
    // Check if user exists
    const existing = await UsersTable.findRows({
      filter: { email: input.email },
      limit: 1,
    })

    if (existing.rows.length > 0) {
      return {
        userId: existing.rows[0].id,
        created: false,
      }
    }

    // Create new user
    const result = await UsersTable.createRows({
      rows: [
        {
          name: input.name,
          email: input.email,
          role: input.role,
          metadata: {},
        },
      ],
    })

    return {
      userId: result.rows[0].id.toString(),
      created: true,
    }
  },
})
```

### In Workflows

```typescript
import { Workflow, z } from '@botpress/runtime'
import { AuditLogTable } from '../tables/AuditLog'

export const ProcessingWorkflow = new Workflow({
  name: 'processing',
  input: z.object({ data: z.string() }),

  handler: async ({ input, step }) => {
    // Log workflow start
    await step('log-start', async () => {
      await AuditLogTable.createRows({
        rows: [
          {
            action: 'workflow_started',
            details: { workflow: 'processing', input },
            timestamp: new Date(),
          },
        ],
      })
    })

    // Process data
    const result = await step('process', async () => {
      return await processData(input.data)
    })

    // Log completion
    await step('log-complete', async () => {
      await AuditLogTable.createRows({
        rows: [
          {
            action: 'workflow_completed',
            details: { workflow: 'processing', result },
            timestamp: new Date(),
          },
        ],
      })
    })

    return { success: true }
  },
})
```

### In Conversations

```typescript
import { Conversation, user } from '@botpress/runtime'
import { ConversationHistoryTable } from '../tables/ConversationHistory'

export const Chat = new Conversation({
  channel: 'chat.channel',

  async handler({ message, conversation }) {
    // Store message in history
    if (message?.type === 'text') {
      await ConversationHistoryTable.createRows({
        rows: [
          {
            conversationId: conversation.id,
            userId: user.id,
            message: message.payload.text,
            timestamp: new Date(),
          },
        ],
      })
    }

    // Search previous conversations
    if (message?.payload.text?.startsWith('/search')) {
      const query = message.payload.text.substring(7).trim()

      const { rows } = await ConversationHistoryTable.findRows({
        search: query,
        limit: 5,
      })

      await conversation.send({
        type: 'text',
        payload: {
          text: `Found ${rows.length} matching conversations`,
        },
      })
    }
  },
})
```

## Using Tables with Knowledge Bases

Tables can be used as data sources for Knowledge Bases to enable RAG (Retrieval Augmented Generation) from your structured data.

For complete documentation on using tables with knowledge bases, including `DataSource.Table.fromTable()`, transform functions, and filtering options, see:

**→ [knowledge-bases.md - Table Data Sources](./knowledge-bases.md)**

## Best Practices

### 1. Use Meaningful Table Names with "Table" Suffix

```typescript
// ✅ CORRECT - Clear, descriptive names
export const UsersTable = new Table({ name: "UsersTable", columns: { ... } });
export const OrdersTable = new Table({ name: "OrdersTable", columns: { ... } });
```

### 2. Timestamps Are Automatic

Every row already has `createdAt` and `updatedAt` (and `id`) — don't define them. Add your own date column only for a distinct meaning, e.g. a soft delete:

```typescript
columns: {
  // createdAt / updatedAt are automatic — read them off the row, don't define them.
  deletedAt: z.date().nullable().optional() // soft delete
}
```

### 3. Handle Pagination

```typescript
export const fetchPaginatedData = new Action({
  input: z.object({
    page: z.number().int().positive().default(1),
    pageSize: z.number().int().positive().max(100).default(20),
  }),

  async handler({ input }) {
    const offset = (input.page - 1) * input.pageSize

    const { rows } = await MyTable.findRows({
      limit: input.pageSize,
      offset,
      orderBy: 'createdAt',
      orderDirection: 'desc',
    })

    // Get total row count
    const { rows: totalRows } = await MyTable.getTable()

    return {
      rows,
      pagination: {
        page: input.page,
        pageSize: input.pageSize,
        total: totalRows,
        totalPages: Math.ceil(totalRows / input.pageSize),
      },
    }
  },
})
```

### 4. Optimize Searchable Content

```typescript
export const DocumentsTable = new Table({
  columns: {
    // Store both original and optimized search content
    content: z.string(), // Original content

    searchContent: {
      schema: z.string(),
      searchable: true, // Optimized for search
    },
  },
})

// When creating rows
await DocumentsTable.createRows({
  rows: [
    {
      content: originalContent,
      searchContent: stripHtml(originalContent).toLowerCase(), // Optimized
    },
  ],
})
```

## Common Patterns

### Audit Log Pattern

```typescript
export const AuditLogTable = new Table({
  name: 'AuditLogTable',
  columns: {
    userId: z.string(),
    action: z.string(),
    entityType: z.string().optional(),
    entityId: z.string().optional(),
    changes: z.object({}).passthrough().optional(),
    metadata: z.object({}).passthrough(),
    timestamp: z.date(),
  },
})

// Helper function
export async function logAction(userId: string, action: string, details: Record<string, any>) {
  await AuditLogTable.createRows({
    rows: [
      {
        userId,
        action,
        ...details,
        timestamp: new Date(),
      },
    ],
  })
}
```

### Cache Pattern

```typescript
export const CacheTable = new Table({
  name: 'CacheTable',
  columns: {
    key: z.string(),
    value: z.unknown(),
    expiresAt: z.date(),
  },
})

// Cache helper
export async function getCached<T>(key: string, fetcher: () => Promise<T>, ttlMinutes: number = 60): Promise<T> {
  // Check cache
  const { rows } = await CacheTable.findRows({
    filter: { key },
    limit: 1,
  })

  const cached = rows[0]
  if (cached && cached.expiresAt > new Date()) {
    return cached.value as T
  }

  // Fetch new value
  const value = await fetcher()

  // Store in cache
  await CacheTable.upsertRows({
    rows: [
      {
        key,
        value,
        expiresAt: new Date(Date.now() + ttlMinutes * 60 * 1000),
      },
    ],
    keyColumn: 'key',
  })

  return value
}
```

## Syncing Tables

As of ADK 1.9+, tables are automatically synced using the CLI during development and deployment.

### Automatic Sync

Table sync runs automatically during:

- `adk dev` - Syncs tables on startup and detects schema changes
- `adk deploy` - Syncs tables before deployment

### What Gets Synced

The table sync process:

1. **Detects all tables** in your `src/tables/` directory
2. **Compares schemas** against the remote bot's tables
3. **Creates new tables** that don't exist remotely
4. **Updates table schemas** when columns are added or modified
5. **Warns about breaking changes** (like column removal)

### Schema Migration

When table schemas change:

```typescript
// Original table
export const UsersTable = new Table({
  name: 'UsersTable',
  columns: {
    name: z.string(),
    email: z.string(),
  },
})

// After adding a column - sync handles this automatically
export const UsersTable = new Table({
  name: 'UsersTable',
  columns: {
    name: z.string(),
    email: z.string(),
    role: z.string().default('user'), // New column with default
  },
})
```

**Important:** Adding columns with defaults is safe. Removing columns or changing types may require manual migration.

### Manual Table Operations

For advanced scenarios, you can use the client directly:

```typescript
import { Workflow } from '@botpress/runtime'

export const MigrateTablesWorkflow = new Workflow({
  name: 'migrateTables',

  async handler({ client }) {
    // Delete and recreate a table (use with caution!)
    await client._inner.deleteTable({ table: 'MyTable' })

    // Note: The table will be recreated on next sync
  },
})
```

## Troubleshooting

### Common Issues

1. **Table creation fails**
   - ❌ **Did you define `id` in columns?** Remove it - `id` is automatic and reserved!
   - ❌ **Does your table name end with "Table"?** Example: `UsersTable`, not `Users`
   - Ensure file is in `src/tables/` directory
   - Check that table is exported with `export const`
   - Verify schema is valid

2. **Search not working**
   - Confirm column has `searchable: true`
   - Use object notation for searchable columns: `{ schema: z.string(), searchable: true }`
   - Check that content is text-based

3. **Type errors**
   - Ensure data matches schema exactly
   - Use `.optional()` for nullable fields
   - Check date formats
   - Remember: don't define `id` in schema - it's auto-assigned as a number by the server

4. **Performance issues**
   - Add indexes on frequently queried columns
   - Limit result sets with `limit`
   - Use pagination for large datasets
   - Consider caching for expensive queries
