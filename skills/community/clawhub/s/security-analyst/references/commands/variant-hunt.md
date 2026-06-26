---
description: "Hunt variants of a known vulnerability across the codebase using git history mining and pattern analysis."
model: opus
---

# Security Analyst — Variant Hunt

Given a known vulnerability, recent fix, or security pattern, find all unpatched variants across the codebase.

## Usage

Invoke with the target vulnerability: `/security-analyst:variant-hunt [vulnerability description or commit hash]`

If no target is specified, ask: "What vulnerability or fix should I hunt variants for? Provide one of:
- A commit hash (e.g., `6dc9bb7`)
- A vulnerability type (e.g., 'OData injection', 'auth bypass', 'SSRF')
- A CVE ID (e.g., 'CVE-2024-XXXX')
- A description (e.g., 'the MIME header injection fix in the message composer', 'the SQL injection fix in the search endpoint')"

## Execution

1. **Phase 0**: Run reconnaissance to map the full codebase
2. **Understand the original**:
   - If commit hash: `git show {hash}` to understand what was fixed
   - If vulnerability type: search git history and recon step files for related patterns
   - If CVE: look up the CVE details and find the affected code
3. **Determine the PATTERN**: What was the root cause? What's the code pattern that was vulnerable?
4. **Select relevant Phase 2 agents** based on the vulnerability type:

| Vulnerability Type | Agents |
|-------------------|--------|
| Injection (SQL, OData, MIME, query, prompt) | history-injections, logic-pipeline |
| Auth bypass (nonce, session, CSRF, token) | history-auth-bypass, logic-authz, logic-races |
| SSRF / open redirect | history-ssrf |
| Data exposure / info leak | history-data-exposure |
| Race condition / TOCTOU | logic-races, history-auth-bypass |

5. **Customize agent prompts**: Add the specific vulnerability context to the agent prompt:
   - "The original fix was [description]. Hunt for similar patterns that weren't fixed."
   - "The vulnerable pattern is [code pattern]. Find all instances."
6. **Run selected agents**
7. **Cross-reference with recon**: Use the recon step files to find ALL locations where the vulnerable pattern could exist
8. **Present variant findings** with references to the original fix

## Output

- `{RUN_DIR}/recon/` — Recon index + atomic step files
- Variant findings presented inline with references to the original vulnerability

## Why Variant Hunting?

Past security fixes are the #1 source of new vulnerabilities:
- A fix for OData injection doesn't mean similar query injection in other API clients was fixed
- A fix in one auth callback doesn't mean the other callbacks were updated
- A fix for one SSRF vector doesn't mean all HTTP clients use the safe wrapper
- A fix for one error handler doesn't mean all error handlers were updated

Variant hunting systematically checks that every fix was applied comprehensively.
