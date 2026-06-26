# Platform Upgrade Rules

This file defines how to evolve a generated algorithm teaching page into a stronger, more reusable, more complete learning platform.

Its purpose is to help the skill answer questions like:
- how should this page be upgraded
- what should be added next
- what is the best version of this platform
- how do we generalize from one algorithm to many algorithms
- how do we move from a single demo to a reusable educational system

---

# Table of Contents

1. Purpose
2. General upgrade principle
3. Upgrade ladder
4. What to upgrade first
5. Single algorithm page upgrade rules
6. Comparison page upgrade rules
7. Reusable platform upgrade rules
8. Interaction upgrade rules
9. Visualization upgrade rules
10. Writing and explanation upgrade rules
11. Architecture upgrade rules
12. Reusability upgrade rules
13. Quality checkpoints
14. Final standard

---

# 1. Purpose

Not every user request should produce the biggest possible platform immediately.

This file helps determine:
- what the current version already does
- what its current limitations are
- what the next most valuable upgrade is
- what the “best version” should look like

The skill should use these rules to avoid:
- overbuilding too early
- adding features without teaching value
- creating pages that are flashy but structurally weak

---

# 2. General Upgrade Principle

Always upgrade in this order:

1. structure
2. explanation
3. interaction
4. visualization
5. comparison
6. reusability
7. export or platform convenience features

In other words:
- first make the page understandable
- then make the formulas visible
- then make the computation visible
- then make it dynamic
- then make it extensible

Do not start by adding decorative features.

---

# 3. Upgrade Ladder

Use this ladder to determine the maturity level of the current page.

## Level 1 — Static Explanation Page
Characteristics:
- concept explanation
- little or no interaction
- formulas may exist
- weak numerical process

Good for:
- quick notes
- simple overviews

Limitations:
- low teaching depth
- weak retention
- weak reuse

## Level 2 — Structured Teaching Page
Characteristics:
- clear section flow
- formulas explained
- visible numerical substitution
- result interpretation

Good for:
- coursework
- presentations
- readable algorithm study notes

Limitations:
- limited interactivity
- weak parameter sensitivity exploration

## Level 3 — Interactive Algorithm Page
Characteristics:
- parameters can be changed
- charts update
- steps are visible
- some dynamic recomputation

Good for:
- learning through experimentation
- algorithm demos
- class explanation

Limitations:
- still centered on one algorithm
- limited comparison power

## Level 4 — Comparison Page
Characteristics:
- multiple algorithms can be compared
- shared task setup
- shared result comparison
- visible formula and workflow differences

Good for:
- understanding families of methods
- choosing between methods
- high teaching value

Limitations:
- may still be hard to extend
- often still page-specific

## Level 5 — Reusable Learning Platform
Characteristics:
- shared outer structure
- switchable algorithm modules
- scalable architecture
- reusable templates
- supports future algorithm expansion

Good for:
- long-term project reuse
- publishing a family-level teaching tool
- general educational product design

---

# 4. What to Upgrade First

When deciding upgrades, prefer the smallest change that creates the largest teaching value.

## Upgrade priority order
1. add missing formula explanation
2. add numerical substitution
3. add visible step-by-step process
4. add meaningful controls
5. add charts that reinforce the math
6. add result interpretation
7. add comparison capability
8. add export or polish features

## Never prioritize first
- decorative animation
- complex framework migration without need
- too many controls with little educational purpose
- excessive styling before content quality is stable

---

# 5. Single Algorithm Page Upgrade Rules

If the current page explains only one algorithm, evaluate it with these questions:

## 5.1 Structure check
Does it already include:
- algorithm goal
- intuition
- formulas
- numerical substitution
- result explanation

If not, upgrade structure first.

## 5.2 Formula check
If formulas are present but unexplained:
- add symbol explanation
- add why-this-formula explanation
- add substitution examples

## 5.3 Process check
If the page has formulas but no visible computation flow:
- add stepper
- add iteration breakdown
- add row-by-row or stage-by-stage tables

## 5.4 Interaction check
If the algorithm changes under parameters:
- add sliders
- add dropdowns
- add toggles
- add recalculation buttons or live updates

## 5.5 Visualization check
If the output is numeric or iterative:
- add at least one chart
- ensure chart meaning is explained
- avoid unmotivated visuals

## 5.6 Result upgrade
If the page calculates something important:
- add summary cards
- add auto-generated conclusion text
- add final result table

---

# 6. Comparison Page Upgrade Rules

If the page already compares multiple algorithms, ask:

## 6.1 Are the shared assumptions visible?
A good comparison page should clearly show:
- same data
- same task
- same output target
- same or intentionally different parameters

If not, add a shared setup section.

## 6.2 Are differences explicit?
A comparison page must explicitly compare:
- formulas
- workflow
- parameters
- results
- strengths and limitations

If differences are only implied, add tables and aligned sections.

## 6.3 Is the comparison visual enough?
Upgrade by adding:
- side-by-side formula cards
- side-by-side result cards
- comparison charts
- algorithm difference summary table

## 6.4 Is there a recommendation section?
A good comparison page should end with:
- when to use algorithm A
- when to use algorithm B
- what tradeoff matters most

If missing, add a final recommendation section.

---

# 7. Reusable Platform Upgrade Rules

If the page should become a reusable platform, move from page logic to modular logic.

## 7.1 Separate common from algorithm-specific
Create two layers:

### Shared layer
- page shell
- input section
- parameter section
- chart containers
- result containers

### Algorithm-specific layer
- formulas
- step logic
- algorithm-specific parameters
- algorithm-specific charts

This separation is the main structural upgrade.

## 7.2 Add a mode selector
A reusable platform should usually have at least one of:
- algorithm selector
- compare mode
- task type selector

## 7.3 Add extension points
Design the page so new algorithms can be inserted without redesigning the entire layout.

Useful extension points:
- formula panel slot
- step panel slot
- chart panel slot
- result summary slot

## 7.4 Preserve stable outer architecture
Do not rebuild the whole page every time a new algorithm is added.
Keep the outer learning structure stable.

---

# 8. Interaction Upgrade Rules

Upgrade interaction only when it deepens understanding.

## 8.1 Good interaction upgrades
- expose parameters that visibly affect results
- show changes across iterations
- allow algorithm switching
- allow step navigation
- allow different tasks or datasets

## 8.2 Weak interaction upgrades
Avoid adding:
- controls that do not change outputs
- too many sliders at once
- controls without visible explanation
- hidden interactions the learner cannot understand

## 8.3 Best interaction sequence
When upgrading interaction, do it in this order:
1. algorithm or task switching
2. step-by-step navigation
3. one or two critical parameter sliders
4. advanced parameter block
5. optional expert mode

---

# 9. Visualization Upgrade Rules

Visualization should make the mathematics easier to understand.

## 9.1 Upgrade path for charts
### Basic
- one result chart

### Better
- one process chart + one result chart

### Strong
- one process chart + one comparison chart + one summary chart

## 9.2 Good chart roles
- process chart: shows iteration or transformation
- result chart: shows final output
- comparison chart: shows differences across methods
- sensitivity chart: shows parameter effects

## 9.3 Do not add charts without purpose
A chart should answer at least one of these:
- how is the algorithm changing
- what is the final result
- how do methods differ
- what parameter matters most

---

# 10. Writing and Explanation Upgrade Rules

A platform becomes better not only by adding features, but by improving explanation quality.

## 10.1 Upgrade weak explanation by adding:
- clearer section labels
- shorter conceptual paragraphs
- stronger formula explanation blocks
- more local numerical substitution
- direct interpretation after each important result

## 10.2 Formula writing upgrade
A formula section becomes stronger when it moves from:
- formula only
to:
- formula
- symbol explanation
- why it is used
- numeric substitution
- interpretation

## 10.3 Result writing upgrade
A result section becomes stronger when it includes:
- what changed
- what the final value means
- what conclusion the learner should remember

---

# 11. Architecture Upgrade Rules

Use these rules when evolving code structure.

## 11.1 First stabilize the single-file version
Before moving to a more modular or framework-based version:
- ensure the page logic is correct
- ensure the teaching structure is strong
- ensure interactions are meaningful

## 11.2 Modularize only after the logic is stable
When modularizing:
- separate shared layout logic
- separate algorithm logic
- separate chart rendering logic
- separate data examples if useful

## 11.3 Preserve direct-run usability when possible
For educational demos, browser-runnable single-file html is often a feature, not a limitation.

Do not force framework complexity unless the user explicitly needs it.

---

# 12. Reusability Upgrade Rules

A reusable educational platform should be able to support more algorithms later.

## 12.1 Signs a page is not reusable enough
- algorithm name is hard-coded everywhere
- formulas are mixed into global layout logic
- charts cannot switch datasets or algorithms
- results assume one fixed task type
- parameters are not modular

## 12.2 Upgrade toward reusability by adding
- algorithm selectors
- algorithm configuration objects
- page templates
- family-based structure mapping
- reusable formula cards
- reusable chart containers

## 12.3 Best reusable pattern
A strong pattern is:
- one stable page shell
- one algorithm registry
- one family-aware rendering flow

Even if the implementation remains simple, the structure should think in these terms.

---

# 13. Quality Checkpoints

Before considering a page “upgraded”, check:

## Structure
- Is the page easier to follow than before?

## Explanation
- Are formulas more understandable?

## Computation
- Is the numerical process more visible?

## Interaction
- Do controls change meaningful outputs?

## Visualization
- Do charts reinforce the explanation?

## Comparison
- If multiple algorithms exist, are differences visible?

## Reusability
- Could this structure support another algorithm later?

If the answer is “no” to several of these, the platform still needs structural improvement.

---

# 14. Final Standard

The best version of an algorithm learning platform should feel like:

- a structured course page
- a dynamic calculator
- a visual explainer
- a comparison tool
- a reusable template for future algorithms

It should not feel like:
- a random collection of widgets
- a concept dump
- a code dump
- a one-off page that cannot be extended

Final goal:
- clarity
- mathematical visibility
- dynamic understanding
- reusable architecture
- strong teaching value