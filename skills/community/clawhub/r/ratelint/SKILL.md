---
name: RateLint
version: 1.0.0
description: "Rate limiting & API throttling anti-pattern analyzer -- detects missing rate limits, brute force exposure, no backoff strategies, unbounded queues, retry storm vulnerability, and flow control gaps"
homepage: https://ratelint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udea6",
      "primaryEnv": "RATELINT_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash"]
      },
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

# RateLint -- Rate Limiting & API Throttling Anti-Pattern Analyzer

RateLint scans codebases for rate limiting anti-patterns, missing throttling middleware, brute force exposure, unprotected endpoints, missing backoff strategies, unbounded queues, retry storm vulnerability, and flow control gaps. It uses regex-based pattern matching against 90 rate-limiting-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `ratelint scan [file|directory]`
One-shot rate limiting quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 rate limiting quality patterns against each file (free tier limit)
4. Calculates a rate limiting quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if rate limiting quality is poor
8. Free tier limited to first 30 patterns (RL + BF categories)

**Example usage scenarios:**
- "Scan my code for missing rate limits" -> runs `ratelint scan .`
- "Check this file for throttling issues" -> runs `ratelint scan src/server.ts`
- "Find brute force exposure" -> runs `ratelint scan src/`
- "Audit rate limiting in my project" -> runs `ratelint scan .`
- "Check for missing API throttling" -> runs `ratelint scan .`

### Pro Tier ($19/user/month -- requires RATELINT_LICENSE_KEY)

#### `ratelint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering rate limiting, brute force, throttling, and backoff.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 rate limiting patterns (RL, BF, TH, BP categories)
3. Detects missing throttling and backpressure patterns
4. Identifies backoff and retry anti-patterns
5. Full category breakdown reporting

#### `ratelint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `ratelint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `ratelint scan --category TH [directory]`
Filter scan to a specific check category (RL, BF, TH, BP, QO, DD).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category TH
```

### Team Tier ($39/user/month -- requires RATELINT_LICENSE_KEY with team tier)

#### `ratelint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including queue overflow and retry backoff.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes queue/buffer overflow checks (unbounded queues, missing max size)
4. Includes retry & backoff checks (infinite retry loops, missing jitter, no circuit breaker)
5. Full category breakdown with per-file results

#### `ratelint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `ratelint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

RateLint detects 90 rate limiting anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Rate Limit Configuration** | RL | 15 | Missing rate limits on API endpoints, no limit headers, unbounded request acceptance, excessively high limits | medium -- critical |
| **Brute Force Protection** | BF | 15 | No login attempt limiting, missing account lockout, password reset flood, OTP brute force, disabled CAPTCHA | high -- critical |
| **Throttling & Backpressure** | TH | 15 | No request throttling, missing debounce, unbounded event handlers, no load shedding, disabled throttle | medium -- critical |
| **Backoff & Retry** | BP | 15 | No backpressure signaling, unbounded worker pools, missing flow control, disabled backpressure mechanisms | medium -- critical |
| **Queue & Buffer Overflow** | QO | 15 | Unbounded queues, no max queue size, memory exhaustion from queue growth, missing overflow handling | medium -- critical |
| **DDoS & Abuse Prevention** | DD | 15 | No exponential backoff, infinite retry loops, missing jitter, aggressive retry intervals, disabled circuit breaker | medium -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | RL, BF |
| **Pro** | 60 | RL, BF, TH, BP |
| **Team** | 90 | RL, BF, TH, BP, QO, DD |
| **Enterprise** | 90 | RL, BF, TH, BP, QO, DD + priority support |

## Scoring

RateLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Security vulnerability or guaranteed failure (unlimited retries, unbounded pools) |
| **High** | -15 per finding | Significant gap that will allow abuse (missing auth rate limit, no brute force protection) |
| **Medium** | -8 per finding | Moderate concern (missing throttle, no backoff strategy) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent rate limiting practices |
| **B** | 80-89 | Good practices with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor rate limiting quality |
| **F** | Below 60 | Critical throttling problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure RateLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "ratelint": {
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
- If license key is invalid or expired, show clear message with link to https://ratelint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use RateLint

The user might say things like:
- "Scan my code for missing rate limits"
- "Check my API throttling"
- "Find brute force exposure"
- "Detect missing backoff strategies"
- "Are there any unthrottled endpoints?"
- "Check for missing rate limiting middleware"
- "Audit my rate limiting practices"
- "Find retry storm vulnerabilities"
- "Check for queue overflow risks"
- "Scan for rate limiting anti-patterns"
- "Run a rate limiting quality audit"
- "Generate a rate limiting quality report"
- "Check if my login endpoint has brute force protection"
- "Find endpoints without rate limits"
- "Check my code for missing exponential backoff"
