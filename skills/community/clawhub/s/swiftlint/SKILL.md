---
name: swiftlint
emoji: "\U0001F9F9"
requires: swiftlint
install: brew install swiftlint
description: Swift linting and style enforcement via CLI
---

# SwiftLint

Enforce Swift style and conventions with static analysis. Lint entire projects, autocorrect fixable violations, manage rules, and integrate with Xcode and CI — all from the CLI.

---

## Verify Installation

```bash
swiftlint version
```

If not installed:

```bash
brew install swiftlint
```

Or via Mint:

```bash
mint install realm/SwiftLint
```

Or as a Swift Package Manager plugin (add to `Package.swift`):

```swift
.package(url: "https://github.com/realm/SwiftLint.git", from: "0.57.0")
```

Then run:

```bash
swift package plugin swiftlint
```

---

## Basic Usage

### Lint Current Directory

```bash
swiftlint
```

This recursively lints all `.swift` files from the current directory.

### Lint a Specific Path

```bash
swiftlint lint --path Sources/
```

### Lint Specific Files

```bash
swiftlint lint --path Sources/App/ViewModel.swift
```

### Lint from Standard Input

```bash
cat MyFile.swift | swiftlint lint --use-stdin --quiet
```

> **Agent guidance:** When a user says "check my code style" or "lint my Swift code," run `swiftlint` from the project root. If they point to a specific file or folder, use `--path`.

---

## Autocorrect

SwiftLint can automatically fix certain violations.

### Fix All Autocorrectable Violations

```bash
swiftlint --fix
```

### Fix a Specific Path

```bash
swiftlint --fix --path Sources/
```

### Fix a Specific File

```bash
swiftlint --fix --path Sources/App/ViewModel.swift
```

### Preview What Would Be Fixed (Dry Run)

Lint first to see violations, then fix:

```bash
swiftlint lint --path Sources/ && swiftlint --fix --path Sources/
```

> **Agent guidance:** Always lint before autocorrecting so the user sees what will change. Some violations are not autocorrectable — report those separately after fixing.

---

## Output Formats

### Default (Human-Readable)

```bash
swiftlint
```

Output: `Sources/App.swift:12:1: warning: Line Length Violation: ...`

### JSON

```bash
swiftlint lint --reporter json
```

### CSV

```bash
swiftlint lint --reporter csv
```

### Checkstyle (XML)

```bash
swiftlint lint --reporter checkstyle
```

### GitHub Actions

```bash
swiftlint lint --reporter github-actions-logging
```

### Xcode Summary (plist)

```bash
swiftlint lint --reporter xcode-summary
```

### SonarQube

```bash
swiftlint lint --reporter sonarqube
```

### Markdown

```bash
swiftlint lint --reporter markdown
```

### Save to File

```bash
swiftlint lint --reporter json > swiftlint-results.json
```

### All Available Reporters

| Reporter | Format | Best For |
|---|---|---|
| `xcode` | Xcode-compatible (default) | Local development |
| `json` | JSON array | Programmatic processing |
| `csv` | CSV | Spreadsheet analysis |
| `checkstyle` | XML | Jenkins, CI tools |
| `codeclimate` | Code Climate JSON | Code Climate integration |
| `github-actions-logging` | GitHub annotations | GitHub Actions CI |
| `sonarqube` | SonarQube JSON | SonarQube integration |
| `markdown` | Markdown table | PR comments |
| `emoji` | Emoji-decorated | Fun terminal output |
| `html` | HTML report | Browser viewing |
| `junit` | JUnit XML | Test reporting tools |
| `xcode-summary` | Plist | Xcode build summaries |

> **Agent guidance:** Use `--reporter json` when you need to parse results programmatically. Use `--reporter github-actions-logging` on GitHub Actions to get inline annotations on PRs.

---

## Rules

### List All Rules

```bash
swiftlint rules
```

### Search for a Specific Rule

```bash
swiftlint rules | grep "force_cast"
```

### Show Rule Details

```bash
swiftlint rules force_cast
```

### Rule Identifiers Quick Reference

Rules fall into categories:

**Enabled by Default (Common)**

| Rule | What It Catches |
|---|---|
| `line_length` | Lines exceeding max length (default 120 warning, 200 error) |
| `trailing_whitespace` | Whitespace at end of lines |
| `trailing_newline` | Missing or extra trailing newlines |
| `opening_brace` | Opening brace placement |
| `closing_brace` | Closing brace placement |
| `colon` | Colon spacing (e.g., `let x : Int` → `let x: Int`) |
| `comma` | Comma spacing |
| `force_cast` | Use of `as!` |
| `force_try` | Use of `try!` |
| `force_unwrapping` | Use of `!` on optionals (opt-in) |
| `type_body_length` | Type bodies exceeding max lines |
| `function_body_length` | Function bodies exceeding max lines |
| `file_length` | Files exceeding max lines |
| `cyclomatic_complexity` | High cyclomatic complexity |
| `nesting` | Deep nesting levels |
| `identifier_name` | Naming convention violations |
| `type_name` | Type naming convention violations |
| `unused_import` | Unused import statements (opt-in) |
| `unused_declaration` | Unused declarations (opt-in) |
| `vertical_whitespace` | Excessive blank lines |
| `todo` | TODO/FIXME comments as warnings |
| `mark` | Improper MARK comment format |
| `void_return` | Explicit `-> Void` instead of `-> ()` |
| `syntactic_sugar` | Prefer `[Int]` over `Array<Int>` |
| `redundant_optional_initialization` | `var x: Int? = nil` (nil is default) |
| `redundant_string_enum_value` | Enum case name matches raw value |

**Opt-In (Must Be Explicitly Enabled)**

| Rule | What It Catches |
|---|---|
| `explicit_type_interface` | Missing explicit type annotations |
| `missing_docs` | Missing documentation comments |
| `multiline_arguments` | Multiline function call formatting |
| `multiline_parameters` | Multiline function param formatting |
| `vertical_parameter_alignment` | Parameter alignment in declarations |
| `sorted_imports` | Unsorted import statements |
| `file_header` | Missing or incorrect file headers |
| `accessibility_label_for_image` | Images without accessibility labels |
| `accessibility_trait_for_button` | Buttons without accessibility traits |
| `strict_fileprivate` | Prefer `private` over `fileprivate` |
| `prohibited_interface_builder` | Storyboard/XIB usage |
| `no_magic_numbers` | Magic numbers in code |
| `prefer_self_in_static_references` | `Self` over explicit type name in static context |
| `balanced_xctest_lifecycle` | setUp without tearDown |
| `test_case_accessibility` | Test methods not marked correctly |

> **Agent guidance:** When setting up SwiftLint for a new project, start with defaults and only add opt-in rules the user specifically requests. Don't overwhelm with every possible rule.

---

## Configuration (.swiftlint.yml)

SwiftLint reads `.swiftlint.yml` from the current directory (or parent directories).

### Generate a Default Config

There's no built-in generator, but here's a minimal config:

```yaml
# .swiftlint.yml

# Paths to include (default: all Swift files)
included:
  - Sources
  - Tests

# Paths to exclude
excluded:
  - Pods
  - DerivedData
  - .build
  - Packages

# Disable specific rules
disabled_rules:
  - todo
  - trailing_whitespace

# Enable opt-in rules
opt_in_rules:
  - sorted_imports
  - unused_import
  - missing_docs

# Configure specific rules
line_length:
  warning: 120
  error: 200
  ignores_comments: true
  ignores_urls: true

type_body_length:
  warning: 300
  error: 500

file_length:
  warning: 500
  error: 1000

function_body_length:
  warning: 50
  error: 100

identifier_name:
  min_length:
    warning: 2
    error: 1
  max_length:
    warning: 50
    error: 60
  excluded:
    - id
    - x
    - y
    - i
    - j
    - ok

type_name:
  min_length:
    warning: 3
    error: 0
  max_length:
    warning: 50
    error: 60

cyclomatic_complexity:
  warning: 10
  error: 20

nesting:
  type_level:
    warning: 2
  function_level:
    warning: 3
```

### Using a Config from a Custom Path

```bash
swiftlint lint --config path/to/.swiftlint.yml
```

### Multiple Configs (Child Config)

```yaml
# Feature/.swiftlint.yml — inherits parent config and overrides
child_config: ../.swiftlint.yml

disabled_rules:
  - force_cast
```

### Parent Config (Extend from Another)

```yaml
# .swiftlint.yml
parent_config: shared/.swiftlint-base.yml
```

### Remote Config

```yaml
parent_config: https://raw.githubusercontent.com/org/repo/main/.swiftlint.yml
```

> **Agent guidance:** When a project already has `.swiftlint.yml`, always read it before suggesting changes. Modify the existing config rather than creating a new one.

---

## Inline Rule Management

### Disable a Rule for a Line

```swift
let value = dict["key"] as! String // swiftlint:disable:this force_cast
```

### Disable a Rule for a Block

```swift
// swiftlint:disable force_cast
let a = x as! String
let b = y as! Int
// swiftlint:enable force_cast
```

### Disable All Rules for a Block

```swift
// swiftlint:disable all
// Legacy code that can't be refactored yet
// swiftlint:disable:enable all
```

### Disable for Next Line Only

```swift
// swiftlint:disable:next force_cast
let value = dict["key"] as! String
```

### Disable for Previous Line

```swift
let value = dict["key"] as! String
// swiftlint:disable:previous force_cast
```

> **Agent guidance:** Prefer targeted disables (`disable:this`, `disable:next`) over broad block disables. Never suggest `disable all` unless the user is dealing with generated code or legacy code they explicitly don't want to lint.

---

## Xcode Integration

### Build Phase Script

Add a Run Script Phase in Xcode (Build Phases):

```bash
if command -v swiftlint >/dev/null 2>&1; then
  swiftlint
else
  echo "warning: SwiftLint not installed, download from https://github.com/realm/SwiftLint"
fi
```

### Build Phase with Autocorrect

```bash
if command -v swiftlint >/dev/null 2>&1; then
  swiftlint --fix && swiftlint
fi
```

### Swift Package Plugin (Xcode 15+)

If SwiftLint is added as a package dependency:

```bash
swift package plugin swiftlint
```

Or in Xcode: right-click the project → "SwiftLintBuildToolPlugin".

> **Agent guidance:** For modern projects (Xcode 15+), prefer the SPM plugin over a build phase script — it pins the SwiftLint version to the project and doesn't require a local install.

---

## CI Integration

### GitHub Actions

```yaml
- name: SwiftLint
  run: |
    brew install swiftlint
    swiftlint lint --reporter github-actions-logging --strict
```

With only changed files:

```yaml
- name: SwiftLint Changed Files
  run: |
    git diff --name-only --diff-filter=d origin/main...HEAD -- '*.swift' | \
    xargs -I{} swiftlint lint --path {} --reporter github-actions-logging --strict
```

### Bitrise

```yaml
- script:
    inputs:
    - content: |
        brew install swiftlint
        swiftlint lint --strict
```

### Jenkins (Checkstyle)

```bash
swiftlint lint --reporter checkstyle > swiftlint-checkstyle.xml
```

Then use the Checkstyle plugin to parse `swiftlint-checkstyle.xml`.

---

## Analyzing Results

### Count Violations by Rule

```bash
swiftlint lint --reporter json | python3 -c "
import json, sys, collections
data = json.load(sys.stdin)
counts = collections.Counter(v['rule_id'] for v in data)
for rule, count in counts.most_common():
    print(f'{count:>5}  {rule}')
"
```

### Show Only Errors (Not Warnings)

```bash
swiftlint lint --strict 2>&1 | grep "error:"
```

### Strict Mode (Warnings Become Errors)

```bash
swiftlint lint --strict
```

This makes SwiftLint return a non-zero exit code for any violation (not just errors).

### Quiet Mode (Errors Only in Output)

```bash
swiftlint lint --quiet
```

Suppresses warnings from output, only shows errors.

### Enable/Disable Specific Rules via CLI

```bash
swiftlint lint --enable-rules sorted_imports,unused_import
swiftlint lint --disable-rules todo,trailing_whitespace
```

---

## Custom Rules

Define custom regex-based rules in `.swiftlint.yml`:

```yaml
custom_rules:
  no_print_statements:
    name: "No Print Statements"
    regex: "\\bprint\\s*\\("
    message: "Use os_log or Logger instead of print()"
    severity: warning
    match_kinds:
      - identifier

  no_hardcoded_strings:
    name: "No Hardcoded Strings in Views"
    regex: "Text\\(\"[^\"]+\"\\)"
    message: "Use LocalizedStringKey or String(localized:) for user-facing text"
    severity: warning
    included: ".*View\\.swift"

  no_force_unwrap_iboutlet:
    name: "No Force Unwrap IBOutlet"
    regex: "@IBOutlet\\s+(weak\\s+)?var\\s+\\w+:\\s+\\w+!"
    message: "Use optional IBOutlets to avoid crashes"
    severity: error

  accessibility_identifier_required:
    name: "Accessibility Identifier"
    regex: "\\.accessibilityIdentifier\\("
    message: "Good — accessibilityIdentifier found"
    severity: warning
    match_kinds:
      - identifier

  prefer_logger_over_print:
    name: "Prefer Logger"
    regex: "\\bNSLog\\s*\\("
    message: "Use Logger (os.Logger) instead of NSLog"
    severity: warning
```

### Match Kinds

| Kind | What It Matches |
|---|---|
| `identifier` | Variable/function names |
| `string` | String literals |
| `comment` | Comments |
| `keyword` | Swift keywords |
| `typeidentifier` | Type names |
| `number` | Numeric literals |
| `parameter` | Function parameters |
| `argument` | Function arguments |

> **Agent guidance:** Custom rules are powerful but regex-based — they can produce false positives. Always test custom rules on the codebase before suggesting them as permanent additions.

---

## Common Flags Reference

| Flag | Purpose |
|---|---|
| `--path <path>` | Lint specific file or directory |
| `--config <path>` | Use custom config file |
| `--reporter <name>` | Output format (json, csv, etc.) |
| `--strict` | Treat warnings as errors |
| `--quiet` | Only show errors in output |
| `--fix` | Autocorrect fixable violations |
| `--enable-rules <rules>` | Enable specific rules (comma-separated) |
| `--disable-rules <rules>` | Disable specific rules (comma-separated) |
| `--use-stdin` | Read Swift from stdin |
| `--force-exclude` | Exclude files even if explicitly passed |
| `--cache-path <path>` | Custom cache directory |
| `--no-cache` | Disable caching |
| `--use-alternative-excluding` | Use alternative file-excluding method |
| `--in-process-sourcekit` | Use in-process SourceKit |
| `--compiler-log-path` | Path to xcodebuild log for analyzer rules |
| `--progress` | Show progress bar |

---

## Common Workflows

### Set Up SwiftLint for a New Project

```bash
# 1. Install
brew install swiftlint

# 2. Run initial lint to see baseline
swiftlint lint --path Sources/ --reporter json > baseline.json

# 3. Create config based on results
cat > .swiftlint.yml << 'EOF'
included:
  - Sources
  - Tests
excluded:
  - Pods
  - DerivedData
  - .build
disabled_rules:
  - todo
opt_in_rules:
  - sorted_imports
  - unused_import
line_length:
  warning: 120
  error: 200
  ignores_urls: true
EOF

# 4. Fix autocorrectable issues
swiftlint --fix --path Sources/

# 5. Re-lint to see remaining issues
swiftlint
```

### Fix All Issues Before a PR

```bash
# Autocorrect what we can
swiftlint --fix

# Check what remains
swiftlint lint --strict
```

### Lint Only Changed Files (vs. main)

```bash
git diff --name-only --diff-filter=d origin/main...HEAD -- '*.swift' | \
  xargs -I{} swiftlint lint --path {} --strict
```

### Compare Violation Counts Between Branches

```bash
# Current branch count
CURRENT=$(swiftlint lint --quiet 2>&1 | wc -l | tr -d ' ')

# Main branch count
git stash
git checkout main
MAIN=$(swiftlint lint --quiet 2>&1 | wc -l | tr -d ' ')
git checkout -
git stash pop

echo "main: $MAIN violations, current: $CURRENT violations"
```

---

## Troubleshooting

### Common Errors

| Error | Solution |
|---|---|
| `No lintable files found` | Check `included` paths in config or run from project root |
| `Invalid configuration` | Validate YAML syntax in `.swiftlint.yml` |
| `SourceKit not found` | Run `sudo xcode-select -s /Applications/Xcode.app` |
| `Rule not found` | Check rule name with `swiftlint rules`, may be opt-in |
| `Slow linting` | Add `excluded` paths for Pods/DerivedData, use `--cache-path` |

### Performance Tips

- Always exclude `Pods/`, `DerivedData/`, `.build/`, and `Packages/` in config
- Use `--cache-path` to persist cache across CI runs
- Lint only changed files on CI instead of the entire project
- Use `--no-cache` only when debugging unexpected results

---

## Notes

### Agent Tips

> When a user asks to "clean up" or "fix style" in Swift code, run `swiftlint --fix` first, then `swiftlint lint` to report remaining issues.

> Before adding SwiftLint to an existing project, run `swiftlint lint --reporter json` to assess the violation count. If there are hundreds of violations, suggest a phased approach: fix autocorrectable ones first, then tackle the rest by category.

> Always check for an existing `.swiftlint.yml` before creating one. Read it to understand the team's style preferences.

> For projects targeting accessibility (which should be all of them), suggest enabling `accessibility_label_for_image` and `accessibility_trait_for_button` opt-in rules.

> When the user's project uses SwiftUI, suggest a custom rule to catch hardcoded strings in `Text()` views — all user-facing strings should use `String(localized:)` for localization support.

> The `--strict` flag is essential for CI — without it, SwiftLint exits 0 even with warnings, which means your CI pipeline won't catch style regressions.
