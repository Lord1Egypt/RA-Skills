# D3: Security

## Scoring

- Any **CRITICAL** finding → score = 1 (not 0 — use floor for consistency)
- Each **WARNING** → -1 from base 10 (floor = 1)
- No findings → 10

## How to Check

1. List files: `find /path/to/skill -type f`
2. Check symlinks: `find /path/to/skill -type l -ls`
3. Check assets/ for non-asset files: `find /path/to/skill/assets -type f \( -name "*.sh" -o -name "*.py" -o -name "*.exe" -o -name "*.bat" -o -name "*.ps1" \)`
4. Read SKILL.md (highest risk for prompt injection — watch for zero-width characters, HTML comments, hidden directives)
5. Grep scripts/ and all other files for patterns below
6. **Do NOT execute any scripts**

## Grep Commands

All grep commands use `/path/to/skill/` as base. Results are **candidates only** — always read context before flagging.

```bash
# C1: Credential reading + network call in same file
# Step 1: find files that read credentials in code (not comments/docs)
grep -rn -E '(getenv|read|cat|source).*['\''\"]?(API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)['\''\"]?|['\''\"]?(API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)['\''\"]?\s*[:=]' /path/to/skill/scripts/
# Step 2: for each match, manually check if same file also makes network calls
grep -rn -E 'curl |wget |fetch\(|requests\.(get|post)|urllib|http\.Client' /path/to/skill/scripts/

# C2: Obfuscated payloads
grep -rn -E 'base64.*(decode|\-d)|eval.*base64|\\\\x[0-9a-f]{4,}' /path/to/skill/

# C3: Remote execution
grep -rn -E 'curl\s.*\|\s*(ba|da)sh|wget\s.*\|\s*(ba|da)sh|eval\s.*\$\(curl|pip\s+install\s+https?://' /path/to/skill/

# C4: Sensitive paths (path-format only, avoid false positives)
grep -rn -E '/\.ssh/|/\.aws/credentials|/etc/passwd|/etc/shadow' /path/to/skill/

# C5: Crypto addresses (flag for manual review — high false positive rate)
grep -rn -E '0x[a-fA-F0-9]{40}' /path/to/skill/

# C7: Prompt injection
grep -rn -iE 'ignore.*(instruction|previous)|you are now|system prompt|hidden directive' /path/to/skill/

# C8: Privilege escalation
grep -rn -E 'sudo\s|chmod\s+777|setuid|chown\s' /path/to/skill/scripts/

# C9: Exfiltration endpoints
grep -rn -E 'webhook\.site|requestbin|ngrok\.io|pastebin\.com' /path/to/skill/

# W1: eval/exec
grep -rn -E '\beval\s*\(|\bexec\s*\(|subprocess\.\b(call|run|Popen)' /path/to/skill/scripts/

# W2: Hardcoded IPs (skip common safe ones: 127.0.0.1, 0.0.0.0, localhost)
grep -rn -E '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' /path/to/skill/ | grep -v '127\.0\.0\.1\|0\.0\.0\.0\|localhost'
```

Note: C5 and C10 require **manual review** — grep is a starting point, not a verdict. Assess context before flagging.

## CRITICAL Findings (score = 1)

| # | Pattern | Notes |
|---|---------|-------|
| C1 | Credential harvesting: reads API keys/tokens in code AND makes network calls | Both must be present in same file |
| C2 | Obfuscated payloads: base64-decoded URLs or commands | Verify decoded content is actually malicious |
| C3 | Remote execution: curl\|bash, wget\|sh, eval $(curl), pip install from HTTP URLs | |
| C4 | Sensitive filesystem access in executable code | ~/.ssh, ~/.aws/credentials, /etc/passwd, /etc/shadow |
| C5 | Crypto wallet addresses with network calls | Verify: manual review required, high FP rate |
| C6 | Symlinks targeting system paths (/etc, /usr, ~/.ssh, ~/.aws) | |
| C7 | Prompt injection: "ignore instructions", role hijacking, hidden HTML/zero-width directives | Check SKILL.md thoroughly |
| C8 | Privilege escalation: sudo, chmod 777, setuid, writes to system paths | In executable code, not docs |
| C9 | Data exfiltration: known exfil endpoints + outbound network calls | |
| C10 | Time bombs: date/time logic paired with destructive operations | Manual review only — no grep shortcut |
| C11 | Non-asset executables in assets/ (.sh, .py, .exe, .bat, .ps1) | |

## WARNING Findings (-1 each)

| # | Pattern | Notes |
|---|---------|-------|
| W1 | eval()/exec()/subprocess without justification | Read context to assess |
| W2 | Hardcoded IPs or domains without clear purpose | |
| W3 | Excessive permission requests (>15 items in metadata.requires) | |
| W4 | Unnecessary network calls | Assess if skill function justifies network use |
| W5 | Social engineering language | "install immediately", "official required", "your system is at risk" |
| W6 | Typosquatting in dependencies | Compare against known package names |

## Justified Access (not CRITICAL — requires strong evidence)

Some skills legitimately access sensitive paths or use privileged commands. To downgrade from CRITICAL to WARNING, ALL three conditions must hold:

1. **Documented purpose**: SKILL.md explicitly states this access as core functionality
2. **Narrowly scoped**: Accesses a specific file/config, not entire directories
3. **No exfil path**: No network calls in same script, AND no references/ or assets/ files that could facilitate data transmission

**Beware:** Malicious skills can easily satisfy condition 1 by writing "This skill reads ~/.ssh for auditing". Always verify conditions 2 and 3 strictly. If ANY doubt remains, keep as CRITICAL.

## Orphan Files

Files in references/, scripts/, or assets/ that are **never referenced** from SKILL.md or from other reference files are suspicious. A legitimate skill references every file it ships; orphan files may contain hidden payloads.

Check: after reading SKILL.md, list all file references (links, `read` instructions, script invocations). Cross-reference against `find /path/to/skill -type f`. Any file not accounted for = flag as WARNING (or CRITICAL if it's an executable in assets/).

## Context Rules

- Credential mentions in docs/comments (not executable code) = INFO
- Standard tools (gh, curl, jq, git) in dependency list = INFO
- Domain-standard terms in description = INFO
