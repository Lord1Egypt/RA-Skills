---
name: qa-suite
description: >
  Testing strategy and execution for any project. Determines what test types
  apply, recommends frameworks, inspects existing test infrastructure, sets
  up environments, generates detailed interaction (E2E) test plans, and
  executes integration tests and E2E tests (including regression, robustness,
  and failure path testing). Produces a QA Report with coverage matrix and
  results. Unit test execution is delegated to coding-tactics (TDD/BDD).
  Triggers when users ask about testing strategy, test setup, test
  environment, what tests to write, how to test interactive features,
  or when integration/E2E test execution is needed.
  Chinese triggers: "测试策略", "写测试", "测试环境", "搭建测试", "单元测试",
  "集成测试", "e2e", "测试框架", "覆盖率", "没有测试", "加测试", "测试数据",
  "mock", "测试计划", "交互测试", "怎么测", "测什么", "回归测试", "边界测试",
  "健壮性", "跑测试", "执行测试".
metadata:
  author: shipmate
  version: "1.0.0"
  openclaw:
    emoji: "🛡️"
    requires:
      bins:
        - python3
---

# QA-Suite: Strategy + Execution

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this skill is active.

**Read this contract aloud before taking any action:**

> I will NOT recommend a test framework before analyzing the project's language, platform, and existing dependencies.
> I will NOT suggest writing tests without first inspecting what test infrastructure already exists.
> I will NOT claim "no tests needed" without reviewing the project structure and risk profile.
> I will reference coding-tactics for unit test execution (TDD/BDD) — I will NOT write unit tests myself.
> I WILL write and execute integration tests and E2E tests, including regression, robustness, and failure path tests.
> I will NOT test only happy paths — every feature point MUST be evaluated against failure paths, boundary attacks, and concurrent operations.
> I will prioritize Docker-based containerized environments (Docker Compose / Testcontainers) when constructing test environments to ensure isolation, reproducibility, and local-CI parity.
> I will treat "no test environment" as a valid starting point, providing incremental adoption steps.
> For E2E/interaction testing, I will investigate specific features, elements, and behaviors before writing a test plan.
> After execution, I will produce a single QA Report with coverage matrix, results, and recommendations.

**These are not suggestions. Breaking any of them means you are not using this skill — you are ignoring it.**

---

## Outcome Contract

- Outcome: A concrete testing strategy with recommended test types, frameworks, environment setup steps, executed integration/E2E tests, internal quality gate verdict, and a QA Report.
- Done when: Test types are selected with rationale, frameworks are recommended, environment is set up, integration tests and E2E tests are written and run, the internal quality gate is evaluated (PASSED, BLOCKED, or CONDITIONAL_PASS), and a QA Report is produced.
- Evidence: Project analysis, environment inspection results, test execution output, internal gate checklist, QA Report.
- Output: Testing strategy document + executable setup commands + test code files + QA Report.

## Mode Picker

| User intent | Mode | Load |
|-------------|------|------|
| "What tests should I write", "testing strategy", "测试策略" | Default: Full strategy | references/test-types.md |
| "Set up test environment", "搭建测试环境" | Environment setup | references/environment-inspection.md, then platform-specific env file |
| "No test environment exists", "没有测试" | No-environment fallback | references/no-environment.md |
| "Add tests to existing project", "加测试" | Incremental adoption | references/test-types.md |
| "Test data management", "测试数据", "fixtures" | Test data | references/test-data.md |
| "CI/CD integration", "automated tests" | CI integration | references/ci-integration.md |
| "E2E test plan", "交互测试", "UI test plan" | Interaction test plan | references/interaction-test-plan.md |
| "Run integration tests", "集成测试", "跑集成测试" | Integration test execution | references/integration-test-execution.md |
| "Run E2E tests", "跑E2E", "回归测试", "边界测试", "健壮性测试" | E2E test execution | references/e2e-test-execution.md |

## Hard Rules

1. **Strategy before execution**: Recommend what and why before running any test command. This skill owns strategy AND execution for integration/E2E tests; coding-tactics owns unit test execution.
2. **Inspect before recommending**: Always run the environment inspection checklist (references/environment-inspection.md) before recommending frameworks or setup steps.
3. **Prefer existing frameworks**: Check package.json / go.mod / requirements.txt / Cargo.toml first. Never introduce a new framework when one is already in use.
4. **No test environment is a valid starting point**, not a failure. Provide incremental adoption steps.
5. **Unit tests → coding-tactics**: Point to coding-tactics for TDD/BDD unit test execution. Do NOT write unit tests in this skill.
6. **Integration/E2E tests → this skill**: Write and run integration tests (references/integration-test-execution.md) and E2E tests (references/e2e-test-execution.md) directly.
7. **Platform-appropriate defaults**: Don't recommend Playwright for a CLI tool. Don't recommend Jest for a Go project.
8. **Risk-proportional scope**: A simple CRUD app needs fewer test types than a payment system.
9. **Coverage is a signal, not a target**: Don't set arbitrary % targets. Calibrate thresholds to risk and test type.
10. **Test what can break**: Don't test framework internals, trivial getters/setters, or generated code.
11. **Interactive effects are first-class**: For UI tests, investigate and plan for interaction behaviors (validation feedback, loading states, error states, empty states, animations, keyboard navigation) — not just happy paths.
12. **Failure paths are mandatory**: Every feature point MUST be tested for failure paths, boundary attacks, and concurrent operations — not just happy paths.
13. **Prioritize Docker for test environment construction**: When building or proposing test environments, prioritize Docker / Docker Compose or Testcontainers over local host installation.
14. **One QA Report**: After all tests complete, produce a single QA Report (see references/e2e-test-execution.md Part 8). The report presents facts; it does NOT make pass/fail judgments for external reviewers.
15. **Internal quality gate is self-enforced**: QA evaluates its own internal quality gate (planning integrity, 100% execution, P0 zero-tolerance, failure evidence) before declaring completion. If P0 tests fail due to product defects, QA issues a `BLOCKED` verdict with reproducible evidence.

## Workflow

### Step 1: Discover Project

Before any strategy recommendation, collect project context:

1. **Language/Platform**: Read package manager files (package.json, go.mod, requirements.txt, pyproject.toml, Cargo.toml, Gemfile, CMakeLists.txt)
2. **Existing test files**: Glob for `*test*`, `*spec*`, `test_*`, `*_test.*`
3. **Existing test config**: Jest config, vitest.config, pytest.ini, pyproject.toml [tool.pytest]
4. **CI config**: `.github/workflows/*.yml`, `.gitlab-ci.yml`, Makefile test targets
5. **Project type**: Backend (API/microservice/CLI), Frontend (SPA/SSR), Mobile (iOS/Android/RN/Flutter), Desktop (Electron/Tauri/native), Library/SDK

### Step 2: Inspect Existing Test Environment

Load `references/environment-inspection.md`. Run the inspection checklist against the project. Check:
- Test frameworks already installed
- Test configuration files present
- Test directories exist
- Test commands defined in package.json/Makefile
- CI pipeline includes test steps
- Test data/fixtures/seeds present

Output a baseline assessment: What exists, what's missing, maturity level (none / minimal / partial / mature).

### Step 3: Determine Test Types

Load `references/test-types.md`. For each applicable category, determine whether it's needed with rationale.

| Test Type | When to apply | Severity if missing |
|-----------|--------------|---------------------|
| Unit | Always | High (no safety net) |
| Integration | External dependencies (DB, API, message queue) | High (can't verify real behavior) |
| API Contract | Multi-service, consumer-provider | Medium (breaking changes undetected) |
| E2E | User-facing flows, critical paths | Medium (user-visible regressions) |
| Performance | Latency-sensitive, high-traffic | Low (until it matters) |
| Visual Regression | UI component library, design system | Low (until it matters) |
| Snapshot | UI components with stable output | Low (overlapping with unit + visual) |
| Accessibility | User-facing UI, compliance | Medium (legal risk) |
| Security | Auth, payment, sensitive data | Medium (security incident risk) |

### Step 4: Recommend Frameworks

Based on discovered project context plus inspection results. Prefer frameworks already in the project's dependencies.

| Platform | Unit | Integration | E2E | Contract | Performance |
|----------|------|-------------|-----|----------|-------------|
| Python | pytest | pytest + testcontainers | Playwright | schemathesis | locust |
| Go | testing + testify | testcontainers-go | Playwright | pact-go | vegeta |
| Node (Backend) | vitest / jest | vitest + testcontainers | Playwright | pact-js | k6 |
| Frontend | vitest + Testing Library | MSW + vitest | Playwright | pact-js | lighthouse |
| Rust | cargo test | testcontainers-rs | Playwright | pact-rust | criterion |
| Mobile | XCTest / JUnit | integration stubs | Detox / Maestro | - | - |
| Desktop | platform-native | Electron: spectron; Tauri: cargo test | Playwright (Electron) | - | - |

State: "Found {framework} in {dependency file}, recommending it."

### Step 5: Environment Setup Routing

When constructing the test environment, **always prioritize Docker-based containerization** (e.g., Docker Compose, Testcontainers, or Dockerized test runners) to ensure environment parity between local development and CI pipelines without host machine pollution.

Based on project type, load the appropriate environment reference:
- Backend → `references/environment-backend.md`
- Frontend → `references/environment-frontend.md`
- Mobile → `references/environment-mobile.md`
- Desktop → `references/environment-desktop.md`
- No existing test infra → `references/no-environment.md`

### Step 6: Interaction Test Plan (when applicable)

**Activate when**: User mentions E2E, 交互测试, UI testing, browser testing, 端到端测试, or recommended test types include E2E.

Load `references/interaction-test-plan.md`. This step produces:

1. **Feature inventory** — List every user-facing feature/page/flow
2. **Element registry** — For each feature, enumerate interactive elements (buttons, inputs, forms, dropdowns, modals, tooltips, drag targets)
3. **Behavior catalog** — For each element, document:
   - Happy path
   - Validation states (invalid input → error, field highlight)
   - Loading states (spinner, skeleton, disabled)
   - Empty states (no data → empty UI)
   - Error states (API failure → error display, retry)
   - Edge cases (max length, special characters, boundary values)
4. **Output**: A feature-by-feature test plan ready for webapp-testing or Agent Browser.

### Step 7: CI Integration Guidance

Load `references/ci-integration.md`. Output CI-ready commands.

### Step 8: What NOT to Test

Explicitly call out anti-patterns for the specific project:
- Framework internals (don't test React/Vue behavior — test your code)
- Trivial getters/setters
- Mock verification (test outcomes, not interactions)
- Test infrastructure itself
- Generated code (proto stubs, OpenAPI clients)
- Config files without logic

### Step 9: Integration Test Execution

**Activate when**: Recommended test types include Integration, or user explicitly requests integration tests.

Load `references/integration-test-execution.md`. This step:

1. Confirms test environment is ready (Docker/Testcontainers from Step 5)
2. Identifies external dependencies of the module under test (DB, API, queue)
3. Writes integration test code files using real services (not mocks)
4. Runs the tests and captures results
5. Each dependency gets: happy path + failure path + data integrity test
6. Reports results in the structured format defined in the reference

### Step 10: E2E Test Execution

**Activate when**: Recommended test types include E2E, user requests E2E/browser/interaction testing, or project has user-facing UI.

Load `references/e2e-test-execution.md`. This step:

1. Takes the interaction test plan from Step 6 as input
2. Converts the plan into Playwright `.spec.ts` files (code mode, default)
   - Or performs live browser automation via Agent Browser (live mode, on request)
3. Tests MUST include:
   - **Happy paths** for each feature
   - **Robustness tests** across 8 categories (input boundary, network failure, concurrent ops, auth, state persistence, browser compat, responsive, accessibility)
   - **Failure path tests** for all API error states and edge conditions
   - **Regression baselines** (visual snapshots + API response structure)
4. Runs the tests, captures screenshots on failures
5. Evaluates internal quality gate (Step 11)
6. Produces the **QA Report** (single report with internal gate verdict, coverage matrix, results, recommendations)

### Step 11: Internal Quality Gate

**Activate after**: Test execution (Step 9 and/or Step 10) completes, before final delivery.

QA enforces its own quality gate using the deterministic validation script:
```bash
python3 scripts/validate_qa_gate.py check <qa_report.json> [--json]
```

The script evaluates 4 deterministic criteria:
1. **Planning Integrity**: Coverage matrix is complete; no unassessed empty cells without explicit reason.
2. **Execution Completeness**: 100% of planned tests executed (`planned == executed`). Zero dropped tests.
3. **P0/P1 Defect Gate**: Zero unresolved P0/P1 failures.
4. **Evidence Chain**: Every failure has attached screenshot, reproduction command, and error trace.

#### Handling Gate Verdicts & Decoupled Decisions

- **`PASSED` (exit code 0)**: All planned tests executed, 0 blocking failures. Deliver the final QA Report.
- **`CONDITIONAL_PASS` (exit code 2)**: Only non-critical (P2/P3) defects remain. Document risks and deliver QA Report with remediation advice.
- **`BLOCKED` (exit code 1)**: Critical P0 failure, unexecuted planned tests, or incomplete planning.
  - **Standalone Mode (direct user interaction)**:
    QA MUST NOT unilaterally terminate or throw a hard error. Instead, QA surfaces the exact blocking failure, root cause, and screenshots, then **presents 3 decision options to the user**:
    1. `[Fix Code]` (Fix production code) → Dispatch/guide fix, then re-run test.
    2. `[Waive Block]` (Waive defect for current scope) → User confirms defect is acceptable for current scope; records waiver rationale in report and completes.
    3. `[Update Expectation]` (Update test expectation) → Requirement changed or assertion overly strict; update test and re-run.
  - **Cross-invocation Mode (`workflow-orchestrator` orchestration)**:
    QA outputs the structured JSON report with `gate_verdict: "BLOCKED"` and failure details. **`workflow-orchestrator`'s meta-orchestrator (judge/evaluator) autonomously decides** whether this truly blocks the task (dispatching `fixer` into `needs_fix`) or can be waived/skipped based on tier, scope boundary, and risk profile.

The gate verdict is embedded at the top of the final QA Report.

## Integration with Other Skills

### Unit tests → coding-tactics
```
Unit test execution is NOT this skill's job.
To write unit tests using TDD: /coding-tactics tdd
To write unit tests using BDD: /coding-tactics bdd
```

### Integration/E2E tests → this skill
```
This skill writes and executes integration tests and E2E tests directly.
- Integration tests: Step 9 (references/integration-test-execution.md)
- E2E tests: Step 10 (references/e2e-test-execution.md)
No external delegation required.
```

### Integration with scenario-standards
```
- Backend Phase: invoke /qa-suite for strategy, env setup, AND integration test execution
- Frontend Phase: invoke /qa-suite for strategy, env setup, AND E2E test execution
- Before E2E steps: use Step 6 interaction test plan → Step 10 E2E execution
- DevOps Phase: reference ci-integration.md for CI patterns
```

## Output

### Standard Output (all modes)

```markdown
## QA Suite: {project name}

### Project Profile
- Language: {language}
- Platform: {backend|frontend|mobile|desktop|library}
- Test maturity: {none|minimal|partial|mature}
- Existing tests: {file count}
- CI: {platform or none}

### Recommended Test Types
| Type | Apply? | Framework | Rationale |
|------|--------|-----------|-----------| 
| ...  | ...    | ...       | ...       |

### Environment Setup
```bash
# Commands to set up test environment
```

### Gap Analysis
- Missing: {test types or capabilities not yet implemented}
- Fallback plan: {no-environment strategy if applicable}

### Next Steps
1. Run: {setup command}
2. Unit tests: invoke /coding-tactics tdd (or /coding-tactics bdd)
3. Integration tests: this skill executes directly (Step 9)
4. E2E tests: this skill executes directly (Step 10)
```

### QA Report Output (after test execution)

See `references/e2e-test-execution.md` Part 8 for the full QA Report template.
The report includes: Summary, Coverage Matrix, Failures, Regression Baseline, Recommendations.

### Interaction Test Plan Output (when applicable)

```markdown
### Interaction Test Plan

#### Feature: {feature name}
| # | Element | Action | Expected Behavior | State Type |
|---|---------|--------|-------------------|------------|
| 1 | Email input | Leave empty, click Submit | Shows "Email is required", red border | Validation |
| 2 | Email input | Type "not-an-email" | Shows "Invalid email format" | Validation |
| 3 | Email input | Type "user@example.com" | No error, green indicator | Happy path |
| 4 | Submit button | Click during loading | Button disabled, shows spinner | Loading |
| 5 | Submit button | Click, API returns 500 | Shows error toast "Something went wrong" | Error |

#### Feature: {next feature}
...
```

## Gotchas

| What happened | Rule |
|---------------|------|
| Recommended Jest for a Go project | Always check package manager first; match framework to language |
| Suggested Playwright for a CLI tool | Playwright is for web UIs only; CLI tools need integration/unit tests |
| Set up complex Docker env for a simple script | Calibrate env complexity to project risk |
| Ignored existing pytest.ini while recommending new setup | Always inspect before recommending |
| Treated "no tests" as a failure | "No tests" is a starting point; provide incremental adoption path |
| Missed input validation behaviors in E2E plan | Investigate every form field for validation states — not just happy paths |
| Skipped empty/error/loading states in interaction plan | Every UI element has 3+ states: happy, empty, loading, error |
