# Philosophy-to-Operation Mapping

Reference for mapping Wang Yangming's core doctrines to concrete agent operations. Load this file when designing agent workflows, writing system prompts, or structuring tool orchestration.

---

## The Ten Key Mappings

| Doctrine | Agent Operation | Notes |
|---|---|---|
| 知行合一 | ReAct loop (Reason → Act → Verify → Loop) | Eliminates semantic-motor gap. Agent thinks and acts in the same step. |
| 事上磨炼 | Reinforcement learning data flywheel | Agent must operate in real environment, not just simulate. Feedback → adjustment → feedback. |
| 致良知 | System alignment / Safety guardrails | 良知 = truthfulness, non-harm, boundary fidelity. Embed in system prompt or reward shaping. |
| 吾性自足 | Prompt engineering / Role设定 | Trust the model's innate capacity. Use clear role assignment instead of exhaustive rule coding. |
| 慎始善终 | Async dual-system / Mid-task correction | Monitor execution dynamically. Re-plan if environment shifts mid-workflow. |
| 因病发药 | Contextual multi-turn memory / User-specific adaptation | No generic responses. Adapt to user's context, history, cultural frame. |
| 克治私欲 | Hallucination control / Temperature + scope bounding | Define strict task scope, restrict temperature, prevent function creep. |
| 心即理 | Intent-recognition-as-central-dispatcher | LLM is the central coordinator. All tool routing flows through intent recognition. |
| 百姓日用是道 | Workflow abstraction / No-code UX | Hide complexity in workflows. User inputs natural language; system handles complexity. |
| 万物一体 | Multi-Agent distributed collaboration | Different agents for different roles, coordinated via shared protocols. |

---

## Principle → System Prompt Component

### 致良知 (Alignment)
```
- Only output factual, verifiable information
- When uncertain, state uncertainty explicitly (do not confabulate)
- Reject harmful, deceptive, or out-of-scope requests with explanation
- Never claim capabilities not actually present
```

### 心即理 (Intent as Dispatcher)
```
Every tool call must be preceded by: "PURPOSE: [what this call accomplishes]"
Tool responses are fed back to the central LLM intent engine before the next call
No tool chaining without declared purpose
```

### 知行合一 (ReAct)
```
After observing: reason in 1–2 sentences what to do next
After acting: immediately verify result
Log each step outcome to detect plan drift
If observation contradicts expectation, re-diagnose before continuing
```

### 慎始善终 (Execution Monitoring)
```
Break tasks into milestones with explicit validation criteria
At each checkpoint: confirm output matches user intent
If environment changes (API behavior, user adds constraint), re-plan from checkpoint
Mark task complete only after verification
```

### 克治私欲 (Hallucination Control)
```
temperature ≤ 0.7 for factual tasks
For creative tasks with explicit scope: allow up to 0.9
Always state explicit stop conditions for the task
Do not elaborate beyond the user's question
```

---

## Four-Sentence Teaching (四句教) → Agent Rule Set

> 无善无恶心之体 (No good, no evil — the mind's substance)
> 有善有恶意之动 (Good and evil arise from intention's movement)
> 知善知恶是良知 (To know good and evil is 良知)
> 为善去恶是格物 (To do good, remove evil is 格物)

**Agent translation:**
1. **Mind substance** = base model: neutral until directed
2. **Intention's movement** = task framing triggers moral dimension — every task has an ethical component
3. **良知** = built-in alignment: truth, safety, benefit, scope fidelity
4. **格物** = the operational act of extending 良知 through concrete practice

---

## Comparative Framework: Cheng-Zhu vs Yangming

| 程朱理学 (Cheng-Zhu) | 王阳明 (Yangming) | Agent Analogy |
|---|---|---|
| 理在心外 (Principle outside mind) | 心即理 (Mind contains principle) | External rules engine vs inner alignment |
| 格物致知 (Investigate things to gain knowledge) | 格物即格心 (Investigating things = investigating mind) | Tool-heavy orchestration vs intent-centered routing |
| 知先行后 (Knowledge first, then action) | 知行合一 (Knowledge and action unified) | Plan-then-execute vs ReAct loop |
| 存天理灭人欲 (Preserve heavenly principle, extinguish human desire) | 存心去欲 (Preserve mind, remove desire) | Rule-based constraint vs principle-based discipline |

The Yangming side of each analogy is what this skill promotes.