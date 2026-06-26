# Multi-Agent Orchestration Patterns

Detailed patterns for designing multi-agent workflows in Claude Code.

## Core Principles

> **"Agent architecture should reflect the dependency graph of the task"**
> — Anthropic Multi-Agent Research

If subtasks don't read or modify each other's state, run them **parallel**.
If previous output is next input, run them **sequential**.

## Parallel vs Sequential Decision Criteria

| Condition | Recommended Pattern |
|-----------|-------------------|
| Subtasks are independent (no shared state) | **Parallel** |
| Previous step output is next step input | **Sequential** |
| Diverse perspectives/expertise needed | **Parallel** (Fan-out) |
| Result coherence/consistency important | **Sequential** |
| Proposals need validation before action | **2-Phase** (Generate→Validate) |

## Anthropic's 6 Composable Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Prompt Chaining** | Sequential steps, each output is next input | Data transformation pipelines |
| **Routing** | Branch to specialized agents by input type | Multi-domain processing |
| **Parallelization** | Independent tasks run simultaneously | Multi-angle analysis, speed optimization |
| **Orchestrator-Worker** | Dynamic task assignment | Complex coding/research |
| **Evaluator-Optimizer** | Generate→Evaluate iteration loop | Quality improvement needed |
| **Autonomous Agent** | Minimal intervention, environment feedback | Long-running tasks |

## 2-Phase Pipeline Pattern

For workflows generating proposals that need validation:

```
Phase 1: Analysis/Generation (Parallel)
┌──────────┬──────────┬──────────┐
│ Agent A  │ Agent B  │ Agent C  │  ← Independent analysis
└────┬─────┴────┬─────┴────┬─────┘
     │          │          │
     └──────────┼──────────┘
                ↓
Phase 2: Validation (Sequential)
┌─────────────────────────────────┐
│         Validator Agent         │  ← Validate Phase 1 results
└─────────────────────────────────┘
```

### Application Examples

**Session wrap workflow:**
- Phase 1: doc-updater, automation-scout, learning-extractor, followup-suggester (parallel)
- Phase 2: duplicate-checker (sequential)

**Code review workflow:**
- Phase 1: security-reviewer, style-checker, performance-analyzer (parallel)
- Phase 2: final-reviewer (sequential)

**Research workflow:**
- Phase 1: source-finder, fact-checker, perspective-gatherer (parallel)
- Phase 2: synthesizer (sequential)

## State Management Principles

```
❌ Avoid:
- Mutable state shared between concurrent agents
- Assuming synchronous updates across agent boundaries
- Assuming independence without explicit verification

✅ Recommend:
- Isolate agents as much as possible
- Pass state explicitly via output_key
- Define conflict resolution strategy for result aggregation
- Pass lightweight references (not full data)
```

## Anti-Patterns

| Anti-Pattern | Problem | Alternative |
|--------------|---------|-------------|
| Adding meaningless agents | Only increases complexity | Check if single agent sufficient first |
| Excessive multi-hop communication | Latency increase | Direct communication or parallelization |
| Unclear task boundaries | Duplicate work, gaps | Define clear objective, output format, boundaries |
| Rigid plan adherence | Can't adapt to runtime discoveries | Use adaptive orchestrator |

## Model Selection for Agents

| Use Case | Recommended Model |
|----------|------------------|
| Analysis requiring depth | `sonnet` or `opus` |
| Quick validation | `haiku` |
| Default/inherit from parent | `inherit` |
| Creative/complex reasoning | `opus` |
| Cost-sensitive batch operations | `haiku` |

## Implementing in Claude Code

### Parallel Execution

Send multiple Task calls in a single message:

```python
# All 4 agents start simultaneously
Task(subagent_type="agent-a", prompt="...")
Task(subagent_type="agent-b", prompt="...")
Task(subagent_type="agent-c", prompt="...")
Task(subagent_type="agent-d", prompt="...")
```

### Sequential Execution

Wait for previous result before next call:

```python
# First call
result_1 = Task(subagent_type="agent-a", prompt="...")

# Use result_1 in next call
Task(subagent_type="agent-b", prompt=f"Validate: {result_1}")
```

### Hybrid (2-Phase)

```python
# Phase 1: Parallel
Task(subagent_type="analyzer-1", prompt="...")
Task(subagent_type="analyzer-2", prompt="...")
Task(subagent_type="analyzer-3", prompt="...")

# Wait for all Phase 1 results

# Phase 2: Sequential (uses Phase 1 results)
Task(
    subagent_type="validator",
    prompt=f"""
    Validate these proposals:

    Analyzer 1: {result_1}
    Analyzer 2: {result_2}
    Analyzer 3: {result_3}
    """
)
```

## Agent Design for Multi-Agent Systems

### Clear Boundaries

Each agent should have:
- **Single responsibility**: One clear focus area
- **Defined inputs**: What it expects to receive
- **Structured output**: Consistent format for downstream consumption
- **No side effects**: Don't modify state other agents depend on

### Communication Protocol

```markdown
## Agent Output Format

### Summary
[One-line summary]

### Detailed Findings
[Structured analysis]

### Recommendations
[Actionable items with priorities]

### Confidence
[Self-assessment of analysis quality]
```

## Scaling Considerations

### When to Add More Agents

✅ Add agent when:
- Distinct expertise domain needed
- Independent analysis possible
- Clear boundary definable
- Reduces complexity vs. single agent

❌ Don't add agent when:
- Same expertise as existing agent
- Would create tight coupling
- Simple prompt modification sufficient
- Adds latency without value

### Performance Optimization

1. **Minimize Phase 2 agents**: Validation should be lightweight
2. **Right-size Phase 1**: 3-5 parallel agents typically optimal
3. **Use haiku for validation**: Fast, cheap, sufficient for checking
4. **Batch where possible**: Combine related analyses in single agent

## References

- [Anthropic Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Building AI Agents - Evaluator-Optimizer Pattern](https://research.aimultiple.com/building-ai-agents/)
