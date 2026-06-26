# Testing Methodologies Reference

This document provides detailed guidance for each testing methodology included in the QA Architecture Auditor skill. Each section covers:

- **Purpose**: Why this testing type matters
- **When to Apply**: Decision criteria based on codebase characteristics
- **Independent Baseline**: Minimum expectations from scratch
- **Key Activities**: Concrete tasks to perform
- **Success Criteria**: How to measure adequacy

## Core Execution Approaches

### Black Box Testing

**Purpose**: Validate functionality without knowledge of internal implementation. Simulates real user behavior and tests the system as a complete unknown.

**When to Apply**:
- When requirements/specs are available but code may not be
- For API contract validation
- For security testing from an attacker's perspective
- When testing third-party integrations

**Independent Baseline**:
- All public interfaces (APIs, UI, CLI) must be tested
- No knowledge of internal code structure used
- Tests derived solely from requirements and observable behavior

**Key Activities**:
1. Identify all inputs, triggers, and expected outputs
2. Create equivalence classes for inputs (valid/invalid/boundary)
3. Build decision tables for complex business rules
4. Execute tests without looking at source code
5. Document actual vs expected behavior

**Success Criteria**:
- 100% of public APIs exercised
- All error messages validated
- Boundary conditions covered

### White Box Testing

**Purpose**: Maximize code coverage by testing internal paths, conditions, and branches. Ensures all logic paths are exercised.

**When to Apply**:
- For unit tests on critical functions
- When achieving high code coverage is mandatory
- To uncover hidden bugs in complex conditional logic
- For security-critical code paths

**Independent Baseline**:
- All functions, methods, and classes must have unit tests
- Statement coverage >90%
- Branch coverage >85%
- Path coverage for complex functions (>15 cyclomatic complexity)

**Key Activities**:
1. Generate control flow graphs
2. Identify all branches and conditions
3. Create test cases to exercise every branch (both true and false)
4. Use mock objects to isolate units
5. Measure coverage with tools (coverage.py, Jest --coverage, etc.)

**Success Criteria**:
- Coverage reports show >80% overall
- All public functions have tests
- Complex functions have 100% branch/path coverage

### Manual Testing

**Purpose**: Leverage human intuition, creativity, and judgment to find issues automation cannot detect.

**When to Apply**:
- Usability and UX evaluation
- Exploratory testing to discover unknown unknowns
- Visual/UI verification (layouts, colors, fonts)
- Accessibility checks with screen readers
- Ad-hoc scenario validation

**Independent Baseline**:
- All user-facing workflows must be manually tested at least once
- Usability heuristics evaluated
- Cross-browser/device checks performed

**Key Activities**:
1. Create test charters with exploration goals
2. Document observations in real-time
3. Take screenshots of defects
4. Note usability issues and confusion points
5. Test on real devices, not just emulators

**Success Criteria**:
- Chartered sessions produce documented insights
- All critical user journeys manually validated
- Usability issues identified and prioritized

### Automated Testing

**Purpose**: Reliable, repeatable tests that run without human intervention, enabling continuous integration.

**When to Apply**:
- Any test run on every commit/PR
- Regression suite
- Smoke tests on build
- API contract validation
- Performance benchmark tests

**Independent Baseline**:
- All unit tests automated
- All integration tests automated
- Critical user journeys (smoke) automated
- CI/CD pipeline runs tests automatically

**Key Activities**:
1. Choose appropriate frameworks (pytest, Jest, TestNG, etc.)
2. Write deterministic, independent test cases
3. Use fixtures and factories for test data
4. Parallelize where possible for speed
5. Integrate with CI platform (GitHub Actions, GitLab CI, Jenkins)

**Success Criteria**:
- Automation runs on every push
- Test execution time <10 minutes
- Flaky tests <1% of total

## Functional & Structural Testing

### Unit Testing

**Purpose**: Test individual functions/methods in isolation with mocked dependencies.

**Independent Baseline**:
- Every public function has at least one test
- Every branch and edge case tested
- Mock all external dependencies (DB, APIs, file system)
- Success: >80% code coverage from unit tests alone

**From-Scratch Test Cases**:
- Calculate Fibonacci with various inputs (including 0, 1, negative)
- String manipulation functions with empty, long, unicode inputs
- Math functions with decimal precision, overflow, zero division
- Date/time handling with timezones, DST, leap years

**Tooling**: pytest (Python), Jest (JS/TS), JUnit (Java), Go test (Go)

### Integration Testing

**Purpose**: Validate interactions between modules, services, and external systems.

**Independent Baseline**:
- All module interfaces tested
- Database transactions verified
- API contracts validated
- External service integrations tested with realistic data
- Success: All integration points have test coverage

**From-Scratch Test Cases**:
- API → Database: Verify data persists correctly and queries return expected results
- Service → Service: Mock external services, verify request/response formats
- Event-driven: Test message queue producers and consumers with real message formats
- Authentication flow: Login → token → call protected endpoint → validate token works

**Tooling**: pytest with fixtures, TestContainers for real databases, WireMock/Mountebank for HTTP mocking

### System Testing

**Purpose**: Validate the complete, integrated application in a production-like environment.

**Independent Baseline**:
- Full deployment to staging environment
- All services start correctly and communicate
- All external integrations configured and working
- Performance benchmarks met
- Success: End-to-end functional validation passes

**From-Scratch Test Cases**:
- Deploy entire stack, run health checks on all components
- Verify service discovery and configuration
- Test failover and redundancy (if applicable)
- Validate monitoring and logging are working
- Load test the complete system with realistic traffic patterns

**Tooling**: Docker Compose, Kubernetes (if applicable), Ansible/Terraform for infrastructure as code, monitoring stacks

### Functional Testing

**Purpose**: Verify that business requirements and logic are correctly implemented.

**Independent Baseline**:
- Every user story and acceptance criterion mapped to test scenarios
- All business rules validated
- Positive and negative scenarios covered
- Edge cases for business logic
- Success: 100% of requirements have passing functional tests

**From-Scratch Test Cases**:
- Requirement: "User can only cancel orders within 24 hours" → test within 24h (allowed) and after 24h (rejected)
- Requirement: "Discount codes apply only to eligible products" → test with eligible/ineligible items
- Requirement: "Admins can delete any content; users can only delete their own" → test role-based access

**Tooling**: BDD frameworks (Cucumber, Behave), test case management tools

### Smoke Testing

**Purpose**: Quick verification that the build is stable enough for further testing.

**Independent Baseline**:
- Smoke test suite runs in <5 minutes
- Covers all critical user paths
- Must pass before any QA or deployment
- Automatically triggered on every build
- Success: 100% smoke tests passing

**From-Scratch Test Cases**:
- Application starts without errors
- Health endpoint returns 200 OK
- Login/logout works
- Create a basic resource (e.g., order, ticket, document)
- Perform primary search operation
- All external connections (DB, cache, queue) are healthy

**Tooling**: pytest, shell scripts, health check endpoints

### Sanity Testing

**Purpose**: Focused testing on specific functionality after code changes to ensure stability.

**Independent Baseline**:
- Sanity checklist for each module
- Run after every change to that module or related modules
- Quick execution (<2 minutes)
- Success: All sanity checks pass before merge

**From-Scratch Test Cases**:
- If auth module changed: Test login, logout, password reset, session management
- If payment module changed: Test successful payment, declined payment, refund
- If database schema changed: Test CRUD on affected tables

**Tooling**: Targeted subset of unit/integration tests

### End-to-End (E2E) Testing

**Purpose**: Test complete user workflows from UI to database.

**Independent Baseline**:
- All critical user journeys covered
- Tests run against deployed application (staging)
- Use real browsers, not headless only
- Include setup/teardown for test isolation
- Success: All E2E tests pass reliably (<1% flaky)

**From-Scratch Test Cases**:
- User Registration → Email Verification → Login → Profile Update → Logout
- Product Search → Product View → Add to Cart → Checkout → Payment → Order Confirmation
- Admin Login → User Management → Create User → Assign Role → Verify Permissions

**Tooling**: Playwright, Cypress, Selenium

### Regression Testing

**Purpose**: Ensure new changes do not break existing functionality.

**Independent Baseline**:
- Full regression suite run on every release candidate
- All previously fixed bugs have regression tests
- Automated regression runs must pass before release
- Success: Zero regression failures

**From-Scratch Test Cases**:
- Re-run all previously failed test scenarios (regression suite)
- Test all stable features unaffected by recent changes
- Performance regression: benchmark critical paths and ensure no degradation

**Tooling**: Full test suite, performance benchmark tools

### API Testing

**Purpose**: Validate REST/GraphQL/other API endpoints thoroughly.

**Independent Baseline**:
- All endpoints documented (OpenAPI/GraphQL schema)
- All HTTP methods tested (GET, POST, PUT, DELETE, PATCH)
- All status codes validated (200, 201, 400, 401, 403, 404, 500)
- Request/response schemas validated with JSON Schema
- Authentication and authorization enforced
- Rate limiting tested
- Success: 100% endpoint coverage with >50 test cases per endpoint

**From-Scratch Test Cases**:
- Valid request with all required fields → expect 200/201
- Missing required field → expect 400 with clear error
- Invalid data types (string vs int) → expect 422
- Unauthenticated request → expect 401
- Authenticated but unauthorized → expect 403
- Non-existent resource → expect 404
- Malformed JSON → expect 400
- SQL injection attempt → expect 400/422, no data leakage
- Large payload (attack/test) → expect appropriate limits

**Tooling**: pytest + requests, Postman/Newman, Schemathesis (property-based), Dredd

### Database/Data Integrity Testing

**Purpose**: Ensure data is stored, retrieved, and migrated accurately without loss or corruption.

**Independent Baseline**:
- All CRUD operations tested
- Database constraints validated (unique, foreign key, check)
- Transactions tested for atomicity, consistency, isolation, durability (ACID)
- Backup and restore procedures tested
- Database migrations tested on realistic datasets
- Data corruption detection and recovery
- Success: Zero data loss or corruption in test scenarios

**From-Scratch Test Cases**:
- Insert record, verify it can be retrieved with exact values
- Update record, verify changes persisted
- Delete record, verify removed but no orphaned rows
- Concurrent transactions: Two users edit same record → handle conflicts
- Transaction rollback: Force error mid-transaction, verify no partial writes
- Constraint violation: Duplicate unique field → expect error
- Foreign key violation: Delete parent with child records → expect error or cascade
- Database migration: Old schema → new schema, verify data intact
- Backup/restore: Full backup, destroy DB, restore, verify all data present
- Data corruption: Inject malformed data, verify detection and recovery

**Tooling**: TestContainers (real DB in Docker), factory_boy/Faker for test data, transaction rollback fixtures

## Non-Functional Testing

### Performance Testing

**Purpose**: Evaluate speed, stability, and capacity under load.

**When to Apply**:
- For user-facing applications with traffic expectations
- Before major releases and scaling events
- When performance SLAs are defined
- After significant architectural changes

**Independent Baseline**:
- Define performance benchmarks (response times, throughput)
- Establish baseline on non-production environment
- Load test at 2x expected peak traffic
- Stress test to find breaking point
- Success: All performance SLAs met at 2x peak load

**From-Scratch Test Cases**:
- **Load Testing**: Simulate expected concurrent users (e.g., 1000 users), measure avg/95th/99th percentile response times, ensure <2s for critical APIs
- **Stress Testing**: Ramp up users until system breaks, identify bottlenecks, ensure graceful degradation (no crashes)
- **Endurance Testing**: Sustained load (70% capacity) for 4+ hours, check for memory leaks, connection pool exhaustion
- **Spike Testing**: Sudden traffic spikes (10x to 100x), verify autoscaling or queueing works
- **Volume Testing**: Database with 10M+ records, test query performance, ensure indexes used
- **Soak Testing**: 24+ hour run to catch slow memory leaks

**Tooling**: k6, Locust, JMeter, Gatling, artillery

### Security Testing

**Purpose**: Identify vulnerabilities before attackers do.

**When to Apply**:
- All Internet-facing applications
- Applications handling sensitive data (PII, payments, health)
- Before production launches and major releases
- After significant security incidents
- Compliance requirements (SOC2, ISO27001, HIPAA, GDPR)

**Independent Baseline**:
- SAST (Static Application Security Testing) on every PR
- DAST (Dynamic Application Security Testing) on staging
- SCA (Software Composition Analysis) for dependency vulnerabilities
- Manual penetration testing at least annually or before major releases
- No critical/high vulnerabilities in automated scans
- Success: All OWASP Top 10 mitigated, zero critical vulnerabilities

**From-Scratch Test Cases**:
- **Authentication Bypass**: Attempt to access protected resources without valid credentials; test token tampering
- **Authorization Flaws**: Horizontal privilege escalation (User A access User B data); Vertical privilege escalation (user access admin functions)
- **Injection Attacks**: SQL injection, NoSQL injection, command injection, XSS, XXE, SSRF
- **Sensitive Data Exposure**: Verify secrets not in code/config; encryption used for PII at rest and in transit (TLS); check for data leakage in logs/error messages
- **XML External Entities (XXE)**: Test parsing of malicious XML payloads
- **Broken Access Control**: Insecure direct object references, missing function-level access control
- **Security Misconfiguration**: Default accounts, verbose error messages exposing stack traces, unused features enabled
- **Cross-Site Scripting (XSS)**: Reflected, stored, DOM-based; verify input sanitization and output encoding
- **Cross-Site Request Forgery (CSRF)**: Verify CSRF tokens or same-site cookies
- **File Upload Vulnerabilities**: Upload malicious files, test path traversal (../), verify content-type validation and virus scanning
- **API Security**: Rate limiting, JWT validation, scope-based authorization, GraphQL query depth limiting

**Tooling**:
- SAST: CodeQL, Semgrep, SonarQube, Snyk Code
- DAST: OWASP ZAP, Burp Suite, Nikto
- SCA: Snyk, Dependabot, OWASP Dependency-Check
- Penetration Testing: Manual with Burp Suite, custom scripts

### Usability Testing

**Purpose**: Ensure the application is intuitive, efficient, and satisfying to use.

**When to Apply**:
- Consumer-facing applications
- Complex enterprise tools with high user adoption barriers
- Major UI/UX redesigns
- Accessibility compliance (WCAG)

**Independent Baseline**:
- Conduct at least 5-10 user testing sessions per release
- Evaluate against Nielsen's 10 heuristics
- Measure task completion rate and time on task
- Success: >90% task completion without assistance, average satisfaction >4/5

**From-Scratch Test Cases**:
- **First-time user onboarding**: Can new users register and complete core workflow in <5 minutes with no help?
- **Error recovery**: When user makes mistake, is error message clear and recovery obvious?
- **Consistency**: Are similar actions performed similarly throughout the app?
- **Accessibility**: Can a blind user complete all critical tasks with a screen reader? Keyboard-only navigation works?
- **Mobile usability**: Touch targets >44x44px, scrolling smooth, no horizontal scroll

**Tooling**: Lookback, UserTesting.com, screen recording, heatmaps (Hotjar)

### Compatibility Testing

**Purpose**: Ensure the application works across different devices, browsers, OSes, and network conditions.

**When to Apply**:
- Web applications (cross-browser)
- Mobile apps (multiple OS versions, device sizes)
- Desktop apps (Windows, macOS, Linux)
- Applications with offline functionality

**Independent Baseline**:
- Define supported platforms matrix (browsers: latest 2 versions; OSes: supported versions)
- Test on all combinations in matrix
- Responsive design validated on multiple screen sizes
- Success: No critical bugs on any supported platform

**From-Scratch Test Cases**:
- **Browser matrix**: Chrome, Firefox, Safari, Edge (latest and previous version)
- **Mobile**: iOS Safari, Chrome Android, responsive breakpoints (320px, 768px, 1024px, 1440px)
- **OS-specific**: Windows 10/11, macOS 12+, Ubuntu 20.04+
- **Network conditions**: 3G (slow), 4G (moderate), WiFi (fast), offline mode (if PWA)
- **Screen readers**: NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android)

**Tooling**: BrowserStack, Sauce Labs, CrossBrowserTesting, real device lab

### Accessibility Testing

**Purpose**: Ensure people with disabilities can use the application (WCAG 2.1/2.2 compliance).

**When to Apply**:
- Public-facing websites and applications
- Government and educational institutions (legal requirements)
- Corporate applications with accessibility policies
- Any application where inclusive design is a goal

**Independent Baseline**:
- WCAG 2.1 AA level compliance
- Automated scan: 0 errors at AA level
- Manual screen reader testing: all critical pages navigable
- Keyboard-only navigation: complete all tasks without mouse
- Success: WCAG 2.1 AA compliance certified

**From-Scratch Test Cases**:
- **Perceivable**:
  - All images have meaningful alt text (except decorative)
  - Videos have captions and audio descriptions
  - Text has minimum contrast ratio 4.5:1 (3:1 for large text)
  - No content flashes more than 3 times per second (seizure safe)
- **Operable**:
  - All functionality available via keyboard (Tab, Enter, Space, Arrow keys)
  - Focus indicators visible on all interactive elements
  - No keyboard traps (user can navigate away)
  - Skip to main content link present
  - Page titles descriptive
- **Understandable**:
  - Language identified in HTML (`lang` attribute)
  - Navigation consistent across pages
  - Error messages clear, suggest corrections
  - Labels and instructions provided
- **Robust**:
  - Valid HTML with no parsing errors
  - ARIA used correctly (only when needed)
  - Custom components have appropriate ARIA roles/states

**Tooling**: axe DevTools, WAVE, Lighthouse accessibility audit, NVDA/VoiceOver screen readers, Pa11y

### Localization/Internationalization Testing

**Purpose**: Ensure application supports multiple languages and regional formats.

**When to Apply**:
- Multi-national deployments
- Languages requiring RTL layout (Arabic, Hebrew)
- Regions with different date/time/number formats
- Applications with user-generated content in multiple languages

**Independent Baseline**:
- No hardcoded strings in code (all in resource files)
- All UI elements accommodate text expansion (German ~30% longer than English)
- Date/time/number formats respect locale
- Unicode/UTF-8 everywhere
- RTL languages fully supported (layout mirroring, text alignment)
- Success: All locales render correctly, no text overflow or truncation

**From-Scratch Test Cases**:
- **String extraction**: Verify all user-facing strings in resource files (no hardcoded text)
- **Text expansion**: UI elements handle longer translations without breaking layout (test with German, Russian)
- **RTL support**: Arabic, Hebrew display right-to-left, punctuation on correct side, layout mirrored
- **Date formats**: US (MM/DD/YYYY), Europe (DD/MM/YYYY), ISO (YYYY-MM-DD)
- **Number formats**: Decimal separator (period vs comma), thousands separator, currency symbols
- **Timezones**: Display times in user's local timezone, DST handled correctly
- **Currency**: Correct symbol placement, formatting, rounding rules
- **Sorting**: Unicode-aware collation for different alphabets
- **Encoding**: UTF-8 files, database collation, API responses Content-Type headers

**Tooling**: Pseudolocalization tools, Crowdin/Transifex for translation management, real translators for validation

## Specialized & Exploratory Testing

### Acceptance Testing (UAT)

**Purpose**: Validate that software meets end-user business needs before production release.

**When to Apply**:
- Before production launches
- After major feature releases
- When stakeholders demand sign-off

**Independent Baseline**:
- Business users test in production-like environment
- All acceptance criteria validated
- Sign-off obtained from business stakeholders
- Success: Formal UAT sign-off received

**From-Scratch Test Cases**:
- For each user story, create UAT scenario in business language
- Provide test data and expected results
- Have business users execute scenarios and sign off
- Document any deviations and get acceptance that they are acceptable

**Structure**:
```
Feature: Order Management
As a: Sales Manager
I want to: View and manage customer orders
So that: I can fulfill orders accurately

Scenario 1: View order details
Given I am logged in as Sales Manager
When I navigate to Order #12345
Then I see customer information
And I see line items with products and quantities
And I see order total and shipping address
And I can print packing slip

Scenario 2: Update order status
Given I am viewing an order
When I change status to "Shipped" and enter tracking number
Then order status updates
And customer receives shipping notification email
```

**Tooling**: TestRail, Zephyr, Xray, Cucumber for BDD-style acceptance tests

### Exploratory Testing

**Purpose**: Unscripted testing to discover unknown bugs and edge cases.

**When to Apply**:
- Early in testing cycle to learn the system
- When requirements are vague or incomplete
- After automated tests complete to find deeper issues
- In bug-bash sessions before release

**Independent Baseline**:
- Regular exploratory testing charters
- Session notes documenting findings
- Issues logged in tracking system
- Success: Each session yields insights or defects

**From-Scratch Charters**:
- **Charter**: "Investigate authentication flow for security bypasses"
  - Try: Invalid tokens, expired sessions, concurrent logins, token reuse after logout
- **Charter**: "Test data validation on all input fields"
  - Try: SQL injection, XSS payloads, extremely long inputs, negative numbers where positive expected, special characters
- **Charter**: "Explore error handling and recovery"
  - Try: Kill process mid-transaction, disconnect network, invalid data in database, corrupt files
- **Charter**: "Race condition hunting"
  - Try: Rapidly click submit buttons, open multiple sessions, simultaneous updates to same record

**Success Metrics**:
- Bugs found per hour > threshold
- New insights documented
- Charter coverage of risk areas

**Tooling**: Session-based test management (SessionBaaS), note-taking apps, screen recording

---

## Risk-Based Testing Prioritization

Use this matrix to allocate testing effort based on risk:

| Risk Level | Test Intensity | Examples |
|------------|----------------|----------|
| **Critical** | Heavy testing: All methodologies, deep coverage | Authentication, payments, PII handling, cryptography |
| **High** | Strong testing: Most methodologies, good coverage | Admin functions, data exports, batch processing |
| **Medium** | Moderate testing: Key methodologies | Reporting, user profiles, settings |
| **Low** | Light testing: Smoke and sanity only | Static pages, help content, rarely used features |

Apply this prioritization when you cannot test everything. Always test critical areas exhaustively.
