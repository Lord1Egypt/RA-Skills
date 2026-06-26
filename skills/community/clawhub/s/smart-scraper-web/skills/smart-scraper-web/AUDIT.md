# Smart Scraper — Security Audit

**Date:** 2026-06-12  
**Auditor:** Jarvis (automated audit)  
**Files:** `smart-scraper.js` (~14KB), `SKILL.md` (~4KB)

---

## Audit Results: ALL CRITICAL ISSUES FIXED ✅

### Fixes Applied

| Finding | Fix | Status |
|---------|-----|--------|
| 🔴 SSRF — No URL validation | `validateUrl()` — blocks file://, gopher://, data:, javascript://, ftp://, localhost, private IPs, cloud metadata (169.254.169.254) | ✅ FIXED |
| 🔴 SSRF — No redirect limit | `MAX_REDIRECTS = 5` with redirect count tracking | ✅ FIXED |
| 🟠 ReDoS — `<[^>]+>` pattern | Bounded to `{0,1024}` | ✅ FIXED |
| 🟠 ReDoS — `<table[\s\S]*?</table>` | Bounded to `{0,500000}` | ✅ FIXED |
| 🟠 Cache grows indefinitely | LRU eviction: max 50 entries / 10MB, TTL cleanup | ✅ FIXED |
| 🟡 No rate limiting | 100ms minimum between requests | ✅ FIXED |
| 🟡 Fake User-Agent | Changed to `Mozilla/5.0 (compatible; SmartScraper/1.0)` | ✅ FIXED |
| 🟡 No timeout on redirects | Timeout inherited on each redirect hop | ✅ FIXED |
| 🟡 Silent cache persistence | `--no-cache` CLI flag + visible warning before first cache write | ✅ FIXED (2026-06-12) |

### All regex patterns now bounded:
- `<[^>]{0,1024}>` — tag matching
- `<table[\s\S]{0,500000}?` — table matching
- `href="([^"]{0,2048})"` — attribute values
- `[^>]{0,1024}` — all tag attribute matching
- `{0,100000}` — content body matching

### Summary

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 Critical | 0 | All fixed |
| 🟠 High | 0 | All fixed |
| 🟡 Medium | 0 | All fixed |
| 🟢 Low | 2 | Noted (HTML entity decoding, JSON size limit) |
| **Total** | **11** | **9 fixed, 2 low-risk noted** |

---

## Resolved Findings

> **Note:** All critical, high, and medium findings below were fixed on 2026-06-12. They are retained here for reference.

### 🔴 CRITICAL (All Resolved)

#### 1. SSRF — No URL Validation Before Fetch
**Severity:** Critical → **✅ RESOLVED**  
**Fix Applied:** `validateUrl()` blocks `file://`, `gopher://`, `data:`, `javascript://`, `ftp://`, localhost, private IPs, and cloud metadata (169.254.169.254). Applied at entry (line 296) and on each redirect target (line 147).

#### 2. SSRF — Redirect Following Has No Loop Limit
**Severity:** Critical → **✅ RESOLVED**  
**Fix Applied:** `MAX_REDIRECTS = 5` enforced at line 141. Redirect count tracked via parameter.

### 🟠 HIGH (All Resolved)

#### 3. Regex ReDoS — `<[^>]+>` Pattern
**Severity:** High → **✅ RESOLVED**  
**Fix Applied:** Bounded to `/<[^>]{0,1024}>/g` (line 194).

#### 4. Regex ReDoS — `<table[\s\S]*?</table>`
**Severity:** High → **✅ RESOLVED**  
**Fix Applied:** Bounded to `{0,500000}` (line 244).

#### 5. Cache Grows Indefinitely — No Eviction
**Severity:** High → **✅ RESOLVED**  
**Fix Applied:** LRU eviction with max 50 entries / 10MB, TTL cleanup.

### 🟡 MEDIUM (All Resolved)

#### 6. No Rate Limiting
**Severity:** Medium → **✅ RESOLVED**  
**Fix Applied:** 100ms minimum between requests.

#### 7. User-Agent Spoofing
**Severity:** Medium → **✅ RESOLVED**  
**Fix Applied:** Changed to `Mozilla/5.0 (compatible; SmartScraper/1.0)`.

#### 8. No Timeout on Redirect Resolution
**Severity:** Medium → **✅ RESOLVED**  
**Fix Applied:** Timeout inherited on each redirect hop.

### 🟢 LOW (All Resolved)

#### 9. JSON Parse — No Size Limit ✅ FIXED (2026-06-18)
**Severity:** Low — **Resolved**  
**Fix:** Added `fs.statSync()` size check before parse — rejects files over 10MB with warning.

#### 10. stripHtml Does Not Handle All HTML Entities ✅ FIXED (2026-06-18)
**Severity:** Low — **Resolved**  
**Fix:** Added `decodeHtmlEntities()` — handles named entities (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&nbsp;`, etc.), numeric (`&#123;`), and hex (`&#x1F;`). Applied in `stripHtml()`.

---

## Not Found (Clean)

| Category | Status |
|----------|--------|
| Command injection | ✅ No execSync with user input |
| eval / Function() | ✅ No dynamic code execution |
| Path traversal | ✅ No user-controlled file paths |
| eval on fetched content | ✅ No eval on HTTP responses |
| Credential handling | ✅ No credentials stored or transmitted |
| Unencrypted network | ✅ Only HTTPS (and HTTP) to user-specified URLs |

---

## ClawHub Security Audit Finding (2026-06-12)

### Finding: Silent Cache Persistence
**Severity:** Medium
**Source:** ClawHub automated security audit (https://clawhub.ai/jlacroix82/smart-scraper-web/security-audit)

**Issue:** The scraper stores fetched page content locally in `memory/scraper-cache/cache.json` without:
- User notice/consent before first write
- A documented opt-out mechanism
- Clear documentation of the privacy implications

**Impact:** Users scraping sensitive or private content may unknowingly leave page contents on disk.

**Fix Applied (2026-06-12):**
1. Added `--no-cache` CLI flag to disable local cache persistence
2. Added visible warning before first cache write: `⚠️ Caching page content to disk: <path>`
3. Warning includes guidance: `Use --no-cache to disable local persistence.`
3. Updated `SKILL.md` with privacy notice and usage example
5. Updated this `AUDIT.md` with finding and fix details

**Verification:**
- Run `node smart-scraper.js --extract --no-cache https://example.com` — no cache file created
- Run without `--no-cache` — warning shown on first write, cache file created

---

## ClawHub Automated Audit (2026-06-12)

### Finding: Persistent Cache Without Adequate User Notice
**Severity:** Medium
**Source:** ClawHub automated security audit (https://clawhub.ai/jlacroix82/smart-scraper-web/security-audit)

**Issue:** The skill stores extracted page data persistently in a local cache file without clear user notice or consent. The previous warning only fired once per process lifetime and was not explicit about what data types were stored.

**Fix Applied (2026-06-12):**
1. **Warning now fires on every cache write** (removed `cacheWarned` one-shot guard)
2. **Warning printed to stderr** (not stdout) with explicit list of stored data types
3. **SKILL.md updated** to explicitly list what data is cached: title, headings, paragraphs, links, tables, lists, prices, images, metadata
4. **`--no-cache` flag** remains available to disable persistence entirely

**Verification:**
- Run `node smart-scraper.js --extract https://example.com` — warning printed to stderr on every cache write
- Run `node smart-scraper.js --extract --no-cache https://example.com` — no cache file created, no warning

---

## ClawHub Security Audit — 2026-06-18 (v1.2.0 → v1.2.1)

**Source:** https://clawhub.ai/jlacroix82/smart-scraper-web/security-audit

### Finding 1: Cache Disabled by Default — Code/Doc Mismatch
**Severity:** Medium
**Outcome:** Review (not Pass)

**Issue:** The scraper defaulted to caching ON (`useCache = true`), but documentation, CLI help, and SKILL.md all claimed caching was "disabled by default" and "opt-in." This mismatch confused users about privacy behavior.

**Root Cause:** Line 40 had `let useCache = true;` — the default was never changed when the opt-in design was implemented.

**Fix Applied (v1.2.1):**
- Changed default to `let useCache = false;` — caching is now truly disabled by default
- Updated all console messages to reflect new default (`--cache to enable` instead of `--no-cache to disable`)
- Behavior with explicit flags unchanged: `--cache` enables, `--no-cache` explicitly disables

### Finding 2: SCRAPER_DIR Path Traversal Risk
**Severity:** Medium (76% confidence)
**Type:** Context-Inappropriate Capability (SkillSpector by NVIDIA)

**Issue:** The `SCRAPER_DIR` env var and `--dir` CLI flag allow redirecting cache write location. In multi-tenant or agent environments, an attacker could direct cache writes to sensitive workspace locations, risking data leakage or file planting.

**Fix Applied (v1.2.1):**
- Added validation in `WORKSPACE` resolution: blocks paths pointing to system roots (`/`, `/etc`, `/proc`, `/sys`, `/dev`, `/bin`, `/sbin`, `/boot`, `/lib`, `/usr`, `/var`, `/opt`)
- Dangerous `SCRAPER_DIR` values are silently ignored, falling back to the auto-detected workspace
- Non-dangerous custom paths still work for legitimate use cases

---

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 Critical | 2 | ✅ All resolved |
| 🟠 High | 3 | ✅ All resolved |
| 🟡 Medium | 5 | ✅ All resolved |
| 🟢 Low | 2 | Noted (no action required) |
| **Total** | **12** | **11 resolved, 2 noted** |

### Verification (v1.2.1)

| Test | Expected | Actual |
|------|----------|--------|
| Default (no flags) | No cache file created | ✅ Cache disabled by default |
| `--cache` flag | Cache file created | ✅ Cache enabled explicitly |
| `--no-cache` flag | No cache file created | ✅ Cache explicitly disabled |
| `SCRAPER_DIR=/etc` | Falls back to auto-detected workspace | ✅ Blocked system path |
| `SCRAPER_DIR=/home/user/custom` | Uses custom path | ✅ Legitimate custom path allowed |

No further remediation required at this time.
