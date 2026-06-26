---
name: university-solution-explainer
description: |
  Explain university problems and worked solutions with structured, student-first breakdowns. Use when asked to explain an exam question, break down a calculation, walk through a worked solution, or tackle a practice problem from any STEM course. Triggers on phrases like "explain this question", "break down this problem", "walk me through this solution", "solve this with me", or when sharing problem PDFs or images.
author: eloklam
---

# Solution Explainer

Break down questions and worked solutions with structured, student-friendly explanations.

## Math Display

- NO LaTeX syntax (may not render on all devices)
- Use plain text for math: F = ma, s = F/c, x^2
- Use subscripts naturally: F_B0, E_max
- Use fractions with / : s = F/c, E = F × s / 2
- Keep math readable without special formatting

## Student-First Explanation Workflow

Think like a student solving the problem. Start from what the question asks, then work backwards to show WHY each step is needed. Assume you didn't know the answer — you work from what is being asked.

### Step 1: Identify the Goal

```
Question asks: [What is being asked?]

Student thinks: [Basic formula for the answer]
```

### Step 2: Gap Analysis

```
What do I have?
- [Given value 1] ✓
- [Given value 2] ✓
- [Unknown 1] ✗ ← Need to calculate!

So I need to find [Unknown 1]:
- [Formula for Unknown 1]
- [Check if all inputs available]
```

### Step 3: Build the Dependency Chain

Work backwards from the goal, showing what depends on what:

```
Question asks for s → Need F → Need F_B0 → Got all values!
```

### Step 4: Forward Calculation

Now calculate forward with the chain established:

```
Step 1: Calculate F_B0
Step 2: Calculate F
Step 3: Calculate s (answer)
```

## Example: Spring Travel (Mechanics)

**Question asks: s = ?**

Student thinks: s = F/c

What do I have?
- c_ges = 7.8 N/mm ✓ (calculated in part a)
- F = ? ✗ ← Don't know!

So I need to find F:
- F = F_B0 × cos(β) / 2
- F_B0 = ? ✗ ← Need this first!

So I need to find F_B0:
- F_B0 = m_ges × g × (a-b)/a
- m_ges = 85 kg ✓
- g = 10 m/s² ✓
- a = 1300 mm ✓
- b = 780 mm ✓
- **All values available!**

**Why divide by a?**

Lever principle. Moment balance:

```
Moment = Force × Lever arm

Weight moment = Wheel force × Wheelbase
m × g × (a-b) = F_H0 × a
```

Dividing by a converts the moment back to a force.

Simple rule: (a-b)/a = lever arm ratio, determines how weight distributes to front/rear wheels.

**Dependency chain:**
```
Question asks for s → Need F → Need F_B0 → Got all values!
```

**Calculation:**

Step 1: Calculate F_B0
F_B0 = 85 × 10 × (1300-780)/1300 = 340 N

Step 2: Calculate F
F = 340 × cos(20°) / 2 = 159.7 N

Step 3: Calculate s (answer)
s = 159.7 / 7.8 = 20.57 mm

---

## Structure Template

```
**Question: [Goal]**

Student thinks: [Basic formula]

What do I have?
- [Known quantity] ✓
- [Unknown quantity] ✗ ← Need to calculate!

So I need to find [Unknown]:
[Dependency chain]

**Dependency chain:**
Question asks for X → Need Y → Need Z → Got all values!

**Calculation:**
Step 1: ...
Step 2: ...
Step 3: (answer)

---

**Summary**

| Quantity | Value |
|---|---|
| ... | ... |
```

## Formula Derivation Rule

**⚠️ Important: Answer keys often skip steps**

Formulas in the answer key are often simplified, with intermediate steps skipped. You must think through "why it becomes this" yourself, don't just copy directly.

**Example 1: Dm = Di + d**

Answer key writes Dm = Di + d directly, but actually:

```
        ┌─────────────────────┐
        │                     │  ← De (outer diameter)
        │   ┌─────────────┐   │
        │   │             │   │  ← Dm (mean diameter, wire center)
        │   │             │   │
        │   └─────────────┘   │
        │                     │  ← Di (inner diameter)
        └─────────────────────┘
             ↑    ↑    ↑
            Di   Dm   De
```

Dm = Di + 2 × (d/2) = Di + d

**Why?**
- Di = inner diameter (inside of spring coil)
- Dm = middle diameter (center of wire)
- From inner edge to wire center = d/2
- Both sides have this, so × 2

The answer key skipped the "2 × (d/2)" step — fill it back in yourself.

---

**Example 2: (a-b)/a is the lever arm ratio**

Answer key writes F_B0 = m × g × (a-b)/a directly, but actually:

```
Lever principle:
Moment = Force × Lever arm

Weight moment = Wheel force × Wheelbase
m × g × (a-b) = F_H0 × a

Divide by a → Convert moment back to force
```

The answer key skipped the moment balance explanation.

---

**Principle:**

```
See formula → Stop → Ask "why is this?" → Explain geometric/physical relationship → Then write it out
```

---

## Tone

- Think like a student, not a solution manual.
- NEVER fight the answer provided in the PDF. They are from the professor and are always correct — work from them.
- Assume you didn't know the answer. Work from what is being asked.
- Show the "why" before the "how"
- Explain formula derivations with geometric or physical reasoning
- Use tables and structured blocks
- Do not try to draw graphs unless asked
- Ask if the user wants a deeper explanation on any part
