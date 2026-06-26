---
name: reflect-critique-revise
version: 1.0.0
description: |
  Three-pass reflection loop that takes draft code, runs a senior-engineer
  critique, then produces a revised version. Closes ~15-20% of the quality
  gap between local M2.7 and cloud Sonnet 4.6 on coding tasks by catching
  bugs, API misuse, and pattern drift.
triggers:
  - after any code generation producing > 30 lines
  - after any iOS/Swift code (always review)
  - when the invoking skill explicitly requests critique
  - when user says "double check" or "review" or "is this right"
tools:
  - llm
inputs:
  - task: original user request (string)
  - draft: the code to review (string)
  - domain: "ios" | "web" | "python" | "trading" | "vc" | "general"
  - num_passes: int, default 2 (each pass = one critique + revise cycle)
outputs:
  - code: final revised code
  - critique_history: list of issues found in each pass
  - confidence: "high" | "medium" | "low" based on final pass
metadata:
  openclaw:
    category: coding
    tags:
      - coding
      - code-review
      - reflection
      - self-critique
    requires_openclaw: ">=2026.3.31"
    binaries:
      - python3
    python_packages:
      - aiohttp
    env_vars:
      - OPENCLAW_LLM_ENDPOINT
---

# Reflect, Critique, Revise

The core insight: M2.7 JANGTQ-CRACK reviewing its own output in a different
context catches a surprising percentage of its own mistakes. Generation
context and review context activate different reasoning paths even in the
same model.

## The three prompts

### Prompt 1 — Senior engineer critique

```
You are a senior {domain} engineer doing a thorough code review. You have no
investment in this code — your job is to find problems, not to validate it.

Task the author was trying to solve:
{task}

Code to review:
```
{draft}
```

{domain_specific_checklist}

For each issue you find, output:
- SEVERITY: critical | major | minor
- LOCATION: line number or function name
- ISSUE: specific problem
- FIX: concrete correction

If you find no issues, say "NO ISSUES FOUND" explicitly.

Be direct. Do not hedge. Do not explain why the code is good.
```

### Prompt 2 — Revise based on critique

```
Original task:
{task}

Original code:
```
{draft}
```

Review findings:
{critique}

Produce a revised version that addresses every critical and major issue.
Minor issues: fix if clean, ignore if fix would compromise clarity.

Output ONLY the revised code. No explanation, no preamble.
```

### Prompt 3 — Final confidence check (after final revision)

```
Task:
{task}

Final code:
```
{revised}
```

Rate your confidence in this code on a three-point scale:
- HIGH: you would ship this to production
- MEDIUM: works but has caveats you'd want reviewed
- LOW: has issues you can't fix without more context

Output exactly one of: HIGH, MEDIUM, LOW
Then one sentence explaining why.
```

## Domain-specific checklists

Inject the relevant checklist into Prompt 1:

### iOS checklist
```
Review this Swift code for:
- Deprecated API usage (any API deprecated in iOS 17+)
- Missing @MainActor annotations on UI-touching code
- Improper Task / async handling (retention cycles, missing awaits)
- SwiftUI view hierarchy issues (missing @State, @Binding, @Observable)
- SwiftData/Core Data migration safety
- Force unwraps that could crash
- Missing availability checks for iOS 26+ APIs
- Incorrect concurrency patterns (Sendable violations)
```

### Web/frontend checklist
```
Review this code for:
- React rendering issues (missing keys, stale closures, effect dependencies)
- Accessibility violations (missing aria labels, keyboard navigation)
- XSS vulnerabilities (unescaped user input)
- Memory leaks (event listeners not cleaned up)
- Bundle size concerns (large imports, unused code)
- TypeScript type safety (any usage, missing types)
- Responsive / mobile breakpoint handling
```

### Python checklist
```
Review this code for:
- Resource leaks (unclosed files, connections, locks)
- Exception handling gaps (bare except, swallowed errors)
- Off-by-one errors in slices/ranges
- Mutable default arguments
- Race conditions in async/threading code
- SQL injection if building queries
- Unsafe pickle/eval/exec usage
- Missing input validation
```

### Trading checklist
```
Review this code for:
- Lookahead bias in backtesting (using future data)
- Survivorship bias in data selection
- Slippage/fees ignored in signal generation
- Position sizing without risk limits
- Division by zero in ratio calculations
- Missing market hours / holiday checks
- Currency/unit mixing
- Float comparison issues (use Decimal for money)
```

### VC/analysis checklist
```
Review this analysis for:
- Unit confusion (ARR vs MRR, net vs gross)
- Missing risk factors (competition, moat erosion, key-person risk)
- Overly optimistic market sizing (TAM bloat)
- Unit economics fundamentals (CAC payback, LTV accuracy)
- Counterfactual reasoning (what if thesis is wrong)
- Selection bias in comparables
- Benchmark staleness
```

## Execution logic

```python
async def reflect_critique_revise(task, draft, domain, num_passes=2):
    current = draft
    critique_history = []

    for i in range(num_passes):
        # Pass N — critique
        critique = await llm.generate(
            prompt=PROMPT_1.format(
                task=task,
                draft=current,
                domain=domain,
                domain_specific_checklist=CHECKLISTS[domain]
            ),
            model="m27-jangtq-crack",
            system="You are a senior engineer code reviewer.",
            temperature=0.2,  # low temp for consistent critique
            max_tokens=2000
        )
        critique_history.append({"pass": i+1, "critique": critique})

        # Early exit if no issues
        if "NO ISSUES FOUND" in critique:
            break

        # Pass N — revise
        current = await llm.generate(
            prompt=PROMPT_2.format(task=task, draft=current, critique=critique),
            model="m27-jangtq-crack",
            system=f"You are a senior {domain} engineer revising code.",
            temperature=0.3,
            max_tokens=6000
        )

    # Final confidence check
    confidence_raw = await llm.generate(
        prompt=PROMPT_3.format(task=task, revised=current),
        model="m27-jangtq-crack",
        temperature=0.1,
        max_tokens=200
    )
    confidence = (
        "HIGH" if "HIGH" in confidence_raw[:10] else
        "LOW" if "LOW" in confidence_raw[:10] else
        "MEDIUM"
    )

    return {
        "code": current,
        "critique_history": critique_history,
        "confidence": confidence
    }
```

## Cost / time

Each pass: ~2 LLM calls (critique + revise), ~5K tokens total.
Default 2 passes: ~10K tokens, ~4 minutes on M4 Max at 40 t/s.

For quick tasks you can drop to num_passes=1. For critical production code,
run num_passes=3 and escalate to Claude Code if confidence != HIGH.

## Integration notes

This skill is called by `coding-orchestrator` as step 7. It can also
be called standalone when user says "review this code" or pastes code with
"is this right?"

When called standalone, the caller must provide `domain` — use `route-specialist`
to classify if not provided.
