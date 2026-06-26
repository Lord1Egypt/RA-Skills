# L1 Static Rule Catalogue — Sentinel Vanguard

Full rule definitions for the static keyword scanner. Each rule has an ID, pattern description, severity, and remediation guidance.

## Destructive Operations (L1-D series)

| ID | Pattern | Severity | Notes |
|---|---|---|---|
| L1-D01 | `rm -rf` | CRITICAL | Recursive force-delete shell command |
| L1-D02 | `rmdir /s` | CRITICAL | Windows recursive directory delete |
| L1-D03 | `shred` | HIGH | Secure file wipe — irreversible |
| L1-D04 | `dd if=/dev/zero` | CRITICAL | Disk overwrite |
| L1-D05 | `os.remove` / `unlink` | MEDIUM | Single file delete — context-dependent |
| L1-D06 | `fs.unlinkSync` | MEDIUM | Node.js synchronous file delete |
| L1-D07 | `DELETE FROM` without WHERE | HIGH | Bulk database record deletion |
| L1-D08 | `DROP TABLE` | CRITICAL | Schema destruction |
| L1-D09 | `TRUNCATE` | HIGH | Table data wipe |
| L1-D10 | `git push --force` | MEDIUM | History-rewriting push |

## Exfiltration Signals (L1-E series)

| ID | Pattern | Severity | Notes |
|---|---|---|---|
| L1-E01 | `upload_file` / `put_object` | HIGH | File upload to external storage |
| L1-E02 | `s3.upload` / `gcs.upload` | HIGH | Cloud storage write |
| L1-E03 | `sendFile` / `postData` | HIGH | HTTP data exfiltration |
| L1-E04 | `os.environ[` | HIGH | Environment variable harvesting |
| L1-E05 | `process.env.` | HIGH | Node.js env var access |
| L1-E06 | `dotenv` combined with HTTP call | HIGH | Secret loading + egress = red flag |
| L1-E07 | Undeclared `http://` or `https://` | LOW | Undocumented external call |
| L1-E08 | `keytar` / `keychain` | HIGH | OS keychain access |
| L1-E09 | `clipboard.read` | MEDIUM | Clipboard harvesting |
| L1-E10 | `screenshot` / `captureScreen` | HIGH | Screen capture |

## Dangerous Execution (L1-X series)

| ID | Pattern | Severity | Notes |
|---|---|---|---|
| L1-X01 | `eval(` | MEDIUM | Dynamic code evaluation |
| L1-X02 | `exec(` | HIGH | Shell/Python arbitrary execution |
| L1-X03 | `Function(` | MEDIUM | JavaScript dynamic function creation |
| L1-X04 | `__import__` | HIGH | Dynamic Python import |
| L1-X05 | `subprocess` | HIGH | Subprocess spawning |
| L1-X06 | `child_process` | HIGH | Node.js process spawning |
| L1-X07 | `os.system` | HIGH | Direct OS shell execution |
| L1-X08 | `pickle.loads` | CRITICAL | Arbitrary code via deserialization |
| L1-X09 | `marshal.loads` | CRITICAL | Python bytecode deserialization |
| L1-X10 | `__reduce__` | HIGH | Custom deserialization exploit hook |

## Permission Anomalies (L1-P series)

| ID | Pattern | Severity | Notes |
|---|---|---|---|
| L1-P01 | `FULL_ACCESS` | HIGH | Overly broad permission scope |
| L1-P02 | `admin: true` | HIGH | Administrative privilege claim |
| L1-P03 | `ignore_errors: true` | MEDIUM | Silent failure suppression |
| L1-P04 | Wildcard scopes `*` | HIGH | Unrestricted access scope |
| L1-P05 | Disabling audit/log | HIGH | Telemetry suppression |
| L1-P06 | `sudo` | HIGH | Superuser command execution |
| L1-P07 | `chmod 777` | MEDIUM | World-writable permissions |
| L1-P08 | `setuid` / `setgid` | CRITICAL | Privilege escalation |
