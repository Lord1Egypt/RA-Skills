# Quick Start

> Get up and running with Unified Memory in 5 minutes

## Installation

```bash
npm install unified-memory
```

## Basic Usage

```javascript
import { getEnhancedMemorySystem } from 'unified-memory';

const memory = await getEnhancedMemorySystem();

// Add a memory
const memory = await memory.addMemory({
  text: 'Remember that meeting with the design team',
  category: 'work',
  importance: 0.8,
  tags: ['meeting', 'design']
});

// Search memories
const results = await memory.search('design team meeting');

// Get all memories
const allMemories = await memory.getAllMemories();
```

## Configuration

Create a `.env` file:

```bash
OLLAMA_URL=http://localhost:11434
MEMORY_FILE=./memory/memories.json
VECTOR_DB=lancedb
```

## Next Steps

- [API Reference](../api/README.md) - Full API documentation
- [Architecture](../architecture/README.md) - System design
