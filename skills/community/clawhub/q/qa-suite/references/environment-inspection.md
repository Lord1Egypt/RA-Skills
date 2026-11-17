# Test Environment Inspection

Before recommending any test setup, inspect what already exists. This prevents:
- Recommending a framework already installed
- Ignoring existing test configuration
- Over-engineering when a working setup is in place
- Missing gaps in an existing (but broken) setup

## Inspection Checklist

Run these checks and classify each as present, partial, or absent.

### 1. Test Framework Detection

Check dependency files for test frameworks:

| Language | Check file | Look for |
|----------|-----------|----------|
| Python | requirements.txt, pyproject.toml, setup.cfg | pytest, unittest, nose, tox |
| Go | go.mod | testify, ginkgo, gomega |
| Node | package.json (devDependencies) | jest, vitest, mocha, jasmine |
| Rust | Cargo.toml (dev-dependencies) | test-related crates |
| Ruby | Gemfile | rspec, minitest |
| C/C++ | CMakeLists.txt, Makefile | ctest, gtest, catch2, unity |

### 2. Test Configuration Files

Search for:
- `jest.config.*`, `vitest.config.*`, `.mocharc.*`
- `pytest.ini`, `pyproject.toml` (tool.pytest), `tox.ini`, `setup.cfg` (tool:pytest)
- `.rspec`, `spec/spec_helper.rb`
- `CMakeLists.txt` with `enable_testing()`, `CTestTestfile.cmake`
- `tsconfig.json` with test-specific settings

### 3. Test Directory Structure

Glob for:
- `tests/`, `test/`, `spec/`, `__tests__/`
- `*_test.go`, `*_test.py`, `*.test.ts`, `*.spec.ts`
- Test files near source: `src/foo_test.py`, `src/__tests__/`

Count test files and estimate coverage from file count vs source file count.

### 4. Test Commands

Check:
- `package.json` scripts: `test`, `test:unit`, `test:integration`, `test:e2e`, `coverage`
- `Makefile` targets: `test`, `test-unit`, `test-integration`, `coverage`
- `tox.ini`, `noxfile.py`
- Project README or CONTRIBUTING.md for test instructions

### 5. Docker & Containerized Environment Inspection

Search for:
- `docker-compose.test.yml`, `docker-compose.yml`, `Dockerfile.test`
- `testcontainers` in dependency manifests (`package.json`, `go.mod`, `requirements.txt`, `Cargo.toml`)
- Container initialization scripts (`scripts/test-env-up.sh`, `make test-env`)

### 6. CI Configuration

Check:
- `.github/workflows/*.yml` for test jobs
- `.gitlab-ci.yml` for test stages
- `Jenkinsfile` for test stages
- `Dockerfile` for test stages

Extract: what commands run, what environments, what services (DB, Redis) are provisioned.

### 6. Test Data and Fixtures

Search for:
- Factory files: `factories.py`, `factories.js`, `factory/`
- Fixture files: `fixtures/`, `*.fixture.*`
- Seed data: `seed.sql`, `seed.py`, `seeds/`
- Mock files: `mocks/`, `__mocks__/`, `handlers.ts`

### 7. Test Documentation

Check for:
- `TESTING.md`, `CONTRIBUTING.md` (test section)
- Comments in README about how to run tests
- Inline documentation about test strategy

## Maturity Classification

From inspection results, classify:

| Level | Signals |
|-------|---------|
| **None** | No test framework, no test files, no CI test steps |
| **Minimal** | Framework installed, < 10 test files, no CI, no test data |
| **Partial** | Framework + CI, reasonable test count, missing some test types |
| **Mature** | All test types covered, CI integration, test data management, documentation |

## Output

```
### Test Environment Inspection

| Area | Status | Details |
|------|--------|---------|
| Test framework | present / absent | {framework} at version {x} |
| Test config | present / partial / absent | {config file path} |
| Test files | {N} found | in {directories} |
| Test commands | present / absent | {commands from npm/make/tox} |
| CI tests | present / absent | in {workflow file} |
| Test data | present / absent | {factories/fixtures/seeds} |
| Documentation | present / absent | {TESTING.md / README section} |

**Maturity**: {none|minimal|partial|mature}
```
