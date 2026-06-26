# Audit Report: sonos-music-search-skill

**Date:** 2026-05-07  
**Version:** 1.0.0  
**Auditor:** Automated + Manual Review

---

## Summary

The skill combines Brave Search with Sonos speaker control to search for and play music via CLI. The concept is sound, but the implementation has **critical issues** that must be resolved before publishing — most notably a non-existent npm dependency, missing error handling, and security concerns.

**Overall Risk Level:** 🔴 HIGH — Do not publish until Critical items are resolved.

---

## Findings

### 🔴 Critical

| # | Category | Finding | Remediation |
| --- | --- | --- | --- |
| C1 | DX / Build | `@brave/search-api@^1.2.0` does not exist in the npm registry. `npm install` fails entirely. Skill cannot be installed or run. | Replace with the correct Brave Search SDK package (e.g. use the official Brave Search REST API via `node-fetch`/`axios`, or verify the correct npm package name from [Brave's developer docs](https://brave.com/search/api/)). |
| C2 | Security | `BRAVE_API_KEY` is checked at module top-level with `throw`, which crashes the entire process on import — even if the importing code doesn't need search. Also, no input sanitization on `query` parameter passed to external API. | Move key validation into the function that needs it. Sanitize user input before passing to API calls. Consider using a config file or secret manager instead of raw env vars. |
| C3 | Security | `safesearch: 'off'` is hardcoded. This can return explicit content without any user opt-in or warning. | Default to `safesearch: 'moderate'` or make it configurable. |

### 🟠 High

| # | Category | Finding | Remediation |
| --- | --- | --- | --- |
| H1 | Reliability | `Sonos.DeviceDiscovery()` is called on every invocation with no timeout or caching. Network discovery can hang indefinitely on some networks. | Add a discovery timeout (e.g. 5s) and cache discovered devices. Consider allowing direct IP configuration as fallback. |
| H2 | Reliability | Spotify URI extraction is fragile — uses a simple `replace()` on the URL. If the URL format changes or contains query parameters (`?si=...`), the URI will be malformed. | Use a proper URL parser to extract the track ID, then construct `spotify:track:<id>`. Strip query parameters. |
| H3 | UX | Only the first search result is used. If it's not the intended track, the user has no way to choose. | Return top N results and let the user pick, or at minimum show what was matched before playing. |
| H4 | Edge Case | No handling for: Sonos speaker not on same network, Spotify not linked to Sonos account, track unavailable in user's region, device discovery returning multiple speakers with same name. | Add specific error messages and graceful degradation for each case. |

### 🟡 Medium

| # | Category | Finding | Remediation |
| --- | --- | --- | --- |
| M1 | Performance | `DeviceDiscovery()` is called separately in `searchAndPlay()` and `getCurrentTrack()`. No device caching means redundant network broadcasts. | Cache device list with TTL. |
| M2 | DX | `package.json` has empty `author` field. ClawHub listing will show no author. | Fill in author information. |
| M3 | DX | No `SKILL.md` file — this is required for ClawHub skills. The skill won't be recognized by the OpenClaw skill system. | Create a proper `SKILL.md` with frontmatter (name, description, metadata) and usage docs. |
| M4 | Code Quality | No tests. Zero test coverage for a skill that controls physical hardware. | Add at minimum: unit tests for URI extraction logic, integration test stubs for API calls, mock-based tests for error paths. |
| M5 | Security | No rate limiting on Brave Search API calls. A runaway script or malicious input could exhaust API quota quickly. | Add basic throttling or warn about quota usage. |

### 🔵 Low

| # | Category | Finding | Remediation |
| --- | --- | --- | --- |
| L1 | Style | Inconsistent error handling: `throw` at module level vs `try/catch` in CLI. | Standardize error handling pattern. |
| L2 | DX | README says "Zero configuration required (just set your Brave API key)" — but Sonos also requires being on the same network and having Spotify linked. | Update README to list all prerequisites honestly. |
| L3 | Compatibility | No `engines` field in `package.json`. Unclear which Node.js versions are supported. | Add `"engines": { "node": ">=18" }` or similar. |
| L4 | Code Quality | Magic string `'off'` for safesearch and `'spotify.com/track'` for site filter should be constants. | Extract to named constants at top of file. |

---

## Action Items (Priority Order)

1. **Fix the dependency** — Replace `@brave/search-api` with a working HTTP client approach or the correct package name.
2. **Add `SKILL.md`** — Required for ClawHub skill registration.
3. **Fix Spotify URI parsing** — Use URL parser instead of string replace.
4. **Change `safesearch` default** — Set to `'moderate'`.
5. **Add discovery timeout** — Prevent indefinite hangs.
6. **Fill `author` field** in `package.json`.
7. **Improve README** — List all prerequisites accurately.
8. **Add basic tests** — At minimum for URI extraction.

---

_Report generated 2026-05-07. Resolve all 🔴 Critical items before publishing._
