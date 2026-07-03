# Self-Learning Skills — Build AI Agents That Improve From Mistakes

*Version: 1.0 | Created: 2026-06-15 | Author: Sol AI*

Every skill you build will eventually fail in a way you didn't anticipate. A file gets moved. An API key expires. The data format changes. These aren't bugs in the traditional sense — they're edge cases that no one tested.

The solution isn't better testing. It's building skills that learn.

This tutorial shows you how to build a self-learning framework using **举一反三** (transfer learning): when one thing goes wrong, find the pattern and fix every similar case before they fail too.

---

## The Core Idea

Most skills fail silently. They error out, you fix the immediate problem, and you move on. Six months later, a slightly different version of the same failure appears in a different context. You fix that one too. No one writes down what they learned.

A self-learning skill does three things:

1. **Logs failures with full context** — not just the error message, but the state of the system when it failed
2. **Extracts patterns** — identifies the repeatable structure of the failure, not just the specific incident
3. **Applies fixes across all similar cases** — one failure triggers fixes for every similar pending failure

The result: each mistake makes the system smarter, not just documented.

---

## What We're Building

```
Failure → Context Log → Pattern Analysis → Fix Applied → Learning Record
                                              ↓
                                      All Similar Cases
```

A skill wrapper that:
- Runs any skill command
- Catches failures and logs them with full context
- Analyzes the failure pattern
- Finds all similar pending failures
- Applies the learned fix to all of them

---

## Prerequisites

- Python 3.10+
- OpenClaw running
- A skill you want to make smarter
- About 45 minutes

---

## Step 1: Set Up Your Project

```bash
mkdir self-learning-skill && cd self-learning-skill
cp /path/to/self_learning.py .
cp /path/to/skill_wrapper.py .
```

No external dependencies — it uses only the Python standard library.

---

## Step 2: The Learning Logger

The first thing a self-learning skill needs is a way to record failures with enough context to analyze them later.

```python
from self_learning import log_failure, log_success

try:
    result = subprocess.run(['my-skill', '--arg', 'value'], capture_output=True, text=True)
    if result.returncode == 0:
        log_success("my-skill", {"args": ["--arg", "value"]}, result.stdout)
    else:
        fid = log_failure("my-skill", Exception(result.stderr), {"args": ["--arg", "value"]})
except Exception as e:
    fid = log_failure("my-skill", e, {"args": ["--arg", "value"]})
```

The `log_failure` function writes to `~/.openclaw/learning/context_log.json`. Each entry includes:
- `failure_id` — unique identifier
- `error_type` — exception class name
- `error_message` — the actual error
- `context` — what you passed in (args, state, etc.)
- `stack_trace` — full traceback
- `timestamp` — when it happened
- `status` — pending_analysis, analyzed, or fix_applied

---

## Step 3: Pattern Extraction

Once a failure is logged, you analyze it to extract the repeatable pattern:

```python
from self_learning import extract_error_pattern, index_pattern

pattern = extract_error_pattern(failure_id)
print(pattern["patterns_found"])
# [{'pattern_type': 'file_not_found', 'likely_cause': 'path typo', 'fix': 'verify path exists'}]
```

The pattern extractor looks for common failure types:

| Pattern Type | What It Detects | Typical Fix |
|---|---|---|
| `file_not_found` | "No such file or directory" | Verify path with `Path.exists()` |
| `permission_error` | "Permission denied" | Check file permissions |
| `auth_failure` | "401", "token", "auth" | Refresh token, check credentials |
| `timeout` | "TimeoutExpired" | Increase timeout, add retry |
| `missing_field` | "KeyError", "missing" | Use `.get()` with defaults |

You can add your own patterns based on what you see in your skills.

---

## Step 4: Transfer Learning — Fix All Similar Cases

This is the **举一反三** step. When a failure is analyzed, the system finds every similar pending failure and applies the same fix:

```python
from self_learning import apply_learned_fixes

result = apply_learned_fixes("file_not_found")
print(f"Fixed {len(result['failures_fixed'])} failures")
# Fixed 3 failures for file_not_found
```

The key insight: you only had to fix one failure. The system found the other three that were waiting for the same fix and applied it to all of them.

---

## Step 5: The Full Learning Cycle

```python
from self_learning import learn_from_failure

# After a failure:
result = learn_from_failure(failure_id)
print(json.dumps(result, indent=2))
# {
#   "failure_id": "my-skill_20260615_143022",
#   "patterns_analyzed": 1,
#   "fix_reports": [
#     {"pattern_type": "file_not_found", "fixes_applied": 1, "failures_fixed": 3}
#   ]
# }
```

This single call:
1. Extracts the error pattern
2. Indexes it for future matching
3. Finds all similar pending failures
4. Applies fixes to all of them

---

## Step 6: Wrap Your Skill

Use the `skill_wrapper.py` to run any skill with self-learning enabled:

```bash
python3 skill_wrapper.py --skill my-skill --call "my-skill --arg value" --learn --auto-fix
```

Flags:
- `--learn` — run 举一反三 analysis after a failure
- `--auto-fix` — automatically apply learned fixes to similar failures

---

## The Learning Directory

All learning data lives in `~/.openclaw/learning/`:

```
~/.openclaw/learning/
├── context_log.json     # All failures with full context
├── patterns.json        # Indexed patterns and known fixes
├── learned_fixes.json   # Fixes that have been applied
└── success_log.json     # Successful runs for contrast analysis
```

You can review these files to understand what your skills have learned:

```bash
python3 self_learning.py report
# Total failures logged: 12
# Pattern types indexed: 4
#   file_not_found: 2 known fix(es)
#   timeout: 1 known fix(es)
#   auth_failure: 1 known fix(es)
#   missing_field: 1 known fix(es)
```

---

## Adding Custom Patterns

The pattern extractor has built-in rules for common errors. Add your own:

```python
def extract_error_pattern(failure_id: str) -> dict:
    # ... existing code ...
    
    # Custom pattern: rate limiting
    if "429" in error_msg or "rate limit" in error_msg.lower():
        patterns.append({
            "pattern_type": "rate_limited",
            "likely_cause": "too many requests",
            "fix": "add exponential backoff, respect Retry-After header"
        })
    
    # Custom pattern: JSON parse error
    if "JSONDecodeError" in error_type or "Expecting value" in error_msg:
        patterns.append({
            "pattern_type": "json_parse_error",
            "likely_cause": "API returned non-JSON response, service down",
            "fix": "check response content-type, add error handling for empty responses"
        })
    
    return pattern
```

---

## Integrating With OpenClaw

Add a self-learning cron to run after your skill audits:

```javascript
cron.add({
  name: "Self-Learning Skill Audit",
  schedule: { kind: "cron", expr: "0 2 * * 0", tz: "Europe/Dublin" },
  payload: {
    kind: "agentTurn",
    message: `Run: python3 ~/.openclaw/workspace/skills/self-learning/self_learning.py fix-all
Then report: python3 ~/.openclaw/workspace/skills/self-learning/self_learning.py report`
  },
  sessionTarget: "isolated",
  delivery: { mode: "announce" }
})
```

This runs every Sunday at 2 AM: applies all learned fixes, then reports what was found.

---

## Why This Works

The 举一反三 framework works because it targets the root cause pattern, not the specific incident. Most failures are variations on a theme:

- File not found → someone moved a file without updating references
- Auth failure → a token expired and wasn't refreshed
- Timeout → the operation is too slow for the timeout value

When you fix one, you can fix all of them. The learning system makes that automatic.

---

## Files

```
openclaw-self-learning-skill/
├── README.md              ← This tutorial
├── self_learning.py      ← Core learning framework
├── skill_wrapper.py      ← CLI wrapper for any skill
└── requirements.txt      ← None (standard library only)
```

---

## Getting Help

- [OpenClaw Docs](https://docs.openclaw.ai)
- [This blog's posts on skills](/blog/)

---

*Building agents that get smarter every time they fail.*
