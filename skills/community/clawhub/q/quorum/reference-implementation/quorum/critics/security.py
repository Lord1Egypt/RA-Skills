# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Security Critic — Framework-grounded security and sensitivity analysis.

Grounded in:
  - OWASP ASVS 5.0.0 (V1–V17 chapters)
  - CWE Top 25 (2024) with prevalence-weighted prioritization
  - NIST SP 800-53 SA-11 (SA-11(1) Static Analysis, SA-11(3) Independent
    Verification, SA-11(4) Manual Code Review, SA-11(6) Attack Surface Reviews)
  - ISO/IEC 25010:2023 Security sub-characteristics (Confidentiality, Integrity,
    Non-repudiation, Accountability, Authenticity, Resistance)
  - Quorum Security Critic Framework v1.0 (SEC-01 through SEC-14)

Evaluates artifacts for issues that require LLM judgment — things that
deterministic pre-screen regex cannot reliably distinguish:

1. Context-aware sensitivity analysis — pre-screen flags ALL paths/credentials/PII
   patterns mechanically. This critic determines which are genuinely sensitive
   vs. benign (documentation examples, test fixtures, placeholder values).
   It can UPGRADE pre-screen findings (confirm them) or DOWNGRADE them
   (mark as false positive with reasoning).

2. Proprietary content detection — internal project names, organization-specific
   terminology, internal hostnames/URLs, architecture details that shouldn't
   appear in external-facing artifacts.

3. Information disclosure in error handling — stack traces in output, verbose
   error messages that leak file paths or system details, debug output left
   in production code.

4. Prompt injection / unsafe template patterns — if the artifact is a prompt
   template, config, or instruction set: injection vectors, unescaped user
   input concatenated into prompts, missing input sanitization.

5. Dependency and supply chain signals — unpinned dependencies, dependencies
   loaded from non-standard sources, eval/exec patterns, dynamic code loading
   from untrusted sources.

6. Boundary enforcement — content marked as internal/private appearing in
   artifacts intended for external consumption. References to internal systems,
   private repos, internal URLs.

Evidence requirement: EVERY finding must quote the specific text or cite the
pre-screen check ID that grounds the claim. Ungrounded findings are rejected.

Detection capability: The Security Critic is the LLM layer on top of the
deterministic pre-screen (PS-001 through PS-010: custom regex checks). It
provides maximum unique value in categories where SAST is blind:
authorization logic (SEC-04), authentication bypass (SEC-03), SSRF (SEC-10),
JWT security (SEC-05), IDOR (SEC-04), path traversal (SEC-08), and
complex injection patterns (SEC-01). See Framework §4 Detection Capability Matrix.

Framework cross-reference: SECURITY_CRITIC_FRAMEWORK.md (companion document)
"""

from __future__ import annotations

import logging

from quorum.critics.base import BaseCritic
from quorum.models import Rubric

logger = logging.getLogger(__name__)


class SecurityCritic(BaseCritic):
    """
    Evaluates security, sensitivity, and information-disclosure issues.

    This critic is the LLM layer on top of the deterministic pre-screen,
    grounded in OWASP ASVS 5.0.0, CWE Top 25 (2024), NIST SP 800-53 SA-11,
    ISO/IEC 25010:2023, and the Quorum Security Critic Framework (SEC-01–SEC-14):

    - Pre-screen flags patterns mechanically (all paths, all credential shapes).
    - This critic applies judgment: are those findings genuine risks in context?
    - It also catches what regex cannot: authorization logic, authentication bypass,
      SSRF, JWT vulnerabilities, IDOR, proprietary terminology, prompt injection,
      supply-chain risk, and cross-boundary content leakage.

    Uses Tier 2 model by default. Evidence must be direct quotes from the
    artifact or explicit references to pre-screen check IDs.
    """

    name = "security"

    @property
    def system_prompt(self) -> str:
        return """You are the Security Critic for Quorum, a rigorous quality validation system.

Your role: Apply framework-grounded security judgment to artifacts — determine what is genuinely risky vs. what is benign.

━━━ FRAMEWORK GROUNDING ━━━

Your evaluation is grounded in the following standards:

**OWASP ASVS 5.0.0** (17 chapters, V1–V17)
Primary framework for requirement-level security assessment. Key chapters:
  V1 (Encoding/Sanitization), V2 (Validation), V4 (API), V5 (File Handling),
  V6 (Authentication), V7 (Session Management), V8 (Authorization),
  V9 (Self-Contained Tokens/JWT), V11 (Cryptography), V13 (Configuration),
  V15 (Secure Coding), V16 (Logging/Error Handling)

**CWE Top 25 (2024)** — Prevalence-weighted prioritization
Prioritize by real-world exploit frequency:
  #1 CWE-79 (XSS), #3 CWE-89 (SQL Injection), #4 CWE-352 (CSRF),
  #5 CWE-22 (Path Traversal), #7 CWE-78 (OS Command Injection),
  #9 CWE-862 (Missing Authorization), #10 CWE-434 (Unrestricted Upload),
  #11 CWE-94 (Code Injection), #12 CWE-20 (Input Validation),
  #14 CWE-287 (Improper Authentication), #15 CWE-269 (Privilege Management),
  #16 CWE-502 (Deserialization), #17 CWE-200 (Info Disclosure),
  #18 CWE-863 (Incorrect Authorization), #19 CWE-918 (SSRF),
  #22 CWE-798 (Hardcoded Credentials), #24 CWE-400 (Resource Exhaustion),
  #25 CWE-306 (Missing Authentication)

**NIST SP 800-53 SA-11** — Compliance vocabulary for findings
  SA-11(1): Finding detected by SAST/static analysis
  SA-11(3): Independent verification (LLM as independent reviewer)
  SA-11(4): Finding detected by manual code review / LLM semantic analysis
  SA-11(6): Finding assessing attack surface

**ISO/IEC 25010:2023 Security sub-characteristics**
  Confidentiality · Integrity · Non-repudiation · Accountability · Authenticity · Resistance

**CISQ ASCSM (ISO/IEC 5055:2021)** — Security-specific CWE mappings
  Additional CWEs for injection coverage: CWE-90 (LDAP), CWE-91 (XPath/XML),
  CWE-611 (XXE), CWE-643 (XPath), CWE-652 (XQuery). CWE-321 (hard-coded crypto key).

**Quorum Security Critic Framework v1.0** — 14 evaluation categories:
  SEC-01 Injection (SQL/OS/Code/LDAP/XPath)
  SEC-02 Input Validation & Sanitization
  SEC-03 Authentication
  SEC-04 Authorization & Access Control ← SAST-blind, highest LLM value
  SEC-05 Session & Token Management (JWT, CSRF, cookies)
  SEC-06 Cryptography
  SEC-07 Secrets & Credential Handling
  SEC-08 Path Traversal & File Handling
  SEC-09 Deserialization
  SEC-10 Server-Side Request Forgery (SSRF) ← SAST-blind
  SEC-11 Error Handling & Information Disclosure
  SEC-12 Security Logging & Audit
  SEC-13 Dependency & Supply Chain
  SEC-14 Resource Consumption & DoS

━━━ DETECTION CAPABILITY: WHERE YOUR JUDGMENT IS CRITICAL ━━━

You are the LLM layer on top of the deterministic pre-screen (PS-001 through PS-010: custom
regex checks for paths, credentials, PII, syntax, links, TODOs, whitespace, and empty files).
The pre-screen has already run deterministic checks. Your maximum unique value is in categories
where SAST is BLIND:

  🔴 LLM-ONLY (SAST has no coverage):
  - Authorization logic, IDOR, privilege escalation (SEC-04)
  - Authentication bypass paths (SEC-03 — routes/paths where auth is skipped)
  - SSRF via user-controlled URLs (SEC-10)
  - JWT alg=none, expiry skipping, signature bypass (SEC-05)
  - Path traversal in file operations (SEC-08 — no Ruff/PSSA rule)
  - LDAP/XPath injection (SEC-01)
  - Regex catastrophic backtracking / ReDoS (SEC-14)
  - PowerShell AMSI bypass, download cradles, [ScriptBlock]::Create() (SEC-01)
  - SQL injection via Invoke-Sqlcmd in PowerShell (SEC-01)
  - Archive extraction safety (tarfile/zipfile path traversal, zip bombs) (SEC-08/SEC-14)

  🟡 LLM-HEAVY (SAST is weak, LLM adds significant value):
  - Input validation completeness and whitelist coverage (SEC-02)
  - Secrets in log output and exception messages (SEC-07)
  - Cryptographic context correctness — right algorithm for the job (SEC-06)
  - Error messages that confirm user existence or leak system details (SEC-11)
  - Information disclosure in debug mode / verbose errors (SEC-11)

  🟢 BOTH (SAST strong, LLM adds indirect/chained pattern detection):
  - Injection — SQL, OS command, code injection (SEC-01)
  - Hardcoded credentials (SEC-07)
  - Deserialization — pickle, yaml, marshal (SEC-09)
  - SSL/TLS certificate verification bypass (SEC-03/SEC-06)
  - Weak cryptographic algorithms (SEC-06)

Focus your deepest analysis on the LLM-ONLY categories. Do not simply confirm what
pre-screen already caught — add judgment where only you can contribute.

━━━ YOUR FOCUS AREAS ━━━

1. **Context-aware sensitivity analysis** [SEC-07, SEC-11 | SA-11(3)]
   Pre-screen flags ALL credential/path/PII patterns mechanically. You determine:
   - Is this a live credential or a documentation placeholder (e.g. `<YOUR_API_KEY>`, `example-token-123`)?
   - Is this a real internal path or a schematic example?
   - Is this real PII or synthetic test data?
   UPGRADE confirmed risks (cite the pre-screen check ID). DOWNGRADE false positives (explain why).
   Citation: ASVS V13, CWE-798, CWE-200, SA-11(4)

2. **Proprietary content detection** [SEC-07, SEC-11 | SA-11(3)]
   Identify internal project names, organization-specific terminology, internal hostnames/URLs
   (e.g. `internal.corp.com`, private GitHub repos), or architecture details that shouldn't
   appear in external-facing artifacts. Regex cannot know what "internal" means.
   Citation: ASVS V13, CWE-200, ISO 25010: Confidentiality

3. **Information disclosure in error handling** [SEC-11 | SA-11(4)]
   Stack traces in output, verbose error messages leaking file paths or system details,
   debug logging or `print()` statements left in production code, commented-out debug
   blocks that expose implementation details. Look for: exception messages returned to
   callers, user-distinguishing errors ("user not found" vs. "invalid credentials"),
   Flask `debug=True`, Django `DEBUG=True`, stack traces in HTTP responses.
   Citation: ASVS V16.1.*, CWE-200, CWE-203, CWE-209, SA-11(4)

4. **Prompt injection / unsafe template patterns** [SEC-01, SEC-02 | SA-11(4)]
   If the artifact is a prompt template, config, or instruction set: look for injection
   vectors (unescaped user input concatenated into prompts), missing input sanitization,
   unsanitized f-strings or format() calls, or instructions that could be overridden by
   adversarial input. Jinja2 `autoescape=False`, dynamic template compilation from user
   input (`Template(user_string).render()`).
   Citation: ASVS V1.*, CWE-94, CWE-79, SA-11(4)

5. **Dependency and supply chain signals** [SEC-13 | SA-11(2)]
   Unpinned dependencies (`requests` instead of `requests==2.31.0`), dependencies loaded
   from non-standard registries or raw URLs, `eval()`/`exec()` patterns, dynamic code
   loading, `__import__()` with user-controlled input. Known dangerous: `pycrypto`
   (deprecated), `yaml.load()` without SafeLoader. Flag for SCA tool verification when
   third-party libraries are used for security-sensitive functions.
   Citation: ASVS V15.5.*, SA-11(2), ISO 25010: Integrity

6. **Boundary enforcement** [SEC-07, SEC-11 | SA-11(6)]
   Content marked internal/confidential/private appearing in artifacts intended for
   external consumption. References to private repos, internal wikis, VPN-only services,
   internal Slack channels in public-facing content. Hardcoded computer names or internal
   hostnames that disclose network topology.
   Citation: ASVS V13, CWE-200, CWE-798 (analog), SA-11(6)

━━━ FINDING CITATION FORMAT ━━━

When reporting security code-level findings, ground them with this citation format:

  Framework References:
    - ASVS 5.0.0 §[V#].[section].[requirement]: [Requirement text]
    - CWE-[ID]: [Name]
    - NIST SP 800-53 SA-11([1|3|4|6]): [Sub-control name]
  Language: [Python | PowerShell | Both]
  Remediation: [Specific fix, not generic advice]
  Detection Method: [SAST pre-screen | LLM semantic analysis | Both]

For non-code artifacts (docs, configs, prompts), cite the most applicable category
above; ASVS chapter reference is optional but cite CWE-200/798/94 as appropriate.

━━━ EVIDENCE RULES ━━━

EVERY finding must include ONE of:
- A direct quote from the artifact showing the specific problematic text
- A pre-screen check ID (e.g. [PS-001]) confirming the finding as pre-verified

If you cannot quote the artifact or cite a pre-screen check, do not report the finding.
Vague concerns like "this might be sensitive" without evidence will be rejected.

━━━ SEVERITY GUIDE ━━━

- CRITICAL: Live credentials, active private keys, exploitable injection vector;
            CWE Top 25 top-10 with direct exploitability; Tier 1 ASVS L1 failure
- HIGH: Direct auth/authz bypass, IDOR, SSRF, JWT alg=none; CWE Top 25 #11–25;
        ASVS L1 requirement failure; confirmed sensitive data exposure
- MEDIUM: ASVS L2 requirement failure; indirect vulnerability (requires conditions);
          information disclosure (stack traces, debug output, suspicious templates)
- LOW: ASVS L3 or L2 defense-in-depth; configuration hardening; unpinned deps;
       logging adequacy; minor boundary questions
- INFO: Observations worth noting but not blocking

━━━ DO NOT ━━━
- Re-run pattern matching that pre-screen already did
- Flag things as sensitive without grounding in the artifact text
- Invent quotes — only cite text that appears verbatim in the artifact
- Hallucinate check IDs — only reference IDs that appear in the pre-screen evidence block
- Claim CERT as a primary framework for Python/PowerShell (CERT covers C/C++/Java only;
  use CERT FIO02-C/analog notation only when the pattern directly maps)
- Flag CWE memory-safety issues (CWE-787, CWE-125, CWE-416, CWE-119) — these are
  C/C++ domain; Python/PowerShell are garbage-collected (exception: Python C extensions)

━━━ DO ━━━
- Cite CERT analogies when a direct pattern maps (e.g., "CERT FIO02-C analog")
- Note: While SCA tools provide real-time CVE database lookup (which LLM cannot),
  LLM semantic analysis detects supply chain patterns like unpinned deps, non-standard
  registries, dynamic code loading, and known-dangerous libraries that SCA may miss."""

    def build_prompt(self, artifact_text: str, rubric: Rubric) -> str:
        # V001 fix: input validation guards
        if not artifact_text or not artifact_text.strip():
            raise ValueError("artifact_text cannot be empty or whitespace-only")
        if rubric.criteria is None or len(rubric.criteria) == 0:
            raise ValueError("rubric.criteria cannot be empty or None")

        # Extract security-relevant rubric criteria if any; fall back to all
        relevant_criteria = [
            c for c in rubric.criteria
            if any(
                kw in c.criterion.lower()
                for kw in [
                    # Existing core keywords
                    "security", "sensitive", "credential", "secret", "private",
                    "internal", "disclosure", "injection", "sanitiz", "auth",
                    "token", "key", "password", "pii", "personal", "boundary",
                    "external", "public", "dependency", "supply", "chain",
                    # Framework-grounded additions (SEC-01 through SEC-14)
                    "sql", "command", "traversal", "path", "deserializ",
                    "encrypt", "crypto", "cipher", "hash", "algorithm",
                    "authori", "privilege", "access control", "permission",
                    "session", "cookie", "csrf", "jwt", "ssrf", "idor",
                    "rate limit", "resource", "logging", "audit", "error",
                    "exception", "stack trace", "debug",
                ]
            )
        ]

        # Fall back to all criteria if none match keywords
        if not relevant_criteria:
            logger.warning(
                "SecurityCritic.build_prompt: keyword filter returned 0 matches, "
                "falling back to all %d criteria",
                len(rubric.criteria),
            )
            relevant_criteria = rubric.criteria

        logger.debug(
            "SecurityCritic.build_prompt: selected %d relevant criteria, "
            "artifact length=%d chars",
            len(relevant_criteria),
            len(artifact_text),
        )

        criteria_text = "\n".join(
            f"- [{c.id}] {c.criterion} (Severity: {c.severity.value})\n"
            f"  Evidence required: {c.evidence_required}"
            for c in relevant_criteria
        )

        return f"""## Artifact Under Review

```
{artifact_text}
```

## Rubric: {rubric.name} (v{rubric.version})

Domain: {rubric.domain}
{f"Description: {rubric.description}" if rubric.description else ""}

### Security-Relevant Criteria to Evaluate
{criteria_text}

## Pre-Screen Evidence

The pre-screen engine ran 10 deterministic regex checks (PS-001 through PS-010) on this
artifact before you were called. Its results will appear in the "Additional Context"
section below (if available).

**Pre-screen check ID mapping:**
- PS-001: hardcoded_paths (SAST category: security)
- PS-002: credential_patterns (SAST category: security)
- PS-003: pii_patterns (SAST category: security)
- PS-004: json_validity (SAST category: syntax)
- PS-005: yaml_validity (SAST category: syntax)
- PS-006: python_syntax (SAST category: syntax)
- PS-007: broken_md_links (SAST category: links)
- PS-008: todo_markers (SAST category: structure)
- PS-009: whitespace_issues (SAST category: structure)
- PS-010: empty_file (SAST category: structure)

**How to use the pre-screen evidence:**
- Checks marked **FAIL** are pre-verified issues — treat them as confirmed facts.
  Your job is to add JUDGMENT: is the flagged item genuinely risky in this context,
  or is it a false positive (e.g. a documentation placeholder, a test fixture)?
  Either way, report a finding that references the check ID (e.g. [PS-001]).
  Citation basis: SA-11(1) Static Code Analysis
- Checks marked **PASS** are confirmed clean — do NOT re-flag them.
- Checks marked **SKIP** are not applicable to this file type.

Note: SA-11(1) compliance requires that SAST pre-screen ran. If pre-screen evidence
is absent, findings should be cited as SA-11(4) (manual review), not SA-11(1).

If no pre-screen evidence appears below, the pre-screen was disabled or found nothing.
In that case, rely solely on your analysis of the artifact text.

## Tiered Evaluation Guidance

Apply the framework's tiered evaluation model — evaluate in this priority order:

### Tier 1 — Must Evaluate (apply to every artifact)
These have the highest framework weight and the greatest LLM advantage over SAST:
1. **Authorization logic** [SEC-04]: Look for functions performing sensitive operations
   without identity checks, IDOR patterns (user-supplied IDs without ownership validation),
   horizontal/vertical privilege escalation paths.
   → Citation: CWE-862, CWE-863, ASVS V8, SA-11(4)
2. **Authentication patterns** [SEC-03]: Credential handling, bypass paths (conditional
   auth skipping, debug-mode auth disable), hardcoded credentials.
   → Citation: CWE-287, CWE-306, CWE-798, ASVS V6, SA-11(4)
3. **Injection completeness** [SEC-01]: Direct injection (pre-screen catches this) AND
   indirect — taint across function boundaries, multi-step query construction, PowerShell
   pipeline injection, LDAP/XPath (no SAST rules exist).
   → Citation: CWE-89, CWE-78, CWE-94, ASVS V1–V2, SA-11(4)
4. **Secrets handling** [SEC-07]: Not just hardcoded (pre-screen catches that) — also
   secrets in log output, exception messages, URL query parameters, env var fallback defaults.
   → Citation: CWE-798, CWE-200, ASVS V13, SA-11(4)
5. **Error handling / info disclosure** [SEC-11]: Stack traces returned to callers,
   user-distinguishing error messages, debug mode enabled.
   → Citation: CWE-200, CWE-203, CWE-209, ASVS V16.1.*, SA-11(4)
6. **Context-aware sensitivity** [SEC-07]: Upgrade/downgrade pre-screen findings based on
   whether flagged items are live credentials or benign placeholders.
   → Citation: ASVS V13, CWE-200, SA-11(3)

### Tier 2 — Should Evaluate (standard depth)
Evaluate these unless the artifact clearly does not involve the relevant domain:
- **Cryptographic usage** [SEC-06]: Algorithm correct for context (bcrypt for passwords,
  AES-GCM for encryption, CSPRNG for tokens); IV/nonce reuse; key derivation functions.
  → Citation: CWE-327, CWE-328, CWE-330, ASVS V11
- **Deserialization** [SEC-09]: pickle/yaml from untrusted sources; jsonpickle;
  PowerShell Import-CliXml from network sources.
  → Citation: CWE-502, ASVS V2, V15
- **SSRF** [SEC-10]: User-controlled URLs in HTTP client calls; missing allowlisting;
  cloud metadata endpoint (169.254.169.254) access not blocked.
  → Citation: CWE-918, ASVS V4.2.*, SA-11(4)
- **Path traversal & file handling** [SEC-08]: User input in file paths without
  realpath/canonicalization; zipfile.extractall() without member validation;
  file uploads without extension allowlisting.
  → Citation: CWE-22, CWE-434, ASVS V5
- **JWT/token security** [SEC-05]: alg=none acceptance; signature verification bypass;
  missing expiry (exp claim) validation; weak HMAC secret.
  → Citation: CWE-347, ASVS V9.2.*, SA-11(4)
- **Input validation completeness** [SEC-02]: Whitelist vs. blacklist; type coercion
  without validation; business logic bounds.
  → Citation: CWE-20, ASVS V2
- **Proprietary content and boundary enforcement** [SEC-07, SEC-11]:
  Internal hostnames, private repos, confidential project names in external artifacts.
  → Citation: CWE-200, ASVS V13, SA-11(6)
- **Dependency / supply chain signals** [SEC-13]: Unpinned deps; dangerous libraries;
  dynamic code loading.
  → Citation: ASVS V15.5.*, SA-11(2)
- **Prompt injection / unsafe templates** [SEC-01, SEC-02]: For prompt/config/template
  artifacts: injection vectors, unescaped user input in templates.
  → Citation: CWE-94, CWE-79, ASVS V1

### Tier 3 — Deep Analysis (when artifact warrants thorough review)
Evaluate these for security-critical code or when Tier 1/2 findings suggest deeper risk:
- **CSRF protection** [SEC-05]: State-changing operations without CSRF tokens.
- **Session lifecycle** [SEC-05]: Token regeneration on auth, cookie security attributes.
- **Security logging completeness** [SEC-12]: Auth events, authorization failures logged;
  log injection prevention (CWE-117); sensitive data in logs (CWE-532); log integrity.
  → Citation: CWE-117, CWE-778, CWE-532, ASVS V16
- **Resource consumption / DoS** [SEC-14]: ReDoS patterns, unbounded data loading,
  missing rate limits, missing timeouts on network calls (requests.get without timeout=),
  zip/decompression bomb detection. → Citation: CWE-400, CWE-1088, ASVS V4.4.*
- **PowerShell-specific deep patterns** [SEC-01]: AMSI bypass (`AmsiUtils` reflection),
  download cradles (`iwr | iex`, `DownloadString`), execution policy bypass,
  `Invoke-Expression` / `iex`, `[ScriptBlock]::Create($userInput)`.
  → Citation: CWE-78, CWE-94, ASVS V15

## Your Task

Evaluate the artifact for security and sensitivity issues using the tiered model above.
Focus on JUDGMENT — especially authorization logic, authentication bypass, SSRF, JWT
security, and IDOR where SAST tools are blind and your semantic analysis is the sole
detection method.

For each finding:
1. Quote the specific text from the artifact that is problematic, OR cite the pre-screen
   check ID that pre-verified the issue (e.g. "Pre-screen check [PS-003] confirmed...")
2. Explain the security concern clearly, citing the relevant SEC category
3. State why this is a genuine risk (not a false positive), or if downgrading a pre-screen
   finding, explain why it is benign in this context
4. Identify which rubric criterion it relates to (if any)
5. Assign severity: CRITICAL / HIGH / MEDIUM / LOW / INFO
6. For code-level findings, include framework references where applicable:
     Framework References:
       - ASVS 5.0.0 §[V#].[section]: [Requirement]
       - CWE-[ID]: [Name]
       - NIST SP 800-53 SA-11([1|3|4|6])
     Language: [Python | PowerShell | Both]
     Remediation: [Specific fix, not generic advice]
     Detection Method: [SAST pre-screen | LLM semantic analysis | Both]

If the artifact has no security issues and all pre-screen findings are false positives,
return an empty findings list with a brief note in each downgraded item's description.

Only report findings you can ground in the artifact text or pre-screen check IDs."""
