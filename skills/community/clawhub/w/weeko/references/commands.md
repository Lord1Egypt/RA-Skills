# Weeko CLI Command Reference

Complete reference for all Weeko CLI commands, output schemas, and architecture details.

## Command Overview

| Category | Command | Description | Output Schema |
|----------|---------|-------------|---------------|
| Auth | `login` | Authenticate with API key | `{ success, user }` |
| Auth | `logout` | Remove stored credentials | `{ success, message }` |
| Auth | `whoami` | Show current user | `User` |
| Context | `status` | Account overview | `{ user, stats, recentGroups }` |
| Context | `tree` | Groups structure | `Group[]` |
| Bookmarks | `list` | List all bookmarks | `Bookmark[]` |
| Bookmarks | `get <id>` | Get bookmark details | `Bookmark` |
| Bookmarks | `add <url>` | Create bookmark | `{ success, id, title }` |
| Bookmarks | `search <query>` | Search bookmarks | `Bookmark[]` |
| Bookmarks | `update <id>` | Update bookmark | `{ success, id, title }` |
| Bookmarks | `delete <id>` | Delete bookmark | `{ success, id }` |
| Groups | `group list` | List groups | `Group[]` |
| Groups | `group get <id>` | Get group details | `Group` |
| Groups | `group create` | Create group | `Group` |
| Groups | `group update <id>` | Update group | `Group` |
| Groups | `group delete <id>` | Delete group | `{ success }` |
| Batch | `batch move` | Move bookmarks | `{ success }` |
| Batch | `batch delete` | Delete bookmarks | `{ success }` |

## Data Schemas

### Bookmark

```typescript
{
  id: string,              // Unique identifier (e.g., "clxabc123...")
  title: string,           // Bookmark title
  url: string | null,      // URL for link bookmarks
  description: string | null,
  type: "link" | "color" | "text",  // Bookmark type
  color: string | null,    // Hex color for color bookmarks
  image: string | null,    // Fetched image URL
  favicon: string | null,  // Site favicon URL
  siteName: string | null, // Extracted site name
  isPublic: boolean | null,
  groupId: string,         // Parent group ID
  createdAt: string,       // ISO timestamp
  updatedAt: string,       // ISO timestamp
  group?: {                // Included when listing
    id: string,
    name: string,
    color: string
  }
}
```

### Group

```typescript
{
  id: string,              // Unique identifier
  name: string,            // Group name
  color: string,           // Hex color (e.g., "#3b82f6")
  isPublic: boolean | null,
  bookmarkCount: number,   // Number of bookmarks in group
  createdAt: string,
  updatedAt: string
}
```

### User

```typescript
{
  id: string,
  name: string,
  email: string
}
```

### Status Output

```typescript
{
  user: User,
  stats: {
    totalBookmarks: number,
    linkBookmarks: number,
    colorBookmarks: number,
    textBookmarks: number,
    publicBookmarks: number,
    groups: number
  },
  recentGroups?: Array<{
    id: string,
    name: string,
    bookmarkCount: number
  }>
}
```

## CLI Architecture

### Project Structure

```
cli/
├── src/
│   ├── index.ts           # Entry point, command definitions
│   ├── commands/          # Command implementations
│   │   ├── login.ts       # Authentication commands
│   │   ├── context.ts     # status, tree commands
│   │   ├── bookmarks.ts   # Bookmark CRUD + search
│   │   ├── groups.ts      # Group CRUD
│   │   └── batch.ts       # Batch operations
│   ├── api/
│   │   ├── client.ts      # WeekoAPI class + HTTP client
│   │   ├── schemas.ts     # Zod validation schemas
│   │   └── types.ts       # TypeScript types
│   └── utils/
│       ├── config.ts      # Config storage (~/.config/weeko-cli/)
│       ├── output.ts      # Output formatting (json/toon/pretty)
│       ├── spinner.ts     # Loading spinners
│       └── update-check.ts # Version update checker
├── package.json
└── bun.lock
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `commander` | CLI framework and argument parsing |
| `@clack/prompts` | Interactive prompts (select, confirm, text) |
| `zod` | Schema validation for API responses |
| `@toon-format/toon` | TOON encoding for AI-optimized output |
| `picocolors` | Terminal colors |
| `cli-table3` | Pretty table formatting |
| `ora` | Spinner animations |
| `boxen` | Card-style boxes |
| `figures` | Unicode symbols |
| `highlight-words` | Search result highlighting |

### API Client (WeekoAPI)

```typescript
class WeekoAPI {
  // Constructor
  constructor(apiKey: string, apiUrl: string, dryRun?: boolean, logger?: Logger)

  // Endpoints
  getUser(): Promise<User>
  getBookmarks(groupId?: string): Promise<Bookmark[]>
  getBookmark(id: string): Promise<Bookmark>
  createBookmark(input: CreateBookmark): Promise<Bookmark>
  updateBookmark(id: string, input: UpdateBookmark): Promise<Bookmark>
  deleteBookmark(id: string): Promise<boolean>
  
  getGroups(): Promise<Group[]>
  getGroup(id: string): Promise<Group>
  createGroup(input: CreateGroup): Promise<Group>
  updateGroup(id: string, input: UpdateGroup): Promise<Group>
  deleteGroup(id: string): Promise<boolean>
}
```

### Request Features

- **Retry Logic**: 3 retries with exponential backoff + jitter
- **Rate Limiting**: Handles 429 with Retry-After header
- **Timeout**: 60-second request timeout with AbortController
- **Validation**: All responses validated with Zod schemas before return
- **Dry Run**: `--dry-run` logs actions without making API calls

### Configuration Storage

Config stored at `~/.config/weeko-cli/config.json`:

```json
{
  "apiKey": "wk_xxx",
  "apiUrl": "https://weeko.blog"
}
```

Environment variables override config:
- `WEEKO_API_KEY` - API key (bypasses login)
- `WEEKO_API_URL` - Custom API URL (default: https://weeko.blog)

## Output Format Details

### JSON Format

Default output. Standard JSON for programmatic use.

```bash
weeko list --format json
weeko list  # json is default
```

Example output:
```json
[
  {
    "id": "clxabc123",
    "title": "React Documentation",
    "url": "https://react.dev",
    "type": "link",
    "groupId": "clxgrp1",
    "group": { "id": "clxgrp1", "name": "Dev", "color": "#3b82f6" }
  }
]
```

### TOON Format

Token-Optimized Output Notation. Uses tab delimiters and key folding for maximum token efficiency. Best for AI agents consuming CLI output.

```bash
weeko list --format toon
```

Example output:
```
bookmarks[1]{id,title,url,type,groupId,group.id,group.name,group.color}:
  clxabc123	React Documentation	https://react.dev	link	clxgrp1	clxgrp1	Dev	#3b82f6
```

**Features**:
- `[N]` prefix shows array length
- `{keys}` shows available fields
- Tab delimiters instead of JSON syntax
- Key folding: `group.id` instead of nested objects
- ~40-60% token reduction vs JSON

### Pretty Format

Human-readable formatted output. Uses colors, tables, and visual elements.

```bash
weeko list --pretty
weeko status --pretty
weeko tree --pretty
weeko search "query" --pretty
weeko group list --pretty
```

**Output types**:
- **Tables**: Bookmarks, groups displayed in bordered tables
- **Cards**: Status shown in rounded boxen card with stats
- **Tree**: Groups shown with `├──`/`└──` tree structure
- **Highlight**: Search results with query highlighting

## Error Handling

### WeekoError Class

```typescript
class WeekoError extends Error {
  statusCode: number  // HTTP status code
  hint?: string       // Resolution hint
}
```

### Common Errors

| Status | Message | Hint |
|--------|---------|------|
| 401 | Unauthorized | Run `weeko login` to authenticate |
| 404 | Not Found | Verify the ID is correct |
| 400 | Bad Request | Check your input parameters |
| 429 | Rate Limited | Wait a few minutes before retrying |
| 500 | Server Error | Server experiencing issues, try later |
| 504 | Timeout | Request took too long |
| 503 | Network Error | Check internet connection |

### Error Output (JSON)

```json
{
  "error": "API Error 404: Bookmark not found",
  "status": 404,
  "hint": "The requested resource was not found. Verify the ID is correct."
}
```

### Error Output (Pretty)

```
error: API Error 404: Bookmark not found
status: 404
hint: The requested resource was not found. Verify the ID is correct.
```

## Validation Schemas

All inputs are validated with Zod:

### CreateBookmark

```typescript
{
  title: string (min 1, max 500),
  url?: string (valid URL, max 2000),
  groupId: string (min 1),
  description?: string (max 5000)
}
```

### CreateGroup

```typescript
{
  name: string (min 1, max 100),
  color?: string (hex format #RRGGBB)
}
```

### UpdateBookmark

```typescript
{
  title?: string (min 1, max 500),
  url?: string (valid URL, max 2000),
  groupId?: string (min 1),
  description?: string (max 5000)
}
```

### UpdateGroup

```typescript
{
  name?: string (min 1, max 100),
  color?: string (hex format #RRGGBB)
}
```

## API Endpoints

Base URL: `https://weeko.blog/api` (or custom `WEEKO_API_URL`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/user/me` | GET | Get current user |
| `/bookmarks` | GET | List all bookmarks |
| `/bookmarks?groupId=X` | GET | List bookmarks in group |
| `/bookmarks/:id` | GET | Get bookmark details |
| `/bookmarks` | POST | Create bookmark |
| `/bookmarks/:id` | PATCH | Update bookmark |
| `/bookmarks/:id` | DELETE | Delete bookmark |
| `/groups` | GET | List all groups |
| `/groups/:id` | GET | Get group details |
| `/groups` | POST | Create group |
| `/groups/:id` | PATCH | Update group |
| `/groups/:id` | DELETE | Delete group |

All endpoints require `Authorization: Bearer <api-key>` header.

## Development

### Local Development

```bash
cd cli
bun install
bun run dev          # Run with watch mode
bun run build        # Build to dist/
bun run typecheck    # TypeScript check
```

### Release Process

```bash
bun run release      # Bump version (patch)
bun run release:minor # Bump version (minor)
bun run release:major # Bump version (major)
bun run publish:npm   # Publish to npm (patch)
```

### Testing Dry Run

```bash
weeko add "https://test.com" --dry-run
weeko delete "abc123" --dry-run
weeko group create "Test" --dry-run
```

Dry run mode logs the action and payload without making API calls.