# SEC-06: Rubric Framework Architecture

**Status:** Stub
**Author:** Akkari (with Daniel Cervera)
**Date:** 2026-03-09
**Scope:** Defines the structural requirements for Quorum-conformant rubrics, following a framework/profile separation pattern

**Origin:** Identified during SEC-03 §4 review. The evidence integrity threat model revealed that rubric quality is the assurance ceiling — if a rubric doesn't specify evidence requirements, no amount of tooling can enforce them. This document establishes the framework that ensures every rubric addresses the dimensions that matter.

---

## 1. Problem Statement

Current Quorum rubrics are freeform: a rubric author decides which criteria to include, what evidence to require, and at what level of rigor. Nothing enforces completeness. A rubric that omits evidence adequacy requirements, skips provenance expectations, or ignores assurance level distinctions is technically valid — and structurally indefensible.

SEC-03 demonstrated that evidence integrity defenses are only as strong as the rubric that drives them. The rubric is the contract. A weak contract produces weak assurance regardless of how sophisticated the validation pipeline becomes.

---

## 2. Architectural Pattern: Framework / Profile Separation

This architecture follows the pattern established by NIST SP 800-130 and SP 800-152 for cryptographic key management systems:

- **SP 800-130 (Framework):** Enumerates every parameter a CKMS design must address. Does not prescribe specific values — defines the *envelope* of what must be specified.
- **SP 800-152 (Profile):** A specific CKMS design that fills in each parameter from the framework for a particular implementation context.

Applied to Quorum:

- **Quorum Rubric Framework (this document):** Enumerates every parameter a conformant rubric must address — evidence requirements, assurance level, corroboration expectations, prohibited forms, provenance, temporal constraints. Defines LOW, MODERATE, and HIGH assurance baselines.
- **Rubric Profile (the actual rubric):** Fills in those parameters for a specific domain, standard, or use case. A PKI profile specifies what CA certificate evidence looks like. A code quality profile specifies what test output is acceptable. Each is different; all are conformant to the same framework.

**Key constraint:** A rubric that does not address a required framework parameter is *non-conformant*. This is enforceable by the pipeline, not advisory.

### What This Solves

1. **Rubric quality floor** — No rubric can skip evidence adequacy, provenance, or corroboration requirements because the framework mandates them. Today, a rubric that omits these is technically valid. Under this architecture, it's non-conformant.
2. **Assurance level consistency** — LOW/MODERATE/HIGH baselines are defined once in the framework and applied uniformly across all profiles. No more ad-hoc decisions about what "rigorous enough" means per rubric.
3. **Decay resistance** — The framework is the structural contract. Profiles can vary across domains but cannot violate the framework's parameter requirements. As rubrics evolve over time, the framework prevents silent erosion of rigor.
4. **Clear open/proprietary boundary** — The framework ships open-source with Quorum. Premium rubric profiles (PKI, CKMS, FedRAMP) are the paid product — domain expertise encoded against a public standard. The framework is visible; the moat is in the profiles.
5. **Familiar pattern for the target audience** — Compliance professionals, auditors, and CKMS architects already understand the framework/profile separation from SP 800-130/152. This isn't a new concept to teach — it's a trusted pattern applied to a new domain.

---

## 3. Framework Parameters (to develop)

The following are candidate parameters that a conformant rubric must address. Each parameter defines a dimension; the rubric profile supplies the value.

### 3.1 Parameters the Framework Defines

| Parameter | Description | Framework Provides |
|-----------|-------------|-------------------|
| **Assurance Level** | LOW / MODERATE / HIGH baseline | Definitions and characteristics of each level |
| **Evidence Adequacy** | What constitutes acceptable evidence for each criterion | Required schema fields (`evidence_requirements`) |
| **Prohibited Evidence Forms** | What explicitly does not count | Enumeration pattern and common prohibitions |
| **Provenance Requirements** | Expected metadata about evidence origin | Provenance dimensions (author, source system, timestamp, integrity) |
| **Corroboration Requirements** | When multiple independent sources are needed | Corroboration levels (none / recommended / required) |
| **Temporal Requirements** | Evidence freshness constraints | Currency window definitions per assurance level |
| **Normative Coverage** | SHALL / SHOULD / MAY / SHALL NOT / SHOULD NOT | Requirement to address all normative forms, not just positive obligations |
| **Gating Behavior** | When human review is required vs. auto-proceed | Confidence thresholds per assurance level |

### 3.2 Parameters the Framework Leaves to the Profile

| Parameter | Description | Why Profile-Specific |
|-----------|-------------|---------------------|
| **Domain criteria** | The actual testable requirements | Derived from the standard under evaluation |
| **Evidence specifics** | What a real CA cert vs. a real CMDB export looks like | Requires domain expertise |
| **Acceptable sources** | Which systems/tools produce authoritative evidence | Varies by organization and domain |
| **Risk weighting** | Relative importance of criteria within the domain | Context-dependent |
| **V-series examples** | Domain-specific genuine/fabricated evidence examples | Proprietary calibration data (see SEC-03 §6) |

---

## 4. Assurance Baselines

Mapped from the Assurance Level Model (SEC-03 §3.3):

| Baseline | Evidence Expectation | Gating Behavior | Human Review | Target Use |
|----------|---------------------|-----------------|-------------|------------|
| **LOW** | Artifact-only; structural validation | Generous — flag but auto-proceed on medium confidence | End-of-run review of flagged items | Code quality, config hygiene, internal standards |
| **MODERATE** | Evidence-augmented; documented analyses expected for key controls | Balanced — gate on low confidence or evidence adequacy concerns | Phase-gate review for flagged items | SOC 2, OWASP ASVS, general compliance |
| **HIGH** | Integrity-backed; provenance, signatures, system-generated evidence | Conservative — gate on anything below high confidence | Phase-gate review; human substantiation required for critical controls | PKI, CKMS, FedRAMP HIGH, critical infrastructure |

---

## 5. Conformance Validation

The Quorum pipeline should be able to validate a rubric against this framework — a meta-validation that checks whether the rubric itself is conformant before it's used to validate artifacts.

- Does every criterion specify an `evidence_requirements` block?
- Does the rubric declare an assurance level?
- Are prohibited evidence forms enumerated?
- Are corroboration requirements specified for HIGH/CRITICAL criteria?

A non-conformant rubric should produce a warning (LOW assurance contexts) or an error (HIGH assurance contexts).

---

## 6. Relationship to Other Documents

| Document | Relationship |
|----------|-------------|
| SEC-03 — Evidence Integrity | Establishes the *need* for this framework (rubric quality is the assurance ceiling) |
| SEC-05 — Pipeline Resilience | Framework parameters may include pipeline safety constraints |
| RUBRIC_BUILDING_GUIDE | Must be updated to reference and enforce this framework |
| CONFIG_REFERENCE | Rubric schema must be extended to support framework parameters |
| Proprietary Rubric Packs | Premium profiles built against this framework |

---

## 7. Open Questions

- Should conformance be binary (conformant / non-conformant) or graduated (Level 1 / 2 / 3 conformance)?
- How do we handle legacy rubrics that predate the framework? Grace period with warnings, or immediate enforcement?
- Should the framework itself version independently of Quorum releases?
- Can a profile declare a *lower* assurance level than its domain typically demands? (e.g., a "quick check" PKI rubric at LOW — is that useful or misleading?)

---

## 8. Acknowledgments

The framework/profile separation pattern in this document is directly informed by the work of **Elaine Barker** (NIST SP 800-130, SP 800-152, SP 800-57) on cryptographic key management system design — specifically the architectural distinction between a framework that enumerates parameters and a profile that fills them in for a specific implementation context.

The assurance level model and evidence-grounded assessment methodology draw from the work of **Ron Ross** (NIST SP 800-37, SP 800-53, SP 800-53A, FIPS 199/200) on the Risk Management Framework — the structured, layered approach to substantiating that a system meets its security requirements.

Their combined influence on this architecture is significant and should not go unacknowledged.
