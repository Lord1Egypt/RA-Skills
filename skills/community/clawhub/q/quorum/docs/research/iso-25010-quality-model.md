# ISO/IEC 25010:2023 — Software Product Quality Model (SQuaRE)
## Complete Taxonomy for Code Hygiene Critic

**Standard:** ISO/IEC 25010:2023 (2nd Edition, November 2023)  
**Full Title:** Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model  
**Replaces:** ISO/IEC 25010:2011 (1st Edition)

---

## Overview

ISO/IEC 25010:2023 defines **9 top-level quality characteristics** (up from 8 in the 2011 edition). Each characteristic is subdivided into sub-characteristics that can be used to specify, measure, and evaluate product quality.

### Key Changes from 2011 → 2023

| Change | Detail |
|--------|--------|
| New characteristic | **Safety** added (was previously embedded in Usability/Reliability) |
| Rename | Usability → **Interaction Capability** |
| Rename | Portability → **Flexibility** |
| New sub-char | **Self-descriptiveness** added to Interaction Capability |
| New sub-char | **Inclusivity** added to Interaction Capability (split from Accessibility) |
| New sub-char | **User engagement** replaces User interface aesthetics |
| New sub-char | **User assistance** added (split from Accessibility) |
| New sub-char | **Resistance** added to Security |
| New sub-char | **Scalability** added to Flexibility (extracted from Adaptability) |
| Replacement | Maturity → **Faultlessness** in Reliability |
| New safety sub-chars | operational constraint, risk identification, fail safe, hazard warning, safe integration |

---

## Evaluability Key

| Symbol | Meaning |
|--------|---------|
| 🔬 **Static** | Evaluable by static analysis of source code (AST, metrics, linters) |
| 🤖 **LLM** | Requires LLM/human judgment (semantic, contextual, or design-level assessment) |
| 🔬🤖 **Hybrid** | Partially automatable by static analysis; LLM adds depth |
| ⚙️ **Runtime** | Requires runtime measurement; not assessable from source code alone |

---

## Complete Taxonomy

---

### 1. Functional Suitability

> The degree to which a product or system provides functions that meet stated and implied needs when used under specified conditions.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Functional Completeness** | Degree to which the set of functions covers all specified tasks and user objectives. | 🤖 **LLM** — requires understanding of specs vs. implementation |
| **Functional Correctness** | Degree to which a product or system provides the correct results with the needed degree of precision. | 🤖 **LLM** + tests — needs semantic understanding of intent |
| **Functional Appropriateness** | Degree to which the functions facilitate the accomplishment of specified tasks and objectives. | 🤖 **LLM** — requires design-level judgment |

**Code hygiene relevance:** Limited. Functional suitability is primarily spec-driven. Static analysis can detect obvious dead code or unreachable branches that hint at incompleteness.

---

### 2. Performance Efficiency

> The performance relative to the amount of resources used under stated conditions.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Time Behaviour** | Degree to which response time and throughput rates meet requirements when performing functions. | ⚙️ **Runtime** — benchmarks required; static analysis can flag O(n²) algorithms |
| **Resource Utilization** | Degree to which amounts and types of resources (CPU, memory, storage, network) meet requirements. | ⚙️ **Runtime** / 🔬🤖 **Hybrid** — static can flag memory leaks, unnecessary allocations |
| **Capacity** | Degree to which the maximum limits of product/system parameters (volume, concurrency, throughput) meet requirements. | ⚙️ **Runtime** / 🔬🤖 **Hybrid** — static can flag unbounded loops, missing limits |

**Code hygiene relevance:** Moderate. Static analysis can identify inefficient patterns (quadratic complexity, memory leaks, unbounded collections). LLM can reason about algorithmic efficiency.

---

### 3. Compatibility

> The degree to which a product, system or component can exchange information with other products, systems or components, and/or perform its required functions, while sharing the same hardware or software environment.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Coexistence** | Degree to which a product can perform its required functions efficiently while sharing a common environment and resources with other products, without detrimental impact on any other product. | 🔬🤖 **Hybrid** — static can detect global state pollution, port conflicts; LLM assesses architectural isolation |
| **Interoperability** | Degree to which two or more systems, products or components can exchange information and use the information that has been exchanged. | 🔬🤖 **Hybrid** — static can check API contract adherence, serialization safety; LLM assesses protocol correctness |

**Code hygiene relevance:** Moderate. Static analysis can detect anti-patterns (global mutable state, hardcoded ports, tight coupling, incompatible data types at interfaces).

---

### 4. Interaction Capability

> The degree to which a product or system can be operated by specified users to achieve specified goals with effectiveness, efficiency and satisfaction in a specified context of use.  
> *(Formerly: Usability)*

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Appropriateness Recognizability** | Degree to which users can recognize whether a product or system is appropriate for their needs. | 🤖 **LLM** — requires UX judgment; code evidence: API naming, documentation quality |
| **Learnability** | Degree to which a product or system can be used by specified users to achieve specified goals of learning to use the product or system with effectiveness, efficiency, freedom from risk and satisfaction. | 🤖 **LLM** — code evidence: code clarity, naming conventions, documentation |
| **Operability** | Degree to which a product or system has attributes that make it easy to operate and control. | 🤖 **LLM** — code evidence: error messages, configuration ergonomics |
| **User Error Protection** | Degree to which a system protects users against making errors. | 🔬🤖 **Hybrid** — static can detect missing input validation, unchecked nulls; LLM assesses completeness |
| **User Engagement** | Degree to which a product or system presents functions and information in an inviting and motivating manner encouraging continued interaction. *(Replaces User Interface Aesthetics)* | 🤖 **LLM** — primarily UX/design; limited code signal |
| **Self-Descriptiveness** | Degree to which a product presents its capabilities so users can understand and use them without need for other resources. *(NEW in 2023)* | 🔬🤖 **Hybrid** — static can detect missing docstrings, poor naming; LLM assesses comprehensiveness |
| **Inclusivity** | Degree to which a product can be used by people with a wide range of characteristics (age, abilities, education level, language, etc.). *(NEW, split from Accessibility)* | 🤖 **LLM** — WCAG compliance hints; LLM evaluates design patterns |
| **User Assistance** | Degree to which a product can be used by users in a specified context to achieve specified goals with effectiveness, efficiency and satisfaction. *(NEW, split from Accessibility)* | 🤖 **LLM** — help system, error recovery guidance |

**Code hygiene relevance:** Low-to-moderate for code critics. Most interaction capability attributes are evaluated at UI/UX level, but code-level signals exist (naming, docstrings, error messages, input validation).

---

### 5. Reliability

> The degree to which a system, product or component performs specified functions under specified conditions for a specified period of time.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Faultlessness** | Degree to which a system, product or component performs specified functions under normal operation without fault. *(Replaces Maturity — 2011)* | 🔬🤖 **Hybrid** — static can detect error-prone patterns; test coverage metrics; LLM assesses error handling completeness |
| **Availability** | Degree to which a system, product or component is operational and accessible when required for use. | ⚙️ **Runtime** / 🔬🤖 **Hybrid** — static can flag missing retry logic, single points of failure |
| **Fault Tolerance** | Degree to which a system, product or component operates as intended despite the presence of hardware or software faults. | 🔬🤖 **Hybrid** — static can detect missing exception handling, unchecked errors; LLM assesses recovery completeness |
| **Recoverability** | Degree to which, in the event of an interruption or a failure, a product or system can recover the data directly affected and re-establish the desired state of the system. | 🔬🤖 **Hybrid** — static can detect transaction patterns, backup logic; LLM assesses recovery path completeness |

**Code hygiene relevance:** HIGH. Exception handling coverage, error propagation patterns, retry logic, and fault tolerance patterns are all statically analyzable with LLM assistance for semantic correctness.

---

### 6. Security

> The degree to which a product or system protects information and data so that persons or other products or systems have the degree of data access appropriate to their types and levels of authorization.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Confidentiality** | Degree to which a product or system ensures that data is accessible only to those authorized to have access. | 🔬🤖 **Hybrid** — static can detect plaintext secrets, missing encryption; LLM assesses access control logic |
| **Integrity** | Degree to which a system, product or component prevents unauthorized access to, or modification of, computer programs or data. | 🔬🤖 **Hybrid** — static can flag injection vulnerabilities, missing input sanitization |
| **Non-repudiation** | Degree to which actions or events can be proven to have taken place so that the events or actions cannot be repudiated later. | 🔬🤖 **Hybrid** — static can detect missing audit logging; LLM assesses logging completeness |
| **Accountability** | Degree to which the actions of an entity can be traced uniquely to the entity. | 🔬🤖 **Hybrid** — static can detect missing authentication checks; LLM assesses identity binding completeness |
| **Authenticity** | Degree to which the identity of a subject or resource can be proven to be the one claimed. | 🔬🤖 **Hybrid** — static can detect weak authentication patterns, missing signature verification |
| **Resistance** | Degree to which a product or system sustains operations while under attack from a malicious actor. *(NEW in 2023)* | 🔬🤖 **Hybrid** — static can flag DoS-vulnerable patterns (unbounded inputs, no rate limiting); LLM assesses hardening completeness |

**Code hygiene relevance:** VERY HIGH. Security sub-characteristics are a primary target for static analysis tooling (SAST). LLM adds semantic reasoning about attack vectors and control flow.

---

### 7. Maintainability

> The degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Modularity** | Degree to which a system or computer program is composed of discrete components such that a change to one component has minimal impact on other components. | 🔬 **Static** — coupling metrics (CBO, LCOM), dependency analysis, circular dependency detection |
| **Reusability** | Degree to which an asset can be used in more than one system, or in building other assets. | 🔬🤖 **Hybrid** — static can detect code duplication (DRY violations); LLM assesses interface generality |
| **Analysability** | Degree of effectiveness and efficiency with which it is possible to assess the impact of an intended change on a product or system, diagnose a product for deficiencies or causes of failures, or identify parts to be modified. | 🔬🤖 **Hybrid** — static: complexity metrics (cyclomatic, cognitive), naming quality; LLM: comprehensibility assessment |
| **Modifiability** | Degree to which a product or system can be effectively and efficiently modified without introducing defects or degrading existing product quality. | 🔬🤖 **Hybrid** — static: coupling, complexity, test coverage; LLM: assessment of change impact |
| **Testability** | Degree of effectiveness and efficiency with which test criteria can be established for a system, product or component, and tests can be performed to determine whether those criteria have been met. | 🔬🤖 **Hybrid** — static: test coverage, dependency injection patterns, test isolation; LLM: testability of complex logic |

**Code hygiene relevance:** VERY HIGH. Maintainability is the most code-analysis-friendly characteristic. Metrics like cyclomatic complexity, coupling, cohesion, duplication, and naming quality are well-established static analysis targets.

---

### 8. Flexibility

> The degree to which a product or system can be adapted for different or evolving hardware, software or other operational or usage environments.  
> *(Formerly: Portability)*

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Adaptability** | Degree to which a product or system can effectively and efficiently be adapted for different or evolving hardware, software or other operational or usage environments. | 🔬🤖 **Hybrid** — static can detect hardcoded environment assumptions, platform-specific code; LLM assesses configuration abstractions |
| **Scalability** | Degree to which a product can handle growing or shrinking workloads or adapt its capacity to handle variability. *(NEW in 2023, extracted from Adaptability)* | 🔬🤖 **Hybrid** — static can detect stateful anti-patterns, synchronization bottlenecks; LLM assesses architectural scalability |
| **Installability** | Degree of effectiveness and efficiency with which a product or system can be successfully installed and/or uninstalled in a specified environment. | 🤖 **LLM** — code evidence: dependency declarations, environment configuration; limited static signal |
| **Replaceability** | Degree to which a product can replace another specified software product for the same purpose in the same environment. | 🤖 **LLM** — requires assessment of interface compatibility and behavioral equivalence |

**Code hygiene relevance:** Moderate. Static analysis can detect portability anti-patterns (platform-specific APIs, hardcoded paths, non-portable numeric types). Scalability is increasingly important.

---

### 9. Safety *(NEW in 2023)*

> The degree to which a product or system avoids a state in which human life, health, property or the environment is endangered.

| Sub-characteristic | Definition | Evaluability |
|-------------------|-----------|--------------|
| **Operational Constraint** | Degree to which a product or system operates within safe parameters and states under hazardous conditions, regardless of operator input. | 🔬🤖 **Hybrid** — static can detect missing boundary checks, unconstrained numerical operations; LLM assesses safety invariants |
| **Risk Identification** | Degree to which a product or system can identify sequences of events with potential danger and signal the risk. | 🤖 **LLM** — requires domain-specific safety reasoning; static can find missing guards |
| **Fail Safe** | Degree to which a product or system, upon failure, automatically transitions to a safe state. | 🔬🤖 **Hybrid** — static can detect missing fallback states, unhandled exception paths; LLM assesses completeness |
| **Hazard Warning** | Degree to which a product or system provides warnings about unacceptable risks to users. | 🤖 **LLM** — requires semantic understanding of warning/alert patterns |
| **Safe Integration** | Degree to which a product maintains safety properties when integrated with other components or systems. | 🔬🤖 **Hybrid** — static can detect integration boundary gaps; LLM assesses safety property preservation |

**Code hygiene relevance:** Context-dependent (safety-critical systems only). For general-purpose software critics, safety analysis is mainly about boundary condition handling and fail-safe patterns.

---

## Summary Table: All 9 Characteristics and Sub-characteristics

| # | Characteristic | Sub-characteristics (count) | Primary Evaluability |
|---|---------------|---------------------------|---------------------|
| 1 | Functional Suitability | Completeness, Correctness, Appropriateness (3) | 🤖 LLM |
| 2 | Performance Efficiency | Time Behaviour, Resource Utilization, Capacity (3) | ⚙️ Runtime / 🔬🤖 Hybrid |
| 3 | Compatibility | Coexistence, Interoperability (2) | 🔬🤖 Hybrid |
| 4 | Interaction Capability | Appropriateness Recognizability, Learnability, Operability, User Error Protection, User Engagement, Self-Descriptiveness, Inclusivity, User Assistance (8) | 🤖 LLM / 🔬🤖 Hybrid |
| 5 | Reliability | Faultlessness, Availability, Fault Tolerance, Recoverability (4) | 🔬🤖 Hybrid |
| 6 | Security | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, Resistance (6) | 🔬🤖 Hybrid / 🔬 Static |
| 7 | Maintainability | Modularity, Reusability, Analysability, Modifiability, Testability (5) | 🔬 Static / 🔬🤖 Hybrid |
| 8 | Flexibility | Adaptability, Scalability, Installability, Replaceability (4) | 🔬🤖 Hybrid / 🤖 LLM |
| 9 | Safety | Operational Constraint, Risk Identification, Fail Safe, Hazard Warning, Safe Integration (5) | 🔬🤖 Hybrid / 🤖 LLM |
| **Total** | **9 characteristics** | **40 sub-characteristics** | |

---

## Code Hygiene Critic Applicability

### Tier 1: Highest Static Analysis Coverage
These sub-characteristics yield the richest signal from code inspection alone:

- **Modularity** — coupling/cohesion metrics, circular dependency detection
- **Analysability** — complexity metrics (cyclomatic, cognitive complexity)
- **Reusability** — code duplication detection (DRY violations)
- **Testability** — test coverage metrics, test isolation patterns
- **Modifiability** — change impact indicators (high coupling, low cohesion)
- **Confidentiality** — hardcoded secrets, missing encryption
- **Integrity** — injection vulnerabilities (SQL, XSS, command injection)
- **Fault Tolerance** — uncaught exceptions, swallowed errors, missing error propagation
- **User Error Protection** — missing input validation, null dereferences

### Tier 2: Strong LLM Enhancement Needed
Static analysis provides starting signal; LLM reasons about semantic correctness:

- **Faultlessness** — error handling completeness assessment
- **Accountability / Authenticity** — authentication/authorization logic review
- **Non-repudiation** — audit logging completeness
- **Resistance** — DoS attack surface analysis
- **Adaptability** — environment assumption assessment
- **Scalability** — stateful bottleneck reasoning
- **Coexistence** — global state pollution analysis
- **Operational Constraint** — boundary safety invariants
- **Fail Safe** — failure mode completeness

### Tier 3: Primarily LLM/Human Judgment
Limited static signal; context and design intent required:

- **Functional Suitability** (all 3) — spec vs. implementation judgment
- **User Engagement, Learnability, Operability** — UX judgment
- **Inclusivity, User Assistance** — accessibility expertise
- **Interoperability** — protocol correctness assessment
- **Recoverability** — recovery path adequacy
- **Risk Identification, Hazard Warning** — domain safety expertise
- **Installability, Replaceability** — deployment/migration reasoning

---

## Sources

1. **ISO/IEC 25010:2023** — Official standard (paywall). Preview: [cdn.standards.iteh.ai](https://cdn.standards.iteh.ai/samples/78176/13ff8ea97048443f99318920757df124/ISO-IEC-25010-2023.pdf)
2. **iso25000.com** — Official SQuaRE series reference site: [iso25000.com/en/iso-25000-standards/iso-25010](https://iso25000.com/en/iso-25000-standards/iso-25010)
3. **arc42 Quality Model** — 2023 update analysis: [quality.arc42.org/articles/iso-25010-update-2023](https://quality.arc42.org/articles/iso-25010-update-2023)
4. **Spree Blog** — 2nd Edition changes summary: [blog.spree.de/2024/01/02/iso-iec-25010-news-from-the-2nd-edition-2023-11](https://blog.spree.de/2024/01/02/iso-iec-25010-news-from-the-2nd-edition-2023-11/)
5. **Zenodo / Pacific Northwest National Lab** — ISO 25010:2023 applied to EVSE software: [zenodo.org/records/14758339](https://zenodo.org/records/14758339)
6. **ISO.org Standard Listing**: [iso.org/standard/78176.html](https://www.iso.org/standard/78176.html)

---

*Research conducted: 2026-03-05. Accuracy reflects the 2023 edition. Sub-characteristic definitions are paraphrased from official sources for practical use.*
