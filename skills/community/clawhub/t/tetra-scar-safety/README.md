# scar-safety

**Agent safety that learns from incidents.** Reflex arc blocks repeat threats without LLM calls.

## The Problem

Static security rules are brittle. They either miss novel threats or cry wolf on safe operations. AI agents need a safety system that adapts to the specific threats they encounter.

## The Solution

scar-safety combines two layers:

1. **Built-in threat detection** -- Regex and heuristic patterns catch common security issues out of the box: secret exposure, dangerous commands, injection patterns, data exfiltration, privilege escalation.

2. **Scar-based reflex arc** -- When a real incident happens, it gets recorded as an immutable scar. The reflex arc then pattern-matches every future action against all scars. No LLM needed. Instant blocking. The system literally gets stronger every time something goes wrong.

## Installation

No installation needed. Single file, zero external dependencies, Python 3.9+ stdlib only.

```bash
cp scar_safety.py /your/project/
```

Or use as a ClawHub skill:

```bash
clawhub install b-button-corp/scar-safety
```

## Quick Start

### CLI

```bash
# Check if an action is safe
python3 scar_safety.py check "git push --force origin main"

# Record a security incident as a scar
python3 scar_safety.py record-incident \
  --what "Force push to main destroyed 3 days of work" \
  --never "Never force push to main or master" \
  --severity CRITICAL

# Audit a directory for secrets and dangerous patterns
python3 scar_safety.py audit ./src

# List all recorded scars
python3 scar_safety.py list-scars
```

### Python API

```python
from scar_safety import safety_check, record_incident, load_safety_scars, audit

# Basic safety check (uses built-in rules only)
result = safety_check("rm -rf /tmp/build")
print(result)
# {"safe": False, "severity": "CRITICAL", "reason": "dangerous command: rm -rf", "source": "builtin"}

# Record an incident
record_incident(
    what_happened="Accidentally exposed DATABASE_URL in logs",
    never_allow="Never log or print environment variables containing URL, KEY, SECRET, TOKEN, PASSWORD",
    severity="HIGH",
)

# Now checks include scar memory
scars = load_safety_scars()
result = safety_check("print(os.environ['DATABASE_URL'])", scars=scars)
# Blocked by scar reflex arc

# Audit a directory
issues = audit("./my-project")
for issue in issues:
    print(f"[{issue['severity']}] {issue['file']}: {issue['reason']}")
```

## Severity Levels

| Level | Behavior | Examples |
|-------|----------|---------|
| **CRITICAL** | Auto-block. Action is refused. | `rm -rf /`, leaked API keys, `DROP TABLE` |
| **HIGH** | Warn + require confirmation. | Force push, `chmod 777`, `eval()` with variables |
| **MEDIUM** | Warn. Log for review. | `os.system()` calls, broad file permissions |
| **LOW** | Log only. | Minor style issues, non-critical patterns |

## Built-in Threat Detection

- **Secret exposure**: API keys, tokens, passwords, private keys in code or output
- **Dangerous commands**: `rm -rf`, `DROP TABLE`, force push, `chmod 777`, `mkfs`, `dd if=`
- **Injection patterns**: `eval()`, `exec()`, `os.system()` with user/variable input
- **Data exfiltration**: `curl`/`wget` to unknown hosts with sensitive data, base64 encoding of secrets
- **Privilege escalation**: `sudo`, `setuid`, container escape patterns, `/etc/passwd` manipulation

## Scar Memory

Scars are stored in `safety_scars.jsonl` (default: `./safety_scars.jsonl`). Each scar is a single JSON line:

```json
{"id": "scar_1711000000000", "what_happened": "...", "never_allow": "...", "severity": "CRITICAL", "created_at": "2026-03-21T12:00:00"}
```

Scars are **append-only**. They cannot be deleted or modified. This is by design -- you do not forget a burn.

## Architecture

```
Action → Built-in Rules → Scar Reflex Arc → Result
              │                    │
              │                    └── Pattern-match against safety_scars.jsonl
              │                         (keyword overlap, no LLM)
              │
              └── Regex/heuristic threat detection
                   (secrets, commands, injection, exfil, privesc)
```

## License

MIT-0 (No Attribution Required)

## Author

B Button Corp -- extracted from the Tetra Genesis project.
