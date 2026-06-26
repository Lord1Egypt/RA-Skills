# University Solution Explainer

**A student-first agent skill for breaking down STEM problems with full reasoning chains.**

> Stop staring at answer keys that skip every other step. This skill explains problems the way a strong senior student would — starting from what the question asks, working backwards to identify every dependency, then showing every step with the physical or geometric reasoning behind it.

---

## Skill Info

- **Name:** university-solution-explainer
- **Input:** Exam problems, problem set questions, worked solutions (PDF, image, or text)
- **Output:** Structured student-first breakdowns with dependency chains and formula derivations
- **Supports:** All STEM subjects, undergraduate level

---

## What It Does

University answer keys almost always skip intermediate reasoning steps. They show the final formula, not how you were supposed to find it. This is frustrating when you're studying and you can't reverse-engineer the thinking chain.

Solution Explainer bridges that gap:

- **Student-first approach** — starts from the question, works backwards to find every missing step
- **Dependency chains** — shows exactly what you need before you can calculate each value
- **Formula derivations** — explains the geometric or physical reasoning behind every formula, not just "use this equation"
- **Gap analysis** — identifies every unknown you need to find before you can reach the answer
- **Structured breakdowns** — organized output with goals, checks, steps, and a summary table

---

## Example

**Input:** A problem PDF about spring travel in mechanics (part of a multi-part problem, part a already solved)

**Output:**
```
Question asks: s = ?

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
- All values available!

**Why divide by a?**

Lever principle. Moment balance:

  Weight moment        =  Wheel force × Wheelbase
  m × g × (a-b)        =  F_H0 × a

Dividing by a converts the moment back to a force.
(a-b)/a = lever arm ratio — determines how weight distributes to wheels.

**Dependency chain:**
Question asks for s → Need F → Need F_B0 → Got all values!

**Calculation:**
Step 1: F_B0 = 85 × 10 × (1300-780)/1300 = 340 N
Step 2: F    = 340 × cos(20°) / 2         = 159.7 N
Step 3: s    = 159.7 / 7.8                = 20.57 mm

**Summary**
| Quantity | Value   |
|----------|---------|
| F_B0     | 340 N   |
| F        | 159.7 N |
| s        | 20.57 mm|
```

---

## Install

Install it for your agent:

```bash
npx skills add eloklam/university-solution-explainer
```

---

## Usage

Activate by sharing a problem PDF, image, or text of an exam question, problem set, or worked solution. Common triggers:

- "Explain this question"
- "Break down this problem"
- "Walk me through this solution"
- "Solve this with me"
- "I don't understand how they got from step X to step Y"

The skill will produce a structured student-first breakdown.

---

## Notes

- **No LaTeX** — plain text math only. Subscripts: `F_B0`, `c_ges`. Fractions: `s = F/c`. No LaTeX rendering required.
- **Works for any STEM course** — mechanics, thermodynamics, circuits, fluid dynamics, control theory, linear algebra, statistics, and more.
- **Does not fight the answer key** — if the problem's answer differs from your calculation, work from the answer key and figure out why.
- **Asks follow-up questions** — if something is unclear or the user wants more depth, the skill will ask before diving deeper.

---


