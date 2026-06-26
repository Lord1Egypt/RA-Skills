# Tooling Recommendations Matrix

Based on the detected tech stack, here are the recommended tools for each testing methodology. All tools are industry-standard, open-source where possible, and integrate well with CI/CD pipelines.

## By Language

### Python

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | pytest | Primary test runner | Rich fixtures, parametrization, plugins |
| | unittest | Built-in alternative | Good for simple cases |
| | Hypothesis | Property-based testing | Generate edge case inputs automatically |
| **Coverage** | coverage.py + pytest-cov | Measure code coverage | Aim >80% overall |
| **Integration** | pytest + fixtures | Test with real databases | Use TestContainers for PostgreSQL/MySQL |
| | requests + responses | HTTP API testing | Mock external APIs |
| **Mocking** | unittest.mock | Built-in mocking | For simple mocks |
| | pytest-mock | Pytest fixture wrapper | More ergonomic |
| | responses | HTTP mocking library | For requests library |
| **E2E** | Playwright | Browser automation | Fast, reliable, auto-wait |
| | Selenium | Alternative | More legacy support |
| **Performance** | locust | Load testing | Python-based, easy to extend |
| | k6 | Load testing (JS-based) | Better metrics, cloud option |
| **Security** | bandit | SAST | Finds common security issues |
| | safety | SCA | Check dependencies for CVEs |
| |OWASP ZAP | DAST | Dynamic scanning |
| **API** | schemathesis | API testing from OpenAPI spec | Property-based API testing |
| | requests | Direct API calls | Flexible, low-level |
| **Mutation Testing** | mutmut | Mutation testing | Identify weak tests |
| **CI/CD** | GitHub Actions | CI platform | Native to GitHub |
| | GitLab CI | CI platform | Integrated |
| **Code Quality** | black | Auto-formatting | Opinionated, consistent |
| | flake8 | Linting | PEP8 compliance |
| | mypy | Type checking | Gradual typing |
| | pre-commit | Git hooks | Run quality checks automatically |

### JavaScript/TypeScript

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | Jest | Primary test runner | Batteries-included, mocking, coverage |
| | Vitest | Vite-based, faster | Modern alternative |
| | Mocha + Chai | Flexible, minimal | More setup required |
| **Coverage** | jest --coverage | Built-in coverage | Istanbul under the hood |
| **React Testing** | React Testing Library | Unit/integration for React | Encourages accessible testing |
| | Cypress component testing | Component E2E | Real browser |
| **E2E** | Playwright | Browser automation | Multi-browser, auto-wait |
| | Cypress | Alternative | Better debugging, time-travel |
| **API** | Supertest | HTTP assertion library | Works with Express |
| | frisby | REST API testing | BDD-style |
| **Performance** | k6 | Load testing (JS) | Write scripts in JS |
| | Artillery | Load testing | YAML or JS config |
| **Security** | ESLint security plugin | SAST | Rules for OWASP issues |
| | npm audit / yarn audit | SCA | Built-in dependency audit |
| | Snyk | SCA + DAST | More comprehensive |
| **Mutation Testing** | Stryker | Mutation testing | For JS/TS |
| **CI/CD** | GitHub Actions | CI platform | Native |
| | CircleCI | CI platform | Fast caching |
| **Code Quality** | Prettier | Auto-formatting | Opinionated |
| | ESLint | Linting | Extensible rules |
| | TypeScript compiler | Type checking | Strict mode |

### Java

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | JUnit 5 | Standard test framework | Modern Jupiter API |
| | TestNG | Alternative | More configuration features |
| **Mocking** | Mockito | Mocking framework | Most popular |
| | EasyMock | Alternative | Record-replay style |
| | WireMock | HTTP mocking | Test external APIs |
| **Integration** | Spring Boot Test | Integration testing | For Spring apps |
| | TestContainers | Real services in Docker | Database, message queues |
| **Coverage** | JaCoCo | Code coverage | Generates reports |
| **E2E** | Selenium WebDriver | Browser automation | Legacy, wide support |
| | Serenity BDD | Acceptance tests | Rich reporting |
| **API** | RestAssured | API testing DSL | Fluent assertions |
| | WireMock | API mocking | Stub external services |
| **Performance** | JMeter | Load testing | Mature, GUI available |
| | Gatling | Load testing (Scala) | Code-based scenarios |
| **Security** | OWASP Dependency Check | SCA | Scan for CVEs |
| | SonarQube | SAST + quality gate | Comprehensive |
| | SpotBugs + FindSecBugs | SAST | Find security bugs |
| **Build** | Maven / Gradle | Build tools | Choose one |
| **CI/CD** | Jenkins | CI server | Highly customizable |
| | GitHub Actions | CI platform | Simple YAML |
| **Code Quality** | Checkstyle | Coding standards | Google/Oracle styles |
| | PMD | Static analysis | Code smells |
| | SpotBugs (FindBugs) | Bug detection | Compiles .class files |

### Go

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | go test (builtin) | Standard test runner | Table-driven tests idiomatic |
| **Coverage** | go test --cover | Built-in coverage | Html report available |
| **Integration** | TestContainers Go | Real services | Database, Kafka, etc. |
| **Mocking** | testify/mock | Mocking framework | Alternative to manual mocks |
| **E2E** | Playwright (via bindings) | Browser automation | Not Go-native but works |
| **API** | httptest | HTTP testing utilities | Part of stdlib |
| | gin + test helpers | For Gin framework | Context testing |
| **Performance** | k6 (via JS) | Load testing | Go isn't primary, but k6 is JS |
| | vegeta | HTTP load testing | Go-based, command line |
| **Security** | staticcheck | Static analysis | Comprehensive |
| | gosec | Security scanner | OWASP patterns |
| **Build Quality** | golangci-lint | Aggregated linter | Fast, runs many linters |
| **CI/CD** | GitHub Actions | CI platform | Go built-in setup |
| | Drone | CI/CD in Go | Container-native |

### Rust

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | cargo test (builtin) | Standard test runner | Unit and integration tests |
| **Property Testing** | proptest | Property-based testing | QuickCheck style |
| **Fuzzing** | cargo fuzz (libfuzzer) | Fuzz testing | Find panics, crashes |
| **Coverage** | cargo tarpaulin | Code coverage | llvm-based |
| **Mocking** | mockall | Mocking framework | Derive macros |
| **E2E** | Playwright via Node | Browser automation | Rust isn't primary for E2E |
| **API** | reqwest | HTTP client | For API testing |
| **Security** | cargo-audit | SCA | Audit dependencies for CVEs |
| | clippy | Linting | Find common mistakes |
| **Build Quality** | rustfmt | Auto-formatting | Opinionated |
| | clippy | Advanced linting | Beyond compiler warnings |
| **CI/CD** | GitHub Actions | CI platform | rustup integration |

### C#/.NET

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | xUnit.net | Modern test framework | Recommended for new projects |
| | NUnit | Alternative | Similar to JUnit |
| | MSTest | Built-in | Basic features |
| **Mocking** | Moq | Mocking library | LINQ-based setup |
| | NSubstitute | Alternative | Simpler syntax |
| **Integration** | TestContainers .NET | Real services | Database, message brokers |
| **Coverage** | coverlet | Code coverage | Cross-platform |
| | dotCover (JetBrains) | Coverage + reporting | Commercial |
| **E2E** | Playwright for .NET | Browser automation | Microsoft's library |
| | Selenium WebDriver | Alternative | Legacy support |
| **API** | FluentAssertions | Fluent assertions | Better error messages |
| | RestSharp | HTTP client | API testing |
| **Performance** | NBomber | Load testing | .NET-native |
| | k6 | Load testing | Write JS scripts |
| **Security** | OWASP ZAP | DAST | Dynamic scanning |
| | Security Code Scan | SAST | Roslyn analyzer |
| | SonarAnalyzer.CSharp | SAST | SonarQube integration |
| **Build Quality** | dotnet format | Formatting | Built-in |
| | Roslyn analyzers | Custom rules | Write your own |
| **CI/CD** | GitHub Actions | CI platform | dotnet/setup-dotnet |
| | Azure DevOps | Azure integration | Complete CI/CD |
| **Code Quality** | SonarQube | Quality gate | Comprehensive |

### Ruby

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | RSpec | BDD-style testing | Most popular |
| | Minitest | Standard library | Simpler, faster |
| **Coverage** | SimpleCov | Code coverage | Easy setup |
| **Integration** | FactoryBot | Test data factories | Fixtures replacement |
| | DatabaseCleaner | Transaction management | Clean state |
| **Mocking** | RSpec Mocks | Built-in mocking | Part of RSpec |
| **E2E** | Capybara | Acceptance testing | Works with RSpec |
| | Selenium WebDriver | Driver for Capybara | Real browser |
| **API** | RSpec API mode | API testing | Request specs |
| **Performance** | k6 | Load testing | Not Ruby-native |
| **Security** | Brakeman | SAST for Rails | Finds security vulnerabilities |
| | bundler-audit | SCA | Check for CVEs |
| **CI/CD** | GitHub Actions | CI platform | Ruby setup |
| | CircleCI | CI platform | Good Ruby support |
| **Code Quality** | RuboCop | Linting and formatting | Enforce Ruby style guide |

### PHP

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | PHPUnit | Standard test framework | xUnit-style |
| **Coverage** | php-code-coverage | Code coverage (Xdebug/PCOV) | Integrated with PHPUnit |
| **Mocking** | Prophecy (PHPUnit) | Built-in mocking | Alternative to Mockery |
| | Mockery | Mocking library | More features |
| **Integration** | Laravel Dusk | Browser automation (Laravel) | ChromeDriver |
| **E2E** | Codeception | Acceptance testing | BDD-style, integrates many tools |
| | Behat | BDD framework | Gherkin syntax |
| **API** | PHPUnit with Guzzle | HTTP testing | Use Guzzle HTTP client |
| **Performance** | Apache JMeter | Load testing | Not PHP-specific |
| **Security** | PHPStan | Static analysis | Find bugs before runtime |
| | Psalm | Static analysis | Type inference |
| | RIPS | SAST for security | Commercial, OWASP focus |
| **CI/CD** | GitHub Actions | CI platform | PHP setup |
| | GitLab CI | CI platform | Shared runners with PHP |
| **Code Quality** | PHP_CodeSniffer | Coding standards | PSR-2/PSR-12 |
| | PHPMD | Mess detector | Code smells |

### Kotlin

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | Kotest | Flexible testing framework | Multiple styles |
| | JUnit 5 (via kotlin-test) | Standard | Interoperable with Java |
| **Mocking** | MockK | Kotlin-specific mocking | Coroutines support |
| | Mockito (Kotlin) | Java mocking | Limited due to final classes |
| **Integration** | TestContainers | Real services | Java-compatible |
| **Coverage** | JaCoCo | Code coverage | Works with Kotlin |
| **E2E** | Selenium/WebDriver | Browser automation | Java-based works |
| | Ktor client testing | API testing | For Ktor framework |
| **Security** | SpotBugs + FindSecBugs | SAST | Java bytecode analysis |
| | KtLint | Linting | Kotlin style |
| **Build** | Gradle | Build tool | Kotlin DSL recommended |
| **CI/CD** | GitHub Actions | CI platform | Setup JDK and Gradle |

### Swift

| Category | Tool | Usage | Notes |
|----------|------|-------|-------|
| **Unit Testing** | XCTest (builtin) | Standard framework | Xcode integration |
| **Mocking** | Cuckoo | Mocking framework | Swift-native |
| | SwiftyMocky | Generate mocks | Protocol-oriented |
| **UI Testing** | XCUITest | UI automation | Xcode's framework |
| **Code Coverage** | Xcode coverage | Built-in | Show coverage in IDE |
| **Security** | SwiftLint | Linting | Security rules available |
| **CI/CD** | GitHub Actions | CI platform | macOS runners for iOS |
| | Bitrise | Mobile CI | iOS/Android focus |
| **Code Quality** | SwiftFormat | Formatting | Opinionated |
| | SwiftLint | Linting | Customizable rules |

---

## Cross-Cutting Tools (Applicable to All Stacks)

| Category | Tool | Purpose | Integration |
|----------|------|---------|-------------|
| **Static Analysis (SAST)** | **SonarQube** | Code quality + security | CI integration, quality gates |
| | **Semgrep** | Fast, rule-based | Custom rules, CLI |
| | **CodeQL** (GitHub) | Advanced semantic analysis | Query code as database |
| **Dependency Scanning (SCA)** | **Snyk** | Vulnerability scanning | CI, PR checks |
| | **Dependabot** (GitHub) | Auto-PR for updates | Native to GitHub |
| | **OWASP Dependency-Check** | Open-source SCA | CLI, Jenkins |
| **Dynamic Scanning (DAST)** | **OWASP ZAP** | Automated security scanning | CI pipeline, baseline |
| | **Burp Suite** | Professional penetration testing | Manual + automated |
| **Container Scanning** | **Trivy** | Vulnerability scanning | Images, filesystems |
| | **Clair** | Container image analysis | Kubernetes ecosystem |
| **Secret Detection** | **GitSecrets** | Prevent secrets in git | Pre-commit hook |
| | **TruffleHog** | Secret scanning | Scan history, high entropy |
| | **Gitleaks** | Fast secret scanner | CI integration |
| **Infrastructure as Code Scanning** | **Checkov** | Terraform/CloudFormation | Misconfiguration detection |
| | **tfsec** | Terraform security | CLI, CI |
| **Compliance & Policy** | **Open Policy Agent (OPA)** | Policy as code | Gate deployments |
| **API Testing** | **Postman/Newman** | API development + testing | Collections, documentation |
| | **Dredd** | API description testing | OpenAPI/Swagger |
| **Contract Testing** | **Pact** | Consumer-driven contracts | Microservices |
| **Mutation Testing** | **Stryker** (JS), **mutmut** (Python), **PITest** (Java) | Test quality assessment | Periodic runs |
| **Performance** | **k6** | Load testing (scriptable) | Cloud and local |
| | **Gatling** | Load testing (Scala) | High performance |
| | **Artillery** | Load testing (YAML/JS) | Simple config |
| **Browser Automation** | **Playwright** | Cross-browser E2E | Fast, reliable |
| | **Cypress** | E2E for web apps | Time-travel, debugging |
| | **Selenium** | Legacy support | Wide browser support |
| **Accessibility** | **axe-core** | Automated a11y testing | Library, CI integration |
| | **Pa11y** | Automated a11y tests | CLI, CI |
| **Code Coverage** | **Codecov** | Coverage reporting | PR comments, badges |
| | **Coveralls** | Alternative | Similar features |

---

## Building the Testing Stack

### Minimum Viable Stack

These tools are essential for any production codebase:

1. **Unit Testing Framework**: Language-specific (pytest, Jest, JUnit, etc.)
2. **Code Coverage**: >80% target
3. **Linter/Formatter**: Consistent code style
4. **CI/CD**: Run tests automatically on every commit
5. **Dependency Scanning**: SCA for vulnerable dependencies
6. **SAST**: Basic static analysis
7. **Secrets Detection**: Prevent credentials in git

### Recommended Full Stack

Add these for comprehensive quality and security:

8. **E2E Testing**: Playwright or Cypress for critical user journeys
9. **API Testing**: Automated tests for all endpoints
10. **Performance Testing**: k6 or Locust for load testing
11. **DAST**: OWASP ZAP against staging
12. **Container Scanning**: Trivy for Docker images
13. **Mutation Testing**: Stryker/mutmut periodically
14. **Accessibility Testing**: axe DevTools automated + manual

### Enterprise/Compliance Stack

For regulated industries (finance, healthcare, government):

15. **Formal Code Review**: Mandatory PR approval (2+ reviewers)
16. **Security Review**: Dedicated security team approval for sensitive changes
17. **Penetration Testing**: Annual or release-based manual testing
18. **Threat Modeling**: STRIDE or PASTA methodology
19. **Audit Trail**: Immutable logs, signed commits
20. **Quality Gates**: No merges without passing all checks
21. **SBOM**: Software Bill of Materials generation (Syft, CycloneDX)
22. **Fuzz Testing**: AFL, libFuzzer, or OSS-Fuzz integration
23. **Compliance Scanners**: HIPAA, PCI-DSS, SOC2 specific checks

---

## Tool Selection Decision Tree

```
Do you have a web UI?
├─ Yes → Playwright or Cypress for E2E
└─ No → Skip E2E, focus on API/CLI

Is mobile testing needed?
├─ Yes → BrowserStack or real device lab
└─ No → Desktop browsers only

Compliance requirements?
├─ SOC2/ISO27001 → SonarQube, formal code review, audit logs
├─ HIPAA/PII → Encryption scanning, secrets detection, DAST
└─ None → Standard stack sufficient

Budget constraints?
├─ Open-source only → pytest/Jest, OWASP ZAP, k6, SonarQube CE
└─ Commercial allowed → Snyk, Burp Suite, SonarQube DE, GitLab Ultimate
```

---

## Common Pitfalls to Avoid

| Pitfall | Consequence | Solution |
|---------|-------------|----------|
| **Flaky tests** | CI unreliable, ignored failures | Make tests deterministic, use retries sparingly, fix flaky tests immediately |
| **Slow test suite** | Developers avoid running tests | Parallelize, cache dependencies, isolate slow tests (E2E), use test impact analysis |
| **Over-mocking** | Tests too coupled to implementation | Mock only external boundaries (DB, API), avoid mocking internal functions |
| **Missing integration tests** | Integration failures in production | Test real database, real service interactions (TestContainers) |
| **No security scanning** | Vulnerabilities reach production | Integrate SCA/SAST/DAST into CI, fail builds on high severity |
| **Ignoring coverage** | Untested code accumulates | Coverage reporting, coverage delta checks, ignore warnings |
| **Manual test cases not automated** | Regression bugs | Automate frequently-run manual tests |
| **Testing in production** | Production incidents | Production-like staging environment mandatory |
| **No performance testing** | Slow app under load | Load test before launch, set performance budgets |
| **Missing accessibility** | Legal/compliance risk | Automated scanning + manual screen reader testing |

---

## Performance Comparison (E2E Tools)

| Tool | Speed | Reliability | Debugging | Parallel |
|------|-------|-------------|-----------|----------|
| Playwright | Fast | Very high | Excellent | Yes |
| Cypress | Fast | High | Excellent (time-travel) | Limited (experimental) |
| Selenium | Slower | Medium | Moderate (logs) | Yes |
| TestCafe | Fast | High | Good | Yes |

Choose **Playwright** for new projects: fastest, most reliable, multi-browser.

---

## Cost Considerations

| Tool | Open Source | Commercial Tier | Typical Cost |
|------|-------------|-----------------|--------------|
| Snyk | Limited | Full | $0-$2500/mo depending on seats/orgs |
| SonarQube | Community | Developer/Enterprise | Free - $20k/year |
| OWASP ZAP | Free | N/A | Free |
| Burp Suite | No | Professional/Enterprise | $399-$3999/year |
| k6 | Open-source | Cloud | Free - custom |
| Codecov | No | tiers | Free-$29/user/mo |
| BrowserStack | No | Live + Automate | $100-$500/mo |
| GitLab Ultimate | No | All-in-one | $99/user/mo |

---

## Quick Recommendations by Use Case

| Scenario | Recommended Tools |
|----------|-------------------|
| **Small startup, limited budget** | pytest/Jest, GitHub Actions (free), OWASP ZAP, k6 (OSS), Codecov (free), Coveralls |
| **Enterprise Java** | JUnit5 + Mockito + TestContainers, SonarQube Enterprise, Snyk, Fortify, JMeter, internal Jenkins |
| **Serverless Node.js** | Jest, c8 for coverage, ESLint security, serverless framework testing plugins, Percy for visual regression |
| **Mobile iOS/Android** | XCTest/Espresso, Fastlane for CI, Firebase Test Lab, Bitrise |
| **Government/Compliance** | Full quality gate: SonarQube, Coverity (or similar), formal code review (2+), manual pen testing, immutable audit trail |

Always choose tools that integrate with your existing CI/CD and developer workflow. Adoption is key — the best tool is the one your team actually uses.
