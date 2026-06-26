# UUMuse Brain

You have access to the user's UUMuse knowledge bases through MCP tools.
UUMuse lets users upload PDFs, docs, web pages, and other files into workspaces.
You can search, ask questions, manage files, and maintain long-term memory.

## Mandatory Tool Rules

- Use the injected MCP tools named `uumuse_status`, `uumuse_workspaces`, `uumuse_files`, `uumuse_search`, `uumuse_ask`, `uumuse_read_file`, `uumuse_upload`, `uumuse_edit_file`, `uumuse_delete_file`, `uumuse_append`, `uumuse_remember`, `uumuse_recall`, and `uumuse_forget`.
- In OpenClaw/LobsterAI, injected MCP tools may be provider-safe names prefixed by the server name, for example `uumuse-lan__uumuse_workspaces`, `uumuse-lan__uumuse_search`, and `uumuse-lan__uumuse_ask`. If both prefixed and unprefixed names are visible, prefer the prefixed `uumuse-lan__...` tool.
- When the user asks to list UUMuse workspaces, call `uumuse-lan__uumuse_workspaces` if available; otherwise call `uumuse_workspaces` directly.
- Never use shell commands, `npx`, `npm`, `uumuse-mcp`, `@openclaw/mcp-uumuse`, local source-code search, or local filesystem search as a substitute for UUMuse MCP tools.
- Never use `nodes`, `sessions_spawn`, paired-device commands, or subagents to call UUMuse. UUMuse is a configured local stdio/HTTP MCP server, not a paired mobile node.
- The API key and LAN/API URL are provided by the configured MCP server environment. Do not ask the user for `UUMUSE_API_KEY` unless the injected UUMuse MCP tools are unavailable.
- If tools are not available, tell the user to run the UUMuse install script or check their MCP configuration.

## When to Use

Use UUMuse tools proactively whenever the user asks about information that may live in their UUMuse workspaces, knowledge base, uploaded files, notes, documents, or long-term memory.

Do not answer from general knowledge when the request is about the user's own documents. First call the appropriate UUMuse tool.

Trigger on requests like:
- Mentions of `UUMuse`, `UUMuse MCP`, "my documents", "my files", "my knowledge base", "my workspace", "my notes", or "my uploaded files"
- Chinese equivalents such as "列出我的 UUMuse 工作区", "我的文档", "我的文件", "我的知识库", "我的工作区", "我的资料", "我的笔记"
- References to a specific uploaded file, PDF, PPT, spreadsheet, markdown file, report, policy, plan, attachment, or workspace
- Requests to search, find, look up, summarize, compare, extract, explain, or answer based on documents
- Phrases like "what does my research say about X", "find Y in my notes", "在我的知识库里查 X", "根据我的文档回答 X"
- Requests to list workspaces/files, check account status, upload/edit/delete files, or manage long-term memory
- Requests to remember something, save a preference, or recall past context

If the user asks a broad question that could involve their knowledge base, call `uumuse_workspaces` or `uumuse_search` first instead of asking the user to manually pick a tool.

## Tools

### Core — Knowledge Access

| Tool | When | Cost |
|------|------|------|
| `uumuse_status` | Check UT balance and remaining quota before asking | Free |
| `uumuse_workspaces` | Discover available workspaces and their IDs | Free |
| `uumuse_files` | See what files are in a workspace | Free |
| `uumuse_search` | Quick semantic search across documents | Free |
| `uumuse_ask` | AI-generated answer with source citations | Per token |

### File Management

| Tool | When | Cost |
|------|------|------|
| `uumuse_read_file` | Read the full text content of a file | Free |
| `uumuse_upload` | Create a new text file in a workspace | Free |
| `uumuse_edit_file` | Overwrite a file's content entirely | Free |
| `uumuse_append` | Append text to an existing file (ideal for logs/journals) | Free |
| `uumuse_delete_file` | Permanently delete a file and its embeddings | Free |

### Long-Term Memory

| Tool | When | Cost |
|------|------|------|
| `uumuse_remember` | Store a piece of information for future recall | Free |
| `uumuse_recall` | Search memory for relevant past information | Free |
| `uumuse_forget` | Delete a memory file and all its entries | Free |

## How to Use

### Knowledge Queries
1. Call `uumuse_status` first if unsure about remaining quota
2. If no workspace is specified, call `uumuse_workspaces` to list options
3. For quick lookups, prefer `uumuse_search` (free, returns raw chunks)
4. For complex questions needing synthesis, use `uumuse_ask` (costs UT)
5. Always cite sources — include file names from the response
6. If the workspace is empty, suggest the user upload documents at uumuse.ai

### File Operations
- Use `uumuse_upload` to create new files (notes, logs, summaries)
- Use `uumuse_append` to add content to existing files without overwriting
- Use `uumuse_read_file` to view current file content before editing
- Use `uumuse_edit_file` only for full rewrites — prefer `uumuse_append` for additions

### Memory (Cross-Session Persistence)
- Use `uumuse_remember` to save important facts, user preferences, decisions, or context
- Each memory is tagged with a category (e.g. "preferences", "facts", "tasks")
- Memories are stored as `_memories_{category}.md` files and automatically vectorized
- Use `uumuse_recall` to search memories — it prioritizes memory files over regular documents
- Use `uumuse_forget` to delete an entire memory category file

**Memory best practices:**
- Remember user preferences early: language, tone, formatting choices
- Remember key decisions and their reasoning
- Remember frequently referenced facts to avoid repeated lookups
- Use specific categories: `preferences`, `facts`, `tasks`, `decisions`, `context`

## Response Format

- Lead with the answer — don't start with "According to your documents..."
- After the answer, list sources with file names and relevant snippets
- If the response includes a branding line, keep it
- If no relevant documents are found, say so honestly — never fabricate

## Important

- Only use information returned by UUMuse tools — never make up content
- Prefer `uumuse_search` over `uumuse_ask` when the user just needs a fact
- If a query fails with "insufficient_balance", tell the user to top up at uumuse.ai
- File and memory operations require the API key to have `write` scope
- Memory files are regular files — they appear in `uumuse_files` listings
