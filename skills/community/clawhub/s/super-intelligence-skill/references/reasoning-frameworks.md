# Reasoning Frameworks

> Advanced cognitive architectures extracted from frontier model behaviors (GLM-4, Kimi K2.5, Claude Opus, GPT-4.5).

---

## 1. Tree of Thoughts (ToT) 🌳

**When to use**: Complex problems with multiple valid paths (planning, debugging, creative tasks).

**Protocol:**

```
Phase 1: BRANCHING
- Generate 3-5 distinct solution paths
- For each path, write a 1-sentence thesis
- Tag each with estimated feasibility (0-100%)

Phase 2: EVALUATION  
- For each branch, identify:
  * Required resources/tools
  * Potential failure points
  * Time/effort estimate
  * Confidence score
- Prune branches below 40% confidence

Phase 3: EXPANSION
- Take top 2 branches and expand each into 3 sub-branches
- Repeat evaluation

Phase 4: SELECTION
- Choose the branch with best confidence × impact score
- Document why others were rejected
```

**Example application:**
> User: "How should I refactor this monolithic API?"
> 
> Branch A: Strangler Fig pattern (Confidence: 85%)
> Branch B: Big Bang rewrite (Confidence: 30%) 
> Branch C: Modular monolith first (Confidence: 75%)
> 
> → Select A with C as fallback plan.

---

## 2. Chain of Verification (CoVe) 🔍

**When to use**: Factual accuracy is critical (research, analysis, medical/legal advice).

**Protocol:**

```
Step 1: DRAFT
- Generate initial answer based on knowledge

Step 2: PLAN VERIFICATION
- List 3-5 specific claims that need verification
- For each: "How would I verify this?"

Step 3: EXECUTE VERIFICATION
- Use tools/search to check each claim
- Note: confidence levels, sources, contradictions

Step 4: CORRECT
- Revise draft based on verification results
- Explicitly mark what changed and why

Step 5: FINAL REVIEW
- "If I were skeptical, what would I question?"
- Address those questions proactively
```

---

## 3. System 2 Thinking (Slow/Deliberate) 🐢

**When to use**: High-stakes decisions, complex analysis, mathematical proofs.

**Protocol:**

Override System 1 (fast/intuitive) responses:

```
1. PAUSE: Resist immediate answer impulse
2. DECOMPOSE: "What are the component questions?"
3. ANALYZE EACH: Work through methodically
4. CHECK BIASES: 
   - Availability bias (am I using recent examples too heavily?)
   - Confirmation bias (am I only seeking supporting evidence?)
   - Anchoring bias (am I stuck on first impression?)
5. SYNTHESIZE: Build answer from verified components
6. SANITY CHECK: "Does this answer feel too simple? Too complex?"
```

---

## 4. First Principles Reasoning ⚛️

**When to use**: Novel problems, breaking conventional thinking, innovation.

**Protocol:**

```
1. IDENTIFY ASSUMPTIONS: List everything you "know" about this problem
2. STRIP TO FUNDAMENTALS: For each assumption, ask "Is this truly necessary?"
3. REBUILD FROM GROUND UP:
   - What are the absolute truths here?
   - What are the physical/mathematical/logical constraints?
   - What is actually possible vs. conventionally done?
4. GENERATE NOVEL SOLUTIONS: Based on fundamentals, not analogy
5. VALIDATE: Check against real-world constraints
```

---

## 5. Abductive Reasoning (Inference to Best Explanation) 🕵️

**When to use**: Diagnostic tasks, debugging, root cause analysis.

**Protocol:**

```
Given: Observation O

1. GENERATE HYPOTHESES:
   H1: [Explanation 1]
   H2: [Explanation 2]
   H3: [Explanation 3]

2. EVALUATE EXPLANATORY POWER:
   - Which best explains ALL observations?
   - Which requires fewest auxiliary assumptions?
   - Which is most falsifiable/testable?

3. PREDICTIVE CHECK:
   - If H1 is true, what else should we see?
   - Search for those predictions

4. SELECT BEST EXPLANATION:
   - Not necessarily "true", but "most warranted"
   - Maintain list of runner-up hypotheses
```

---

## 6. Adversarial Reasoning (Red Team Thinking) 🥊

**When to use**: Security analysis, robust solution design, debate preparation.

**Protocol:**

```
1. BUILD YOUR CASE: Create the strongest argument for position X

2. SWITCH ROLES: Now argue against X with equal vigor
   - What are the weakest points?
   - What evidence contradicts X?
   - When does X fail?

3. ITERATE:
   - Strengthen X against the attacks
   - Repeat until X survives all reasonable attacks

4. SYNTHESIS:
   - Present X with acknowledged limitations
   - "This is strong because..., but weak when..."
```

---

## 7. Probabilistic Thinking 🎲

**When to use**: Risk assessment, forecasting, decision under uncertainty.

**Protocol:**

```
For any prediction or recommendation:

1. BASE RATE: What's the historical frequency?
2. EVIDENCE UPDATE: How does new info change the probability?
3. CONFIDENCE INTERVAL: Give range, not point estimate
   - "60-80% chance" not "70% chance"
4. SCENARIO PLANNING:
   - Best case (20th percentile)
   - Expected case (50th percentile)  
   - Worst case (80th percentile)
5. PRE-MORTEM: "If this fails, what most likely caused it?"
```

---

## 8. Recursive Self-Improvement Loop 🔄

**When to use**: Any extended task where quality can be iteratively improved.

**Protocol:**

```
Iteration 1: Generate initial solution
Iteration 2: Critique solution (be harsh but fair)
Iteration 3: Generate improved solution addressing critiques
Iteration 4: Verify improvements didn't break anything
Iteration 5: Polish and finalize

STOP when:
- Marginal improvement < 5%
- Time budget exhausted
- Solution meets "excellent" threshold
```

---

## Framework Selection Guide

| Task Type | Primary Framework | Secondary |
|-----------|------------------|-----------|
| Planning/Strategy | Tree of Thoughts | Probabilistic Thinking |
| Research/Facts | Chain of Verification | System 2 Thinking |
| Debugging/Diagnosis | Abductive Reasoning | Adversarial Reasoning |
| Innovation/Creativity | First Principles | Tree of Thoughts |
| Risk Assessment | Probabilistic Thinking | Adversarial Reasoning |
| Writing/Content | Recursive Improvement | System 2 Thinking |
| Math/Logic | System 2 Thinking | Chain of Verification |
