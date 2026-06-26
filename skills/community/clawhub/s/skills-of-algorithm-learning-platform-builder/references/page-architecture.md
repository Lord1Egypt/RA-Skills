# Page Architecture

This file defines reusable structures for algorithm teaching pages.

## Table of Contents
1. Single Algorithm Page
2. Comparison Page
3. Reusable Platform Page
4. Section Ordering Rules
5. Page Construction Notes

---

## 1. Single Algorithm Page

Use this structure when the user wants to explain one algorithm clearly.

### Recommended section order
1. hero / page intro
2. algorithm overview
3. input data and parameters
4. formula core
5. step-by-step calculation
6. interactive controls
7. charts and visualization
8. results and conclusion
9. auto-generated summary text

### Purpose of each section
- hero: define what the page is about
- overview: explain intuition and use case
- input section: show what the algorithm consumes
- formula core: present mathematical basis
- step-by-step section: make computation visible
- interaction: allow parameter or step changes
- charts: visualize behavior and outcomes
- results: summarize what happened

---

## 2. Comparison Page

Use this when the user wants to compare multiple algorithms.

### Recommended section order
1. hero / comparison goal
2. shared problem setup
3. comparison summary table
4. per-algorithm intuition cards
5. formula comparison section
6. parameter comparison section
7. chart comparison section
8. result comparison table
9. conclusion and recommendation

### Key rule
A comparison page must show both:
- shared structure
- meaningful differences

It should never present multiple algorithms as if they are only name variations.

---

## 3. Reusable Platform Page

Use this when the user wants a general platform that can be extended to many algorithms.

### Recommended section order
1. hero / platform intro
2. algorithm selector
3. task selector
4. shared data input area
5. shared parameter area
6. algorithm-specific formula area
7. algorithm-specific step area
8. shared chart area
9. shared result area
10. comparison mode or extension area

### Platform principles
- keep the outer structure stable
- make the inner algorithm modules switchable
- separate common sections from algorithm-specific sections
- design for extensibility

---

## 4. Section Ordering Rules

General rule:
- intuition before abstraction
- formulas before detailed computation
- detailed computation before charts
- charts before final conclusion

Avoid this order:
- large code first
- charts before formulas
- final results without showing how they were obtained

---

## 5. Page Construction Notes

### Always include
- a clear learning objective
- visible formulas
- visible numerical process when applicable
- a structured section flow

### Prefer
- card-based layout
- one main idea per section
- one chart per visual purpose
- modular design for extension

### Avoid
- overly dense concept dumps
- giant unbroken code blocks before explanation
- formula-only pages without narrative explanation