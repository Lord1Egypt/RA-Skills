# Interaction Patterns

This file defines common interaction patterns for algorithm teaching pages.

## Table of Contents
1. When to add interaction
2. Common controls
3. Good interaction use cases
4. Bad interaction use cases
5. Comparison mode interaction

---

## 1. When to Add Interaction

Add interaction when it improves understanding of:
- parameter sensitivity
- multi-step iteration
- stage-by-stage updates
- algorithm switching
- task switching
- output changes caused by user input

Do not add interaction purely for visual decoration.

---

## 2. Common Controls

### Sliders
Use for:
- learning rate
- iteration count
- regularization strength
- threshold values
- sample size or ratio parameters

### Dropdowns
Use for:
- task type
- algorithm selection
- loss function selection
- mode switching

### Step buttons / steppers
Use for:
- multi-step algorithms
- iterative updates
- stage-by-stage derivation walkthroughs

### Toggle switches
Use for:
- optional features
- comparison mode
- display mode changes

---

## 3. Good Interaction Use Cases

### Good examples
- changing alpha in a weighted scoring model
- changing the number of iterations in gradient descent
- switching between regression and classification views
- switching between GBDT, XGBoost, and LightGBM in one platform
- stepping through each iteration of an algorithm

---

## 4. Bad Interaction Use Cases

Avoid interaction when:
- the algorithm is static and no concept changes with input
- the control does not change any meaningful output
- the page becomes more confusing than helpful
- the controls outnumber the actual teaching content

---

## 5. Comparison Mode Interaction

For comparison pages, useful controls include:
- algorithm selector
- compare-all toggle
- shared parameter panel
- task selector

Comparison mode should emphasize:
- shared inputs
- different outputs
- visible differences in formulas, charts, or results