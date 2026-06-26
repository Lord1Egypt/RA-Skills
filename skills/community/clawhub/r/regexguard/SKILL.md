---
name: RegexGuard
version: 1.0.0
description: "Regex safety & correctness analyzer -- detects catastrophic backtracking, portability errors, correctness bugs, maintainability issues, anchoring problems, and pattern injection risks"
homepage: https://regexguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83c\udfaf",
      "primaryEnv": "REGEXGUARD_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# RegexGuard -- Regex Safety & Correctness Analyzer

RegexGuard scans codebases for regex anti-patterns: catastrophic backtracking (ReDoS), portability errors across engines, correctness bugs, maintainability issues, anchoring and boundary problems, and pattern injection risks. It uses regex-based pattern matching against 90 regex-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

**Note:** RegexGuard focuses on regex patterns found in source code (JavaScript, Python, Go, Java, Ruby, shell scripts, config files). It detects anti-patterns in how regexes are written, constructed, and used.

## Commands

### Free Tier (No license required)

#### `regexguard scan [file|directory]`
One-shot regex safety scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 regex patterns against each file (free tier limit)
4. Calculates a regex quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if regex quality is poor
8. Free tier limited to first 30 patterns (CB + PE categories)

**Example usage scenarios:**
- "Scan my code for regex issues" -> runs `regexguard scan .`
- "Check this file for ReDoS vulnerabilities" -> runs `regexguard scan src/validators.ts`
- "Find catastrophic backtracking patterns" -> runs `regexguard scan src/`
- "Check for non-portable regex syntax" -> runs `regexguard scan .`
- "Audit regex patterns for correctness" -> runs `regexguard scan .`

### Pro Tier ($19/user/month -- requires REGEXGUARD_LICENSE_KEY)

#### `regexguard scan --tier pro [file|directory]`
Extended scan with 60 patterns covering backtracking, portability, correctness, and maintainability.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 regex patterns (CB, PE, CE, MA categories)
3. Detects correctness bugs like unescaped dots, bad character class ranges
4. Identifies maintainability issues: overly complex patterns, missing comments
5. Full category breakdown reporting

#### `regexguard scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `regexguard scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `regexguard scan --category CB [directory]`
Filter scan to a specific check category (CB, PE, CE, MA, AN, PI).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category CB
```

### Team Tier ($39/user/month -- requires REGEXGUARD_LICENSE_KEY with team tier)

#### `regexguard scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including anchoring and injection.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes anchoring checks (missing ^/$, multiline flag gaps, \b misuse)
4. Includes pattern injection checks (unsanitized user input, DoS vectors)
5. Full category breakdown with per-file results

#### `regexguard scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `regexguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

#### `regexguard patterns`
List all 90 detection patterns across all categories.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" patterns
```

## Check Categories

RegexGuard detects 90 regex anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Catastrophic Backtracking** | CB | 15 | Nested quantifiers, exponential patterns, ReDoS vectors, overlapping greed | low -- critical |
| **Portability Errors** | PE | 15 | Non-POSIX features, engine-specific syntax, lookbehind gaps, Unicode escapes | low -- high |
| **Correctness Errors** | CE | 15 | Unescaped dots, bad character class ranges, greedy vs lazy, redundant quantifiers | low -- high |
| **Maintainability Issues** | MA | 15 | Overly complex patterns, missing comments, duplication, magic regex strings | low -- high |
| **Anchoring & Boundaries** | AN | 15 | Missing ^/$, \b misuse, multiline flag gaps, validation anchor bypass | low -- critical |
| **Pattern Injection** | PI | 15 | Unsanitized user input in regex, string concat into RegExp, DoS vectors | low -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | CB, PE |
| **Pro** | 60 | CB, PE, CE, MA |
| **Team** | 90 | CB, PE, CE, MA, AN, PI |
| **Enterprise** | 90 | CB, PE, CE, MA, AN, PI + priority support |

## Scoring

RegexGuard uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe risk (ReDoS, injection, missing validation anchors) |
| **High** | -15 per finding | Significant problem (portability bugs, correctness errors) |
| **Medium** | -8 per finding | Moderate concern (engine-specific features, maintainability) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent regex quality |
| **B** | 80-89 | Good patterns with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor regex quality |
| **F** | Below 60 | Critical regex problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure RegexGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "regexguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://regexguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use RegexGuard

The user might say things like:
- "Scan my code for regex issues"
- "Check for catastrophic backtracking"
- "Find ReDoS vulnerabilities in my patterns"
- "Check for non-portable regex syntax"
- "Audit regex correctness in my codebase"
- "Find regex injection risks"
- "Check if my validation regex has proper anchors"
- "Detect overly complex regex patterns"
- "Scan for regex portability problems"
- "Find unsafe dynamic regex construction"
- "Run a regex quality audit"
- "Generate a regex health report"
- "Check for unescaped dots in my patterns"
- "Find missing anchors in validation regex"
- "Check for user input in regex constructors"
