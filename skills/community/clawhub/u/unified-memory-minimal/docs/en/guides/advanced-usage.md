# Advanced Usage Guide

> Advanced features for power users: version control, deduplication, export, profiles, and more.

## 📚 Table of Contents

1. [Version Control](#-version-control)
2. [Deduplication](#-deduplication)
3. [Export & Import](#-export--import)
4. [Memory Profiles](#-memory-profiles)
5. [Preference Management](#-preference-management)
6. [Tier Management](#-tier-management)
7. [Quality & Decay](#-quality--decay)
8. [Prompt Composition](#-prompt-composition)

## 🔄 Version Control

Track changes and restore previous versions of memories.

### List Versions
```javascript
const { memoryVersion } = require('unified-memory');

const versions = await memoryVersion({
  action: "list",
  memoryId: "mem_xxx",
  limit: 10
});
```

### Compare Versions (Diff)
```javascript
const diff = await memoryVersion({
  action: "diff",
  memoryId: "mem_xxx",
  versionId1: "v1",
  versionId2: "v2"
});
```

### Restore Version
```javascript
await memoryVersion({
  action: "restore",
  memoryId: "mem_xxx",
  versionId: "v1",
  preview: false  // Set true to preview without restoring
});
```

## 🔀 Deduplication

Find and merge duplicate memories.

### Find Duplicates (Dry Run)
```javascript
const { memoryDedup } = require('unified-memory');

const duplicates = await memoryDedup({
  threshold: 0.85,  // Similarity threshold (0-1)
  dryRun: true      // Preview only
});
```

### Merge Duplicates
```javascript
// Actually merge duplicates
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: false
});
```

### Dedup Response
```javascript
{
  found: 5,
  merged: 3,
  candidates: [
    {
      original: "mem_xxx",
      duplicate: "mem_yyy",
      similarity: 0.92,
      merged: true
    }
  ]
}
```

## 📤 Export & Import

### Export Formats

```javascript
const { memoryExport } = require('unified-memory');

// Export as JSON
await memoryExport({
  format: "json",
  output: "~/exports/memories.json"
});

// Export as Markdown
await memoryExport({
  format: "markdown",
  output: "~/exports/memories.md"
});

// Export as CSV
await memoryExport({
  format: "csv",
  output: "~/exports/memories.csv"
});
```

### Export with Filters
```javascript
await memoryExport({
  format: "json",
  output: "~/exports/work-memories.json",
  category: "preference",
  minImportance: 0.7,
  tags: ["work"]
});
```

## 👤 Memory Profiles

Get aggregated user profiles with static/dynamic separation.

```javascript
const { memoryProfile } = require('unified-memory');

const profile = await memoryProfile({
  scope: "user",        // "agent", "user", "team", "global"
  container_tag: "project-x",
  entity_filter: "preferences",
  static_days: 30,      // Days without access to mark as static
  limit: 100
});
```

### Profile Response
```javascript
{
  scope: "user",
  static: {
    preferences: [
      { key: "language", value: "Python", confidence: 0.95 },
      { key: "meeting_time", value: "morning", confidence: 0.85 }
    ],
    lastUpdated: "2026-03-15"
  },
  dynamic: {
    recent_topics: ["project-x", "deadlines", "meetings"],
    interaction_count: 42
  }
}
```

## ❤️ Preference Management

Unified preference slots with confidence scores.

### Get Preference
```javascript
const { memoryPreference } = require('unified-memory');

const pref = await memoryPreference({
  action: "get",
  key: "meeting_preference"
});
```

### Set Preference
```javascript
await memoryPreference({
  action: "set",
  key: "preferred_language",
  value: "Python",
  confidence: 0.9,
  source: "explicit"
});
```

### Update Preference
```javascript
await memoryPreference({
  action: "update",
  key: "preferred_language",
  value: "JavaScript",
  confidence: 0.85
});
```

### Merge Preferences
```javascript
await memoryPreference({
  action: "merge",
  slots: {
    language: { value: "TypeScript", confidence: 0.9 },
    editor: { value: "VS Code", confidence: 0.95 }
  }
});
```

### Delete Preference
```javascript
await memoryPreference({
  action: "delete",
  key: "old_preference"
});
```

### Infer Preferences
```javascript
const inferred = await memoryPreference({
  action: "infer",
  messageCount: 20
});
```

### Preference Actions

| Action | Description |
|--------|-------------|
| `get` | Get single preference |
| `set` | Create new preference |
| `update` | Update existing preference |
| `merge` | Merge multiple preferences |
| `delete` | Delete preference |
| `reset` | Reset all preferences |
| `stats` | Get preference statistics |
| `explain` | Explain preference confidence |
| `infer` | Infer from conversation |

## 📊 Tier Management

HOT/WARM/COLD tier operations.

### Check Tier Status
```javascript
const { memoryTier } = require('unified-memory');

const status = await memoryTier({
  action: "status"
});
```

### Migrate Memory to Tier
```javascript
await memoryTier({
  action: "migrate",
  memories: [{ id: "mem_xxx", targetTier: "COLD" }],
  apply: true
});
```

### Compress Memories
```javascript
await memoryTier({
  action: "compress",
  memories: [{ id: "mem_xxx" }],
  apply: true
});
```

### Redistribute Tiers
```javascript
await memoryTier({
  action: "redistribute",
  apply: true
});
```

### Tier Thresholds

| Tier | Age | Compression | Eligible for Dedup |
|------|-----|------------|-------------------|
| HOT | ≤ 7 days | None | Yes |
| WARM | 7-30 days | Light | Yes |
| COLD | > 30 days | Heavy | Yes |

Pinned memories are **never** compressed or deduplicated.

## ⭐ Quality & Decay

### Quality Scoring
```javascript
const { getMemoryQuality } = require('unified-memory');

const quality = await getMemoryQuality("mem_xxx");
```

### Time-Based Decay
Memories automatically decay in importance over time unless accessed.

## 📝 Prompt Composition

Compose memory context blocks for prompt injection.

```javascript
const { memoryCompose } = require('unified-memory');

const context = await memoryCompose({
  messages: [
    { role: "user", content: "What about the project deadline?" },
    { role: "assistant", content: "The project deadline is next Friday." }
  ],
  targetTokens: 2000,
  categories: ["fact", "preference"],
  query: "project deadline",
  messageWindow: 10
});
```

### Composition Priority
Memories are included in this order:
1. **PINNED** - Always included
2. **HOT** - Recently accessed (≤ 7 days)
3. **WARM** - Medium-term (7-30 days)
4. **COLD** - Older memories (> 30 days)

## 🔍 Advanced Search

### Maximum Marginal Relevance (MMR)
```javascript
const { memoryEngine } = require('unified-memory');

const results = await memoryEngine({
  action: "mmr",
  query: "project updates",
  documents: [{ id: "1", text: "..." }],
  topK: 5,
  lambda: 0.5  // Balance relevance vs diversity
});
```

### Reranking
```javascript
const ranked = await memoryEngine({
  action: "rerank",
  query: "meeting notes",
  documents: [{ id: "1", text: "..." }],
  method: "keyword"  // or "llm", "cross"
});
```

## 🧪 Testing & Verification

### Run Health Check
```javascript
const { memoryHealth } = require('unified-memory');

const health = await memoryHealth();
```

### Get Metrics
```javascript
const { memoryMetrics } = require('unified-memory');

const metrics = await memoryMetrics();
```

### WAL Operations
```javascript
const { memoryWal } = require('unified-memory');

// Initialize WAL
await memoryWal({
  action: "init",
  runId: "run-001"
});

// Flush WAL
await memoryWal({
  action: "flush"
});

// List WAL entries
const entries = await memoryWal({
  action: "list"
});
```

## 📚 Next Steps

- [Plugin Development](./plugins.md) - Build custom plugins
- [Integration Guide](./integration.md) - Connect to other systems
- [API Reference](../api/overview.md) - Complete API docs
- [Architecture Overview](../architecture/overview.md) - System design
