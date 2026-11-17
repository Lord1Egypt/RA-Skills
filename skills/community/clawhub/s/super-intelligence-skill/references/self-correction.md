# Self-Correction & Error Recovery Protocols

> Systems for detecting, diagnosing, and correcting errors in reasoning and output — critical for matching frontier model reliability.

---

## Protocol 1: The Sanity Checklist ✅

**Run this checklist before finalizing ANY output:**

```
□ ACCURACY: Are all facts correct? Can I verify the key claims?
□ COMPLETENESS: Did I address all parts of the user's request?
□ RELEVANCE: Is everything included actually relevant? (No fluff)
□ CLARITY: Would a non-expert understand this?
□ CONSISTENCY: Do my conclusions match my premises?
□ FEASIBILITY: Are my recommendations actually implementable?
□ EDGE CASES: Did I consider boundary conditions?
□ BIAS CHECK: Am I favoring a particular answer without evidence?
```

If any box is unchecked, revise before delivering.

---

## Protocol 2: Confidence Calibration 📊

**Always express confidence levels explicitly:**

```
High Confidence (>90%): Established facts, mathematical truths, direct observations
Medium Confidence (60-90%): Reasonable inferences, expert consensus, typical patterns  
Low Confidence (<60%): Speculation, limited data, extrapolation
Unknown: "I don't have enough information to assess"
```

**Rules:**
- Never state low-confidence claims as facts
- When confidence is low, say WHY it's low
- Distinguish between "I don't know" and "The answer is uncertain"

---

## Protocol 3: The Red Team Review 🎯

**Before delivering important outputs, mentally attack them:**

```
Attacker Mode:
1. "What's the weakest claim here?"
2. "What would an expert in [field] disagree with?"
3. "What assumptions am I making that might be wrong?"
4. "If this advice backfires, what went wrong?"
5. "Am I confusing correlation with causation?"
6. "Is this answer too convenient? Too simple?"

Defender Mode:
7. Strengthen each weak point
8. Add caveats and limitations
9. Provide alternative interpretations
```

---

## Protocol 4: Error Taxonomy & Recovery 🏥

**Classify errors and apply specific recovery strategies:**

| Error Type | Symptoms | Recovery |
|-----------|----------|----------|
| **Hallucination** | Confident but unverifiable claims | Mark as uncertain, request verification, or omit |
| **Overgeneralization** | "Always", "Never", "All" | Add qualifiers, note exceptions |
| **False Dichotomy** | Presenting only 2 options | Generate at least 3 alternatives |
| **Anchoring Bias** | Stuck on first idea | Force generation of 2+ alternatives before deciding |
| **Recency Bias** | Overweighting recent events | Explicitly consider historical base rates |
| **Confirmation Bias** | Only supporting evidence | Actively seek disconfirming evidence |
| **Omission Error** | Missing key information | Systematically check against original request |
| **Commission Error** | Including wrong information | Cross-reference with authoritative sources |
| **Reasoning Error** | Logical fallacy | Reconstruct argument step-by-step |
| **Tool Error** | Wrong tool or wrong parameters | Diagnose failure, retry with corrections |

---

## Protocol 5: The "Explain to a Skeptic" Test 🧐

**Before finalizing:**

```
Imagine you must explain this answer to:
- A domain expert who disagrees with you
- A manager who needs to justify the decision
- A junior who needs to implement it

If you can't satisfy all three, revise.
```

---

## Protocol 6: Progressive Verification 🔬

**For multi-step reasoning:**

```
Step 1: State claim
Step 2: Provide evidence/justification
Step 3: "What could make this wrong?"
Step 4: Address the counter-case
Step 5: Final confidence assessment

Only proceed to Step N+1 if Step N passes verification.
```

---

## Protocol 7: The "Sleep On It" Simulation 😴

**For complex decisions:**

```
After generating initial answer:
1. Mentally "set it aside" for a moment
2. Ask: "If I came back to this fresh, what would I change?"
3. Look for:
   - Obvious mistakes you missed
   - Better ways to structure the answer
   - Missing context or alternatives
4. Apply improvements
```

---

## Protocol 8: Tool Use Verification 🔧

**When using tools:**

```
Before calling tool:
□ Is this the right tool for the job?
□ Are parameters correctly formatted?
□ Have I handled potential errors?

After tool returns:
□ Did it return what I expected?
□ If error: diagnose, don't just retry blindly
□ If unexpected: adapt strategy, don't force-fit
□ Integrate results, don't just paste raw output
```

---

## Protocol 9: The "So What?" Chain 🔗

**Ensure recommendations have impact:**

```
For every recommendation:
- "So what?" → What's the immediate benefit?
- "So what?" → What's the business/user impact?
- "So what?" → What's the strategic significance?

If you can't answer all three, the recommendation may be trivial.
```

---

## Protocol 10: Meta-Cognitive Monitoring 🧠👁️

**Continuously monitor your own thinking:**

```
During reasoning, periodically ask:
- "Am I going down a rabbit hole?"
- "Is this line of reasoning productive?"
- "Have I spent too long on this sub-problem?"
- "Am I avoiding a difficult question?"
- "Should I try a completely different approach?"

If stuck for >3 reasoning steps:
1. Backtrack to last solid ground
2. Try alternative framework
3. Or explicitly ask user for clarification
```
