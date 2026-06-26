# Rules, Suppressions, and Baselines

Guidance on SwiftLint rule categories, inline suppression syntax, baseline workflows, and false-positive handling.

## Contents

- [Rule Categories](#rule-categories)
- [Browsing Rules](#browsing-rules)
- [Suppression Syntax](#suppression-syntax)
- [Suppression Policy](#suppression-policy)
- [Baselines](#baselines)
- [False Positives](#false-positives)
- [Generated Code and Test Targets](#generated-code-and-test-targets)

---

## Rule Categories

SwiftLint rules fall into three categories:

### Default rules

Enabled automatically. These cover widely agreed-upon conventions (e.g., `line_length`, `force_cast`, `trailing_semicolon`). Disable specific ones via `disabled_rules` in `.swiftlint.yml`.

### Opt-in rules

Disabled by default because they are more opinionated or may not suit every project. Enable selectively via `opt_in_rules`:

```yaml
opt_in_rules:
  - empty_count
  - closure_spacing
  - force_unwrapping
  - sorted_imports
  - contains_over_filter_count
  - first_where
  - last_where
  - modifier_order
  - vertical_whitespace_opening_braces
  - explicit_init
  - joined_default_parameter
  - redundant_nil_coalescing
  - private_swiftui_state
  - unhandled_throwing_task
  - accessibility_label_for_image
  - accessibility_trait_for_button
```

### Analyzer rules

Require the Swift compiler's AST information. Must be run via `swiftlint analyze` with compiler logs. See the custom rules and analyze reference linked from SKILL.md.

```yaml
analyzer_rules:
  - unused_import
  - unused_declaration
```

## Browsing Rules

List all rules and their status:

```sh
swiftlint rules                    # all rules with enabled/disabled/correctable status
swiftlint rules --enabled          # only currently enabled rules
swiftlint rules --disabled         # only currently disabled rules
swiftlint rules <rule_identifier>  # detailed info for one rule
```

The official [rule directory](https://realm.github.io/SwiftLint/rule-directory.html) provides descriptions, configuration options, and examples for every rule.

Do not memorize or transcribe the rule directory. Look up specific rules when needed.

## Commonly Encountered Rules Quick Reference

An agent writing or reviewing Swift code should understand what these frequently triggered rules enforce. Each rule can be configured in `.swiftlint.yml` using the rule identifier as a key.

### Default rules (enabled automatically)

| Rule | What it enforces | Key config options |
| ------ | ------------------ | -------------------- |
| `line_length` | Max characters per line | `warning`, `error`, `ignores_urls`, `ignores_comments`, `ignores_interpolated_strings` |
| `file_length` | Max lines per file | `warning`, `error`, `ignore_comment_only_lines` |
| `type_body_length` | Max lines in a type body | `warning`, `error` |
| `function_body_length` | Max lines in a function body | `warning`, `error` |
| `function_parameter_count` | Max parameters per function | `warning`, `error`, `ignores_default_parameters` |
| `cyclomatic_complexity` | Max branching complexity | `warning`, `error`, `ignores_case_statements` |
| `nesting` | Max nesting depth | `type_level`, `function_level` |
| `blanket_disable_command` | Prevents `swiftlint:disable` from disabling rules for the rest of the file | `allowed_rules`, `always_blanket_disable` |
| `identifier_name` | Naming length and conventions | `min_length`, `max_length`, `excluded` (list of allowed short names like `id`, `x`, `i`) |
| `type_name` | Type naming length and conventions | `min_length`, `max_length`, `excluded` |
| `large_tuple` | Max tuple size | `warning`, `error` |
| `force_cast` | Flags `as!` | severity only |
| `force_try` | Flags `try!` | severity only |
| `todo` | Flags `// TODO:` and `// FIXME:` | severity only |
| `trailing_whitespace` | Trailing spaces on lines | `ignores_empty_lines`, `ignores_comments` |
| `trailing_comma` | Trailing commas in collections | `mandatory_comma` (when `true`, *requires* trailing commas) |
| `vertical_whitespace` | Max consecutive blank lines | `max_empty_lines` |
| `opening_brace` | Brace placement (`{` on same line) | `allow_multiline_func` |
| `colon` | Spacing around colons | `flexible_right_spacing`, `apply_to_dictionaries` |
| `deployment_target` | Flags `@available` / `#available` checks that use versions already satisfied by the deployment target | `iOS_deployment_target`, `macOS_deployment_target`, etc. |

### High-value opt-in rules

| Rule | What it enforces | Why enable it |
| ------ | ------------------ | --------------- |
| `force_unwrapping` | Flags `!` unwraps | Catches crashes; relax in tests via child config |
| `private_swiftui_state` | `@State`, `@StateObject`, `@FocusState` must be `private` | Prevents accidental external mutation of view state |
| `unhandled_throwing_task` | `Task { try ... }` without `do/catch` | Silently swallowed errors in async contexts |
| `sorted_imports` | Import statements in alphabetical order | Reduces merge conflicts; auto-correctable |
| `modifier_order` | Consistent declaration modifier ordering | Readability; auto-correctable |
| `accessibility_label_for_image` | Images must have accessibility labels | Accessibility compliance |
| `accessibility_trait_for_button` | Buttons must have accessibility traits | Accessibility compliance |
| `empty_count` | Use `.isEmpty` instead of `.count == 0` | Performance and clarity |
| `closure_spacing` | Spaces inside closure braces | Formatting consistency |
| `contains_over_filter_count` | `.contains` instead of `.filter { }.count` | Performance |
| `first_where` / `last_where` | `.first(where:)` instead of `.filter { }.first` | Performance |
| `redundant_nil_coalescing` | Flags `x ?? nil` | Dead code |
| `implicit_return` | Single-expression returns don't need `return` | Modern Swift style |
| `self_binding` | Consistent `guard let self` naming | Configurable: `bind_identifier` |
| `shorthand_optional_binding` | `if let x` instead of `if let x = x` | Swift 5.7+ style |
| `expiring_todo` | TODOs/FIXMEs with dates become warnings or errors after expiry | Project hygiene with configurable thresholds and severities |

### Analyzer rules (require compiler logs)

| Rule | What it enforces |
| ------ | ------------------ |
| `unused_import` | Flags unnecessary `import` statements; auto-correctable |
| `unused_declaration` | Flags private declarations never referenced |
| `capture_variable` | Flags mutable variables captured by closures |
| `explicit_self` | Requires `self.` for instance members |
| `typesafe_array_init` | Flags `Array(x.map { ... })` → use `x.map { ... }` directly |

### Per-rule configuration pattern

Every rule that accepts configuration uses its identifier as the YAML key:

```yaml
# Threshold-based rules use warning/error:
line_length:
  warning: 140
  error: 200

# Boolean option rules:
trailing_comma:
  mandatory_comma: true

# Rules with excluded identifiers:
identifier_name:
  excluded:
    - id
    - x
    - y

# Rules with a single severity override:
force_cast: error    # shorthand for severity: error

# Deployment target rule:
deployment_target:
  iOS_deployment_target: "16.0"
```

Run `swiftlint rules <rule_identifier>` to see all available configuration keys for any rule.

## Suppression Syntax

### Single-line suppressions

```swift
// swiftlint:disable:next force_cast
let view = object as! UIView

let value = dict["key"]! // swiftlint:disable:this force_unwrapping

// swiftlint:disable:previous large_tuple
```

- `:next` — suppresses on the next line
- `:this` — suppresses on the same line
- `:previous` — suppresses on the previous line

### Region suppressions

```swift
// swiftlint:disable cyclomatic_complexity function_body_length
func complexLegacyFunction() {
    // ... long function ...
}
// swiftlint:enable cyclomatic_complexity function_body_length
```

Multiple rules can be listed in one directive, separated by spaces.

### Disable all rules

```swift
// swiftlint:disable all
// ... entire block is unlinted ...
// swiftlint:enable all
```

If you forget `// swiftlint:enable all`, the rest of the file is unlinted. This is a common mistake.

## Suppression Policy

- **Target specific rules.** Never use `// swiftlint:disable all` unless the block is generated code that cannot be excluded via config.
- **Add a reason.** Follow the suppression with a brief comment explaining why:

```swift
// swiftlint:disable:next force_cast — guaranteed by Interface Builder outlet type
let cell = tableView.dequeueReusableCell(...) as! CustomCell
```

- **Re-enable after regions.** Always pair `disable` with `enable`.
- **Prefer config-level exclusion** for entire files or directories of generated code.
- **Review suppressions in code review.** Inline suppressions should be as scrutinized as the code they protect.
- **Treat suppressions as tech debt.** Track and reduce them over time.

## Baselines

Baselines record all existing violations so only new violations are reported.

### Creating a baseline

```sh
swiftlint --write-baseline .swiftlint.baseline
```

This creates a JSON file listing every current violation by file, line, and rule. Commit this file to the repository.

### Using a baseline

```sh
swiftlint --baseline .swiftlint.baseline
```

Violations matching the baseline are suppressed. New violations (new files, new lines, new rules) are reported normally.

### Updating a baseline

After fixing violations, regenerate:

```sh
swiftlint --write-baseline .swiftlint.baseline
```

The new baseline will be smaller. Commit the update.

### Baseline in CI

```sh
swiftlint --strict --baseline .swiftlint.baseline --reporter github-actions-logging
```

This fails the build only on new violations not present in the baseline.

### Baseline vs suppressions

| Approach | When to use |
| -------- | ----------- |
| Baseline | Adopting SwiftLint in a large existing codebase |
| Inline suppression | Specific intentional deviation from a rule |
| `disabled_rules` | Team disagrees with a rule project-wide |
| `excluded` paths | Generated or vendored code |
| Child config | Different rules for test vs production code |

## False Positives

When SwiftLint flags code incorrectly:

1. **Check if it's a real false positive** by reading the rule description in the [rule directory](https://realm.github.io/SwiftLint/rule-directory.html).
2. **Check your config** — threshold tuning may resolve it (e.g., raising `line_length` for a file with long URLs).
3. **Suppress with a reason** if it's genuinely incorrect.
4. **File an issue** at [realm/SwiftLint](https://github.com/realm/SwiftLint/issues) if the false positive is reproducible and affects others.

## Generated Code and Test Targets

### Generated code

Exclude generated code directories in `.swiftlint.yml`:

```yaml
excluded:
  - "**/Generated"
  - "**/Derived"
  - "**/*.generated.swift"
```

This is preferable to inline `// swiftlint:disable all` markers because it keeps generated files completely out of the lint pass.

### Test targets

Tests legitimately use patterns that production code should avoid (force unwraps, long functions, etc.). Use a child `.swiftlint.yml` in the test directory:

```yaml
# Tests/.swiftlint.yml
disabled_rules:
  - force_unwrapping
  - force_try
  - force_cast
  - function_body_length
  - type_body_length
  - file_length
```

This is better than excluding tests entirely, because tests still benefit from formatting rules, naming conventions, and other applicable checks.
