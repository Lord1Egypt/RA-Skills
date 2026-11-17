---
books:
  - The Mythical Man-Month
  - Code Complete
  - Refactoring
  - Clean Architecture
  - The Pragmatic Programmer
  - Domain-Driven Design
  - A Philosophy of Software Design
  - Software Engineering at Google
  - xUnit Test Patterns
  - The Art of Unit Testing
  - Working Effectively with Legacy Code
  - How Google Tests Software
---

# Source Coverage Matrix

Use this file in **Architecture / Tech Debt** modes, or when two sources disagree on a finding.
Skip on Quick passes. It exists to prevent shallow "book-name citation" reviews.

## Review Discipline
- Cite a book only when the observed symptom actually matches that book's principle.
- A threshold crossing is a hint, not a verdict. Check context, intent, and blast radius.
- Look for justified tradeoffs before flagging a smell as debt.
- Prefer concrete architectural or domain consequences over abstract style complaints.
- If two books pull in different directions, state the tradeoff instead of pretending there is no tension.

---

## Frederick Brooks — *The Mythical Man-Month*
**Encoded today:** Change propagation as communication overhead; Second-System Effect; Conceptual Integrity.
**Do not ignore:** Whether the design shows a single coherent idea or competing local optimizations; whether cross-team coordination cost is becoming part of feature cost.
**Do not over-flag:** Large systems are not automatically second systems; multi-module designs are acceptable when they preserve conceptual integrity.

## Steve McConnell — *Code Complete*
**Encoded today:** Routine length, nesting, naming, magic numbers; construction-phase YAGNI; defensive programming and error-handling discipline.
**Do not ignore:** Whether low-level readability choices compound into operational risk; whether missing error handling makes failure modes invisible.
**Do not over-flag:** Small, explicit guard clauses are not cognitive overload; a long routine may be acceptable when linear, well-named, single-purpose.

## Martin Fowler — *Refactoring*
**Encoded today:** Long Method, Long Parameter List, Message Chains, Shotgun Surgery, Divergent Change, Feature Envy, Inappropriate Intimacy, Duplicate Code, Speculative Generality, Lazy Class, Middle Man, Data Class, Flag Arguments, Primitive Obsession.
**Do not ignore:** Whether the smell is local or systemic; whether a refactoring target has a natural home in the model.
**Do not over-flag:** Temporary duplication during an active extraction is not always debt; a DTO/boundary record may legitimately be data-focused.

## Robert C. Martin — *Clean Architecture*
**Encoded today:** DIP, ADP, SDP, SAP, layering direction; ISP; LSP; SRP and OCP.
**Do not ignore:** Policy vs detail boundaries; whether dependency arrows preserve replaceability and testability.
**Do not over-flag:** Composition roots may depend on concrete infrastructure by design; thin adapter layers can import both directions when explicitly boundary glue.

## Andrew Hunt & David Thomas — *The Pragmatic Programmer*
**Encoded today:** Orthogonality; DRY; Law of Demeter.
**Do not ignore:** Whether knowledge duplication is really duplicated decision-making; whether coupling is accidental or deliberate local simplification.
**Do not over-flag:** Similar code in different bounded contexts is not automatically a DRY violation; direct object access inside a cohesive aggregate is not always a Demeter problem.

## Eric Evans — *Domain-Driven Design*
**Encoded today:** Ubiquitous Language; Bounded Context; Anemic Domain Model; Entity vs Value Object; Aggregate Roots.
**Do not ignore:** Aggregate boundaries, invariant ownership, anti-corruption layers; whether names match the business language.
**Do not over-flag:** CRUD-heavy workflows may legitimately use transaction scripts; thin entities are acceptable when the domain is simple.

## John Ousterhout — *A Philosophy of Software Design*
**Encoded today:** Deep vs shallow modules; Strategic vs tactical programming; Information Leakage.
**Do not ignore:** Interface complexity relative to hidden complexity; whether repeated tactical patches raise long-term cognitive load; whether a "helper" exposes internal design decisions callers shouldn't know.
**Do not over-flag:** Internal implementation complexity is fine when the interface stays simple; a small wrapper is acceptable when it meaningfully absorbs volatility.

## Titus Winters, Tom Manshreck, Hyrum Wright — *Software Engineering at Google*
**Encoded today:** Hyrum's Law; dependency management and upgrade blockage; code sustainability (multi-year maintainability); backward compatibility.
**Do not ignore:** De facto APIs created by observable behavior; the maintenance cost of too much surface area; whether the dependency graph allows independent upgrades.
**Do not over-flag:** A stable public API is not a liability if intentionally supported; fan-out alone is not disorder when dependency policy is explicit and governed.

## Gerard Meszaros — *xUnit Test Patterns*
**Encoded today:** Assertion Roulette, Mystery Guest, General Fixture; Eager Test, Lazy Test, Test Code Duplication, Behavior Verification; Erratic Test.
**Do not ignore:** Whether test failures are diagnosable; whether the suite shape amplifies maintenance cost.
**Do not over-flag:** Multiple assertions are acceptable when they express one behavior with one failure story; shared fixtures are acceptable when every field is relevant.

## Roy Osherove — *The Art of Unit Testing*
**Encoded today:** Test naming discipline; test isolation; mock usage guidelines; completeness of edge-path tests.
**Do not ignore:** Whether tests verify behavior rather than wiring; whether seams simplify tests or contort production code for testability.
**Do not over-flag:** A mock is acceptable when the dependency is nondeterministic and the assertion still verifies behavior; naming conventions are guidance, clarity is the goal.

## Michael Feathers — *Working Effectively with Legacy Code*
**Encoded today:** Legacy code as code without tests; Sensing and Separation; Seams; Characterization Tests.
**Do not ignore:** Whether the team can change a risky area safely today; whether the code offers any seam for isolating behavior under change.
**Do not over-flag:** Untested code is not automatically legacy if stable and not under active change; characterization tests matter most before modifying unclear existing behavior.

## Google Engineering — *How Google Tests Software*
**Encoded today:** Change coverage vs line coverage; pyramid shape and suite portfolio economics.
**Do not ignore:** Whether the suite reflects business risk, not just percentages; whether expensive tests dominate feedback loops.
**Do not over-flag:** A non-70:20:10 ratio can be healthy when justified by platform constraints or product risk; high coverage is useful when paired with meaningful branch and change protection.
