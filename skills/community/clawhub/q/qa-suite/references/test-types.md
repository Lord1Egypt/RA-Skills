# Test Types Decision Reference

## Decision Tree

For each test type, answer three questions in order:

1. Has this class of bug occurred in this project's history?
2. If this class of bug occurs, how severe is the impact?
3. Is the maintenance cost of this test type acceptable for this project?

The more "yes" answers, the more likely the test type should be adopted.

## Test Type Definitions and Criteria

### Unit Tests

- **What**: Individual function/method/class behavior, no external dependencies
- **When needed**: Always
- **When NOT needed**: Never — unit tests are the floor
- **Target**: Core logic 100%, boundary and utility functions 80%+
- **Not for**: Testing that mocks were called, testing third-party library behavior

### Integration Tests

- **What**: Your code interacting with external systems (database, API, message queue, filesystem)
- **When needed**: When external dependencies exist
- **When NOT needed**: Pure computation/transformation functions with no side effects
- **Target**: At least one happy path + one failure path per external integration
- **Tools**: testcontainers (preferred), Docker Compose, transaction rollback

### API Contract Tests

- **What**: API request/response format compatibility between producers and consumers
- **When needed**: Multi-service architecture, independent consumer and producer teams
- **When NOT needed**: Monolith, internal services without independent consumers
- **Tools**: Pact, schemathesis

### E2E Tests

- **What**: Complete user flows (login → action → result)
- **When needed**: User-visible critical paths with high regression risk
- **When NOT needed**: No-UI services, pure APIs, CLI tools
- **Count**: 3-10 critical flows, not 100+
- **Tools**: Playwright (Web), Detox/Maestro (Mobile), Cypress (alternative)

### Performance Tests

- **What**: Response time, throughput, resource usage
- **When needed**: Latency-sensitive, high-traffic, SLA-bound
- **When NOT needed**: Internal tools, prototypes, low-traffic services
- **Method**: Measure baseline → fix → re-measure → report before/after numbers
- **"Feels faster" is not evidence**

### Visual Regression Tests

- **What**: Pixel-level comparison of UI rendering before and after changes
- **When needed**: UI component library, design system, brand pages
- **When NOT needed**: Content-driven pages (intentional style changes), prototypes
- **Tools**: Chromatic, Percy, Playwright screenshot diff

### Snapshot Tests

- **What**: Text representation of component/output
- **When needed**: UI components with stable output, config generation, serialized output
- **When NOT needed**: Frequently changing output, timestamps or unstable fields
- **Trap**: Updating snapshots without inspection = testing nothing

### Accessibility Tests

- **What**: Keyboard navigation, screen reader compatibility, contrast
- **When needed**: User-facing products, compliance requirements
- **When NOT needed**: Internal tools, developer tools, CLI
- **Tools**: axe-core, Lighthouse, Pa11y

### Security Tests

- **What**: Known vulnerabilities, injection attacks, auth bypass
- **When needed**: Handling sensitive data, auth systems, public-facing
- **When NOT needed**: Internal tools, isolated networks
- **Tools**: Static analysis (bandit, gosec), dependency scanning (npm audit, trivy), SAST (semgrep)

## Test Pyramid Ratios by Project Type

| Project Type | Unit | Integration | E2E | Other |
|-------------|------|-------------|-----|-------|
| Library/SDK | 80% | 15% | 5% (property-based) | - |
| Backend API | 40% | 40% | 5% | 15% contract |
| Frontend SPA | 35% | 30% (MSW) | 25% | 10% visual/a11y |
| Mobile App | 30% | 30% (component) | 15% (smoke) | 25% other |
| CLI Tool | 50% | 40% (exec+assert) | 10% (snapshot) | - |

These are starting points, not laws. Adjust based on project risk profile.

## Warning Signs

- **All E2E, no unit tests** — E2E is too slow and brittle to be the safety net
- **Zero integration tests with a database** — Unit tests mock the DB, never test real queries
- **Snapshot explosion** — One snapshot per component = maintenance nightmare; only snapshot stable outputs
- **Zero coverage** — No safety net at all, every change is a gamble
