# Three-Tier Optimization Strategies Explained

## L1: Prompt Compression & Output Truncation (Effect 10-30%)

### Specific Actions

**1. System Prompt Streamlining**
```diff
- "You are a professional, patient, and meticulous AI assistant, skilled at analyzing problems and providing comprehensive, organized, and in-depth answers..."
+ "Professional AI assistant. Provide concise answers."
```

**2. max_tokens Limiting**
Set output limits based on task type:
- Simple Q&A: max_tokens=200
- Routine tasks: max_tokens=500
- Long-form generation: max_tokens=1500

**3. History Message Pruning**
When conversations exceed 20 rounds, delete the earliest 1/3 of history messages (preserving recent context).

### Quantified Effect

| Scenario | Tokens Before | Tokens After | Savings |
|----------|---------------|--------------|---------|
| Simple Q&A | 800/session | 500/session | 37% |
| Code Review | 2000/session | 1400/session | 30% |
| Long-form Text | 5000/session | 3500/session | 30% |

---

## L2: Conversation Summary Caching (Effect 30-50%)

### Specific Actions

**1. High-Frequency Question FAQ Shortcuts**
```python
# Pseudocode example
faq_cache = {
    "What's the weather today?": "Beijing, sunny, 25°C",
    "What's my name?": "Determined based on context",
}
# Cache hit → Return directly, no API call
```

**2. Dynamic Summary Compression**
After every N conversation rounds, compress history into a single summary:
```
[Summary] User is working on project X, discussed issues Y and Z, currently at stage Z.
```

**3. Reference Document Caching**
Store user-provided documents, code, contracts, etc., in a vector database; subsequent questions are answered via retrieval.

### Quantified Effect

| Scenario | Cost/Month Before | Cost/Month After | Savings |
|----------|-------------------|------------------|---------|
| 10 rounds/day × 30d | $90 | $45 | 50% |
| 30 rounds/day × 30d | $270 | $162 | 40% |
| 100 rounds/day × 30d | $900 | $450 | 50% |

---

## L3: Model Downgrade + Task Routing (Effect 50-70%)

### Model Routing Strategy

| Task Type | Route To | Cost Reduction |
|-----------|----------|----------------|
| Simple Q&A, Translation | gpt-4o-mini / claude-haiku | 90% |
| Normal Tasks, Summarization | gpt-4o / claude-sonnet | 50% |
| Complex Reasoning, Long Context | gpt-4-turbo / claude-opus | Baseline |

### Configuration Example (OpenAI API)

```python
def route_model(task_type, complexity):
    if complexity == "low":
        return "gpt-4o-mini"
    elif complexity == "medium":
        return "gpt-4o"
    else:
        return "gpt-4-turbo"
```

### Quantified Effect

| Monthly Calls | All 4o | Smart Routing | Savings |
|---------------|--------|---------------|---------|
| 5,000 | $75 | $23 | 69% |
| 20,000 | $300 | $95 | 68% |
| 50,000 | $750 | $240 | 68% |

---

## Pitfalls to Avoid

### ❌ Common Mistakes

1. **Over-compressing system prompt**
   - Consequence: Unstable model behavior, degraded output quality
   - Suggestion: Retain core directives; remove "polite fluff," not "constraints"

2. **Setting max_tokens too low**
   - Consequence: Truncated output, incomplete answers
   - Suggestion: Estimate + 20% buffer, gradually reduce to find the optimal value

3. **Caching without expiration**
   - Consequence: Outdated information leading to incorrect answers
   - Suggestion: Set TTL for FAQ; periodically refresh summary caches

4. **One-size-fits-all model downgrade**
   - Consequence: Simple tasks using cheaper models may waste more due to retries
   - Suggestion: Use a classifier to assess task complexity first, then route

5. **Premature L3 optimization**
   - Consequence: Incomplete routing rules degrade user experience
   - Suggestion: Validate L1+L2 effects first, then introduce L3

### ✅ Best Practices

- Record a baseline after each optimization phase and compare effects
- Keep detailed cost logs for analysis
- L3 routing should include a "downgrade failure auto-upgrade" fallback strategy
- Periodically (monthly) review token consumption trends