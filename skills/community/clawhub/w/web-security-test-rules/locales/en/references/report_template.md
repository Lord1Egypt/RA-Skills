# Security Test Report Template (General)

> Companion to `SKILL.md` rules 4, 13, 19, 20.
> Filename: `YYYY-MM-DD_findings.md`.
> **Report save path is customizable** (default `reports/security/<target>/`, overridable by project config `report.path` / `report_dir` or call arguments, see rule 20); custom location must be storage controllable by the authorizer.
> Multiple tests on the same day **append to the same file**; re-review results also append to the same file with a date noted.
> **All time fields must fetch the real current time (to the second) before filling; never fill only a date or estimate from memory (rule 4).**
> **Every test operation must be written into the "Operation Log" below (rule 20, mandatory).**

---

## File Header (written once when first created)

```
# <target> Security Test Report

- Target: <domain / endpoint scope>
- Authorization scope: <accounts / methods / time window>
- Report maintainer: <name / role>
- Report save path: <actual save directory, customizable, rule 20>
- Created: YYYY-MM-DD HH:MM:SS
```

---

## Single Test Record (append a block per test session)

```
## Test Record — YYYY-MM-DD HH:MM:SS

### Overview
- Test time: YYYY-MM-DD HH:MM:SS ~ HH:MM:SS
- Account used: <account identifier>
- New vectors tried this time: <list methods newly used, for dedup reference>
- Skipped already-used vectors (within 7 days): <list skipped, rule 14>

### Operation Log (rule 20: one entry per action, fill immediately, no backfill from memory)
| Time(sec) | Endpoint | Method | Request summary | Key response | Side effects | As expected |
|-----------|----------|--------|-----------------|--------------|--------------|-------------|
| YYYY-MM-DD HH:MM:SS | /api/xxx | POST | param a=1, test privilege | 403 denied (expected) | none | yes |
| YYYY-MM-DD HH:MM:SS | /api/yyy | GET | read other user's resource ID=2 | 200 returns other user's data | none | no (suspected IDOR) |

### Vulnerability List

#### [V-001] <vuln name>
- Severity: Critical / High / Medium / Low / Info
- Location: <endpoint / param / module>
- Description: <phenomenon and principle>
- PoC:
  ```http
  POST /api/xxx HTTP/1.1
  ...
  ```
- Impact: <what consequence>
- Remediation: <concrete actionable fix>
- Truly effective? <bare-request verification result, rule 7>
- Restored? <yes / no (if no, explain and flag to authorizer)>

#### [V-002] ...

### Business Acceptable (not a vuln, record only)
- <some endpoint public with no restriction, judged a design decision>

### Next Directions
- <new methods / modules / endpoints to try next time>
```

---

## Re-review Record (rule 19, append to same file)

```
## Re-review Record — YYYY-MM-DD HH:MM:SS

- Object: [V-001] <vuln name>
- Type: 7-day / 1-month / 6-month / 1-year
- Method: only verify whether fixed, no new attacks
- Result: fixed / not fixed / partially fixed
- Note: <if not fixed, describe current state>
```

---

## Timestamp Rules (rule 4)

- Every record, every finding, every test result carries a **specific current time**.
- **Before filling, fetch the real current time with a time tool / system command, to the second**; never fill only a date or estimate from memory.
- Format (mandatory): `YYYY-MM-DD HH:MM:SS`.
- Purpose: trace the real discovery time; avoid mistaking historical state as ongoing; avoid inability to sort multiple same-day records.

---

## Severity Definitions (adjustable)

| Severity | Meaning | Example |
|----------|---------|---------|
| Critical | direct takeover, DB exfiltration, RCE | unauthorized password change, SQLi data dump |
| High | unauthorized read/write, sensitive info leak | IDOR read others' data, token leak |
| Medium | exploitation requiring conditions, partial bypass | login-required stored XSS |
| Low | info leak, config flaw | verbose error, missing security header |
| Info | hardening advice, not a vuln | business-logic observation, design decision |

---

## Archive & Send (rules 13, 20)

- After generation, send to the authorizer via file-share / send tool.
- Report save path customizable: default `reports/security/<target>/`; project config `report.path` / `report_dir` or call arguments may override (rule 20).
- May upload to agreed / custom archive location (e.g. authorized internal storage, WebDAV backup dir), **keep only the latest copy**.

---

## Report Location Config (rule 20)

- Priority: call argument / CLI > project `report.path` or `report_dir` config > `report_dir` in `AUTHORIZATION.json` > default `reports/security/<target>/`.
- Custom location must be **authorizer-controllable** storage; must not write to third-party public locations.
- Example (project config `.mowen/report.json` or `AUTHORIZATION.json`):
  ```json
  { "report_dir": "/path/to/custom/reports/example.com" }
  ```
