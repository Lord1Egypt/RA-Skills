# Tool Reference

Read this when running any of the senior-mobile scripts, configuring their flags, or interpreting their output.

## `mobile_scaffold.py`

**Purpose:** Scaffold a production-ready mobile project with proper directory structure, navigation setup, state management, and base configuration files.

**Usage:**
```bash
python scripts/mobile_scaffold.py <name> --platform <platform> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | positional | Yes | -- | Project name, used as the directory name |
| `--platform`, `-p` | choice | Yes | -- | Target platform: `android-native`, `flutter`, `ios-native`, `react-native` |
| `--typescript`, `-t` | flag | No | `False` (auto-enabled for react-native) | Use TypeScript (React Native only) |
| `--state`, `-s` | string | No | `none` | State management library. React Native: `zustand`, `redux`, `jotai`, `none`. Flutter: `riverpod`, `bloc`, `provider`, `none`. Not applicable for native platforms. |
| `--output-dir`, `-o` | path | No | `.` (current directory) | Parent directory for the generated project |
| `--json` | flag | No | `False` | Output result as JSON instead of human-readable summary |

**Example:**
```bash
# Scaffold a React Native app with Zustand state management
python scripts/mobile_scaffold.py MyApp --platform react-native --state zustand

# Scaffold a Flutter app with Riverpod, output as JSON
python scripts/mobile_scaffold.py my-flutter-app --platform flutter --state riverpod --json

# Scaffold an iOS native app in a specific directory
python scripts/mobile_scaffold.py HealthTracker --platform ios-native --output-dir ~/Projects
```

**Output Formats:**
- **Human-readable (default):** Prints the project name, platform, state management choice, created directory path, and a list of all generated files.
- **JSON (`--json`):** Returns a JSON object with `project_name`, `platform`, `typescript`, `state_management`, `output_directory`, `files_created`, and `generated_at` fields.

---

## `store_metadata_generator.py`

**Purpose:** Generate structured metadata for App Store (iOS) and Google Play Store (Android) submissions, including title variants, keywords, category recommendations, privacy labels, age rating guidance, and submission checklists.

**Usage:**
```bash
python scripts/store_metadata_generator.py --app-name <name> --category <category> --features <features> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--app-name` | string | Yes | -- | The app name for store listings |
| `--category` | choice | Yes | -- | Primary app category. Choices: `business`, `education`, `entertainment`, `finance`, `food`, `games`, `health`, `lifestyle`, `music`, `navigation`, `news`, `photo`, `productivity`, `shopping`, `social`, `sports`, `travel`, `utilities`, `weather` |
| `--features` | string | Yes | -- | Comma-separated list of features (e.g., `"offline,sync,biometric"`). Recognized features expand into keywords and trigger privacy/age-rating guidance. |
| `--description` | string | No | `""` | Short app description used in generated store copy |
| `--json` | flag | No | `False` | Output results as JSON |

**Example:**
```bash
# Generate metadata for a health app
python scripts/store_metadata_generator.py --app-name "FitTrack" --category health --features "workout,tracking,social" --description "Track your workouts"

# JSON output for CI integration
python scripts/store_metadata_generator.py --app-name "BudgetPal" --category finance --features "payment,offline,biometric,push" --json
```

**Output Formats:**
- **Human-readable (default):** Formatted report with sections for Title Variants, Keywords (with iOS 100-char field), Store Categories, Privacy Labels / Data Safety, Age Rating Guidance, and Submission Checklist.
- **JSON (`--json`):** Full metadata object including `titles`, `keywords`, `categories`, `descriptions`, `privacy_labels`, `age_rating`, `screenshot_specs`, and `submission_checklist`.

---

## `app_performance_analyzer.py`

**Purpose:** Analyze a mobile project directory for common performance issues including oversized image assets, re-render patterns, memory leak patterns, bundle size estimation, and platform-specific anti-patterns.

**Usage:**
```bash
python scripts/app_performance_analyzer.py <project_dir> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_dir` | positional | Yes | -- | Path to the mobile project directory to analyze |
| `--platform`, `-p` | choice | No | Auto-detected | Target platform: `react-native`, `flutter`, `ios-native`, `android-native`. Auto-detected from project files if omitted. |
| `--json` | flag | No | `False` | Output results as JSON |

**Example:**
```bash
# Analyze with auto-detected platform
python scripts/app_performance_analyzer.py ./my-app

# Analyze a React Native project explicitly
python scripts/app_performance_analyzer.py ./my-app --platform react-native

# JSON output for CI pipeline integration
python scripts/app_performance_analyzer.py ./my-app --platform flutter --json
```

**Output Formats:**
- **Human-readable (default):** Performance score (0-100 with letter grade), issue summary (critical/warning/info counts), bundle size estimate, detailed issues grouped by category, and platform-specific recommendations.
- **JSON (`--json`):** Full report object including `performance_score`, `summary`, `bundle_estimate` (source code size, asset size, file counts), `issues_by_category`, and the flat `issues` array with `category`, `severity`, `file`, `line`, and `message` per issue.
