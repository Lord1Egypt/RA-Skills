# SoulForge Architecture

## Overview

SoulForge is a memory evolution system that continuously reads AI agent memory sources, discovers patterns using MiniMax API, and automatically updates workspace identity files.

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         SoulForge                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │   Memory     │ ──▶ │  Pattern     │ ──▶ │   Soul       │   │
│  │   Reader     │     │  Analyzer    │     │  Evolver     │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │ memory/*.md │     │  MiniMax     │     │ SOUL.md       │   │
│  │ .learnings/ │     │  API         │     │ USER.md       │   │
│  │ hawk-bridge │     │              │     │ IDENTITY.md   │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Module Design

### soulforge.config.SoulForgeConfig

Configuration management. Loads from:
1. `soulforge/config.json` (file)
2. Environment variables (env overrides)
3. Runtime arguments (overrides)

Key settings:
- `workspace`: Agent workspace path
- `memory_paths`: Where to read memories from
- `target_files`: Files to potentially update
- `trigger_threshold`: Min occurrences before update
- `backup_enabled`: Whether to backup before writes

### soulforge.memory_reader.MemoryReader

Reads memory entries from multiple sources:

1. **Daily Logs** (`memory/*.md`)
   - Parsed by date (YYYY-MM-DD)
   - Content extracted (no markdown formatting)
   - Categorized as "conversation"

2. **Learnings** (`.learnings/*.md`)
   - LEARNINGS.md → categories: correction, insight, knowledge_gap, best_practice
   - ERRORS.md → category: error
   - FEATURE_REQUESTS.md → category: feature_request

3. **hawk-bridge Vector Store** (optional)
   - LanceDB `hawk_memories` table
   - Recent 50 entries loaded
   - Requires lancedb package

Returns: `List[MemoryEntry]` sorted newest-first

### soulforge.analyzer.PatternAnalyzer

Uses MiniMax API to:
1. Analyze memory entries for recurring patterns
2. Map patterns to appropriate target files
3. Generate update content
4. Return structured `DiscoveredPattern` objects

**API Call Flow:**
```
SYSTEM_PROMPT + USER_PROMPT (entries + existing content)
    ↓
MiniMax Chat Completion API
    ↓
JSON Response Parse
    ↓
List[DiscoveredPattern]
```

**Pattern Structure:**
```python
@dataclass
class DiscoveredPattern:
    pattern_id: str
    target_file: str        # Which file to update
    update_type: str       # SOUL | USER | IDENTITY | MEMORY | AGENTS | TOOLS
    category: str          # behavior | preference | decision | error | etc.
    summary: str           # One-line description
    content: str           # Content to add
    confidence: float      # 0.0 - 1.0
    evidence_count: int    # Times observed
    source_entries: List[str]  # Source file references
    suggested_section: str  # Where in the target file
```

### soulforge.evolver.SoulEvolver

Safely applies patterns to target files:

1. **Duplicate Detection**: Skip patterns already in file
2. **Backup**: Create timestamped backup before write
3. **Incremental Write**: Append update block, never overwrite
4. **Dry Run**: Preview without writing

**Update Block Format:**
```markdown
<!-- SoulForge Update | 2026-04-05T12:00:00+08:00 -->
## Pattern Summary

**Source**: memory/2026-04-05.md, .learnings/LEARNINGS.md
**Pattern Type**: behavior
**Confidence**: High (observed 4 times)

**Content**:
User prefers numbered lists when selecting options.

<!-- /SoulForge Update -->
```

## Data Flow

```
1. CLI invokes soulforge.py run
         ↓
2. SoulForgeConfig loads configuration
         ↓
3. MemoryReader reads all sources → List[MemoryEntry]
         ↓
4. PatternAnalyzer calls MiniMax API
         ↓
5. MiniMax returns JSON with proposed updates
         ↓
6. PatternAnalyzer parses → List[DiscoveredPattern]
         ↓
7. SoulEvolver filters by threshold
         ↓
8. SoulEvolver checks for duplicates
         ↓
9. SoulEvolver creates backup
         ↓
10. SoulEvolver appends update blocks to files
         ↓
11. Summary printed
```

## Error Handling

| Error | Handling |
|-------|----------|
| No API key | Exit with error message |
| No memory entries | Exit gracefully with message |
| API call fails | Log error, return empty patterns |
| JSON parse fails | Log warning, skip malformed response |
| File write fails | Log error, continue with other files |
| Duplicate pattern | Skip silently, count in results |

## Extension Points

### Adding New Memory Sources

Subclass `MemoryReader` or add to `_read_*` methods:

```python
def _read_my_source(self) -> None:
    """Add new source reader."""
    source_dir = self.workspace / "my-source"
    for file in source_dir.glob("*.md"):
        entry = MemoryEntry(
            source=str(file.relative_to(self.workspace)),
            source_type="my_source",
            category="custom",
            content=self._extract_text_content(file.read_text()),
            timestamp=file.stem,
            importance=0.7,
        )
        self._entries.append(entry)
```

### Adding New Target Files

1. Add filename to `target_files` in config
2. Update `USER_PROMPT_TEMPLATE` in `analyzer.py` to know about it
3. Add update type mapping in the prompt

### Custom API Provider

Subclass `PatternAnalyzer` and override `_call_minimax`:

```python
class CustomAnalyzer(PatternAnalyzer):
    def _call_minimax(self, system: str, user: str) -> str:
        # Use different API
        return my_custom_llm_call(system, user)
```
