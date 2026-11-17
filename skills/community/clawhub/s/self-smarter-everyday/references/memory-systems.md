# Memory Systems Architecture for Self-Improving Agents

## Overview

Memory is the foundation of self-improvement. An agent that cannot remember cannot learn from experience. This document describes a comprehensive memory architecture designed for AI agents that need to persist, retrieve, update, and eventually forget information in a structured and efficient manner. The architecture draws from cognitive science models of human memory, database management principles, and practical patterns from existing self-improving agent implementations.

## Tiered Memory Model

Inspired by CPU cache hierarchies and database storage tiering, we implement a three-tier memory system optimized for different access patterns and persistence requirements.

### HOT Memory (Active Working Context)
**Characteristics:**
- Always loaded in current context window
- Immediate access, no retrieval latency
- Size: bounded by model context window (~128K tokens)
- Volatile: lost when session ends
- Contains: current task state, active conversation, working buffer

**Contents:**
- Active session messages and context
- Currently relevant skill instructions
- Working memory for complex reasoning chains
- Temporary variables and intermediate results
- Active goal state and plan

**Management:**
- Automatically managed by the runtime
- Agent has no direct control over what's in HOT memory
- Context window pressure triggers implicit demotion (older content becomes less accessible)

### WARM Memory (Session-Persistent)
**Characteristics:**
- Persisted across turns within a session
- Accessible via explicit retrieval (file reads, memory_search)
- Size: effectively unlimited (file system backed)
- Semi-volatile: persists during session, may be archived after
- Contains: session-specific knowledge, accumulated context

**Contents:**
- Session-specific notes and observations
- Task results from earlier in the session
- Retrieved memories relevant to current work
- Sub-agent outputs and evidence
- Session-specific temporary files

**Management:**
- Agent explicitly reads/writes WARM memory
- Promoted from HOT when context window fills
- Demoted to COLD at session end if not flagged for persistence
- Indexed for search via QMD (memory_search)

### COLD Memory (Permanent Store)
**Characteristics:**
- Persisted indefinitely across all sessions
- Requires explicit retrieval (search, file read)
- Size: effectively unlimited (file system + database)
- Permanent: survives session boundaries, container restarts
- Contains: accumulated knowledge, learned patterns, historical records

**Contents:**
- MEMORY.md (long-term memory index)
- memory/*.md (daily logs, incident reports)
- LESSONS.md (accumulated lessons learned)
- skills/ (learned procedures and capabilities)
- SOUL.md, USER.md (core identity and user model)
- Historical session archives
- Performance metrics and trends

**Management:**
- Explicit write operations required for updates
- Regular compaction and pruning to maintain efficiency
- Semantic indexing for retrieval (QMD/memory_search)
- Periodic review and consolidation during 2 AM reflection

## Memory Operations

### Promotion (Lower → Higher Tier)
Promotion moves information from a lower tier to a higher tier when it becomes relevant.

**COLD → WARM Promotion Triggers:**
- memory_search returns a result (loaded into WARM)
- File read operation (content loaded into WARM)
- Skill invocation (skill instructions loaded into WARM)
- Session start (relevant memories pre-loaded based on context)

**WARM → HOT Promotion Triggers:**
- Information referenced in current reasoning
- Active task requires the information
- User explicitly asks about the information
- Pattern match with current context

**Promotion Rules:**
1. Relevance is the primary criterion for promotion
2. Recency is a secondary criterion (recent > old when equally relevant)
3. Frequency of access matters (frequently accessed > rarely accessed)
4. Promoted content must fit within HOT memory bounds
5. When HOT is full, least-relevant content is implicitly demoted

### Demotion (Higher → Lower Tier)
Demotion moves information from a higher tier to a lower tier when it's no longer immediately needed.

**HOT → WARM Demotion Triggers:**
- Context window pressure (automatic)
- Task completion (task-specific context no longer needed in HOT)
- Turn boundary (previous turn's details move to WARM)

**WARM → COLD Demotion Triggers:**
- Session end (valuable session knowledge persisted to COLD)
- Information not accessed for N turns (lazy demotion)
- Explicit agent decision to persist something for future sessions

**Demotion Rules:**
1. Never lose information without first persisting to lower tier
2. Demoted content should be summarized/compacted when possible
3. Flag important content to prevent demotion past its useful life
4. Demotion is not deletion — content remains accessible via search

## Compaction Strategies

As memory accumulates, it must be compacted to maintain efficiency. Unbounded memory growth leads to slower retrieval, higher token costs, and signal-to-noise degradation.

### Temporal Compaction
**Process:** Merge multiple entries from the same time period into a single summary.
**Example:** 30 daily memory files from January → 1 monthly summary
**When:** Monthly, or when file count exceeds threshold
**Implementation:**
```
1. Read all entries from the period
2. Extract key themes and events
3. Generate consolidated summary
4. Archive original entries (move to archive/ folder)
5. Update MEMORY.md index to point to summary
```

### Semantic Compaction
**Process:** Merge entries about the same topic that are scattered across time.
**Example:** 15 lessons about Docker debugging → 1 comprehensive Docker troubleshooting guide
**When:** During 2 AM reflection when topic clusters are detected
**Implementation:**
```
1. Search for entries sharing common themes
2. Extract unique insights from each entry
3. Synthesize into comprehensive reference
4. Cross-reference from original locations
5. Update relevant skill files
```

### Redundancy Elimination
**Process:** Identify and remove duplicate or near-duplicate information.
**Example:** Same lesson recorded in 3 different memory files
**When:** During weekly deep reflection
**Implementation:**
```
1. Search for overlapping content
2. Identify the most complete/accurate version
3. Consolidate into single authoritative source
4. Add cross-references from removed locations
5. Update indexes
```

## Namespace Isolation

Different types of memory serve different purposes and should be isolated to prevent interference.

### Memory Namespaces
| Namespace | Purpose | Location | Access Pattern |
|-----------|---------|----------|----------------|
| Identity | Core personality, values | SOUL.md, IDENTITY.md | Read on session start |
| User Model | User preferences, context | USER.md, USER-*.md | Read on session start |
| Episodic | Specific events, interactions | memory/YYYY-MM-DD.md | Search by date/topic |
| Semantic | Facts, knowledge, references | MEMORY.md, TOOLS.md | Search by topic |
| Procedural | How-to knowledge, skills | skills/*/SKILL.md | Load when task matches |
| Lessons | Learned improvements | LESSONS.md, lessons/ | Search by pattern |
| Working | Current task state | Session context | Always in HOT |
| Archive | Historical records | archive/ | Rare access |

### Isolation Rules
1. **Identity namespace is read-only** during normal operation — changes require explicit user approval
2. **Episodic memories are append-only** during a session — edits happen during reflection
3. **Procedural memories (skills) have version control** — changes go through Skill Workshop
4. **Working memory is session-scoped** — never directly persisted without explicit action
5. **Archive namespace is write-once** — files are never modified after archival

## Conflict Resolution

When multiple memory sources provide conflicting information, a resolution strategy is needed.

### Conflict Types
1. **Temporal conflict**: New information contradicts old information
2. **Source conflict**: Different sources provide different facts
3. **Context conflict**: Information valid in one context but not another

### Resolution Strategies
| Conflict Type | Strategy | Example |
|---------------|----------|---------|
| Temporal | Newest wins (with validation) | User changed preference → update USER.md |
| Source | Higher-authority source wins | SOUL.md overrides inferred behavior |
| Context | Both valid, add context tags | "Works for Python" vs "Works for JavaScript" |

### Resolution Process
```
1. Detect conflict (contradictory information retrieved)
2. Classify conflict type
3. Apply resolution strategy
4. Update affected memory entries
5. Record resolution in daily log
6. If ambiguous, flag for user clarification
```

## Decay Functions

Not all memories are equally important forever. Decay functions model the decreasing relevance of memories over time.

### Exponential Decay Model
```
Relevance(t) = Initial_Relevance × e^(-λt)
```
Where:
- t = time since last access
- λ = decay rate (tunable per namespace)

### Decay Rates by Namespace
| Namespace | Decay Rate | Rationale |
|-----------|------------|-----------|
| Identity | 0 (no decay) | Core identity should be stable |
| User Model | Very slow (λ=0.001) | Preferences change slowly |
| Episodic | Fast (λ=0.1) | Specific events lose relevance quickly |
| Semantic | Medium (λ=0.01) | Facts remain relevant but may become outdated |
| Procedural | Very slow (λ=0.005) | Working procedures remain useful |
| Lessons | Slow (λ=0.005) | Lessons should persist but be reviewed |
| Working | Very fast (λ=0.5) | Task context becomes irrelevant quickly |

### Decay in Practice
- Memories with relevance below threshold are candidates for compaction
- Decay does NOT mean deletion — content remains in archive
- Access resets the decay timer (use it → it stays relevant)
- Critical memories can be flagged as "undying" (no decay)

## Memory Statistics and Health

### Key Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| Total memory files | Count of files across all namespaces | < 500 active |
| Memory index size | Size of MEMORY.md | < 500 lines |
| Search latency | Time for memory_search to return | < 2 seconds |
| Cache hit rate | % of memory needs met by WARM/HOT | > 60% |
| Staleness | % of memories not accessed in 30+ days | < 30% |
| Compaction ratio | Size after / size before compaction | > 3:1 |
| Conflict frequency | Conflicts detected per week | < 5 |

### Health Checks (During 2 AM Reflection)
```
1. MEMORY.md size check — if > 500 lines, trigger compaction
2. Staleness scan — identify memories not accessed in 30+ days
3. Conflict scan — search for contradictory entries
4. Index integrity — verify all referenced files exist
5. Namespace balance — ensure no namespace is growing disproportionately
6. Lesson implementation rate — are recorded lessons being applied?
```

## Cross-Namespace Inheritance

Some memory properties should propagate across namespaces:

### Inheritance Rules
1. **User preferences propagate to all namespaces**: If user prefers concise format, all memory writes should be concise
2. **Identity constraints propagate to procedural memory**: Skills must align with agent identity
3. **Lessons propagate to procedural memory**: When a lesson implies a procedure change, update the skill
4. **Episodic patterns propagate to semantic memory**: Repeated events become knowledge

### Inheritance Mechanism
```
During 2 AM reflection:
1. Check episodic memories for recurring patterns
2. If pattern detected 3+ times → promote to semantic memory
3. Check lessons for procedural implications
4. If lesson implies skill change → queue skill update
5. Check user model for preference changes
6. If preference changed → audit all namespaces for compliance
```

## Integration with Existing Patterns

### OpenClaw Memory System
The tiered memory model integrates with OpenClaw's existing memory infrastructure:
- **QMD indexing** provides semantic search over COLD memory
- **memory_search** is the primary retrieval interface
- **memory_get** provides exact excerpt retrieval
- **Session context** serves as HOT memory
- **File system** backs WARM and COLD tiers

### Self-Improving Skill Patterns
The existing self-improving skill establishes patterns we extend:
- **self-improving/memory.md** → becomes part of COLD episodic memory
- **self-improving/corrections.md** → becomes part of COLD lessons namespace
- **Daily reflection cycle** → becomes the compaction/consolidation trigger
- **LESSONS.md** → becomes the lessons namespace index

## Conclusion

A well-designed memory system is the prerequisite for genuine self-improvement. The tiered approach (HOT/WARM/COLD) optimizes for both speed and persistence. Promotion and demotion rules ensure the right information is available at the right time. Compaction strategies prevent unbounded growth. Namespace isolation prevents interference between different types of knowledge. Decay functions model natural relevance decline. And health monitoring ensures the system remains efficient over time. Together, these mechanisms create a memory architecture that scales with the agent's experience while maintaining retrieval efficiency and knowledge quality.
