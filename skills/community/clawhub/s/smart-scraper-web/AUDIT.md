# Smart Scraper — Security Audit

**Date:** 2026-06-09  
**Auditor:** Jarvis (automated audit)  
**Files:** `smart-scraper.js` (~15KB), `SKILL.md` (~5KB), `manifest.json` (~1KB)

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
| 🟡 Silent cache persistence | `--no-cache` flag + visible warning before caching | ✅ FIXED |
| 🟡 Manifest missing capabilities | `manifest.json` declares network, cache, file I/O permissions | ✅ FIXED |

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
| **Total** | **12** | **10 fixed, 2 low-risk noted** |

---

## Findings (All Resolved)

> All critical and high findings below were present in the initial audit and have been **fully remediated**. The original issue descriptions are retained for reference.

### 🔴 CRITICAL (All Resolved)

#### 1. SSRF — No URL Validation Before Fetch ✅ FIXED
**Severity:** Critical (resolved)  
**Location:** `fetchPage()`  
**Original Issue:** The URL from `--extract <url>` was passed directly to `http.get()` / `https.get()` with no validation. Any URL scheme was accepted — `file://`, `http://localhost`, `https://169.254.169.254` (AWS metadata), `gopher://`, etc.

**Original Impact:** An agent or user could fetch internal services, cloud metadata endpoints, or local files via `file://` URLs.

**Remediation:** URL validation added — blocks `file://`, `gopher://`, `data:`, `javascript://`, `ftp://`, localhost, private IPs, and cloud metadata (169.254.169.254). Only http/https schemes allowed.

---

#### 2. SSRF — Redirect Following Has No Loop Limit ✅ FIXED
**Severity:** Critical (resolved)  
**Location:** `fetchPage()`  
**Original Issue:** Redirects were followed recursively with no maximum depth. A malicious URL that returns a redirect loop or a very long redirect chain could cause infinite recursion → stack overflow → DoS.

**Original Impact:** Denial of service via redirect loop. Also enabled SSRF by redirecting to an internal IP after an initial external redirect.

**Remediation:** `MAX_REDIRECTS = 5` added with redirect count tracking. Redirects to private/internal IP ranges are rejected.

---

### 🟠 HIGH (All Resolved)

#### 3. Regex ReDoS — `<[^>]+>` Pattern ✅ FIXED
**Severity:** High (resolved)  
**Location:** `stripHtml()`  
**Original Issue:** The pattern `<[^>]+>` was a classic ReDoS vector. While V8's regex engine handles it well in practice, it was a documented vulnerability class.

**Original Impact:** Theoretical DoS with crafted HTML input.

**Remediation:** Replaced with bounded pattern: `/<[^>]{0,1024}>/g`

---

#### 4. Regex ReDoS — `<table[\s\S]*?</table>` ✅ FIXED
**Severity:** High (resolved)  
**Location:** `parseHtml()`  
**Original Issue:** `<table[\s\S]*?</table>` used non-greedy cross-line matching on unbounded input.

**Original Impact:** CPU exhaustion on pages with unclosed `<table>` tags in large documents.

**Remediation:** Bounded to `{0,500000}`: `<table[\s\S]{0,500000}?</table>`

---

#### 5. Cache Grows Indefinitely — No Eviction ✅ FIXED
**Severity:** High (resolved)  
**Location:** `extractFromUrl()`  
**Original Issue:** Cache entries were written to `cache.json` but never evicted.

**Original Impact:** Disk space exhaustion over time. Cache became slower as it grew.

**Remediation:** LRU eviction implemented: max 50 entries / 10MB with TTL cleanup.

---

### 🟡 MEDIUM (All Resolved)

#### 6. No Rate Limiting / Request Throttling ✅ FIXED
**Severity:** Medium (resolved)  
**Location:** `fetchPage()`  
**Original Issue:** No rate limiting between requests.

**Original Impact:** IP blocking, abuse detection, wasted bandwidth.

**Remediation:** 100ms minimum delay between requests added.

---

#### 7. User-Agent Spoofing ✅ FIXED
**Severity:** Medium (resolved)  
**Location:** `fetchPage()`  
**Original Issue:** Used a fake User-Agent which was easily detectable.

**Original Impact:** IP blocking, ToS violation.

**Remediation:** Changed to realistic User-Agent: `Mozilla/5.0 (compatible; SmartScraper/1.0)`

---

#### 8. No Timeout on Redirect Resolution ✅ FIXED
**Severity:** Medium (resolved)  
**Location:** `fetchPage()`  
**Original Issue:** The redirect `fetchPage()` call inherited no timeout.

**Original Impact:** Resource exhaustion, stuck requests.

**Remediation:** Timeout inherited on each redirect hop.

---

#### 9. Silent Cache Persistence (Data Exfiltration) ✅ FIXED
**Severity:** Medium (resolved)  
**Location:** `extractFromUrl()`  
**Original Issue:** Scraper silently stored parsed content on disk without disclosure or consent.

**Original Impact:** Cached files may contain sensitive page content, URLs, or metadata.

**Remediation:**
- `--no-cache` flag for privacy mode (no local storage)
- Visible warning before caching: `⚠️ Caching page content to disk`
- Cache documented in SKILL.md with privacy implications
- Cache is opt-in via `--no-cache` for sensitive material

---

#### 10. Manifest Missing Capability Declarations ✅ FIXED
**Severity:** Medium (resolved)  
**Location:** Skill manifest  
**Original Issue:** No manifest.json declaring network access and caching permissions.

**Original Impact:** Agents could not determine what permissions the skill requires before using it.

**Remediation:** Created `manifest.json` with declared capabilities:
- Network: outbound http/https with SSRF protection
- Cache: location, limits, opt-out flag
- File I/O: read/write paths
- Security: validation settings

---

### 🟢 LOW (Noted — Not Critical)

#### 11. JSON Parse — No Size Limit
**Severity:** Low  
**Location:** `loadJSON()`  
**Issue:** `JSON.parse()` has no size limit.

**Impact:** Minimal — the try/catch provides protection.

**Status:** Noted as low-risk. Fix (max file size check before parsing) deferred.

---

#### 12. stripHtml Does Not Handle All HTML Entities
**Severity:** Low  
**Location:** `stripHtml()`  
**Issue:** `stripHtml()` removes script/style tags and strips remaining HTML tags, but does not decode HTML entities.

**Impact:** Minor — extracted text may have entity codes instead of readable characters.

**Status:** Noted as low-risk. Fix (HTML entity decoding) deferred.

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
| SSRF bypass | ✅ URL validation + redirect re-validation |
| Redirect loops | ✅ Max 5 redirects with validation |

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 High | 0 |
| 🟡 Medium | 0 |
| 🟢 Low | 2 |
| **Total** | **12** |

### Current State

**All findings have been resolved.**

All critical, high, and medium-severity findings were previously addressed. Low-severity findings (HTML entity decoding, JSON size limit) were fixed on 2026-06-18:

- **JSON parse size limit** — Added `fs.statSync()` size check before `JSON.parse()`, rejecting files over 10MB with a warning
- **HTML entity decoding** — Added `decodeHtmlEntities()` handling named, numeric, and hex entities, applied in `stripHtml()`
- **Image regex bug** — Fixed stray `\?` in img regex that prevented all image extraction
- **Missing `--cache` flag** — Added explicit `--cache` CLI flag for consistency with documented API

## New ClawHub Findings (2026-06-18, v1.2.0 → v1.2.1)

### #11 — Cache Default Mismatch (Medium)
**Issue:** Code defaulted to `useCache = true` while docs said "disabled by default."
**Fix:** Changed to `useCache = false` — caching is now truly opt-in.

### #12 — SCRAPER_DIR Path Traversal (Medium)
**Issue:** `--dir` / `SCRAPER_DIR` allowed writing cache to arbitrary locations.
**Fix:** Added validation blocking dangerous system roots (`/`, `/etc`, `/proc`, etc.).

Both findings resolved in v1.2.1.
