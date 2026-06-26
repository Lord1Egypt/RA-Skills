---
name: deep-research-suite
version: 1.0.0
description: Deep Research Suite - One command to aggregate, analyze, and synthesize research from multiple sources. Search → Extract → Summarize → Report.
emoji: 🔬
tags: [research, automation, productivity, analysis, ai-agent]
---

# Deep Research Suite 🔬

One command to aggregate, analyze, and synthesize research from multiple sources.

## What It Does

```
Input: "Research AI agent memory management trends 2026"

Output:
1. Search 5+ sources
2. Extract key findings
3. Identify patterns
4. Generate structured report
5. Save to file for reference
```

## Research Pipeline

### Stage 1: Multi-Source Search
```
Sources to check:
- Web search (general)
- GitHub (code/examples)
- Hacker News (discussions)
- ArXiv (papers, if relevant)
- Reddit (community opinions)
- News sites (recent articles)
```

### Stage 2: Content Extraction
```
For each source:
1. Fetch content
2. Extract main points
3. Identify key facts/statistics
4. Note source credibility
5. Tag by topic relevance
```

### Stage 3: Synthesis
```
Combine findings:
- Group by theme
- Identify consensus views
- Note contradictions
- Highlight emerging trends
- Flag outdated info
```

### Stage 4: Report Generation
```
Output format:

# Research Report: [Topic]
**Date**: YYYY-MM-DD
**Sources**: X sources analyzed

## Executive Summary
[2-3 sentence overview]

## Key Findings

### Trend 1: [Name]
- Source: X, Y, Z
- Evidence: ...
- Implications: ...

### Trend 2: [Name]
...

## Contradictions / Debates
- View A says: ... (Source: X)
- View B says: ... (Source: Y)
- Assessment: ...

## Actionable Insights
1. ...
2. ...

## Sources
- [Source 1](url) - relevance: high
- [Source 2](url) - relevance: medium
```

## Usage Examples

### Quick Research
```
User: "What's new in LLM context window management?"

Agent:
[Searching 5 sources...]
[Extracting key findings...]
[Synthesizing...]

## LLM Context Window Management - 2026 Update

### Key Trends
1. **Dynamic Context Sizing** - Models now auto-adjust context based on task complexity
2. **Semantic Chunking** - Replace fixed-size chunks with meaning-based segments
3. **Context Compression** - 10x compression with minimal info loss

[Full report saved to memory/research/llm-context-2026-04-21.md]
```

### Deep Dive
```
User: "Deep research on AI agent subagent architecture patterns"

Agent:
[This will take 5-10 minutes for comprehensive analysis]

Stage 1/4: Multi-source search...
- GitHub: 15 repos found
- Papers: 3 relevant
- Discussions: 12 threads

Stage 2/4: Content extraction...
- Analyzing top 10 GitHub repos...
- Extracting paper findings...
- Summarizing discussions...

Stage 3/4: Synthesis...
- Identified 4 architecture patterns
- Found 2 debates
- 3 emerging trends

Stage 4/4: Report generation...

[Report saved to memory/research/subagent-architecture-2026-04-21.md]
```

### Competitive Analysis
```
User: "Compare popular AI agent memory solutions"

Agent:
[Generating comparison matrix...]

| Solution | Approach | Pros | Cons | Stars |
|----------|----------|------|------|-------|
| Mem0 | Persistent memory | Easy integration | Limited context | 25k |
| Letta | Stateful agents | Full state | Complex setup | 15k |
| LangGraph | Graph memory | Flexible | Learning curve | 100k |

[Full comparison saved to memory/research/memory-solutions-comparison.md]
```

## Output Files

All research saved to `memory/research/`:
```
memory/research/
├── llm-context-2026-04-21.md
├── subagent-architecture-2026-04-21.md
└── memory-solutions-comparison.md
```

## Integration with Other Skills

- **Workflow Checkpoint** - Research is a multi-step workflow
- **Memory Guard** - Save key findings to long-term memory
- **Content Creator** - Generate polished reports

## Anti-Patterns

❌ Don't rely on single source
❌ Don't skip source credibility check
❌ Don't present outdated info as current
❌ Don't fabricate sources or statistics

## License

MIT
