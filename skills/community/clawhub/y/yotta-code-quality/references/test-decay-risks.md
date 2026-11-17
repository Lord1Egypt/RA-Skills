# Test Decay Risk Reference

Six patterns that cause test suites to degrade. Apply the Iron Law to each finding.

## Risk T1: Test Obscurity

**Diagnostic question:** How much effort does it take to understand what this test verifies?

Unclear test intent breeds distrust, missed failures, and duplicates — one step from an abandoned suite.

### Symptoms
- Assertion Roulette: multiple assertions with no message string.
- Mystery Guest: test depends on external state (files, DB rows, shared fixtures) invisible in the body.
- Test names that do not express scenario and expected outcome (`test1`, `shouldWork`, `testLogin`).
- General Fixture: oversized setUp/beforeEach shared by unrelated tests.
- Test body requires reading production code to understand what is verified.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Assertion Roulette | Meszaros — xUnit Test Patterns | Assertion Roulette (p.224) |
| Mystery Guest | Meszaros — xUnit Test Patterns | Mystery Guest (p.411) |
| General Fixture | Meszaros — xUnit Test Patterns | General Fixture (p.316) |
| Test naming | Osherove — The Art of Unit Testing | method_scenario_expected naming |

### Severity Guide
- 🔴 Critical: no test name describes the behavior; all assertions lack messages.
- 🟡 Warning: multiple Mystery Guests; several ambiguous test names.
- 🟢 Suggestion: minor naming issues; isolated General Fixture.

### What Not to Flag
- Multiple assertions are acceptable when they describe one coherent behavior and fail with a clear story.
- Shared setup is fine when every initialized value is relevant to nearly every test.
- Concise test names are acceptable if scenario and expected outcome are still obvious.

---

## Risk T2: Test Brittleness

**Diagnostic question:** Do tests break when you refactor without changing behavior?

Brittle tests punish refactoring — eventually developers stop refactoring to protect the suite.

### Symptoms
- Tests assert on private method results, internal state, or implementation details.
- Eager Test: one method verifies multiple unrelated behaviors.
- Over-specified: assertions enforce mock call order or exact param values irrelevant to behavior.
- Renaming/extracting a method causes > 5 tests to fail with no behavior change.
- Erratic Test: different results across runs without production change (race, time, random, shared state).

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Eager Test | Meszaros — xUnit Test Patterns | Eager Test (p.228) |
| Erratic Test | Meszaros — xUnit Test Patterns | Erratic Test |
| Implementation coupling | Osherove — The Art of Unit Testing | Test isolation principle |
| Orthogonality violation | Hunt & Thomas — The Pragmatic Programmer | Ch. 2: Orthogonality |

### Severity Guide
- 🔴 Critical: behavior-preserving refactor causes test failures; > 5 tests coupled to one impl detail.
- 🟡 Warning: Eager Tests common; moderate implementation-detail assertions.
- 🟢 Suggestion: isolated over-specification in non-critical tests.

### What Not to Flag
- Verifying an externally observable event or emitted command is not implementation coupling.
- One test with several assertions is acceptable when all support one behavior claim.
- A fake/in-memory adapter is not brittleness if the test still asserts behavior, not wiring.

---

## Risk T3: Test Duplication

**Diagnostic question:** Is the same test scenario expressed in more than one place?

Duplicated tests must change in multiple places and create false confidence without testing distinct behavior.

### Symptoms
- Test Code Duplication: same setup/assertion logic copy-pasted without extraction.
- Lazy Test: multiple tests verifying identical behavior with no differentiation.
- Same boundary condition tested identically at unit, integration, and E2E with no layer differentiation.
- Test helpers/fixtures duplicated across files instead of shared.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Test Code Duplication | Meszaros — xUnit Test Patterns | Test Code Duplication (p.213) |
| Lazy Test | Meszaros — xUnit Test Patterns | Lazy Test (p.232) |
| DRY violation in tests | Hunt & Thomas — The Pragmatic Programmer | DRY |

### Severity Guide
- 🔴 Critical: core scenario fully duplicated across all three test layers with no differentiation.
- 🟡 Warning: common scenario setup repeated in 5+ tests without extraction.
- 🟢 Suggestion: minor helper duplication; isolated Lazy Tests.

### What Not to Flag
- The same scenario may appear at unit and integration level when each verifies a distinct risk.
- Small local setup duplication can be clearer than an over-abstracted fixture maze.
- Similar assertions against different domain rules are not Lazy Tests if business intent differs.

---

## Risk T4: Mock Abuse

**Diagnostic question:** Is the test more complex than the behavior it tests?

Mock abuse produces tests that pass while verifying nothing — production code can be fully broken as
long as the mocks are wired up.

### Symptoms
- Mock setup code longer than the test logic itself.
- Primary assertion is `expect(mock).toHaveBeenCalledWith(...)` — verifies a mock was called, not real behavior.
- Test-only methods added to production classes for lifecycle management in tests.
- Single unit test uses > 3 mocks.
- Incomplete Mock: mock missing fields downstream code will access (silent integration failures).
- Hard-Coded Test Data: no resemblance to real data shapes/constraints.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Mock count > 3 | Osherove — The Art of Unit Testing | Mock usage guidelines |
| Testing mock behavior | Meszaros — xUnit Test Patterns | Behavior Verification (p.544) |
| Test-only production methods | Feathers — Working Effectively with Legacy Code | Ch. 3: Sensing and Separation |
| Hard-Coded Test Data | Meszaros — xUnit Test Patterns | Hard-Coded Test Data (p.534) |
| Incomplete Mock | Osherove — The Art of Unit Testing | Mock completeness requirement |

### Severity Guide
- 🔴 Critical: mock setup > 50% of test code; production class has methods only called from tests.
- 🟡 Warning: mocks consistently > 3 per test; primary assertions are mock call verifications.
- 🟢 Suggestion: isolated Incomplete Mocks; minor Hard-Coded Test Data.

### What Not to Flag
- A small number of mocks around nondeterministic dependencies is acceptable when assertions still verify behavior.
- Fakes and spies used to observe state transitions are not mock abuse by default.
- One interaction assertion may be appropriate when the interaction itself is the behavior under test.

---

## Risk T5: Coverage Illusion

**Diagnostic question:** Does the test suite actually protect against the failures that matter?

Coverage measures execution, not verification. 90% line coverage can still miss every critical
failure mode.

### Symptoms
- High line coverage but error-handling branches, boundaries, exception paths untested.
- Happy-path only: no sad paths, no null/empty/zero inputs, no concurrency edge cases.
- Legacy code areas actively modified with no tests (Feathers: "legacy code is code without tests").
- Coverage % treated as a sign-off criterion; critical change paths remain untested.
- Tests assert return values but not important side effects (DB writes, event publishes, state transitions).

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Legacy code = no tests | Feathers — Working Effectively with Legacy Code | Ch. 1 |
| Change coverage vs line coverage | Google — How Google Tests Software | Ch. 11: Testing at Google Scale |
| Happy-path only | Osherove — The Art of Unit Testing | Test completeness principle |

### Severity Guide
- 🔴 Critical: legacy code area actively modified with no tests; error-handling paths entirely absent.
- 🟡 Warning: coverage > 80% but edge and exception paths systematically absent.
- 🟢 Suggestion: a few non-critical paths missing sad-path tests.

### What Not to Flag
- High line coverage is useful when paired with branch, boundary, and change-path coverage.
- A new module may have limited coverage early if still private and low-risk.
- Side-effect assertions may live in integration tests without implying a gap.

---

## Risk T6: Architecture Mismatch

**Diagnostic question:** Does the test suite structure reflect the system's actual risk profile?

Wrong suite shape is slow and expensive — not from bad tests, but from using the wrong type at the
wrong layer.

### Symptoms
- Inverted test pyramid: E2E/integration count exceeds unit count → slow, fragile suite.
- Legacy code with no seam points (no interfaces, DI, or seams) → impossible to test in isolation.
- Legacy areas modified with no Characterization Tests to capture current behavior before changes.
- Full suite execution > 10 minutes (architectural problem, not performance).
- High-risk and low-risk paths tested at identical density; no risk-based prioritization.

### Sources
| Symptom | Book | Principle / Smell |
|---------|------|-------------------|
| Inverted pyramid | Google — How Google Tests Software | 70:20:10 unit:integration:E2E ratio |
| No seam points | Feathers — Working Effectively with Legacy Code | Ch. 4: Seam Model |
| Missing Characterization Tests | Feathers — Working Effectively with Legacy Code | Ch. 13: Characterization Tests |
| Suite execution time | Meszaros — xUnit Test Patterns | Slow Tests (p.253) |

### Severity Guide
- 🔴 Critical: legacy code modified has no seams and no characterization tests; pyramid fully inverted.
- 🟡 Warning: suite > 10 min; integration/E2E count exceeds unit tests.
- 🟢 Suggestion: localized pyramid deviation; a few legacy areas missing characterization tests.

### What Not to Flag
- Deviating from 70:20:10 can be justified by platform constraints or product risk.
- A suite heavy on integration tests can be healthy if feedback is fast and purposefully layered.
- A small number of critical-path E2E tests is desirable, not a smell.
