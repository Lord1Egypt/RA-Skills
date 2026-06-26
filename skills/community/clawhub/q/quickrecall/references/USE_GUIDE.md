# Memory Enhancement Engine — Usage Guide

## Installation

### Method 1: Copy files
```bash
# Copy to your project
cp -r memory-enhancement-engine ./my-project/
```

### Method 2: ClawHub
```bash
clawhub install memory-enhancement-engine
```

## Quick Start

### Basic Usage

```javascript
const { MemorySystem } = require('./memory-enhancement-engine/memory.js');

// Initialize
const mem = new MemorySystem();

// Store memories
mem.add({ content: "User prefers dark theme", importance: 1.5 });
mem.add({ content: "Billing is on the 15th of each month", importance: 1.2 });

// Search
const results = mem.query("dark mode preference");
console.log(results[0].content); // "User prefers dark theme"
console.log(results[0].score);   // 0.87 (example)

// Check status
const stats = mem.status();
console.log(`Memories stored: ${stats.count}`);
```

### CLI Tool

```bash
# View status
node memo.cjs status

# Search memories
node memo.cjs query "dark theme"

# View recent
node memo.cjs recent

# Compact old memories
node memo.cjs compact 5 0.3
```

### With Metadata

```javascript
mem.add({
  content: "Database connection string format",
  importance: 0.8,
  metadata: {
    tags: ["technical", "config"],
    source: "documentation",
    category: "backend"
  }
});

// Search with metadata context
const results = mem.query("database config");
```

## Best Practices

1. **Importance Levels** — Use 1.5+ for critical facts, 0.5-1.0 for normal info, 0.3 for ephemeral
2. **Compaction** — Run `compact()` periodically to keep memory lean (suggested: every 500 writes)
3. **Backup** — `MEMORY_STORE.json` is your persistence file; back it up regularly
4. **Capacity** — Default max 1000, adjust via constructor if needed

## Test

```bash
# Run test client
node scripts/test-client.js
```
