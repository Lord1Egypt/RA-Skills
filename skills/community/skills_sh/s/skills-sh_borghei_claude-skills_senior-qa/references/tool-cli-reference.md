# Tool CLI Reference

Read this when running `test_suite_generator.py`, `coverage_analyzer.py`, or `e2e_test_scaffolder.py` — full flag tables, usage examples, output formats, and generated artifacts.

## 1. test_suite_generator.py

**Purpose:** Scans React/TypeScript source directories for components and generates Jest + React Testing Library test stubs with render tests, prop tests, interaction tests, state tests, and optional accessibility tests.

**Usage:**
```bash
python scripts/test_suite_generator.py <source> [options]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `source` | -- | positional | *(required)* | Source directory containing React components |
| `--output` | `-o` | string | `<source>/__tests__/` | Output directory for generated test files |
| `--include-a11y` | -- | flag | `false` | Include accessibility tests using `jest-axe` |
| `--scan-only` | -- | flag | `false` | Scan and report components without generating test files |
| `--template` | -- | string | `None` | Path to a custom template file for test generation |
| `--verbose` | `-v` | flag | `false` | Enable verbose output showing each detected component |
| `--json` | -- | flag | `false` | Output results as JSON after generation |

**Example:**
```bash
python scripts/test_suite_generator.py src/components/ \
  --output __tests__/ \
  --include-a11y \
  --verbose

# Scanning: src/components/
# Found 24 React components
#   Button.test.tsx (4 test cases)
#   Modal.test.tsx (3 test cases)
#   ...
# Summary: 24 test files, 87 test cases
```

**Output Formats:**
- **Default (text):** Human-readable summary printed to stdout listing each generated file and test case count.
- **JSON (`--json`):** Structured object with `status`, `components` (array of detected component metadata), `generated_files` (array of output paths), and `summary` (totals).

---

## 2. coverage_analyzer.py

**Purpose:** Parses Jest/Istanbul coverage reports (JSON or LCOV format), identifies coverage gaps by severity, flags critical business-logic paths, and generates actionable recommendations in text, HTML, or JSON format.

**Usage:**
```bash
python scripts/coverage_analyzer.py <coverage> [options]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `coverage` | -- | positional | *(required)* | Path to coverage file (`.json`, `.info`) or directory containing coverage data |
| `--threshold` | `-t` | int | `80` | Coverage threshold percentage for pass/fail determination |
| `--strict` | -- | flag | `false` | Exit with code 1 if overall coverage is below threshold |
| `--critical-paths` | -- | flag | `false` | Focus analysis on critical business paths (auth, payment, security) |
| `--format` | `-f` | choice | `text` | Output format: `text`, `html`, or `json` |
| `--output` | `-o` | string | `None` | Write report to file instead of stdout |
| `--verbose` | `-v` | flag | `false` | Enable verbose output with detailed parsing information |
| `--json` | -- | flag | `false` | Output summary results as JSON (independent of `--format`) |

**Example:**
```bash
python scripts/coverage_analyzer.py coverage/coverage-final.json \
  --threshold 80 \
  --strict \
  --format html \
  --output report.html

# Analyzing coverage from: coverage/coverage-final.json
# Found coverage data for 42 files
# Report written to: report.html
```

**Output Formats:**
- **Text (`--format text`):** Structured report with overall percentages, threshold pass/fail, critical gaps, files below threshold, and prioritized recommendations.
- **HTML (`--format html`):** Styled HTML report with color-coded coverage stats, gap severity table, and per-file breakdown. Suitable for CI artifact upload.
- **JSON (`--json`):** Summary object with `status` (pass/fail), `threshold`, `coverage` (statement/branch/function/line percentages), `files_analyzed`, `files_below_threshold`, `total_gaps`, and `critical_gaps`.

---

## 3. e2e_test_scaffolder.py

**Purpose:** Scans Next.js App Router or Pages Router directories, detects routes (including dynamic segments, route groups, and authenticated pages), and generates Playwright test files with navigation, form, auth, and interaction test stubs. Optionally generates Page Object Model classes and Playwright configuration.

**Usage:**
```bash
python scripts/e2e_test_scaffolder.py <source> [options]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `source` | -- | positional | *(required)* | Source directory (`src/app/` for App Router or `pages/` for Pages Router) |
| `--output` | `-o` | string | `e2e/` | Output directory for generated test and fixture files |
| `--include-pom` | -- | flag | `false` | Generate Page Object Model classes in `<output>/pages/` |
| `--routes` | -- | string | `None` | Comma-separated list of routes to generate (e.g., `"/login,/dashboard"`) |
| `--verbose` | `-v` | flag | `false` | Enable verbose output showing each detected route |
| `--json` | -- | flag | `false` | Output results as JSON |

**Example:**
```bash
python scripts/e2e_test_scaffolder.py src/app/ \
  --output e2e/ \
  --include-pom \
  --routes "/login,/dashboard,/checkout"

# Scanning: src/app/
# Found 3 routes
#   auth-login.spec.ts
#   pages/AuthLoginPage.ts
#   dashboard.spec.ts
#   pages/DashboardPage.ts
#   checkout.spec.ts
#   pages/CheckoutPage.ts
#   fixtures/auth.ts
#
# Summary: 3 routes, 8 files generated
```

**Output Formats:**
- **Default (text):** Human-readable list of generated files and a route/file count summary.
- **JSON (`--json`):** Structured object with `status`, `routes` (array of route metadata including path, type, params, form/auth detection), `generated_files` (array with type, route, and path), and `summary` (totals and configuration flags).

**Generated Artifacts:**
- `<route>.spec.ts` -- Playwright test file per route with contextual test cases.
- `pages/<RouteName>Page.ts` -- Page Object Model class (when `--include-pom` is set).
- `playwright.config.ts` -- Multi-browser configuration with dev server integration (generated once if not already present).
- `fixtures/auth.ts` -- Authentication fixture with UI and API login patterns (generated once if not already present).
