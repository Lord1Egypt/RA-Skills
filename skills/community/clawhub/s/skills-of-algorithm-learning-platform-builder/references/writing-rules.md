# Writing Rules

This file defines writing and output standards for the skill.

## Table of Contents
1. General writing rules
2. Teaching rules
3. Html output rules
4. Things to avoid

---

## 1. General Writing Rules

Always write in a way that is:
- structured
- readable
- explanation-first
- suitable for teaching

Use short sections and visible section purposes.
Prefer concrete explanation over abstract compression.

---

## 2. Teaching Rules

Always prefer pages that combine:
- intuition
- formulas
- numerical substitution
- interaction
- charts
- summary

Do not stop at concept explanation when the user's request clearly asks for a learning page or dynamic demo.

When writing formula explanations:
- explain symbols
- explain why the formula is used
- show a concrete substitution when possible

When the user is a beginner:
- simplify wording
- add more examples
- keep the visual structure obvious

---

## 3. Html Output Rules

When generating html:
- prefer a single-file html page
- keep it directly runnable in a browser
- include complete html structure
- include script and style blocks when needed
- keep mathjax and chart.js configuration consistent
- keep the code internally consistent
- do not leave placeholders like TODO in final output unless the user asked for a scaffold

Prefer a polished teaching layout over a raw utility layout.

---

## 4. Things to Avoid

Avoid:
- static concept dumps without visible structure
- formula-only pages without narrative
- code-only outputs without explanation when the task is educational
- disconnected charts that are not explained
- interactions that do not change anything meaningful
- incomplete html output