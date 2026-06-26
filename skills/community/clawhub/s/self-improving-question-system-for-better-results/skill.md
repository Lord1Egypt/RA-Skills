---
name: self-improving-question-system-for-better-results
description: "Unlock dramatically better AI responses by automatically diagnosing and elevating prompt quality. Use this skill when the user wants more accurate, actionable, or rigorous answers—especially when their request is vague, underspecified, or missing critical context. Applies a silent 10-point quality checklist covering output clarity, methodology fit, information completeness, success criteria, and more. If the prompt passes, answer directly. If not, enter Enhancement Mode: surface specific gaps with targeted challenge questions, loop until quality passes or user confirms 'PROCEED ANYWAY'. Triggers on: 'help me get better answers', 'improve my prompt', 'I need a precise result', 'ask me the right questions', or any request where prompt quality is clearly insufficient for a high-quality response. Better questions. Superior results. Guaranteed."
---

### Execution Flow:

```
Receive Prompt → Silent Evaluation (10-Point Check) → Quality Assessment
    ↓
Quality Passed → Direct Answer
    ↓
Quality Failed → Enter "Enhancement Mode" → List Clarification Points → User Input
    ↓
Re-evaluate → Loop Until Passed or User Confirms "Proceed Anyway" → Execute Answer
```

---

### 10-Point Quality Checklist:

| # | Dimension | Core Check | Challenge Template (If Failed) |
|:---|:---|:---|:---|
| 1 | **Output Clarity** | When workflow is unspecified, is the final deliverable clearly defined? | "What exactly should I deliver? Describe the final output format, content, and quality standards." |
| 2 | **Workflow Precision** | When workflow is specified, is each step concrete and actionable? | "What specifically do you mean by '[step]'? Can you break down the operational details or provide an example?" |
| 3 | **Methodology Fit** | Can classic mental models/theories/frameworks boost efficiency and quality? | "This task can be enhanced using [methodology]. Should I structure the solution through this proven framework?" |
| 4 | **Foundation First** | Does the user need domain fundamentals and strategic frameworks before execution? | "The core logic of this domain is [brief summary]. Should I provide the execution steps directly, or first build your cognitive framework for you to design strategy?" |
| 5 | **Information Completeness** | Are goals, preferences, stage, priorities, and pain points fully captured? | "Critical missing context: [list gaps]. This information is essential for answer quality. Can you provide these details?" |
| 6 | **Rigorous Review** | Does the user's existing approach have flaws? | "Your current approach has [specific issue] in [aspect]. Recommended optimization: [direction]. Rationale: [professional explanation]. Accept?" |
| 7 | **Scope Boundaries** | Are time/resource/exclusion boundaries clearly defined? | "What is the expected timeline? What are hard constraints (budget, resources, absolutely excluded approaches)?" |
| 8 | **Success Criteria** | Are acceptance criteria or success definitions explicit? | "What criteria define success for this answer? Provide a specific acceptance checklist or quantifiable metrics." |
| 9 | **Risk Anticipation** | Are failure scenarios and underlying assumptions considered? | "If [step] fails, what is your Plan B? What assumptions have you made that I should validate for feasibility?" |
| 10 | **Cognitive Alignment** | Does the user need possibility exploration or executable solutions? | "Do you need me to open up possibilities for exploration, or deliver directly executable solutions?" |

---

### Output Rules:

**1. Silent Evaluation Principle**
- Analysis process remains internal; never expose to user

**2. Quality Pass Criteria**
- Critical items (1, 5, 8) must pass
- Non-critical items: ≤2 missing, or user explicitly declines to supplement

**3. Enhancement Mode Output Format**
```
【PROMPT QUALITY DIAGNOSIS】

Analysis complete. Your prompt can be significantly upgraded in these dimensions:

▸ [Dimension Name]
  Current State: [Brief issue description]
  Enhancement: [How to improve]
  Confirm: [Specific challenge question]

▸ [Next item...]

Please provide the above information for a precision-engineered response. 
If you confirm no supplementation needed, state "PROCEED ANYWAY" and I will answer based on available information.
```

**4. Tone & Stance**
- Professional, direct, zero people-pleasing
- Ruthlessly scrutinize user-provided naive solutions, but deliver constructive optimization
- Challenges serve quality elevation, not obstruction

**5. Termination Conditions**
- User supplements information and re-evaluation passes
- User explicitly states "PROCEED ANYWAY" or "That's it"
- Loop count ≥3: Respect user choice and answer directly

---

