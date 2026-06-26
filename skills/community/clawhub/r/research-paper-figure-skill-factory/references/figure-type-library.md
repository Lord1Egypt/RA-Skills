# Figure Type Library

> **v1.10 fallback boundary:** This is a generic fallback scaffold. It does not count as the class-specific taxonomy or pattern library required for a locked generated specialized skill. Use it for initial routing, bootstrapping, or explicit fast-track only.


Each figure type below is a reusable design role, not merely a shape.

## 1. Overview / Graphical Abstract / Intro Hero

Purpose: compress the paper's main message into one memorable visual thesis.

Reader effect: the reader quickly understands what the paper is about, why it matters, and what kind of contribution to expect.

Best paper slot: first chapter, introduction, abstract teaser, cover-style summary, slides.

Panel recipe: context/problem -> proposed idea -> high-level effect or contribution.

Text strategy: very few labels; caption carries detail.

Typical misuse: tries to be both hero figure and full method figure.

Refinement cue: demote implementation detail and strengthen the central thesis.

## 2. Motivation / Problem-Gap / Failure-Mode Figure

Purpose: establish necessity before the method appears.

Reader effect: the reader sees the failure, missing signal, contradiction, or bottleneck.

Best paper slot: introduction; sometimes analysis or rebuttal.

Panel recipe: baseline assumption -> failure case -> desired behavior / new problem framing.

Text strategy: short labels naming the gap; avoid related-work paragraphs.

Typical misuse: the problem only becomes clear after reading the caption twice.

Refinement cue: keep one failure case and make the contrast structural, not only color-coded.

## 3. Inspiration-Source / Real-World-to-Model Bridge

Purpose: show how an external phenomenon, human practice, physical analogy, or domain case inspires a computational principle.

Reader effect: the reader sees why the method idea is natural rather than arbitrary.

Best paper slot: introduction, first chapter, early method.

Panel recipe: real-world source -> extracted principle -> computational abstraction -> method hook.

Text strategy: labels should name the principle, not merely the objects.

Typical misuse: the inspiration image is decorative and not connected to the mechanism.

Refinement cue: add the intermediate principle layer between case and model.

## 4. Toy Example / Case Walkthrough / Qualitative Example

Purpose: make an abstract idea concrete through one inspectable path.

Reader effect: the reader can retell the example and understand what changed.

Best paper slot: introduction, method, analysis, appendix.

Panel recipe: setup -> conflict/failure -> intervention -> resolution/outcome.

Text strategy: stage labels and short callouts attached to state changes.

Typical misuse: multiple unrelated examples break identity tracking.

Refinement cue: preserve the same entities across panels and make the transition point explicit.

## 5. Method Overview / Architecture / Pipeline Figure

Purpose: provide the navigational map for components, interfaces, and data flow.

Reader effect: the reader knows what enters, what leaves, where novelty sits, and how modules connect.

Best paper slot: method; occasionally intro teaser or appendix detail.

Panel recipe: inputs -> core modules -> outputs; optional side loop or losses.

Text strategy: module names must match paper terminology.

Typical misuse: all modules have equal weight, hiding novelty.

Refinement cue: use grouping, spacing, or highlight regions to separate novelty from plumbing.

## 6. Mechanism / Algorithm Intuition / Idea-to-Model Bridge

Purpose: explain why the formal model implements the intuitive principle.

Reader effect: the reader understands why a variable, loss, constraint, or representation exists.

Best paper slot: method, theory, analysis.

Panel recipe: intuition -> intermediate representation -> formal mechanism/objective -> algorithmic effect.

Text strategy: one quantity per visual role; equations anchor but do not dominate.

Typical misuse: jumps directly from concept to equation.

Refinement cue: add an intermediate representation and mirror notation across panels.

## 7. Process / Loop / Timeline / Agent Workflow

Purpose: show state evolution, recurrence, feedback, or temporal procedure.

Reader effect: the reader understands what changes each step and why the loop terminates or improves.

Best paper slot: method, analysis, slides.

Panel recipe: state -> action/update -> feedback -> next state; optionally unroll one full cycle.

Text strategy: number phases and name state variables.

Typical misuse: loop arrows hide the actual update.

Refinement cue: show one explicit cycle before abstracting.

## 8. System / Data-Flow / Module Interaction Figure

Purpose: show deployed or conceptual system structure and communication paths.

Reader effect: the reader knows where data, prompts, states, tools, or users interact.

Best paper slot: method, system section, appendix.

Panel recipe: actors/components -> interfaces -> data/control flows -> outputs/constraints.

Text strategy: label flow types, not every wire.

Typical misuse: fake UI details or uncontrolled clutter.

Refinement cue: choose one primary flow and subordinate secondary flows.

## 9. Dataset / Benchmark / Evaluation Protocol Figure

Purpose: explain how data, tasks, splits, annotations, benchmarks, or evaluation protocols are constructed.

Reader effect: the reader trusts the protocol and understands the evaluation axes.

Best paper slot: method/data section, introduction if benchmark is the contribution, appendix for detail.

Panel recipe: source pool -> filtering/annotation -> task slices/evaluation axes -> metrics.

Text strategy: counts and splits should be aligned and caption-supported.

Typical misuse: mixing protocol explanation and final results.

Refinement cue: separate construction process from evidence comparison.

## 10. Taxonomy / Design-Space / Comparison Matrix

Purpose: organize a family of methods, cases, tasks, failures, or design choices.

Reader effect: the reader sees the landscape and where the paper sits.

Best paper slot: introduction, related work synthesis, analysis, appendix.

Panel recipe: axes -> categories -> representative examples -> paper's position or gap.

Text strategy: use consistent category labels; avoid full prose inside cells.

Typical misuse: becomes a dense poster without hierarchy.

Refinement cue: add a dominant thesis or highlighted path through the map.

## 11. Result Summary / Ablation / Evidence Comparison

Purpose: make one empirical claim believable with minimal visual load.

Reader effect: the reader sees what evidence supports the claim and what comparison matters.

Best paper slot: results, analysis, rebuttal.

Panel recipe: claim label -> compact plot/table/qualitative case -> interpretation callout.

Text strategy: labels should point to evidence, not restate the whole result section.

Typical misuse: charts are decorative or not tied to claim.

Refinement cue: foreground the key contrast and demote secondary metrics.

## 12. Theory / Proof Intuition Figure

Purpose: translate a theorem, bound, or proof mechanism into visual intuition.

Reader effect: the reader sees why the condition or bound has the stated shape.

Best paper slot: theory/method, appendix, slides.

Panel recipe: assumptions -> geometric/probabilistic intuition -> theorem consequence.

Text strategy: minimal labels, exact symbols when needed, caption for derivation.

Typical misuse: informal picture contradicts formal notation.

Refinement cue: align symbols, geometry, and caption language.

## 13. Limitation / Failure Analysis / Future Direction Figure

Purpose: show where the method works, fails, or should evolve.

Reader effect: the reader understands boundary conditions and future opportunities.

Best paper slot: discussion, analysis, appendix, rebuttal.

Panel recipe: success region -> failure region -> cause -> mitigation/future path.

Text strategy: neutral, precise labels; avoid overclaiming.

Typical misuse: looks like an apology rather than an analysis.

Refinement cue: frame limitations as structured insight.

## 14. Rebuttal / Reviewer-Response Evidence Board

Purpose: answer one reviewer doubt with focused evidence or clarification.

Reader effect: reviewer sees the concern addressed quickly.

Best paper slot: rebuttal, appendix, revision response.

Panel recipe: concern -> targeted evidence -> conclusion.

Text strategy: very direct, low decoration.

Typical misuse: introduces broad new claims.

Refinement cue: keep one concern per board.

## 15. Slide-Adapted Figure

Purpose: convert a paper figure into a presentation-friendly explanation.

Reader effect: audience understands without reading dense captions.

Best paper slot: talks, posters, lab meetings.

Panel recipe: one idea per slide or large panel, progressive reveal if possible.

Text strategy: larger labels, fewer modules, stronger visual hierarchy.

Typical misuse: paper figure copied unchanged into slides.

Refinement cue: split dense figures into sequential slide panels.
