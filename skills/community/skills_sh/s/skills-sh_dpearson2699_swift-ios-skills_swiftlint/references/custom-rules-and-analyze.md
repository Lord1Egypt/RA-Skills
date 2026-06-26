# Custom Rules and Analyze

Regex custom rules for project-specific enforcement, brief coverage of Swift custom rules, and the `swiftlint analyze` workflow.

## Contents

- [Regex Custom Rules](#regex-custom-rules)
- [Swift Custom Rules](#swift-custom-rules)
- [SwiftLint Analyze](#swiftlint-analyze)
- [When to Use Analyzer Rules](#when-to-use-analyzer-rules)

---

## Regex Custom Rules

Regex custom rules let you enforce project-specific patterns directly in `.swiftlint.yml` without building a custom SwiftLint binary.

```yaml
custom_rules:
  no_print_statements:
    name: "No print()"
    regex: '^\s*print\s*\('
    message: "Use os_log or Logger instead of print()"
    severity: warning
    match_kinds:
      - identifier

  no_hardcoded_colors:
    name: "No hardcoded colors"
    regex: 'UIColor\(\s*red:|\.init\(\s*red:'
    message: "Use Color asset catalog entries instead of hardcoded RGB values"
    severity: warning


  todo_requires_ticket:
    name: "TODO requires ticket"
    regex: '//\s*TODO(?!.*\b[A-Z]+-\d+)'
    message: "TODOs must reference a ticket (e.g., TODO: PROJ-123)"
    severity: warning
```

### Custom rule configuration keys

| Key | Required | Description |
| --- | -------- | ----------- |
| `name` | No | Human-readable name shown in violations |
| `regex` | Yes | The pattern to match |
| `capture_group` | No | Which regex capture group to highlight; defaults to `0` (the whole match) |
| `message` | No | Custom violation message |
| `severity` | No | `warning` (default) or `error` |
| `match_kinds` | No | Limit matches to specific syntax kinds (e.g., `comment`, `identifier`, `string`) |
| `excluded_match_kinds` | No | Exclude specific syntax kinds from matching; cannot be combined with `match_kinds` |
| `included` | No | Regex pattern for file paths to include (note: regex, not glob) |
| `excluded` | No | Regex pattern for file paths to exclude (note: regex, not glob) |
| `execution_mode` | No | Per-rule execution mode: `default`, `swiftsyntax`, or `sourcekit` |

### match_kinds values

Syntax token kinds that SwiftLint recognizes: `argument`, `attribute.builtin`, `attribute.id`, `buildconfig.id`, `buildconfig.keyword`, `comment`, `comment.mark`, `comment.url`, `doccomment`, `doccomment.field`, `identifier`, `keyword`, `number`, `objectliteral`, `parameter`, `placeholder`, `string`, `string_interpolation_anchor`, `typeidentifier`.

Use `match_kinds` to avoid false positives. For example, matching `print` only in `identifier` context avoids flagging it inside strings or comments.

**Regex flags:** Custom rule regexes run with `s` (dot matches newlines) and `m` (`^`/`$` match line boundaries) enabled by default. Prepend `(?-s)` if you don't want `.` to match newlines.

**`only_rules` interaction:** If using `only_rules` alongside `custom_rules`, you must include the literal string `custom_rules` in your `only_rules` list, or custom rules will not run.

**Execution mode:** Individual custom rules can set `execution_mode` to `default`, `swiftsyntax`, or `sourcekit`. You can also set a top-level `default_execution_mode` to apply the same mode across all custom regex rules unless a rule overrides it.

```yaml
default_execution_mode: swiftsyntax

custom_rules:
  no_print_statements:
    regex: '^\s*print\s*\('
    execution_mode: sourcekit
```

## Swift Custom Rules

SwiftLint supports rules written in Swift using the SwiftSyntax AST. These are more powerful than regex rules but require building SwiftLint from source with Bazel.

This is an advanced workflow primarily useful for organizations that need precise AST-based enforcement. For most projects, regex custom rules are sufficient.

If you need Swift custom rules:

1. Clone [realm/SwiftLint](https://github.com/realm/SwiftLint)
2. Scaffold a new rule with `swift run swiftlint-dev rules template <RuleName>` or add it under `Source/SwiftLintBuiltInRules/Rules/`
3. Register the rule so it becomes part of the executable (`make register` in the SwiftLint repo workflow)
4. Build the binary with Bazel: `bazel build :swiftlint`
5. Use the resulting custom `swiftlint` binary in your project

This is out of scope for typical project-level adoption.

## SwiftLint Analyze

`swiftlint analyze` runs analyzer rules that require the Swift compiler's type-checked AST. These rules can detect issues like unused imports and unused declarations that are impossible to catch with syntactic analysis alone.

### Workflow

1. Perform a **clean** build and capture the compiler log (incremental builds will fail):

```sh
# Xcode — clean build required
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp clean build \
    | tee xcodebuild.log

# SwiftPM — clean build required, -v needed for compiler command lines
swift package clean
swift build -v 2>&1 | tee swift-build.log
```

1. Run analyze with the compiler log:

```sh
swiftlint analyze --compiler-log-path xcodebuild.log
```

Or via the command plugin:

```sh
swift package plugin swiftlint -- analyze --compiler-log-path swift-build.log
```

1. Configure which analyzer rules to enable:

```yaml
# .swiftlint.yml
analyzer_rules:
  - unused_import
  - unused_declaration
```

### Autocorrect with analyze

Analyzer rules that support autocorrect can fix issues:

```sh
swiftlint analyze --fix --compiler-log-path xcodebuild.log
```

`unused_import` is the most commonly used correctable analyzer rule — it removes unnecessary import statements.

## When to Use Analyzer Rules

Analyzer rules are slower than regular rules because they require a full build first. Use them when:

- **Codebase hygiene matters**: `unused_import` catches import bloat that accumulates over refactoring.
- **Dead code detection**: `unused_declaration` finds private declarations that are never referenced.
- **CI only**: Run analyzer rules in CI rather than on every local build to avoid slowing down the development loop.

A practical pattern is to run analyzer rules in a separate CI job that runs less frequently (e.g., nightly or on main branch only):

```yaml
# GitHub Actions — nightly analyze
on:
  schedule:
    - cron: '0 6 * * *'

jobs:
  analyze:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: swift build -v 2>&1 | tee swift-build.log
      - name: Analyze
        run: |
          brew install swiftlint
          swiftlint analyze --strict --compiler-log-path swift-build.log
```
