# Explanation Patterns

This file defines how algorithm explanations should be written.

## Table of Contents
1. Formula explanation pattern
2. Algorithm explanation order
3. Numerical substitution pattern
4. Beginner adaptation
5. Advanced adaptation

---

## 1. Formula Explanation Pattern

For each important formula, explain it in four layers.

### Required pattern
1. write the formula
2. explain each symbol
3. explain why this formula is used
4. substitute concrete numbers whenever possible

### Example structure
- Formula:
  $$y = ax + b$$
- Symbol meaning:
  - y: output
  - x: input
  - a: slope
  - b: intercept
- Why it is used:
  This formula describes a linear relation between input and output.
- Numerical substitution:
  If x = 2, a = 3, b = 1, then y = 3×2 + 1 = 7.

This pattern should be reused for algorithm updates, loss functions, scoring rules, probability formulas, decomposition formulas, and optimization targets.

---

## 2. Algorithm Explanation Order

Prefer this order for a single algorithm:
1. what problem it solves
2. intuition
3. mathematical formulation
4. key formulas
5. step-by-step process
6. numerical example
7. interactive controls
8. charts
9. result interpretation

This order makes the page readable for both beginners and intermediate learners.

---

## 3. Numerical Substitution Pattern

Whenever the algorithm includes a real computation chain, show numerical substitution in at least these places when possible:
- initialization
- first major formula
- intermediate update
- final score or result

Good numerical substitution is:
- short
- local to the formula
- clearly linked to symbols
- consistent with the data shown elsewhere on the page

Avoid symbolic-only explanation when the user clearly wants a teaching page.

---

## 4. Beginner Adaptation

For beginners:
- explain intuition before notation
- do not overload sections with too many formulas at once
- add small examples
- explain what changes after each step
- prefer simple language

Typical signs a beginner page needs:
- more substitution
- more small notes
- more visible process
- fewer compressed theoretical statements

---

## 5. Advanced Adaptation

For advanced users:
- allow denser mathematical detail
- compare variants of formulas
- discuss parameter meaning more deeply
- include complexity or optimization interpretation where relevant

Even for advanced outputs, keep the structure readable.
Do not turn the page into a raw note dump.