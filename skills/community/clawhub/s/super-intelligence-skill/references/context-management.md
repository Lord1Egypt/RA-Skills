# Context Management & Long-Context Optimization

> Techniques for handling large contexts efficiently — matching the 2M+ token context capabilities of frontier models like Kimi K2.5.

---

## Principle 1: Progressive Disclosure Architecture 📚

**Don't load everything at once. Use tiered access:**

```
Tier 1 - Identity (Always Loaded):
  - Who you are
  - Current task
  - Available tools/skills

Tier 2 - Relevant Context (Loaded on Demand):
  - Specific documents needed for current sub-task
  - Previous conversation turns relevant to NOW
  - Active skill instructions

Tier 3 - Reference Material (Loaded When Referenced):
  - Full API documentation
  - Complete codebases
  - Historical archives

Tier 4 - Background (Rarely Loaded):
  - General knowledge (already in model weights)
  - Irrelevant past conversations
  - Outdated information
```

---

## Principle 2: The Index-First Approach 📇

**Before reading full documents, build/search an index:**

```
When given large documents:
1. SCAN: Quickly identify structure (headings, sections, key terms)
2. INDEX: Create mental or explicit map:
   - Section A: covers topics X, Y
   - Section B: contains data about Z
   - Section C: has examples of W
3. QUERY: Only read sections relevant to current question
4. CROSS-REFERENCE: Link related sections
5. SYNTHESIZE: Combine insights from multiple sections
```

---

## Principle 3: Context Compression 🗜️

**Summarize and compress before context grows too large:**

```
When context approaches limits:
1. IDENTIFY REDUNDANCY: Remove repeated information
2. SUMMARIZE OLD TURNS: 
   - "Turns 1-5: We established X, decided Y, rejected Z"
3. EXTRACT KEY FACTS: 
   - Convert paragraphs to bullet points
   - Convert bullet points to single phrases
4. PRIORITIZE:
   - Keep: User's original request, current plan, recent findings
   - Compress: Older reasoning steps, explored dead-ends
   - Drop: Fully resolved sub-tasks, acknowledged greetings
```

---

## Principle 4: Working Memory Management 🧠

**Maintain clean working memory:**

```
Active Working Memory (keep in mind):
□ Current objective
□ Active hypotheses/plan
□ Recent tool results
□ Open questions

Archive (refer when needed):
□ Resolved sub-problems
□ Background context
□ Previous versions of plan

Clear (remove from attention):
□ Fully completed tasks
□ Irrelevant digressions
□ Superseded information
```

---

## Principle 5: The "Re-read Before Answering" Rule 📖

**When context is large, verify before concluding:**

```
Before finalizing answer involving large context:
1. "What specific evidence supports my conclusion?"
2. Re-read those specific sections
3. "Did I miss anything contradictory?"
4. Search for disconfirming evidence
5. Only then finalize

This prevents "hallucinating" based on partial reading.
```

---

## Principle 6: Temporal Context Awareness ⏰

**Track what happened when:**

```
Maintain mental timeline:
- [T-0] User's original request
- [T-1] First analysis/approach
- [T-2] Tool results/findings
- [T-3] Revised approach
- [T-now] Current state

When user asks follow-up:
- "Earlier you said X, has that changed?"
- Reference specific points in timeline
- Note when information was obtained
```

---

## Principle 7: Multi-Document Synthesis 📑

**When combining information from multiple sources:**

```
Source A says: [extract with citation]
Source B says: [extract with citation]
Source C says: [extract with citation]

Synthesis:
- Agreement: "Both A and B confirm X"
- Conflict: "A claims Y but B claims Z. Resolution:..."
- Gap: "No source addresses W; inference:..."
- Novel insight: "Combining A's data with B's method suggests..."
```

---

## Principle 8: The "Context Budget" Mindset 💰

**Treat context as a limited resource:**

```
Allocation Strategy:
- 30%: Task instructions and current plan
- 40%: Relevant source material/evidence
- 20%: Working memory (intermediate results)
- 10%: Buffer for unexpected needs

When budget is tight:
- Prefer summaries over full text
- Use references/pointers instead of inline content
- Offload to external storage when possible
```

---

## Principle 9: State Checkpointing 🚩

**Save mental state at key points:**

```
After completing major sub-task:
CHECKPOINT:
- What was accomplished
- Key findings/decisions
- Open issues
- Next planned step

If context gets corrupted or lost:
- Can resume from last checkpoint
- Don't need to restart from scratch
```

---

## Principle 10: Active Forgetting 🗑️

**Strategically forget to maintain focus:**

```
When switching tasks or topics:
1. Acknowledge transition: "Moving from X to Y..."
2. Archive X-related context
3. Load Y-relevant context
4. Explicitly state: "For Y, the relevant facts are..."

This prevents cross-contamination between unrelated tasks.
```

---

## Long-Context Specific Techniques

### For Codebases:
```
1. Map architecture first (directories, key files)
2. Identify entry points and data flow
3. Trace specific execution paths when needed
4. Don't try to hold entire codebase in memory
```

### For Documents:
```
1. Read table of contents/headings
2. Identify key sections for current task
3. Deep-read relevant sections
4. Skim irrelevant sections (note they exist)
5. Synthesize across sections
```

### For Conversations:
```
1. Summarize each turn's key points
2. Track unresolved threads
3. Note user preferences/stated constraints
4. Reference specific turns when needed
```
