# Cognitive Patterns from Frontier Models

> Thinking patterns and heuristics observed in GLM-4, Kimi K2.5, Claude Opus, and GPT-4.5 that produce exceptional outputs.

---

## Pattern 1: The "Step Back" Maneuver ⏮️

**What**: Before diving into details, zoom out to see the bigger picture.

**How to apply**:
```
When given a specific question:
1. Ask: "What domain does this belong to?"
2. Ask: "What is the user's ACTUAL goal?" (not just stated question)
3. Ask: "What constraints am I not seeing?"
4. THEN answer the specific question with this context
```

**Example:**
> User: "How do I optimize this SQL query?"
> 
> Step Back: "This is a database performance question. The actual goal is likely faster user-facing operations. Constraints might include: can't change schema, needs to work with existing ORM, must maintain ACID compliance."
> 
> → Answer addresses not just query optimization but also indexing strategy, caching layers, and ORM configuration.

---

## Pattern 2: Multi-Scale Analysis 🔬🔭

**What**: Analyze at multiple zoom levels simultaneously.

**How to apply**:
```
For any complex system or problem:
- Micro: Individual components, lines of code, specific facts
- Meso: Interactions between components, modules, paragraphs
- Macro: Overall architecture, thesis, strategic implications

Never stay at one level. Constantly cross-reference between levels.
```

**Example in code review:**
> Micro: "This line has a potential null pointer"
> Meso: "This function doesn't handle the error case that calls it"
> Macro: "The entire error handling strategy needs revision"

---

## Pattern 3: Contrastive Thinking ⚖️

**What**: Define what something IS by understanding what it is NOT.

**How to apply**:
```
When explaining a concept or recommending a solution:
1. State the positive case clearly
2. Explicitly state what it is NOT: "This is NOT..."
3. Compare with alternatives: "Unlike X, this approach..."
4. Define boundaries: "This works when..., but not when..."
```

**Why it works**: Eliminates ambiguity. Shows deep understanding. Prevents misapplication.

---

## Pattern 4: Temporal Reasoning ⏳

**What**: Consider time as a critical dimension.

**How to apply**:
```
For any recommendation or analysis:
- Past: "How did we get here? What historical decisions led to this?"
- Present: "What is the current state? What are the immediate constraints?"
- Future: "What happens in 1 week? 1 month? 1 year?"
- Branching: "If we choose A, timeline is X. If B, timeline is Y."
```

---

## Pattern 5: Constraint Relaxation 🧘

**What**: Solve an easier version first, then add constraints back.

**How to apply**:
```
When stuck on a hard problem:
1. Remove the hardest constraint mentally
2. Solve the relaxed problem
3. Now add constraints back one by one
4. For each constraint: "How does this change the solution?"
5. The final solution often emerges from understanding the relaxed version
```

---

## Pattern 6: Analogical Transfer 🌉

**What**: Map solutions from one domain to another.

**How to apply**:
```
When facing a novel problem:
1. Abstract the problem: "At its core, this is about..."
2. Search mental database: "Where have I seen this pattern before?"
3. Map the analogy explicitly:
   - Source domain: [known system]
   - Target domain: [current problem]
   - Mapping: A↔X, B↔Y, C↔Z
4. Validate: "Does the analogy break down anywhere?"
5. Adapt solution from source to target
```

---

## Pattern 7: Inversion Thinking 🙃

**What**: Instead of "How do I achieve X?", ask "How do I guarantee failure at X?"

**How to apply**:
```
For goal-setting or problem-solving:
1. State the goal: "We want to improve API latency"
2. Invert: "How do we GUARANTEE terrible API latency?"
   - No caching
   - N+1 queries
   - Synchronous external calls
   - No connection pooling
3. Invert again: "Therefore, we must do the opposite"
   - Implement caching
   - Eliminate N+1 queries
   - Make external calls async
   - Use connection pooling
```

**Why it works**: Often easier to identify failure modes than success paths.

---

## Pattern 8: The 5 Whys (Root Cause Analysis) ❓

**What**: Iteratively ask "why" to find root causes.

**How to apply**:
```
For any problem or symptom:
Problem: "The server is crashing"
Why 1: "Because memory usage spikes"
Why 2: "Because the cache grows unbounded"
Why 3: "Because we don't have cache eviction"
Why 4: "Because we assumed data would stay small"
Why 5: "Because we didn't design for scale"

Root cause: Design assumption failure
Solution: Implement bounded cache with LRU eviction + capacity planning
```

---

## Pattern 9: Pre-Mortem Analysis 💀

**What**: Imagine the project failed spectacularly. Why?

**How to apply**:
```
Before committing to a plan:
1. Imagine it's 6 months later and the project failed
2. Generate 5-10 plausible failure reasons
3. For each: "How could we prevent this NOW?"
4. Build prevention into the plan
5. Identify early warning signals for each failure mode
```

---

## Pattern 10: Second-Order Thinking 🌊

**What**: Consider the consequences of consequences.

**How to apply**:
```
For any action or decision:
- First-order: Direct immediate effect
- Second-order: Effect of the effect (1-3 months)
- Third-order: Long-term systemic changes (6-12 months)
- Unintended: What side effects might emerge?

Example:
Action: "Add a new feature quickly"
1st: Users get new capability
2nd: Technical debt accumulates, team morale drops
3rd: Refactor becomes necessary, velocity slows
Unintended: Competitors copy feature, advantage neutralized
```

---

## Pattern 11: The Steel Man 🏗️

**What**: Strengthen the opposing argument before attacking it.

**How to apply**:
```
When disagreeing or evaluating alternatives:
1. State the opposing view in its STRONGEST form
   - "The best version of their argument is..."
2. Acknowledge what is valid in it
3. Only THEN present your critique
4. "Their view is strong because X, but it fails on Y because..."
```

**Why it works**: Builds credibility. Shows intellectual honesty. Leads to better solutions.

---

## Pattern 12: Cognitive Load Management 🧠📊

**What**: Don't overwhelm working memory. Externalize thinking.

**How to apply**:
```
During complex reasoning:
1. WRITE DOWN intermediate results
2. Use structured formats (lists, tables, diagrams)
3. Number your steps explicitly
4. Summarize before proceeding: "So far we have established..."
5. If lost, backtrack to last known good state
```

---

## Quick Reference Card

| Situation | Pattern to Use |
|-----------|---------------|
| Stuck on hard problem | Constraint Relaxation |
| Need creative solution | Analogical Transfer + First Principles |
| Evaluating alternatives | Contrastive Thinking + Steel Man |
| Planning project | Temporal Reasoning + Pre-Mortem |
| Debugging | 5 Whys + Abductive Reasoning |
| Making decision | Second-Order Thinking + Probabilistic |
| Explaining complex concept | Multi-Scale + Contrastive |
| Risk assessment | Inversion + Pre-Mortem |
| Disagreement | Steel Man + Adversarial |
