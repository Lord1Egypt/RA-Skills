---
name: memory-manager
description: Long-term memory management system for OpenClaw agents. Automatically archives conversations, organizes memories, and provides semantic search capabilities.
version: "1.0.0"
author: xiucheng
type: skill
tags: [memory, long-term, archiving, search, persistence]
homepage: https://github.com/xiucheng/memory-manager
license: MIT
---

# Memory Manager

A robust long-term memory management system for OpenClaw agents that automatically archives conversations and enables intelligent memory retrieval.

## Features

- 📝 **Automatic Conversation Logging**: Saves dialogues to daily memory files
- 🔍 **Semantic Search**: Retrieve relevant memories using natural language queries  
- 📅 **Time-based Organization**: Memories organized by date (YYYY-MM-DD.md)
- 🗂️ **Long-term Storage**: Curated memories in MEMORY.md
- 🔗 **Integration Ready**: Works with existing agent workflows

## Installation

```bash
clawhub install memory-manager
```

## Usage

### Automatic Mode
The skill automatically saves conversations during agent operation.

### Manual Memory Search
```python
from memory_manager import MemoryManager

mm = MemoryManager()
results = mm.search_memory("project discussions about KPI")
```

### Daily Log Structure
```
memory/
├── 2026-03-07.md
├── 2026-03-06.md
└── ...
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| memory_dir | ./memory/ | Daily memory files location |
| memory_file | ./MEMORY.md | Long-term memory file |
| auto_save | true | Auto-save conversations |

## Requirements

- Python 3.8+
- OpenClaw workspace structure

## License

MIT License - Contribute back to the community!
