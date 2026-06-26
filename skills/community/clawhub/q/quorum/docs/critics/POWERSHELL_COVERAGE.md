# PowerShell Coverage — Honest Assessment

**Status:** v0.5.2  
**Last Updated:** March 2026

---

## Summary

Quorum's Security and Code Hygiene critics evaluate both Python and PowerShell code. **Python coverage is stronger (~85%+) due to a richer SAST ecosystem. PowerShell coverage is approximately 70%**, with known gaps documented below.

This document exists because we believe honest disclosure of coverage limitations is more valuable than pretending they don't exist. If you're using Quorum to evaluate PowerShell code, you should know exactly where the blind spots are.

---

## What Works Well

### PSScriptAnalyzer Integration (Deterministic Pre-Screen)

The following PSSA rules are integrated or planned for the pre-screen layer:

| Category | Rules | Status |
|----------|-------|--------|
| **Credential handling** | `PSAvoidUsingConvertToSecureStringWithPlainText`, `PSAvoidUsingUsernameAndPasswordParams`, `PSAvoidUsingPlainTextForPassword`, `PSUsePSCredentialType` | ✅ LLM-evaluated |
| **Injection** | `PSAvoidUsingInvokeExpression` | ✅ LLM-evaluated |
| **Crypto** | `PSAvoidUsingBrokenHashAlgorithms` | ✅ LLM-evaluated |
| **Error handling** | `PSAvoidUsingEmptyCatchBlock` | ✅ LLM-evaluated |
| **Network security** | `PSAvoidUsingAllowUnencryptedAuthentication` | ✅ LLM-evaluated |
| **Infrastructure** | `PSAvoidUsingComputerNameHardcoded` | ✅ LLM-evaluated |

These rules provide solid coverage for the most common PowerShell security anti-patterns.

### LLM Semantic Analysis

The Security Critic's LLM judgment checks work equally well on PowerShell and Python for:

- Authorization logic review (SEC-04)
- Business logic validation (SEC-02)  
- Certificate validation bypass patterns
- Download cradle detection (`iwr | iex`, `DownloadString`)
- AMSI bypass pattern recognition
- Registry persistence detection
- `[ScriptBlock]::Create()` with user-controlled input
- Path traversal in `Get-Content`/`Set-Content`

---

## Known Gaps

### No PSSA Rules Exist For:

| Gap | Security Impact | Workaround |
|-----|----------------|------------|
| **SQL injection via `Invoke-Sqlcmd`** | T1 — High | LLM detection only; no deterministic pre-screen |
| **Path traversal** | T2 — Medium | LLM detection only |
| **SSRF via `Invoke-WebRequest`** | T2 — Medium | LLM detection only |
| **Deserialization (`Import-CliXml`, `ConvertFrom-Json` type hydration)** | T3 — Low-Medium | LLM detection only |
| **Session management** | T2 — Medium | LLM detection only |
| **DoS / resource consumption** | T3 — Low | LLM detection only |
| **Missing `-ErrorAction Stop` in try/catch** | T2 — Medium | LLM detection only |
| **`-TimeoutSec` on web requests** | T1 — Medium | LLM detection only |

### Ecosystem Gap: Why PowerShell Lags

PSScriptAnalyzer is the only mainstream PowerShell SAST tool. It has ~60 rules focused primarily on style and best practices, with limited security coverage. By comparison, Python has:

- **Ruff:** 80+ security rules (Bandit-derived `S*` series)
- **Bandit:** Dedicated Python security linter
- **Semgrep/CodeQL:** Deep taint analysis with Python support

PowerShell has no equivalent to Bandit, and PSScriptAnalyzer's security rules are mostly credential-focused. This is a tooling ecosystem gap, not a Quorum limitation — but it means PowerShell security evaluation leans more heavily on LLM judgment than deterministic checks.

### What This Means in Practice

For **Python** code: ~60% of findings come from deterministic pre-screen (SAST), ~40% from LLM judgment.  
For **PowerShell** code: ~25% of findings come from deterministic checks (PSSA), ~75% from LLM judgment.

LLM-only findings are still grounded in framework citations (OWASP ASVS, CWE, SA-11) and require evidence. They are not less valid — but they lack the reproducibility guarantee of deterministic checks. Two runs of the same PowerShell file may surface different LLM findings, while SAST findings are identical every time.

---

## Improvement Roadmap

1. **Microsoft DevSkim integration** — MIT-licensed, CLI-invokable (`devskim analyze`), SARIF/JSON output. Adds ~15 cross-language security patterns (dangerous functions, hardcoded URLs, credential patterns). Complementary to PSSA, low integration effort.
2. **Custom PSScriptAnalyzer rules** — Write ~10-15 custom PSSA rules for the highest-impact gaps (SQL injection via `Invoke-Sqlcmd`, path traversal in `Get-Content`, `Start-Process` with unsanitized input). PSSA supports custom rules in PowerShell or compiled C# — this is the highest-leverage improvement.
3. **Pre-screen expansion** — Add regex-based deterministic checks for PowerShell patterns that don't need full PSSA (e.g., `Invoke-Sqlcmd` + string concatenation)
4. **Community contribution** — Contribute security rules upstream to PSScriptAnalyzer

**Not on the horizon:** Semgrep and CodeQL have both confirmed PowerShell is not on their roadmaps (as of early 2026). No maintained community security rule packs for PSSA exist. The gap is structural — no major SAST engine has built a PowerShell AST parser outside of PSSA's .NET implementation.

---

## Recommendation

If you're evaluating **security-critical PowerShell** code with Quorum:

1. Run at **standard** or **thorough** depth — quick depth may miss LLM-only findings
2. Cross-reference findings with a manual review for SEC-04 (authorization) and SEC-01 (injection) — the two categories with the highest LLM-only dependency
3. Consider supplementing with ScriptAnalyzer custom rules for your specific environment
4. Treat the PowerShell assessment as a strong starting point, not a complete audit

---

> ⚖️ **LICENSE** — This file is part of [Quorum](https://github.com/SharedIntellect/quorum).  
> Copyright 2026 SharedIntellect. MIT License.  
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
