# Simple Local Memory 🧠

**Zero-dependency AI memory system. No API keys. No cloud. Just pure local storage.**

## Features

- ✅ **No API keys required** - 100% local operation
- ✅ **Intelligent search** - TF-IDF based local search with relevance scoring
- ✅ **Multi-layer storage** - Hot RAM + Persistent storage + Curated archive
- ✅ **Easy to use** - Simple CLI tools
- ✅ **Privacy focused** - Your data never leaves your machine
- ✅ **Works everywhere** - Claude Code, ChatGPT, Cursor, Copilot, any AI agent

## Quick Start

### 1. Install

```bash
# Local install (recommended)
npm install -g simple-local-memory

# Or use without installing
npx simple-local-memory memory-init
```

### 2. Initialize

```bash
cd your-project
memory-init
```

This creates:
- `SESSION-STATE.json` - Active working memory
- `MEMORY.md` - Long-term curated memory
- `memories/` - Directory for memory storage

### 3. Start Using

```bash
# Store a memory
memory-store --content "User prefers dark mode" --type preference --importance 0.9

# Search memories
memory-search "CSS preferences"

# Check status
memory-stats
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `memory-init` | Initialize memory system |
| `memory-store` | Store a new memory |
| `memory-search` | Search memories |
| `memory-list` | List recent memories |
| `memory-stats` | Show memory statistics |
| `memory-export` | Export memories to file |
| `memory-import` | Import memories from file |

## Usage Examples

### Store a User Preference

```bash
memory-store \
  --content "User prefers TypeScript over JavaScript" \
  --type preference \
  --importance 0.95 \
  --tags typescript,language,preference
```

### Store a Decision

```bash
memory-store \
  --content "Use React for frontend, not Vue" \
  --type decision \
  --importance 0.9 \
  --context "Discussed during architecture planning"
```

### Store a Lesson Learned

```bash
memory-store \
  --content "Always validate user input on both client and server side" \
  --type lesson \
  --importance 0.9 \
  --tags security,validation
```

### Search Memories

```bash
# General search
memory-search "frontend framework"

# Search by type
memory-search "React" --type decision

# Recent memories only
memory-search "API" --days 7

# Limit results
memory-search "CSS" --limit 5
```

### List Memories

```bash
# List all recent
memory-list

# List by type
memory-list --type preference

# List specific date
memory-list --date 2026-03-15

# Limit results
memory-list --limit 10
```

## Memory Types

| Type | When to Use | Default Importance |
|------|-------------|-------------------|
| `preference` | User likes/dislikes | 0.5 |
| `decision` | Project decisions | 0.5 |
| `fact` | Important information | 0.5 |
| `lesson` | Learned from mistakes | 0.5 |

Set importance from 0.0 to 1.0:
- **0.8-1.0**: Critical (always include)
- **0.5-0.7**: Important (usually relevant)
- **0.0-0.4**: Nice to have

## Integration with AI Agents

### Claude Code

Add to your custom instructions or project notes:

```markdown
## Memory Protocol

When I give you important information:
1. Update SESSION-STATE.json
2. Store it using memory-store command
3. Then respond to me

When starting conversation:
1. Read SESSION-STATE.json
2. Search relevant: memory-search "topic"
3. Check MEMORY.md for context
```

### ChatGPT Custom Instructions

```
You have access to local memory tools. When the user shares important information:
1. First update SESSION-STATE.json
2. Then use memory-store to save it
3. Then respond

When starting, read SESSION-STATE.json and search for relevant context.
```

### Cursor / IDEs

Create a `.cursorrules` or similar file:

```
When user expresses preferences or decisions:
1. Document in SESSION-STATE.json
2. Store using: memory-store --type preference --content "..."
3. Maintain context across sessions

Memory commands available:
- memory-store: Save information
- memory-search: Find past context
- memory-stats: Check memory health
```

## File Structure

```
your-project/
├── SESSION-STATE.json       # Active working memory
├── MEMORY.md                # Curated long-term memory
└── memories/
    ├── 2026-03-15.json      # Daily memories
    ├── preferences.json     # User preferences
    ├── decisions.json       # Project decisions
    └── lessons.json         # Lessons learned
```

## WAL Protocol (Write-Ahead Logging)

**CRITICAL**: Save to memory BEFORE responding

| User Action | Agent Response Order |
|-------------|---------------------|
| States preference | Update SESSION-STATE → Store → Respond |
| Makes decision | Update SESSION-STATE → Store → Respond |
| Corrects you | Update SESSION-STATE → Store → Respond |
| Gives deadline | Update SESSION-STATE → Store → Respond |

This ensures context is never lost, even if response fails.

## Search Algorithm

The search uses a scoring system:

```
Total Score = Relevance Score + Recency Boost + Importance
```

- **Relevance**: TF-IDF like matching
- **Recency Boost**: Recent memories get higher scores (decays over 7 days)
- **Importance**: Manual importance weighting (0.0-1.0)

## Best Practices

### DO ✓
- Be specific: "User prefers dark mode for code editors"
- Add context: "Decided during team meeting on 2026-03-15"
- Use importance: Critical items get 0.9+, nice-to-haves get 0.5
- Tag properly: Helps with retrieval
- Review weekly: Archive important items to MEMORY.md

### DON'T ✗
- Store everything: Not every conversation needs saving
- Be vague: "User has a preference" vs "User prefers TypeScript"
- Ignore context: Why was this decision made?
- Forget maintenance: Review and clean up regularly

## Maintenance

### Daily
```bash
memory-stats  # Check system health
```

### Weekly
- Review SESSION-STATE.json - archive completed tasks
- Move important insights to MEMORY.md
- Clean up low-importance memories

### Monthly
```bash
# Export backup
memory-export --format json --output monthly-backup.json

# Clean old files (keep what you need)
rm memories/2026-02-*.json  # Example: remove Feb logs
```

## Comparison with elite-longterm-memory

| Feature | Elite | Simple Local |
|---------|-------|--------------|
| API keys | Required (OpenAI) | None |
| Dependencies | LanceDB, Mem0 | None |
| Cloud sync | Yes | No (optional) |
| Vector search | OpenAI embeddings | Local TF-IDF |
| Auto-extraction | Mem0 service | Manual |
| Privacy | Cloud-dependent | 100% local |
| Cost | Free tier limits | 100% free |
| Setup complexity | Medium | Simple |

## Advanced Usage

### Programmatic Usage

```javascript
const MemoryCore = require('simple-local-memory');

const memory = new MemoryCore('/path/to/project');

// Store a memory
memory.storeMemory('User prefers dark mode', {
  type: 'preference',
  importance: 0.9,
  tags: ['ui', 'preferences']
});

// Search memories
const results = memory.searchMemories('UI preferences', {
  limit: 5,
  type: 'preference'
});

// Get statistics
const stats = memory.getStats();
console.log(`Total memories: ${stats.totalMemories}`);

// Update session state
memory.updateSessionState({
  current_task: 'Build authentication system',
  key_context: ['User wants JWT tokens'],
  pending_actions: ['Create login form', 'Setup JWT middleware']
});
```

### Export/Import

```bash
# Export to JSON
memory-export --format json --output backup.json

# Export to Markdown
memory-export --format markdown --output readable-backup.md

# Import from backup
memory-import --file backup.json
```

## Troubleshooting

**"memories not being saved"**
→ Check file permissions
→ Verify disk space
→ Check JSON syntax

**"search returns nothing"**
→ Verify memories/ directory exists
→ Try broader search terms
→ Check that memories were actually stored

**"SESSION-STATE.json too large"**
→ Archive old items to memory-store
→ Move completed tasks to MEMORY.md
→ Keep only active context

## Future Enhancements

Potential additions (community contributions welcome):

- [ ] Local embedding models (Transformers.js)
- [ ] Memory compression for old entries
- [ ] Encryption for sensitive data
- [ ] Sync via GitHub Gist
- [ ] Web UI for memory management
- [ ] Automatic deduplication
- [ ] Memory expiry dates
- [ ] Relationship graph between memories

## License

MIT

## Contributing

Contributions welcome! This is an open-source project.

---

**No API keys. No cloud. No tracking. Just pure local memory.**

Perfect for privacy-conscious users, offline development, and building custom AI agents.
