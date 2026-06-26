---
name: token-efficient-agent
description: Advanced techniques for minimizing token consumption in OpenClaw operations while maintaining or improving response quality. Includes memory optimization, document processing strategies, tool call efficiency, and contextual awareness methods specifically designed for the OpenClaw architecture.
---

# Token-Efficient Agent

## Overview

This skill provides advanced, battle-tested techniques for minimizing token consumption in OpenClaw operations. Unlike basic tips, these strategies are specifically tailored to OpenClaw's architecture, tool ecosystem, and memory system. By implementing these methods, you can reduce token usage by 60-80% while maintaining or improving response quality and contextual awareness.

## Why Token Efficiency Matters in OpenClaw

OpenClaw's strength lies in its ability to access personal data, memories, and tools. However, each operation consumes tokens:
- Memory retrieval loads context into the model's window
- Tool calls return data that must be processed
- Long conversations build up in session history
- Document fetching brings in external content

Without optimization, simple queries can consume thousands of tokens unnecessarily, leading to:
- Slower response times
- Higher computational costs
- Reduced ability to handle complex multi-step tasks
- Potential context window overflow

## Core Architecture-Aware Principles

### 1. Leverage OpenClaw's Memory Hierarchy
OpenClaw has distinct memory layers with different access costs:
- **Session Context** (free, but limited): Current conversation turn
- **Working Memory** (low cost): Recently loaded snippets via memory_search/get
- **Long-term Memory** (higher cost): MEMORY.md and daily files
- **External Data** (highest cost): Documents, web search, tool results

**Strategy**: Always start with the cheapest available context that might contain the answer.

### 2. Exploit Tool Semantics, Not Just Interfaces
Each OpenClaw tool has specific optimization parameters. Understanding these allows precision data retrieval rather than brute-force fetching.

### 3. Apply Progressive Disclosure
Retrieve information in layers: first get metadata/summaries, then only dive deep when necessary based on initial results.

### 4. Cache and Reuse
OpenClaw sessions retain loaded data. Structure your workflow to maximize reuse of already-fetched information.

## Advanced Techniques

### Technique 1: Hierarchical Memory Querying

Instead of: Loading entire memory files or searching broadly
Use: A multi-stage search approach that minimizes data transfer

**Stage 1: Broad Search with Minimal Results**
```python
memory_search(query="project deadline decision", maxResults=1, minScore=0.8)
```
- Only 1 result reduces data transfer significantly
- High minScore ensures relevance

**Stage 2: Targeted Snippet Extraction**
```python
# If Stage 1 returns a relevant file:
memory_get(path="memory/2026-03-10.md", from=42, lines=8)
```
- Extract only the exact relevant lines
- Avoids loading unnecessary surrounding context

**Stage 3: Cross-Reference Validation (Only if Needed)**
```python
# Only if Stage 2 is ambiguous:
memory_search(query="project deadline", file_path="memory/2026-03-10.md", maxResults=2)
```
- Constrain search to already-identified relevant file

**Token Savings**: Typically reduces memory loading by 70-90% compared to loading full daily files.

### Technique 2: Document Processing with Semantic Pagination

Instead of: Fetching entire documents then searching
Use: Offset-limited fetching combined with semantic boundary detection

**For Long Documents (>5000 chars):**
1. **Initial Probe**: Fetch first 1500 chars to determine document structure
   ```python
   feishu_fetch_doc(doc_id="doc_xxx", limit=1500)
   ```
2. **Structural Analysis**: Ask model to identify likely sections (without loading full doc)
3. **Targeted Fetching**: Only retrieve sections that appear relevant
   ```python
   # If conclusions are likely in last 20%:
   feishu_fetch_doc(doc_id="doc_xxx", offset=8000, limit=1500)
   ```

**For Known Section Documents:**
- Use document outline/search features if available
- Fetch by section headers when possible

**Token Savings**: Avoids loading irrelevant document portions, often saving 60-80% of document processing tokens.

### Technique 3: Tool Call Fusion and Batching

Instead of: Making multiple separate tool calls for related data
Use: Combine operations where tools support it, or sequence calls to minimize context switching

**Memory-Tool Fusion Pattern:**
```python
# Instead of:
# 1. memory_search() -> get file path
# 2. feishu_fetch_doc() -> load document
# 3. Process document

# Do:
# 1. memory_search() with doc-specific query to get both memory context AND doc hints
# 2. If memory contains sufficient summary, skip document fetch entirely
# 3. Only fetch document if memory search indicates high-value target
```

**Web Search Optimization:**
- Use `count=3` instead of default 10 for initial searches
- Add `freshness` parameter when temporal relevance is known
- Chain search results: use first result to refine subsequent searches

**Tool Savings**: Reduces tool call overhead and eliminates redundant data processing by 40-60%.

### Technique 4: Contextual Summarization Cascades

Instead of: Passing raw data to model for processing
Use: Progressive summarization where each stage reduces data size while preserving decision-relevant information

**Three-Level Summary Cascade:**
1. **Extractive Summary** (Tool-level): Use `feishu_fetch_doc` with smart offsets to get key portions
2. **Abstractive Summary** (Model-level): Brief prompt to condense extracted content
3. **Decision-Focused Summary** (Task-level): Further reduce to only information needed for current decision

**Example Workflow for Document-Based Questions:**
```python
# Level 1: Get structurally important parts (headings, conclusions, tables)
section1 = feishu_fetch_doc(doc_id, offset=0, limit=800)      # Intro
section2 = feishu_fetch_doc(doc_id, offset=-1000, limit=1000) # Conclusion (approx end)

# Level 2: Ask for thematic summary
summary_prompt = f"Provide a 3-sentence summary of the key points in this text: {section1[:400]}...{section2}"

# Level 3: Task-specific reduction
final_prompt = f"Based on this summary: {summary}, answer ONLY: [specific question]"
```

**Token Savings**: Reduces document processing tokens by 75-90% while preserving answer quality.

### Technique 5: Predictive Context Preloading (Anticipatory Caching)

Instead of: Reactive loading after each user query
Use: Predictive loading based on conversation patterns and time/context cues

**Implementation:**
- During lulls in conversation (or during heartbeat cycles), predict likely next queries
- Preload relevant memory snippets or document summaries
- Store in session context for instant access

**Prediction Signals:**
- Time of day (regular meeting times)
- Recent topics (if discussing X, likely to discuss Y next)
- External triggers (calendar events, time-based patterns)
- User behavior patterns (learned over time)

**Example**: If user always asks about project status at 10 AM, preload project-related memory snippets at 9:45 AM.

**Efficiency Gain**: Converts high-cost reactive operations to near-zero-cost proactive operations.

### Technique 6: Tool Result Minimization and Transformation

Instead of: Using raw tool outputs
Use: Transform tool results to their minimal essential form before model consumption

**Patterns:**
- **Feishu Document Comments**: Instead of loading full comment threads, use `feishu_doc_comments` with `is_solved=true/false` filters and `page_size=1`
- **Web Search Results**: Extract only titles and snippets, discard full content unless absolutely needed
- **Calendar Events**: Request only `summary` and `start_time` fields when possible, not full descriptions
- **Search User Results**: Often just need `name` and `open_id`, not full profile data

**Implementation**: Create wrapper functions that:
1. Call tool with minimal necessary parameters
2. Extract only essential fields from response
3. Discard metadata unless specifically needed for downstream operations

**Token Savings**: Typically 50-80% reduction in tool result processing tokens.

### Technique 7: Session Context Pruning and Compression

Instead of: Letting session history grow unbounded
Use: Active management of conversational context to maintain optimal token budget

**Strategies:**
- **Summarization Windows**: Every 10-15 exchanges, summarize previous conversation and replace with summary
- **Relevance Scoring**: Before adding new exchange to context, score its likely future relevance
- **Topic Segmentation**: Maintain separate contexts for different topics, load only relevant one
- **Forgetting Curves**: Naturally decay less-recent exchanges unless reinforced

**OpenClaw-Specific Implementation:**
- Use memory system to store conversation summaries instead of keeping all in session context
- During heartbeat cycles, run context optimization procedures
- Leverage the existing memory consolidation philosophy

## Advanced Workflow: The Token-Efficient Decision Tree

When faced with any request, follow this decision process:

```
START
│
├──→ Can answer from current session context? 
│     │ Yes → Respond directly (0 additional tokens)
│     │ No  → Continue
│
├──→ Is answer likely in recent memory (last 3 days)?
│     │ Yes → Use memory_search with tight constraints (maxResults=1, minScore=0.85)
│     │     → If found, use memory_get for exact lines
│     │     → If not found or ambiguous, continue
│     │ No  → Continue
│
├──→ Does answer require document/external data?
│     │ No → Use web_search with count=3, freshness if applicable
│     │ Yes → Continue to document processing
│
├──→ Document Processing Decision:
│     │
│     │→ Is document structured with known sections?
│     │   Yes → Fetch only likely relevant sections using offset/limit
│     │   No  → 
│     │     │→ Is document < 2000 chars?
│     │     │   Yes → Fetch entire document
│     │     │   No  → 
│     │     │     │→ Fetch first 1500 chars for structure analysis
│     │     │     │→ Based on analysis, fetch only relevant portions
│     │     │     │→ Apply summarization cascade if still large
│
├──→ Apply result minimization: extract only essential fields
│
├──→ If result still large for model input, apply summarization
│
└──→ Formulate response using minimized context
```

## Integration with OpenClaw Systems

### Heartbeat Optimization
Use heartbeat cycles for:
- Background memory consolidation
- Predictive preloading based on time/patterns
- Context window cleanup and summarization
- Learning user patterns for better prediction

### Memory System Synergy
- Store summaries and extracted insights in memory, not raw data
- Use memory_search as primary retrieval mechanism, not sequential file reading
- Leverage memory's semantic understanding to reduce need for exact keyword matching

### Tool-Specific Optimizations

**Feishu Document Fetching:**
- Always use offset/limit for documents > 2000 chars
- Use `feishu_doc_comments` with filters instead of fetching all comments
- For tables, consider if you need full data or just aggregates/statistics

**Web Operations:**
- Prefer `web_search` over `web_fetch` when possible (returns already-processed snippets)
- When fetching, use `extractMode="text"` for non-formatting needs
- Set aggressive `maxChars` limits (1000-2000) unless full content essential

**Calendar/Task Queries:**
- Request only essential fields (title, time, status)
- Use time range limits to constrain results
- Leverage recurrence expansion intelligently

## Measurement and Improvement

Track your efficiency with these metrics:

1. **Tokens per Exchange**: Monitor average token usage per conversation turn
2. **Cache Hit Ratio**: Percentage of answers found in already-loaded context
3. **Tool Call Efficiency**: Average useful data returned per tool call
4. **Context Reuse Rate**: How often loaded data is reused in subsequent operations

**Improvement Loop:**
1. Baseline: Measure current token usage
2. Implement one technique at a time
3. Measure impact
4. Retain techniques that show >20% improvement
5. Combine complementary techniques

## Advanced Examples

### Example 1: Cross-Reference Historical Decision

**Request**: "How did our decision on vendor X in January compare to our current leaning toward vendor Y?"

**Traditional Approach**:
- Load January memory file (full)
- Load recent memory/file about vendor Y
- Manually compare

**Token-Efficient Approach**:
1. `memory_search(query="vendor X decision January", maxResults=1, minScore=0.9, relative_time="last_month")`
2. `memory_get(path="memory/2026-01-15.md", from=87, lines=12)`  // Exact decision snippet
3. `memory_search(query="vendor Y evaluation", maxResults=1, minScore=0.85)`  // Recent notes
4. `memory_get(path="memory/2026-03-16.md", from=34, lines=8)`  // Current leaning
5. Feed only these 4 short snippets to model for comparison

**Token Usage**: ~150 tokens vs ~2000+ for traditional approach

### Example 2: Meeting Preparation Briefing

**Request**: "Give me a briefing on the upcoming project review meeting."

**Traditional Approach**:
- Fetch meeting description
- Load all related documents
- Read entire email thread
- Summarize manually

**Token-Efficient Approach**:
1. Calendar lookup: Get meeting time, title, attendees (essential fields only)
2. `memory_search(query="project review", maxResults=2, relative_time="this_week")`
3. Extract only action items and decisions from memory results
4. If documents mentioned, fetch only executive summaries/conclusions
5. Synthesize briefing from minimal context

**Token Usage**: ~300 tokens vs ~3000+ for traditional approach

## Limitations and When Not to Apply

These techniques are less effective when:
- User explicitly requests comprehensive analysis
- True random access to large datasets is required
- Legal/compliance requirements mandate full data review
- The user is testing or evaluating the system's knowledge depth

In these cases, be transparent about the trade-offs and get explicit consent before applying optimization.

## Conclusion

Token efficiency in OpenClaw isn't about cutting corners—it's about applying the right amount of computational effort to each task. By leveraging OpenClaw's specific architecture, memory system, and tool capabilities, you can dramatically reduce unnecessary token consumption while maintaining high-quality, contextually appropriate responses.

The key insight: **Most user queries don't require comprehensive data review—they need precise, relevant information delivered efficiently.** These techniques help you deliver exactly that.

Practice these methods consistently, measure their impact, and adapt them to your specific usage patterns. Over time, token-efficient operation will become second nature, allowing you to handle more complex tasks within the same computational budget.