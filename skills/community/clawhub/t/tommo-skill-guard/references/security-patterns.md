# Security Pattern Reference

Complete list of patterns used by skill-guard, with explanations and examples.

## Pattern Categories

### 1. Shell Execution (`exec_danger`)
**Risk: HIGH** — Can run arbitrary system commands.

| Pattern | Language | Why it's flagged |
|---------|----------|-----------------|
| `exec()` | Python/JS | Execute shell commands |
| `child_process` | Node.js | Spawn system processes |
| `os.system()` | Python | Run shell commands |
| `subprocess` | Python | Process execution |
| `spawn` | Node.js/Python | Create new processes |
| `eval()` | JS/Python | Execute arbitrary code strings |
| `Function()` | JS | Dynamic function creation |

### 2. Network Calls (`network`)
**Risk: MEDIUM** — External communication, data could be exfiltrated.

| Pattern | Language | Why it's flagged |
|---------|----------|-----------------|
| `curl` | Shell/Bash | HTTP requests |
| `wget` | Shell | File downloads |
| `fetch()` | JS | HTTP requests |
| `http.get/post` | Node.js | HTTP requests |
| `axios` | JS | HTTP client library |
| `requests.get/post` | Python | HTTP library |

**Note:** Many legitimate skills use network calls (weather APIs, email, etc.). Context matters.

### 3. External Filesystem (`fs_external`)
**Risk: MEDIUM** — Accessing files outside the workspace.

| Pattern | Why it's flagged |
|---------|-----------------|
| `rm -rf` | Recursive force delete |
| `/etc/` | System config access |
| `/var/` | System data access |
| `/tmp/` | Temp directory (common attack staging) |
| `chmod 777` | Remove all permissions restrictions |
| `chown` | Change file ownership |

### 4. Hardcoded Secrets (`secrets`)
**Risk: HIGH** — Credentials should never be in skill files.

| Pattern | Service |
|---------|---------|
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID |
| `ghp_[0-9a-zA-Z]{36}` | GitHub Personal Access Token |
| `sk_live_[0-9a-zA-Z]{24}` | Stripe Live Secret Key |
| `xox[bposa]-[0-9-]+` | Slack Bot/User Token |
| `eyJ...eyJ` | JWT Token |

### 5. Obfuscated Code (`obfuscation`)
**Risk: HIGH** — Legitimate skills don't hide their code.

| Pattern | What it does |
|---------|-------------|
| `base64 -d` | Decode base64 at runtime |
| `atob()` | JS base64 decode |
| `Buffer.from(..., 'base64')` | Node.js base64 decode |
| `\x41\x42\x43...` | Hex-encoded strings |

### 6. Elevated Permissions (`elevated`)
**Risk: HIGH** — Running as admin/root bypasses all security.

| Pattern | Platform |
|---------|----------|
| `sudo` | Linux/macOS |
| `su -` | Linux/macOS |
| `runas` | Windows |
| `Set-ExecutionPolicy Bypass` | PowerShell |
| `New-Object System.Diagnostics.Process` | PowerShell process creation |

## Scoring Weights

| Category | Points per match |
|----------|-----------------|
| Obfuscation | 30 |
| Secrets | 25 |
| Shell execution | 20 |
| Elevated permissions | 20 |
| External filesystem | 15 |
| Network calls | 10 |

Large skills (20+ files) get an additional +10 points.

## Domain Analysis

The scanner extracts all URLs/domains from skill files. These should be reviewed manually:

- **Known services** (api.openai.com, api.github.com, etc.) — likely safe
- **Known legitimate** (wttr.in, open-meteo.com) — common in weather/tools skills
- **Unknown/new domains** — investigate before trusting
- **IP addresses** — directly connecting to IPs is suspicious
- **Shortened URLs** (bit.ly, t.co) — could mask malicious destinations

## False Positives

Not every match is a real threat. Consider context:

- A coding-agent skill mentioning `child_process` in documentation is informational
- An email skill using `requests.post` to send emails is expected behavior
- A setup guide mentioning `sudo apt install` is instructional, not execution

The scanner reports raw pattern matches. Use judgment to interpret results.
