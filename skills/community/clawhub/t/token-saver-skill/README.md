# TokenSaver for OpenClaw

> Smart Token Cost Optimization - Save 50-80% on AI Token Usage

## Overview

TokenSaver automatically reduces AI token consumption while maintaining response quality. It intelligently compresses conversation context, caches similar queries, and optimizes prompts.

## Features

| Feature | Description | Savings |
|---------|-------------|---------|
| **Smart Compression** | Hierarchical context compression based on importance scoring | 50-70% |
| **Semantic Cache** | Multi-level caching (exact → semantic → pattern) | 30-50% |
| **Quality Guard** | Prevents over-compression, auto-rollback if quality drops | Safety |
| **Adaptive Mode** | Auto-adjusts compression based on token pressure | Optimal |
| **Transparent UI** | Real-time savings indicator with detailed stats | Visibility |

## Installation

```bash
npx clawhub@latest install tokensaver
```

## Commands

```bash
/tokens           # Show status and stats
/tokensave        # Aggressive mode (max savings)
/tokenbalance     # Balanced mode (default)
/tokenquality     # Quality priority (min compression)
/tokenreport      # Detailed usage report
/tokencache clear # Clear cache
/tokenoff         # Disable temporarily
```

## How It Works

### Smart Compression
```
Original: 8,000 tokens of conversation history
↓
TokenSaver analyzes message importance (0-100 score)
↓
Level 0: Recent 5 messages (full)
Level 1: Messages 6-15 (summarized)
Level 2: Messages 16-30 (key points only)
Level 3: 30+ messages (critical info only)
↓
Optimized: 2,400 tokens
Savings: 70%
```

### Semantic Cache
```
Query 1: "How to write a file in Python?" → Process & cache
Query 2: "Python file write method?" → L2 semantic match → Cached result
Query 3: "JavaScript file write?" → L3 pattern match → Similar response
```

### Adaptive Stages
| Token Count | Action | Compression |
|-------------|--------|-------------|
| < 3K | No action | None |
| 3-6K | Light optimization | Light |
| 6-10K | Medium compression | Medium |
| > 10K | Heavy + suggest new chat | Heavy |

## Configuration

```json
{
  "tokenSaver": {
    "enabled": true,
    "defaultMode": "adaptive",
    "compression": {
      "alwaysKeep": 5,
      "qualityThreshold": 0.85
    },
    "cache": {
      "enabled": true,
      "ttl": 3600
    }
  }
}
```

## Safety Features

- **Never Compress**: Code blocks, errors, user-marked important messages
- **Auto Rollback**: If quality drops > 15%, restores original context
- **One-Click Restore**: `/tokens original` to see uncompressed version
- **Snapshots**: Every compression creates rollback point

## Expected Savings

| Scenario | Original | Optimized | Savings |
|----------|----------|-----------|---------|
| Tech discussion (50 rounds) | 12K tokens | 3.5K tokens | 71% |
| Code review | 25K tokens | 5K tokens | 80% |
| General chat | 8K tokens | 2K tokens | 75% |

## License

MIT
