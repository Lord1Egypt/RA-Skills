# Rubric Building Guide

*How to encode a standard into something Quorum can actually run.*

---

## 1. Overview

A rubric is a machine-readable encoding of what "good" looks like. It's not a vague checklist — it's a set of testable criteria, each with a clear assertion, a severity level, assessment guidance, and evidence requirements. When Quorum runs a rubric, critics evaluate an artifact against each criterion and must cite evidence. No evidence, no finding.

The distinction that matters: a rubric turns a compliance question from *"does this seem right?"* into *"can you prove it meets criterion X from standard Y?"* That's substantiation. It's the difference between a vibe check and a defensible finding.

Building a rubric is fundamentally a knowledge-encoding problem. You take a standard — a published specification, an industry framework, a regulatory requirement — and systematically extract its requirements into a form Quorum's critics can evaluate. This guide walks through that process, using OWASP ASVS (Application Security Verification Standard) as worked examples throughout.

**The payoff is compounding.** A good rubric runs indefinitely. You build it once; every subsequent evaluation is essentially free expertise.

---

## 2. Prerequisites

Before you start, you need:

1. **The source document in parseable format.** PDFs with embedded text work fine; scanned PDFs need OCR. See Step 1.
2. **Domain knowledge.** This is non-negotiable. Standards are dense, and normative decomposition without domain knowledge produces rubrics that are technically correct and practically useless. The criteria generation step (Step 3) is where expertise matters most.
3. **A clear scope boundary.** Full standards are large. Decide upfront which sections or requirement types you're encoding. Scope creep kills rubric projects.
4. **The Quorum rubric schema.** See [CONFIG_REFERENCE.md](../configuration/CONFIG_REFERENCE.md) for the full spec. A rubric is a JSON file; critics consume it at evaluation time.

---

## 3. Step 1: Source Acquisition

Getting the standard into clean markdown is the foundation. Everything downstream depends on text quality.

### Tools

| Situation | Tool | Notes |
|-----------|------|-------|
| Clean, text-based PDF | **PyMuPDF** (`fitz`) | Fast, accurate, preserves structure |
| Scanned or OCR-heavy PDF | **Marker** | Higher quality output, slower |
| Already HTML | Direct fetch | OWASP docs, IETF RFCs, many NIST publications |
| DOCX/XLSX | **python-docx** / **openpyxl** | Straightforward |

### Examples

**For OWASP ASVS:** Available as markdown directly from GitHub — no PDF processing needed:

```bash
git clone https://github.com/OWASP/ASVS.git
# Requirements are in structured markdown tables under each chapter
```

**For NIST publications:** PDFs from `csrc.nist.gov`. Most have embedded text — PyMuPDF works:

```python
import fitz  # PyMuPDF
doc = fitz.open("sp800-53r5.pdf")
text = "\n".join(page.get_text() for page in doc)
```

**For IETF RFCs:** Fetch directly — clean plaintext or HTML available at `https://www.rfc-editor.org/rfc/rfcNNNN.txt`.

**For ISO standards:** Purchase required. If you have access, export to PDF and process with PyMuPDF or Marker.

### Quality Check

Before proceeding, verify:
- Section numbers are preserved (you'll need them for citations)
- Tables rendered correctly (many requirements live in tables)
- No garbled characters from encoding issues

Invest time here. Garbage in, garbage rubric out.

---

## 4. Step 2: Normative Decomposition

This is the systematic extraction of testable requirements from the source text.

### What You're Looking For

Standards use normative language to distinguish requirements from background text. Per RFC 2119:

| Keyword | Strength | Rubric Category |
|---------|----------|-----------------|
| SHALL / MUST | Mandatory | **CRITICAL** |
| SHALL NOT / MUST NOT | Prohibited | **CRITICAL** |
| SHOULD / RECOMMENDED | Advisory | **HIGH** |
| SHOULD NOT / NOT RECOMMENDED | Advisory prohibition | **HIGH** |
| MAY / OPTIONAL | Permissive | **MEDIUM** |
| Informational / best practice | Non-normative | **LOW** |

Category mapping is deterministic from normative strength. This isn't a judgment call — it's a mechanical mapping. The domain judgment comes in Step 3 when you define what evidence satisfies the criterion.

### Decomposition Process

For each normative statement you find:

1. **Record the section reference** — e.g., `ASVS V2.1.1`
2. **Extract the full statement** — verbatim, not paraphrased
3. **Identify the subject** — what entity does this apply to? (application, API, service, developer, etc.)
4. **Tag normative strength** — SHALL/SHOULD/MAY (or ASVS levels: L1/L2/L3)
5. **Flag compound statements** — "The application SHALL do X AND Y AND Z" → three separate criteria

Compound requirements are the most common mistake. A single sentence can contain multiple independent testable assertions. Decompose them. Assessment against a compound assertion is ambiguous; assessment against three atomic assertions is precise.

### OWASP ASVS Note

ASVS uses a three-level verification model (L1/L2/L3) rather than RFC 2119 normative language. Map levels to severity:
- **L1** (Opportunistic) → `HIGH` — minimum baseline, every application should meet these
- **L2** (Standard) → `CRITICAL` — standard applications handling sensitive data
- **L3** (Advanced) → `CRITICAL` — high-value applications (medical, military, critical infrastructure)

Each requirement also has a unique ID (e.g., V2.1.1) with structured chapters, making decomposition straightforward.

### Output Format

Produce a working document (markdown table or spreadsheet) with columns:

| Section | Statement (verbatim) | Subject | Level | Notes |
|---------|---------------------|---------|-------|-------|
| V2.1.1 | Verify that user set passwords are at least 12 characters in length | Application | L1 | Compound — also implies password field accepts 12+ chars |

Don't try to generate rubric JSON yet. This intermediate format lets you review and refine before committing to structure.

---

## 5. Step 3: Criteria Generation

This is where the rubric comes alive — and where domain expertise is irreplaceable.

Each normative statement from Step 2 becomes a rubric criterion. A criterion has:

- **`id`** — unique identifier, e.g., `asvs.v2.1.1`
- **`category`** — severity tier: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` (from Step 2 mapping)
- **`criterion`** — the testable claim (what must be true)
- **`evidence_type`** — how to gather evidence: `tool` (grep, file read), `web_search`, `manual`
- **`evidence_instruction`** — specific directions for what the critic should look for and how
- **`rationale`** — *why* this criterion matters; what risk does a failure represent?

The **evidence instruction** is where expertise earns its keep. "The application SHALL enforce minimum password length" is the normative statement. But what does enforcement look like in evidence? Is a frontend validation sufficient? Does it need server-side enforcement too? What about API endpoints — do they share the same validation? Someone who doesn't understand application security will write vague guidance. Someone who does knows to check both client and server, and to look for password policy configuration rather than trusting UI-only checks.

### Example: ASVS V2.1 — Password Security

Normative statement: *"Verify that user set passwords are at least 12 characters in length (after combining spaces)."* (V2.1.1, L1)

```json
{
  "id": "asvs.v2.1.1",
  "category": "HIGH",
  "criterion": "The application enforces a minimum password length of 12 characters for user-set passwords.",
  "evidence_type": "tool",
  "evidence_instruction": "Search the codebase for password validation logic — look for length checks in authentication modules, user registration handlers, and password change flows. Check for: (1) server-side validation (client-side only is insufficient), (2) the minimum is at least 12 characters (not 8 — ASVS updated from NIST SP 800-63B), (3) spaces are allowed and counted toward length, (4) configuration-driven thresholds are set to ≥12. Check password policy configuration files if validation is externalized (e.g., identity provider settings).",
  "rationale": "Short passwords are trivially brute-forced. The 12-character minimum aligns with NIST SP 800-63B and provides meaningful resistance against offline attacks. Allowing spaces encourages passphrases, which are both more secure and more memorable."
}
```

### Practical Notes

- **Start with L1 requirements.** These define the minimum floor. Get those right first.
- **Evidence instruction is the hard part.** Budget most of your domain expertise time here.
- **Evidence instructions should be concrete.** "Check for password validation" is too vague. "Search authentication modules for length checks" is better. "Grep for password policy configuration showing minimum_length ≥ 12" is best.
- **Avoid circular criteria.** "The application shall comply with OWASP guidelines" isn't testable — it's a reference to itself. Decompose the actual requirement.

---

## 6. Step 4: Concordance Mapping (Optional but Powerful)

Concordance mapping cross-references terms and requirements across related standards. It's optional for a working rubric — but it turns a rubric into an intelligence layer.

### What It Adds

Single-standard rubrics answer: *"Does this meet OWASP ASVS V2?"*

Multi-standard concordance answers: *"This requirement in ASVS V2 maps to this control in NIST SP 800-53, which is assessed differently in SOC 2 — here's the gap."*

That's a qualitatively different output. It surfaces alignment, gaps, and conflicts across the standards landscape automatically.

### Process

1. **Identify related standards.** For application security: OWASP ASVS ↔ NIST SP 800-53 ↔ SOC 2 ↔ ISO 27001 ↔ PCI DSS.
2. **Extract vocabulary.** Key terms from each standard. "Authentication," "identity verification," "credential management" may refer to the same concept across standards — or subtly different ones.
3. **Map requirements to requirements.** Which criterion in Standard A corresponds to which in Standard B? One-to-one, one-to-many, or gap (no counterpart)?
4. **Document the mapping.** Add `concordance` metadata to each criterion:

```json
{
  "id": "asvs.v2.1.1",
  "concordance": {
    "nist_sp800_53": "IA-5(1)(h)",
    "soc2": "CC6.1",
    "pci_dss": "Req 8.3.6",
    "alignment": "aligned",
    "notes": "NIST 800-53 defers to 800-63B for specifics; PCI DSS 4.0 now requires 12 chars, aligning with ASVS"
  }
}
```

### Timeline Impact

Concordance adds 1-2 days to a single-standard rubric build. The payoff: future rubrics for related standards build on existing mappings rather than starting from scratch. The first concordance-mapped rubric in a domain is expensive; subsequent ones are incremental.

---

## 7. Step 5: Packaging

Structure your criteria as a Quorum rubric configuration.

### Rubric File Structure

```json
{
  "id": "owasp-asvs-v2-auth",
  "name": "OWASP ASVS V2 — Authentication",
  "version": "1.0.0",
  "source": {
    "standard": "OWASP ASVS 4.0.3",
    "title": "Application Security Verification Standard — Chapter V2: Authentication",
    "url": "https://github.com/OWASP/ASVS",
    "pinned_version": "4.0.3"
  },
  "scope": "Evaluates application authentication implementations against OWASP ASVS V2 requirements.",
  "critics": ["correctness", "completeness"],
  "grading": {
    "pass_threshold": 0.85,
    "critical_tolerance": 0,
    "high_tolerance": 2
  },
  "criteria": [
    {
      "id": "asvs.v2.1.1",
      "category": "HIGH",
      "criterion": "The application enforces a minimum password length of 12 characters for user-set passwords.",
      "evidence_type": "tool",
      "evidence_instruction": "Search authentication modules for password length validation...",
      "rationale": "Short passwords are trivially brute-forced..."
    }
  ]
}
```

### Key Packaging Decisions

**Which critics?** Match critics to what the rubric is evaluating:
- `correctness` — always include; verifies claims are accurate
- `completeness` — always include; checks coverage
- Security and Code Hygiene critics are shipped. Architecture, Delegation, and Style are on the roadmap — see SPEC.md for the full 9-agent design.

**Grading thresholds:**
- `critical_tolerance: 0` means any CRITICAL failure → REJECT verdict. Appropriate for compliance rubrics.
- `pass_threshold: 0.85` means 85% of criteria must pass for a PASS verdict.

**Evidence requirements format:** Be specific. Critics use these to know what to look for in the artifact.

---

## 8. Worked Example: OWASP ASVS V2.1 — Password Security Requirements

This walks through all five steps for a concrete slice of OWASP ASVS.

### Source Text (Step 1)

From OWASP ASVS 4.0.3, Chapter V2.1 — Password Security:

> | # | Description | L1 | L2 | L3 |
> |---|-------------|----|----|-----|
> | V2.1.1 | Verify that user set passwords are at least 12 characters in length (after combining spaces). | ✓ | ✓ | ✓ |
> | V2.1.2 | Verify that passwords of at least 64 characters are permitted, and that passwords of more than 128 characters are denied. | ✓ | ✓ | ✓ |
> | V2.1.3 | Verify that password truncation is not performed. | ✓ | ✓ | ✓ |

### Normative Decomposition (Step 2)

ASVS uses "Verify that..." as its normative form — each row is a single testable requirement. The L1/L2/L3 columns indicate which verification level requires it.

| Section | Statement | Subject | Level | Notes |
|---------|-----------|---------|-------|-------|
| V2.1.1 | Passwords at least 12 chars in length | Application | L1 | Includes space combining |
| V2.1.2 | Passwords up to 64 chars permitted; over 128 denied | Application | L1 | Both min-max requirements in one |
| V2.1.3 | Password truncation not performed | Application | L1 | Prohibition — test differently than positive req |

### Criteria Generation (Step 3)

```json
[
  {
    "id": "asvs.v2.1.1",
    "category": "HIGH",
    "criterion": "The application enforces a minimum password length of 12 characters for user-set passwords.",
    "evidence_type": "tool",
    "evidence_instruction": "Search for password validation logic in authentication modules, registration handlers, and password change endpoints. Verify: (1) server-side enforcement exists (not just client-side JavaScript), (2) minimum threshold is ≥12, (3) spaces are permitted and counted toward length. Check configuration files (e.g., password policy YAML/JSON, identity provider settings) for configurable thresholds.",
    "rationale": "Short passwords are trivially brute-forced. 12-character minimum per NIST SP 800-63B provides meaningful offline attack resistance."
  },
  {
    "id": "asvs.v2.1.2",
    "category": "HIGH",
    "criterion": "The application permits passwords of at least 64 characters and rejects passwords exceeding 128 characters.",
    "evidence_type": "tool",
    "evidence_instruction": "Check password validation for maximum length handling. Look for: (1) no maximum below 64 characters, (2) an explicit maximum at or below 128 (prevents DoS via bcrypt's 72-byte limit or similar). Check database schema — VARCHAR(50) on a password column would violate this. Check if the hashing algorithm has input limits (bcrypt truncates at 72 bytes — a pre-hash step is needed for longer passwords).",
    "rationale": "Low maximums prevent passphrases. No maximum risks denial-of-service via expensive hashing of enormous inputs. The 64-128 range balances usability with safety."
  },
  {
    "id": "asvs.v2.1.3",
    "category": "HIGH",
    "criterion": "The application does not silently truncate passwords during storage or comparison.",
    "evidence_type": "tool",
    "evidence_instruction": "Trace the password from input to hash storage. Check for: (1) no substring/slice operations on the password before hashing, (2) no database column length constraints that would silently truncate (e.g., VARCHAR(20) storing a 30-char password), (3) bcrypt usage — if the password exceeds 72 bytes, verify a pre-hashing step (SHA-256 then bcrypt) rather than silent truncation.",
    "rationale": "Silent truncation means users think their password is 'correct horse battery staple' but only 'correct horse b' is actually verified. This dramatically reduces effective entropy without the user's knowledge."
  }
]
```

### Packaging (Step 5)

These three criteria go into a rubric file targeting web application codebases. The critic configuration:
- `correctness` — is the password handling implementation actually sound?
- `completeness` — does the codebase address all V2.1 requirements?

The output: a running Quorum evaluation of any application's authentication code against OWASP ASVS V2.1, with cited evidence gaps and actionable findings.

---

## 9. Timeline Estimates

| Milestone | Duration |
|-----------|----------|
| Source acquisition + quality check | 2-4 hours |
| Normative decomposition (single standard) | 4-8 hours |
| Criteria generation (with domain expertise) | 1-2 days |
| Review pass + refinement | 4-8 hours |
| **Working rubric** | **1-2 days** |
| Validation run (dogfood against known-good artifact) | 4 hours |
| Refinement based on validation | 4-8 hours |
| **Validated rubric** | **3 days** |
| Concordance mapping (1 related standard) | 1-2 days |
| **Rubric with concordance** | **4-5 days** |

These assume focused work, good source quality, and pre-existing domain expertise. If you're learning the domain as you go, add 50-100%.

---

## 10. Tips

**Scope discipline is the most important thing.** Pick one section of one standard and do it well. A complete rubric for OWASP ASVS V2 beats a sketchy rubric for the entire ASVS. You can always extend.

**Start with the highest-ROI standards.** "ROI" means: how often will this rubric run, and what's the cost of a missed finding? OWASP ASVS is high-frequency (every sprint) and high-stakes (security vulnerabilities). SOC 2 is relevant to any SaaS vendor. NIST SP 800-53 matters for any federal system.

**Dogfood immediately.** Run your rubric against a document you already understand — ideally one with known issues. If the rubric catches the issues you know about, it's working. If it misses them, your assessment guidance needs refinement.

**Evidence instructions are more important than criteria.** A critic with a clear criterion but vague evidence instruction will produce findings you can't verify. A critic with specific evidence instructions forces the evaluation to be concrete.

**Version your rubrics.** Standards update. OWASP ASVS versions roughly annually. When a standard changes, your rubric needs a version bump with a changelog. Build this expectation in from the start.

**Build concordance incrementally.** Don't try to map everything at once. When you build your second rubric in a domain, map it to your first. Concordance grows naturally if you make it a habit.

---

*Questions or rubric contributions → [CONTRIBUTING.md](../../CONTRIBUTING.md)*
