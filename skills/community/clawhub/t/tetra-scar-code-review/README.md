# scar-code-review

Code review that learns from failures. Reflex arc blocks repeat mistakes without LLM calls.

Part of the [Tetra Genesis](https://github.com/b-button-corp/tetra-genesis) project (B Button Corp, Nagoya, Japan).

## Installation

No installation needed. Single file, zero dependencies, Python 3.9+.

```bash
cp scar_code_review.py /your/project/
```

## CLI Usage

### Review a file

Run all checklist dimensions (security, performance, correctness, maintainability) against a source file:

```bash
python3 scar_code_review.py review path/to/file.py
```

Output:
```
[critical] [security] Possible SQL injection via string formatting (line 42)
[warning] [maintainability] Function exceeds 50 lines (line 10)
[info] [performance] Unbounded SELECT without LIMIT (line 88)

3 findings (1 critical, 1 warning, 1 info)
```

Exit code is 1 if any critical findings, 0 otherwise.

### Check a diff against past scars

Before the LLM reviews the code, run the reflex arc against your diff:

```bash
python3 scar_code_review.py check-diff path/to/changes.diff
```

Output if a scar matches:
```
BLOCKED by scar rscar_17345: 'Missed SQL injection in format strings' (matched: execute, format, user)
```

Exit code is 1 if any scar fires, 0 if clean.

### Record a missed finding

When a review missed something that later caused a bug or incident:

```bash
python3 scar_code_review.py record-miss \
  --what-missed "Missed SQL injection in user input handler" \
  --pattern "execute.*format.*user" \
  --severity critical
```

Severity levels: `critical`, `high`, `warning`, `info`.

### List recorded review scars

```bash
python3 scar_code_review.py list-scars
```

## Python API

```python
from scar_code_review import review, reflex_check, record_miss, load_review_scars

# 1. Static review with checklist
findings = review("app/views.py")
for f in findings:
    print(f"[{f['severity']}] [{f['dimension']}] {f['message']} (line {f['line']})")

# 2. Reflex check on a diff
scars = load_review_scars()
blocks = reflex_check(open("changes.diff").read(), scars)
if blocks:
    for b in blocks:
        print(f"BLOCKED: {b}")
else:
    print("No scar collisions.")

# 3. Record a miss
record_miss(
    what_missed="Missed unvalidated redirect in login flow",
    pattern="redirect.*request\\.GET",
    severity="high",
)

# 4. Review with scars (combines both)
findings = review("app/views.py", scars=load_review_scars())
```

## Checklist Dimensions

### Security
| Check | Pattern |
|-------|---------|
| SQL injection | String formatting/concatenation in SQL queries |
| Hardcoded secrets | Passwords, API keys, tokens in source |
| XSS | innerHTML, document.write, v-html |
| Dangerous eval | eval(), exec(), subprocess with shell=True |

### Performance
| Check | Pattern |
|-------|---------|
| N+1 queries | Query calls inside loops |
| Missing pagination | List endpoints without limit/offset |
| Unbounded SELECT | SELECT without WHERE or LIMIT |

### Correctness
| Check | Pattern |
|-------|---------|
| Null access | Attribute access without null check |
| Off-by-one | Common fencepost patterns (<=len, range(1,n)) |
| Unhandled promises | Async calls without await/catch/then |

### Maintainability
| Check | Pattern |
|-------|---------|
| Long functions | Functions exceeding 50 lines |
| Deep nesting | Indentation deeper than 4 levels |
| Magic numbers | Unexplained numeric literals in logic |

## How the Reflex Arc Works

Same algorithm as [tetra-scar](../tetra-scar/), adapted for code diffs:

1. Each review scar has a `pattern` field (regex string)
2. `reflex_check` runs every scar pattern against the diff text
3. Also extracts keywords from `what_missed` and checks keyword overlap (40% threshold, minimum 2 matches)
4. If either the regex or keyword check fires, the diff is blocked

No LLM. No API calls. No latency. Pure pattern matching.

## Storage

Review scars are stored in `review_scars.jsonl` (default: `./review_scars.jsonl`).

Format:
```json
{"id": "rscar_1711234567890", "what_missed": "...", "pattern": "...", "severity": "critical", "created_at": "2026-03-21T12:00:00"}
```

Compatible with tetra-scar's JSONL conventions.

## License

MIT-0
