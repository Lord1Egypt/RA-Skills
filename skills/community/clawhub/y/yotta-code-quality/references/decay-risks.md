# Decay Risk Reference (Production Code)

Six patterns that cause software to degrade. Apply the Iron Law to each finding.

## Risk 1: Cognitive Overload (R1)

**Diagnostic question:** How much mental effort does a human need to understand this?

Cognitive load beyond working memory causes mistakes, avoidance, and blocks the refactoring that
would fix it.

### Symptoms
- Function longer than 20 lines where multiple levels of abstraction are mixed.
- Nesting depth greater than 3 levels.
- Parameter list with more than 4 parameters.
- Magic numbers or unexplained constants.
- Variable names that require reading the implementation to understand (e.g., `d`, `tmp2`, `flag`).
- Boolean expressions with 3+ conditions combined.
- Train-wreck chains: `a.getB().getC().doD()`.
- Code names that do not match what the business calls the same concept.
- Flag Arguments: a boolean parameter that makes a function do two fundamentally different things.
- Primitive Obsession: domain concepts as primitives (`String email`, `int orderId`, `double money`)
  rather than value types.
- Shallow module: interface/documentation more complex than the functionality provided.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Long Method | Fowler — Refactoring | Long Method |
| Long Parameter List | Fowler — Refactoring | Long Parameter List |
| Message Chains | Fowler — Refactoring | Message Chains |
| Flag Arguments | Fowler — Refactoring | Flag Arguments |
| Primitive Obsession | Fowler — Refactoring | Primitive Obsession |
| Function length and nesting | McConnell — Code Complete | Ch. 7: High-Quality Routines |
| Variable naming | McConnell — Code Complete | Ch. 11: The Power of Variable Names |
| Magic numbers | McConnell — Code Complete | Ch. 12: Fundamental Data Types |
| Domain name mismatch | Evans — Domain-Driven Design | Ubiquitous Language |
| Shallow Module | Ousterhout — A Philosophy of Software Design | Ch. 4: Modules Should Be Deep |

### Severity Guide
- 🔴 Critical: function > 50 lines, nesting > 5, or virtually no meaningful names.
- 🟡 Warning: function 20–50 lines, nesting 4–5, some unclear names.
- 🟢 Suggestion: minor naming issues, 1–2 magic numbers, isolated train-wreck chains.

### What Not to Flag
- Linear code with clear names and guard clauses is not automatically high cognitive load.
- Internal implementation detail hidden behind a deep, simple module boundary is not a shallow-module problem.
- Domain-specific terminology is fine if it matches how experts actually speak.

---

## Risk 2: Change Propagation (R2)

**Diagnostic question:** How many unrelated things break when you change one thing?

Each change ripples to unrelated modules, slowing velocity and multiplying regression risk.

### Symptoms
- Modifying one feature requires touching > 3 files in unrelated modules.
- One class changes for multiple different business reasons.
- A method uses more data from another class than from its own.
- Two classes know each other's internal state directly.
- Changing one module requires recompiling/retesting many unrelated modules.
- **Hyrum's Law**: with sufficient callers, every observable behavior (implementation details,
  error message text, coincidental call ordering, undocumented side effects) becomes an implicit
  contract callers depend on.
- **Orthogonality violation**: changing one dimension forces edits in unrelated dimensions.
- **Information Leakage**: a design decision (file format, protocol, data shape) encoded in > 1
  module, so changing it needs coordinated edits.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Shotgun Surgery | Fowler — Refactoring | Shotgun Surgery |
| Divergent Change | Fowler — Refactoring | Divergent Change |
| Feature Envy | Fowler — Refactoring | Feature Envy |
| Inappropriate Intimacy | Fowler — Refactoring | Inappropriate Intimacy |
| Orthogonality violation | Hunt & Thomas — The Pragmatic Programmer | Ch. 2: Orthogonality |
| DIP violation | Martin — Clean Architecture | Dependency Inversion Principle |
| High change propagation radius | Brooks — The Mythical Man-Month | Brooks's Law (communication overhead) |
| Hyrum's Law | Winters et al. — Software Engineering at Google | Ch. 1: Hyrum's Law |
| Information Leakage | Ousterhout — A Philosophy of Software Design | Ch. 5: Information Hiding and Leakage |

### Severity Guide
- 🔴 Critical: one change touches > 5 files, or structural dependency inversion (domain depends on infrastructure).
- 🟡 Warning: one change touches 3–5 files, mild coupling between modules.
- 🟢 Suggestion: minor coupling, easily isolatable.

### What Not to Flag
- A composition root wiring concrete dependencies is not a DIP violation by itself.
- A stable public API with intentionally supported behavior is not automatically Hyrum's Law debt.
- Coordinated edits inside one bounded context may be normal, not shotgun surgery.

---

## Risk 3: Knowledge Duplication (R3)

**Diagnostic question:** Is the same decision expressed in more than one place?

Multiple copies drift apart silently. DRY is about decisions, not code lines.

### Symptoms
- Same logic copy-pasted across files or functions.
- Same concept named differently (`user`, `account`, `member`, `customer`).
- Parallel class hierarchies that must change in sync.
- Config values repeated as literals in multiple places.
- Two modules implementing the same algorithm independently.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Code duplication | Fowler — Refactoring | Duplicate Code |
| Parallel Inheritance | Fowler — Refactoring | Parallel Inheritance Hierarchies |
| DRY violation | Hunt & Thomas — The Pragmatic Programmer | DRY |
| Inconsistent naming | Evans — Domain-Driven Design | Ubiquitous Language |
| Alternative Classes | Fowler — Refactoring | Alternative Classes with Different Interfaces |

### Severity Guide
- 🔴 Critical: core business logic duplicated across modules, or same domain concept named 3+ ways.
- 🟡 Warning: utility code duplicated, naming inconsistent within a subsystem.
- 🟢 Suggestion: minor literal duplication, single naming inconsistency.

### What Not to Flag
- Repetition across separate bounded contexts is not automatically duplicate knowledge.
- Temporary duplication during an active extraction/migration is not necessarily debt.
- Shared protocol constants at explicit boundaries may be acceptable when local ownership is clearer.

---

## Risk 4: Accidental Complexity (R4)

**Diagnostic question:** Is the code more complex than the problem it solves?

Accidental complexity accumulates addition by addition until developers fight scaffolding more than
solving the problem.

### Symptoms
- Abstractions built "for future use" with no current consumer.
- Classes that barely justify existence (wrap a single method call).
- Classes that only delegate without adding behavior (pure middle-men).
- Second attempt at a system significantly more elaborate than the first.
- Switch statements signaling missing polymorphism.
- Config options never changed from defaults.
- Framework code larger than the application it powers.
- Code grown under sustained tactical shortcuts.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Speculative Generality | Fowler — Refactoring | Speculative Generality |
| Lazy Class | Fowler — Refactoring | Lazy Class |
| Middle Man | Fowler — Refactoring | Middle Man |
| Switch Statements | Fowler — Refactoring | Switch Statements |
| Second System Effect | Brooks — The Mythical Man-Month | Ch. 5: The Second-System Effect |
| YAGNI violations | McConnell — Code Complete | Ch. 5: Design in Construction |
| Over-engineering | Hunt & Thomas — The Pragmatic Programmer | Topic 4: Good-Enough Software |
| Tactical programming debt | Ousterhout — A Philosophy of Software Design | Ch. 3: Strategic vs. Tactical Programming |

### Severity Guide
- 🔴 Critical: entire subsystem built around a speculative requirement, or framework overhead dominates domain logic.
- 🟡 Warning: several unnecessary abstractions or wrapper classes, unused config systems.
- 🟢 Suggestion: one or two lazy classes or middle-men in non-critical paths.

### What Not to Flag
- A switch over an external protocol, wire format, or closed enum is not automatically missing polymorphism.
- Thin wrappers that absorb vendor churn or hide instability may be justified.
- A larger second version is not second-system effect unless added generality exceeds present needs.

---

## Risk 5: Dependency Disorder (R5)

**Diagnostic question:** Do dependencies flow in a consistent, predictable direction?

When business logic depends on infrastructure, infrastructure changes cascade into domain changes.
Cycles prevent isolation.

### Symptoms
- Circular dependencies between modules/packages.
- High-level business logic directly imports low-level infrastructure (domain service imports a DB driver).
- Stable, widely-used components depend on unstable, frequently-changing ones.
- Abstract components depending on concrete implementations.
- Law of Demeter violations: `order.getCustomer().getAddress().getCity()`.
- Module fan-out > 5.
- A module implements an interface but uses only a subset (ISP violation: fat interface).
- "One mind did not design this" — incompatible patterns with no clear rule for which to use where.
- Direct version-pinned deps on transitive packages (diamond dependency / upgrade blockage).

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Dependency cycles | Martin — Clean Architecture | Acyclic Dependencies Principle (ADP) |
| DIP violation | Martin — Clean Architecture | Dependency Inversion Principle (DIP) |
| Instability direction | Martin — Clean Architecture | Stable Dependencies Principle (SDP) |
| Abstraction mismatch | Martin — Clean Architecture | Stable Abstractions Principle (SAP) |
| ISP violation | Martin — Clean Architecture | Interface Segregation Principle (ISP) |
| Conceptual integrity | Brooks — The Mythical Man-Month | Ch. 4: Conceptual Integrity |
| Law of Demeter | Hunt & Thomas — The Pragmatic Programmer | Ch. 5: Decoupling and the Law of Demeter |
| SOLID violations | Martin — Clean Architecture | SRP, OCP |
| Diamond dependency | Winters et al. — Software Engineering at Google | Ch. 21: Dependency Management |

### Severity Guide
- 🔴 Critical: dependency cycles present, or domain layer directly depends on infrastructure layer.
- 🟡 Warning: several SDP/DIP violations but no cycles; conceptual inconsistency across modules.
- 🟢 Suggestion: minor Demeter violations, slightly elevated fan-out in isolated modules.

### What Not to Flag
- High fan-out in an orchestration layer or composition root is not automatically disorder.
- Adapter modules may depend on both domain and infrastructure when they explicitly translate across the boundary.
- A stable facade over many leaf dependencies can be healthy if dependency policy is clear.

---

## Risk 6: Domain Model Distortion (R6)

**Diagnostic question:** Does the code faithfully represent the problem it is solving?

Code that mismatches business language forces mental translation. Over time it models schemas instead
of the domain, with logic bleeding into service layers.

### Symptoms
- Business logic scattered across service layers while domain objects have only getters/setters
  (anemic domain model).
- Names that do not match what business stakeholders call the concept.
- A class whose only purpose is to hold data with no behavior (pure data bag).
- A subclass that ignores/overrides most of its parent's behavior (Refused Bequest).
- Bounded context boundaries crossed without translation or anti-corruption layer.
- Methods more interested in another class's data than their own (Feature Envy).
- A subclass overrides parent methods with incompatible behavior or throws where the parent
  guarantees success (LSP violation).
- Value Objects treated as Entities (mutable ID + lifecycle instead of replacement on change).

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Anemic Domain Model | Evans — Domain-Driven Design | Domain Model pattern |
| Ubiquitous Language drift | Evans — Domain-Driven Design | Ubiquitous Language |
| Bounded context violation | Evans — Domain-Driven Design | Bounded Context |
| Data Class | Fowler — Refactoring | Data Class |
| Refused Bequest | Fowler — Refactoring | Refused Bequest |
| Feature Envy | Fowler — Refactoring | Feature Envy |
| LSP violation | Martin — Clean Architecture | Liskov Substitution Principle (LSP) |

### Severity Guide
- 🔴 Critical: domain logic entirely in service layer, domain objects are pure data bags.
- 🟡 Warning: partial anemia, some naming inconsistency between code and domain language.
- 🟢 Suggestion: minor naming drift in non-core areas, isolated cases of Feature Envy.

### What Not to Flag
- CRUD-heavy workflows may legitimately use transaction scripts instead of rich domain objects.
- DTOs, persistence records, and API payload models are allowed to be data-only.
- Shared infrastructure language is not domain drift if the business model itself is simple.
