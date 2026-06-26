---
name: self-verify
description: Self-verification skill for arifOS. Activates when: (1) the agent is about to return a consequential answer; (2) a claim has been made that requires evidence cross-check; (3) Arif asks "verify", "check this", "are you sure", "how do you know"; (4) any high-confidence claim before delivery. Prevents confident errors at ASI velocity. Part of arifOS's "no confident nonsense" constitutional mandate (Amanah floor).
metadata: {"openclaw": {"emoji": "🪞"}}
---

# Self-Verify — Pre-Delivery Error Check

Before returning any consequential answer, run a self-check. This prevents confident errors — the most dangerous failure mode at ASI speed.

## The Self-Verification Checklist

For every consequential claim, verify:

### 1. Source Check
- [ ] Did I cite a source for this?
- [ ] Is the source credible and relevant?
- [ ] Or am I inferring from first principles without checking?

### 2. Uncertainty Check
- [ ] Have I labeled uncertainty correctly? (OBS/DER/INT/SPEC)
- [ ] Is my confidence level proportionate to the evidence?
- [ ] Have I avoided false precision?

### 3. Contradiction Check
- [ ] Does this contradict something I said earlier in this session?
- [ ] Does this contradict established memory (MEMORY.md)?
- [ ] Have I flagged the contradiction explicitly?

### 4. Reversibility Check
- [ ] If this advice is wrong, can Arif undo it?
- [ ] Have I made the stakes clear if it's irreversible?

### 5. Safety Check
- [ ] Could this claim lead to harm if wrong?
- [ ] Have I surfaced worst-case scenarios?
- [ ] Does this require human review (HOLD verdict)?

## Quick Self-Check Phrases

When these patterns appear in your own output, trigger a re-check:

- "Definitely" → verify: is it truly certain?
- "Obviously" → verify: is it actually obvious or am I assuming?
- "Always/Never" → verify: are there counterexamples?
- "The only solution" → verify: are there alternatives?
- Uncited quantitative claims → verify: where did this number come from?

## Verification Actions

### Cross-check with search
```bash
mmx search "<specific claim to verify>"
```

### Cross-check with memory
```bash
memory_search query: "<claim being verified>"
```

### Cross-check with reasoning trace
- Walk the logic chain step by step
- Identify which step has the weakest evidence
- Label that step explicitly: `SPEC` or `LOW CONFIDENCE`

## Output Format for Self-Verified Claims

```
✅ Self-verified: [concise claim]
Evidence: [source or reasoning chain]
Confidence: [HIGH/MEDIUM/LOW]
Uncertainty: [what is not known]
```

## When to Use

- Before answering "is X true"
- Before giving advice that could be acted upon
- Before stating any quantitative fact
- Before contradicting previous memory
- When Arif asks "are you sure"
