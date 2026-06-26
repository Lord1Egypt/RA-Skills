# Plugins, Run Scripts, and Integrations

Setup instructions for each SwiftLint integration method: build tool plugin, command plugin, Xcode run scripts, CI, and secondary integrations.

## Contents

- [Build Tool Plugin (Recommended)](#build-tool-plugin-recommended)
- [Command Plugin](#command-plugin)
- [Xcode Run Script Build Phase](#xcode-run-script-build-phase)
- [CI Recipes](#ci-recipes)
- [Working With Multiple Swift Versions](#working-with-multiple-swift-versions)
- [VS Code](#vs-code)
- [Fastlane](#fastlane)
- [Docker](#docker)
- [Pre-commit Hook](#pre-commit-hook)

---

## Build Tool Plugin (Recommended)

The `SwiftLintBuildToolPlugin` from [SimplyDanny/SwiftLintPlugins](https://github.com/SimplyDanny/SwiftLintPlugins) runs SwiftLint as part of the build. No Homebrew or PATH setup needed.

### SwiftPM setup

```swift
// Package.swift
let package = Package(
    name: "MyApp",
    dependencies: [
    .package(url: "https://github.com/SimplyDanny/SwiftLintPlugins", from: "<reviewed-version>")
    ],
    targets: [
        .target(
            name: "MyApp",
            plugins: [.plugin(name: "SwiftLintBuildToolPlugin", package: "SwiftLintPlugins")]
        ),
        .testTarget(
            name: "MyAppTests",
            dependencies: ["MyApp"],
            plugins: [.plugin(name: "SwiftLintBuildToolPlugin", package: "SwiftLintPlugins")]
        )
    ]
)
```

### Xcode project setup (no Package.swift)

1. **File > Add Package Dependencies** → add `https://github.com/SimplyDanny/SwiftLintPlugins`
2. For each target you want to lint, go to **Build Phases** and add `SwiftLintBuildToolPlugin` under **Run Build Tool Plug-ins**
3. When prompted, trust the plugin

### Plugin trust

On first build, Xcode shows a trust dialog. Select **Trust & Enable All** for the SwiftLintPlugins package. In CI with `xcodebuild`, pass:

```sh
xcodebuild -skipPackagePluginValidation -skipMacroValidation ...
```

These unattended flags bypass Xcode's validation dialogs and implicitly trust package plugins and macros. Use them only for reviewed dependencies in controlled CI.

### Limitations

- The build tool plugin cannot run `--fix` (it has read-only access to sources).
- It cannot pass `--baseline` or other CLI flags — build tool plugins do not accept arguments. Use config keys like `baseline:` / `write_baseline:` where available, or switch to the command plugin / direct CLI for advanced flag-based workflows.
- It may fail when Swift files or the config live outside the package/project directory because it cannot pass `--config`. Add a local `.swiftlint.yml` with `parent_config:` pointing to the shared config, or use a run script.
- It runs on every build, which is desirable for local development but may slow clean builds in large projects.

## Command Plugin

The command plugin provides broad SwiftPM-based CLI access to SwiftLint, including `--fix`, `--baseline`, and `analyze` workflows that the build tool plugin cannot handle directly:

```sh
swift package plugin swiftlint
swift package plugin swiftlint --fix
swift package plugin swiftlint -- --strict --baseline .swiftlint.baseline
swift package plugin swiftlint -- analyze --compiler-log-path swift-build.log
```

The command plugin requires the same `SwiftLintPlugins` dependency. It accepts SwiftLint CLI flags after `--`; when using `--fix`, expect SwiftPM's package-directory write-permission handling because fixes can modify source files.

## Xcode Run Script Build Phase

Use a run script when the build tool plugin is impractical for your project shape or when you need CLI features the build tool plugin cannot provide (for example `--fix` locally or `--baseline`). Xcode projects can still use the build tool plugin via Xcode Package Dependency even without a local `Package.swift`.

### Basic run script

1. Select the target → **Build Phases** → **+** → **New Run Script Phase**
2. Move the phase **after Compile Sources** — SwiftLint is designed to analyze valid, compilable source code; linting before compilation leads to confusing results
3. Add the script:

```sh
if command -v swiftlint >/dev/null 2>&1; then
    swiftlint
else
    echo "warning: SwiftLint not installed. Install with: brew install swiftlint"
fi
```

On Apple Silicon with Homebrew, `swiftlint` is often installed at `/opt/homebrew/bin/swiftlint`. If the run script cannot find it, either export that path in the build phase or create a symlink into `/usr/local/bin`:

```sh
if [[ "$(uname -m)" == arm64 ]]; then
  export PATH="/opt/homebrew/bin:$PATH"
fi

if command -v swiftlint >/dev/null 2>&1; then
  swiftlint
else
  echo "warning: SwiftLint not installed. Install with: brew install swiftlint"
fi
```

### Run script with script input files (Xcode 15+)

Xcode 15 sandboxes run scripts by default. If SwiftLint fails with `Sandbox: swiftlint ... deny(1) file-read-data`, set `ENABLE_USER_SCRIPT_SANDBOXING = NO` for the target. Input files and input file lists are a separate optimization for limiting which files are linted.

1. Set `ENABLE_USER_SCRIPT_SANDBOXING = NO` for the target if the script cannot read source files under Xcode 15+
2. Under the run script phase, check **Based on dependency analysis**
3. Add either explicit **Input Files** or readable `.xcfilelist` paths under **Input File Lists**
4. Use `--use-script-input-file-lists` when Xcode is providing `.xcfilelist` paths:

```sh
if command -v swiftlint >/dev/null 2>&1; then
  swiftlint --use-script-input-file-lists
fi
```

This requires Xcode to populate `SCRIPT_INPUT_FILE_LIST_COUNT` and `SCRIPT_INPUT_FILE_LIST_n` with readable `.xcfilelist` paths. Use `--use-script-input-files` only when Xcode is populating `SCRIPT_INPUT_FILE_COUNT` and `SCRIPT_INPUT_FILE_n` directly via **Input Files** rather than **Input File Lists**.

Alternatively, to lint the full target without file lists:

```sh
if command -v swiftlint >/dev/null 2>&1; then
    swiftlint lint --config "${SRCROOT}/.swiftlint.yml"
fi
```

And uncheck **Based on dependency analysis** if you want it to run every build.

### CocoaPods run script

```sh
"${PODS_ROOT}/SwiftLint/swiftlint"
```

## CI Recipes

### GitHub Actions

```yaml
name: SwiftLint
on:
  pull_request:
    paths: ['**/*.swift']

jobs:
  lint:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install SwiftLint
        run: brew install swiftlint
      - name: Lint
        run: swiftlint --strict --reporter github-actions-logging
```

For SARIF upload to GitHub code scanning:

```yaml
      - name: Lint (SARIF)
        run: swiftlint --strict --reporter sarif > swiftlint.sarif
        continue-on-error: true
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: swiftlint.sarif
```

### GitHub Actions with baseline

```yaml
      - name: Lint (baseline)
        run: swiftlint --strict --baseline .swiftlint.baseline --reporter github-actions-logging
```

### GitLab CI

```yaml
swiftlint:
  image: ghcr.io/realm/swiftlint:latest
  script:
    - swiftlint --strict --reporter codeclimate > swiftlint.json
  artifacts:
    reports:
      codequality: swiftlint.json
```

If you want GitLab JUnit-style output instead, use `--reporter gitlab` and publish the result as a JUnit artifact rather than `codequality`.

### Bitrise / other CI

```sh
brew install swiftlint
swiftlint --strict
```

### Reporter summary

| Reporter | Format | Best for |
| -------- | ------ | -------- |
| `xcode` | Xcode-compatible text | Local builds, Xcode run scripts |
| `github-actions-logging` | GitHub Actions annotations | PR inline comments |
| `sarif` | SARIF JSON | GitHub code scanning |
| `json` | JSON array | Custom tooling, dashboards |
| `checkstyle` | XML | Jenkins, SonarQube |
| `csv` | CSV | Spreadsheet analysis |
| `emoji` | Text with emoji | Fun terminal output |

## Working With Multiple Swift Versions

SwiftLint is predominantly SwiftSyntax-based, but some rules still rely on SourceKit/Clang for additional analysis. It must remain compatible with the Swift toolchain used to compile your project.

**Key rules:**

1. Run SwiftLint with the same Swift toolchain used to build your project.
2. On macOS, SwiftLint resolves the toolchain in this order: `XCODE_DEFAULT_TOOLCHAIN_OVERRIDE`, `TOOLCHAIN_DIR` or `TOOLCHAINS`, `xcrun -find swift`, `/Applications/Xcode.app/...`, `/Applications/Xcode-beta.app/...`, `~/Applications/Xcode.app/...`, `~/Applications/Xcode-beta.app/...`.
3. In CI with multiple Xcode versions, set `DEVELOPER_DIR` before running SwiftLint:

```sh
export DEVELOPER_DIR=/Applications/Xcode_16.app/Contents/Developer
swiftlint
```

1. The build tool plugin automatically uses the correct toolchain because it runs within the build system.
2. Homebrew-installed SwiftLint may lag behind the latest Swift release. If you see parsing errors after updating Xcode, check for a SwiftLint update.
3. `sourcekitd.framework` is expected in the selected toolchain’s `usr/lib/` directory. Toolchain mismatches typically show up as parsing or SourceKit failures.

## VS Code

The [SwiftLint VS Code extension](https://marketplace.visualstudio.com/items?itemName=vknabel.vscode-swiftlint) runs SwiftLint on save.

```json
// .vscode/settings.json
{
    "swiftlint.enable": true,
    "swiftlint.path": "/opt/homebrew/bin/swiftlint",
    "swiftlint.autoLintWorkspace": false
}
```

## Fastlane

```ruby
# Fastfile
lane :lint do
  swiftlint(
    mode: :lint,
    config_file: ".swiftlint.yml",
    strict: true,
    raise_if_swiftlint_error: true
  )
end
```

## Docker

The official SwiftLint Docker image is useful for Linux CI:

```sh
docker run --rm -v "$(pwd):/work" -w /work ghcr.io/realm/swiftlint:<reviewed-version> --strict
```

## Pre-commit Hook

### Using the pre-commit framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/realm/SwiftLint
    rev: <reviewed-version>
    hooks:
      - id: swiftlint
```

To apply fixes and fail on warnings/errors from the hook, use an `entry` override:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/realm/SwiftLint
    rev: <reviewed-version>
    hooks:
      - id: swiftlint
        entry: swiftlint --fix --strict
```

### Manual git hook

```sh
#!/bin/sh
# .git/hooks/pre-commit
if command -v swiftlint >/dev/null 2>&1; then
    git diff --cached --name-only --diff-filter=d -- '*.swift' | \
        xargs -I{} swiftlint lint --path "{}" --strict --quiet
fi
```

Make it executable: `chmod +x .git/hooks/pre-commit`
