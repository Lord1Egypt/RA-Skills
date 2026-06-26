\---

name: zero-loss-methodology

description: "Zero-Loss Research \& Planning Methodology v2.1 — a self-configuring, executable algorithm for hallucination-free, traceable AI-assisted research and planning. Use this skill whenever performing multi-document research, gap analysis, deliverable generation, translation, document consolidation, or verification tasks. Also triggers on: research planning, document review, critical analysis, gap filling, source validation, document fusion, translation verification, compliance artifacts, traceability matrix, or any task requiring zero content loss and full source traceability. This skill should be used for ANY research or planning task involving multiple source documents, even if the user doesn't explicitly mention 'methodology'."

\---

&#x20;

\# Zero-Loss Research \& Planning Methodology v2.1

&#x20;

A self-configuring, domain-agnostic executable algorithm for AI-assisted research and planning that guarantees zero content loss, zero hallucination, and full traceability.

&#x20;

\## Core Guarantees

&#x20;

1\. \*\*Zero Content Loss\*\*: No source content is dropped, summarized, or silently omitted. Word count of output ≥ word count of source content.

2\. \*\*Zero Hallucination\*\*: Every fact is either (a) directly from a source document, (b) from a verified external source with citation, or (c) explicitly marked as an assumption.

3\. \*\*Full Traceability\*\*: Every deliverable traces back to a user request, a gap in the analysis, or a decision point. Every fact traces to a source. The full decision chain is logged.

4\. \*\*Reproducibility\*\*: Build scripts archived alongside deliverables; any output can be regenerated. Given the same inputs and algorithm, another AI agent should produce substantially equivalent output.

&#x20;

\## When to Apply This Methodology

&#x20;

Apply the \*\*full P00–P10 pipeline\*\* when:

\- Working with 3+ source documents

\- Deliverables will be used for decision-making, funding, or compliance

\- Translation or multilingual content is involved

\- Document consolidation/fusion is needed

&#x20;

Apply a \*\*lightweight subset\*\* (P00 + P01 + P02 + P05 + P06) when:

\- Working with 1–2 source documents

\- Quick turnaround needed

\- Lower-stakes deliverables

\- Note: P00 is always included — even lightweight runs need domain detection and scaffold

&#x20;

\## The 11 Processes

&#x20;

\### P00: Project Bootstrap (Self-Configuration)

\*\*INPUT\*\*: User request R, this methodology document M

\*\*OUTPUT\*\*: Project scaffold S with domain profile D

&#x20;

```

ALGORITHM:

&#x20; # STEP 1: DOMAIN DETECTION

&#x20; 1. Analyze user request R to extract:

&#x20;    a. Domain (e.g., healthcare, fintech, legal, SaaS, manufacturing)

&#x20;    b. Project type (research, planning, audit, compliance, product dev)

&#x20;    c. Output language(s) (for deliverables and sources)

&#x20;    d. Regulatory context (jurisdiction, applicable standards)

&#x20; 2. Build Domain Profile D:

&#x20;    D = {domain, project\_name, review\_dimensions, regulatory\_standards,

&#x20;         source\_languages, output\_language, authority\_sources}

&#x20;

&#x20; # STEP 2: REVIEW DIMENSIONS (auto-selected per domain)

&#x20; 3. Select review dimensions based on D.domain:

&#x20;    Healthcare/MedTech: \[Clinical, Regulatory, Technical, Security, Business, Data Privacy]

&#x20;    FinTech:            \[Regulatory, Security, Technical, Business, Compliance, Financial]

&#x20;    SaaS:              \[Technical, Business, Security, Scalability, Compliance, Financial]

&#x20;    Legal:             \[Regulatory, Compliance, Risk, Contractual, Jurisdictional, Financial]

&#x20;    Manufacturing:     \[Technical, Safety, Regulatory, Supply Chain, Quality, Financial]

&#x20;    General:           \[Technical, Business, Regulatory, Strategic, Financial, Operational]

&#x20;

&#x20; # STEP 3: DIRECTORY SCAFFOLD

&#x20; 4. Create project directory structure:

&#x20;    {project\_name}/

&#x20;    ├── Deliverables/          ← P05/P09 outputs go here

&#x20;    ├── ProcessArtifacts/      ← compliance artifacts go here

&#x20;    │   ├── Source-Inventory      (created empty, filled by P01)

&#x20;    │   ├── Traceability-Matrix   (created empty, filled live during P05)

&#x20;    │   ├── Source-Registry       (created empty, filled live during P05)

&#x20;    │   ├── Validated-Claims      (created empty, filled by P03)

&#x20;    │   ├── Spot-Check-Guide      (created at P10, for human reviewer)

&#x20;    │   ├── Verification-Report   (created by P08, if translation used)

&#x20;    │   ├── Process-History       (created live, updated each phase)

&#x20;    │   ├── Manifest              (created at P10)

&#x20;    │   └── BuildScripts/         (archived at P10)

&#x20;    └── Sources/               ← user-provided input files

&#x20;

&#x20; # STEP 4: DOMAIN-SPECIFIC L1 AUTHORITY SOURCES

&#x20; 5. Pre-populate D.authority\_sources based on domain:

&#x20;    Healthcare: \[WHO, EMA, FDA, MDR, GDPR, national health authority]

&#x20;    FinTech:    \[ECB, SEC, FCA, PSD2, MiFID II, national financial regulator]

&#x20;    SaaS:      \[GDPR, SOC2, ISO 27001, NIST, CCPA, national data authority]

&#x20;    Legal:     \[National legislation, bar association, court rulings, treaties]

&#x20;    These pre-populated sources become the MINIMUM L1 checklist for P03.

&#x20;

&#x20; 6. Present D and scaffold to user for confirmation

&#x20; \[GATE G0] User confirms domain profile and structure? Y → proceed to P01.

&#x20;           N → adjust domain profile per user feedback.

```

&#x20;

\### P01: Source Ingestion

\*\*INPUT\*\*: Set of files F = {f1, f2, ..., fn}

\*\*OUTPUT\*\*: Source Inventory Table I

&#x20;

```

FOR each file f in F:

&#x20; 1. Detect format (docx, pdf, xlsx, csv, md, txt, image)

&#x20; 2. Detect language (auto-detect, confirm with user if <90% confidence)

&#x20; 3. Extract raw text content

&#x20; 4. Count: words, paragraphs, tables, images, headings

&#x20; 5. Extract: title, date, author (if present)

&#x20; 6. Extract: key topics (top 5 by frequency)

&#x20; 7. Store in I: {filename, format, language, word\_count,

&#x20;                 structure\_counts, metadata, topics}

END FOR

8\. Cross-reference: identify overlapping topics between documents

&#x20;  Build overlap matrix O:

&#x20;  O\[i]\[j] = {shared\_topics: \[...], contradiction\_count: N,

&#x20;              overlap\_pct: %, primary\_owner: doc\_with\_most\_content}

&#x20;  Use O to detect redundancy and assign section ownership during P05.

9\. Flag: contradictions in metadata (dates, versions, authors)

10\. Present I to user for confirmation

\[GATE G1] User confirms inventory is complete? Y → proceed. N → add missing files.

```

&#x20;

\### P02: Critical Review

\*\*INPUT\*\*: Source Inventory I, Domain context D

\*\*OUTPUT\*\*: Gap List G with priority scores

&#x20;

```

1\. Define review dimensions based on domain (from P00 D.review\_dimensions):

&#x20;  \[Technical, Business, Regulatory, Strategic, Financial, Operational]

2\. FOR each document d in I:

&#x20;  FOR each dimension dim:

&#x20;    a. Check: Does d contain content for dim?

&#x20;    b. If yes: Assess completeness (0-100%) and accuracy

&#x20;    c. If yes: Flag unverified claims → queue for P03

&#x20;    d. If no: Record as gap

&#x20;  END FOR

END FOR

3\. Cross-document consistency check:

&#x20;  a. Compare overlapping topics for contradictions

&#x20;  b. Compare numerical data (costs, timelines, headcount)

&#x20;  c. Flag discrepancies with magnitude (e.g., "4x cost difference")

4\. External benchmark check:

&#x20;  a. Identify applicable standards (ISO, GDPR, industry-specific)

&#x20;  b. Check each document against applicable standards

&#x20;  c. Flag missing compliance areas

5\. Compile G: {gap\_id, source\_doc, dimension, description,

&#x20;              severity(CRITICAL/HIGH/MEDIUM/LOW), evidence}

6\. Present G to user

\[GATE G2] User confirms gap list? Y → proceed to P04. N → revise.

```

&#x20;

\### P03: Source Validation

\*\*INPUT\*\*: Claims queue CQ from P02

\*\*OUTPUT\*\*: Validated Claims Table (VCT)

&#x20;

Authority hierarchy for verification:

\- \*\*L1\*\*: Official/government source (legislation, standards body)

\- \*\*L2\*\*: Peer-reviewed/industry report (journal, analyst report)

\- \*\*L3\*\*: Vendor documentation (official docs, release notes)

\- \*\*L4\*\*: News/blog (reputable outlet, dated)

\- \*\*L5\*\*: Unverifiable (no external source found)

&#x20;

```

FOR each claim c in CQ:

&#x20; 1. Classify type: \[Statistic, Date/Deadline, Technical Spec, Market Data,

&#x20;                    Legal Requirement, Cost Estimate, Performance Claim]

&#x20; 2. Identify authoritative source hierarchy (L1–L5)

&#x20; 3. Search for verification (minimum 2 independent sources for L3+)

&#x20; 4. Compare source claim vs found data

&#x20; 5. Assign status:

&#x20;    +==============+===================================================+

&#x20;    | VERIFIED     | Claim matches ≥2 authoritative sources             |

&#x20;    | CORRECTED    | Claim was wrong; replacement data provided        |

&#x20;    | OUTDATED     | Claim was true but data has since changed          |

&#x20;    | UNVERIFIABLE | No authoritative source found; marked in output    |

&#x20;    | REFUTED      | Claim contradicted by authoritative source(s)      |

&#x20;    +==============+===================================================+

&#x20; 6. Record in VCT: {claim, source\_doc, claim\_type, status,

&#x20;                    verification\_source, verification\_date, notes}

END FOR

&#x20;

CORRECTED and REFUTED require: {original\_claim, correction,

correction\_source, deliverable\_updated, update\_description}

&#x20;

CRITICAL RULE: REFUTED and CORRECTED claims MUST be addressed

in deliverables. Never silently drop a refuted claim.

```

&#x20;

\### P04: Priority Triage

\*\*INPUT\*\*: Gap List G, Project context

\*\*OUTPUT\*\*: Prioritized Work Packages WP = {P0, P1, P2, P3}

&#x20;

```

Priority tiers:

&#x20; P0 (Immediate): Blocking launch or causing legal/safety risk

&#x20; P1 (Short-term): Required within 1-2 sprints for viability

&#x20; P2 (Medium-term): Required before MVP but can be parallelized

&#x20; P3 (Pre-launch): Required before go-live but not for core dev

&#x20;

FOR each gap g in G:

&#x20; a. Assess: deadline pressure (is there a hard date?)

&#x20; b. Assess: dependency (does other work block on this?)

&#x20; c. Assess: severity (what happens if ignored?)

&#x20; d. Assign tier: P0/P1/P2/P3

Group gaps into deliverables, define format, estimate effort.

\[GATE G3] User approves work packages? Y → proceed. N → re-triage.

```

&#x20;

\### P05: Deliverable Generation

\*\*INPUT\*\*: Work package spec WPi, VCT, source documents

\*\*OUTPUT\*\*: Professional document(s)

&#x20;

```

FOR each deliverable:

&#x20; Phase A — Research:

&#x20;   1. Extract all relevant source content

&#x20;   2. Identify knowledge gaps requiring external research

&#x20;   3. Conduct external research, add sources to Source-Registry

&#x20;   4. Validate all external facts via P03 source hierarchy

&#x20; Phase B — Structure:

&#x20;   Define outline, map source content to sections (traceability),

&#x20;   update Traceability-Matrix live

&#x20; Phase C — Write:

&#x20;   Write each section with source annotations,

&#x20;   ensure numerical consistency, mark assumptions explicitly

&#x20; Phase D — Format:

&#x20;   Apply consistent formatting, generate output file, validate

END FOR

```

&#x20;

\*\*ANTI-HALLUCINATION RULES\*\* (these are absolute):

\- Never invent statistics. If data not found → "Data not available."

\- Never invent URLs. Only link to URLs you have visited and confirmed.

\- Never invent timelines. Base on source data or industry benchmarks.

\- If unsure → mark with \[NEEDS VERIFICATION] for user review.

&#x20;

\### P06: Plan-vs-Content Verification

\*\*INPUT\*\*: Plan document, Deliverable set

\*\*OUTPUT\*\*: Gap Report

&#x20;

```

1\. Parse plan into checklist items

2\. FOR each item: locate in deliverable, assess coverage:

&#x20;  FULL | PARTIAL | MISSING | DIVERGED

3\. Calculate coverage: count(FULL) / count(ALL) \* 100

4\. If coverage < 100% → return to P07

5\. If coverage = 100% → mark VERIFIED

```

&#x20;

\### P07: Multi-Pass Gap Closure

\*\*INPUT\*\*: Gap Report from P06

\*\*OUTPUT\*\*: Zero-gap deliverable set

&#x20;

```

pass\_count = 0, MAX\_PASSES = 5

WHILE gaps remain:

&#x20; pass\_count += 1

&#x20; IF pass\_count > MAX\_PASSES: ESCALATE to user

&#x20; FOR each gap:

&#x20;   Diagnose why missed, fix using P05 rules, insert at correct location

&#x20; Re-run P06

END WHILE

```

&#x20;

\### P08: Translation \& Localization

\*\*INPUT\*\*: Source document (language A)

\*\*OUTPUT\*\*: Translated document (language B) + Verification Report

&#x20;

```

Phase A — Structure Extraction:

&#x20; Parse into structural units, extract all numbers/dates, proper nouns/URLs

Phase B — Translation:

&#x20; Translate preserving: all numbers unchanged, proper nouns/URLs unchanged,

&#x20; table structure, technical terminology in original where standard

Phase C — 4-Check Verification:

&#x20; Check 1 (Structural Parity): paragraph/table/heading counts match

&#x20; Check 2 (Numeric Exact Match): all numbers present and unchanged

&#x20; Check 3 (Proper Noun/URL Preservation): all preserved unchanged

&#x20; Check 4 (Semantic Mapping): every source paragraph has translation

IF any check fails: fix and re-run Phase C

```

&#x20;

\### P09: Document Fusion (Zero-Loss Merge)

\*\*INPUT\*\*: Ordered list of .docx files

\*\*OUTPUT\*\*: Single merged .docx

&#x20;

```

CRITICAL RULE: NEVER regenerate content. Use XML-level merge only.

&#x20;

Why: Content regeneration (reading + rewriting) ALWAYS loses content.

Observed in practice: 33-85% content loss from agent-based fusion.

XML merge copies raw nodes: mathematically impossible to lose content.

THIS IS THE SINGLE MOST IMPORTANT RULE IN THIS METHODOLOGY.

&#x20;

Use docxcompose (Python) or equivalent XML-level merge tool.

After merge: verify word count ≥ 99% of source total.

```

&#x20;

\### P10: Final Consolidation

\*\*INPUT\*\*: All deliverables, verification reports, build scripts

\*\*OUTPUT\*\*: Organized 3-directory structure with manifest and compliance artifacts

&#x20;

```

ALGORITHM:

&#x20; 1. Create 3-directory output structure (matching P00 scaffold):

&#x20;    {project\_name}/

&#x20;    ├── Deliverables/        — project outputs (docs, spreadsheets, reports)

&#x20;    ├── ProcessArtifacts/     — compliance artifacts and process records

&#x20;    │   └── BuildScripts/     — archived build/generation scripts

&#x20;    └── Sources/              — original user-provided input files

&#x20;

&#x20; 2. Move verified deliverables to Deliverables/

&#x20; 3. Copy original source files to Sources/ (preserve originals)

&#x20; 4. Generate compliance artifacts in ProcessArtifacts/:

&#x20;    a. SOURCE-INVENTORY      — P01 output: catalogued source documents

&#x20;    b. TRACEABILITY-MATRIX    — every deliverable traced to origin

&#x20;    c. SOURCE-REGISTRY        — all external sources classified L1–L5

&#x20;    d. VALIDATED-CLAIMS       — all claims assessed with status

&#x20;    e. SPOT-CHECK-GUIDE       — 10 verifiable facts for human reviewer

&#x20;    f. VERIFICATION-REPORT    — translation 4-check results (if applicable)

&#x20;    g. PROCESS-HISTORY        — chronological record of all phases and decisions

&#x20;    h. MANIFEST               — full file inventory with sizes and status

&#x20; 5. Archive build scripts in ProcessArtifacts/BuildScripts/

&#x20;    Include: README with execution order, dependencies, expected outputs

&#x20; 6. Verify all files open correctly

&#x20; 7. Generate MANIFEST with:

&#x20;    {filename, directory, size\_kb, word\_count, status, completeness\_check}

&#x20; 8. Present manifest to user for final approval

```

&#x20;

\## Master Flow

&#x20;

```

START

│

├→ P00: Project Bootstrap (auto-detect domain, create scaffold)

│     │

│     \[GATE G0: User confirms domain profile + structure]

│     │

├→ P01: Source Ingestion      \[GATE G1: inventory complete?]

├→ P02: Critical Review

│   ├→ P03: Source Validation (parallel, for flagged claims)

│                             \[GATE G2: gap list confirmed?]

├→ P04: Priority Triage       \[GATE G3: work packages approved?]

├→ FOR each tier (P0→P1→P2→P3):

│   ├→ P05: Deliverable Generation  \[GATE G4: plan approved?]

│   ├→ P06: Verification

│   ├→ P07: Gap Closure (loops back to P06)

│                             \[GATE G5: tier complete?]

│ END FOR

├→ P08: Translation (if multilingual)

├→ P09: Document Fusion (if consolidation needed)

│                             \[GATE G6: fusion verified?]

├→ P10: Final Consolidation

END

```

&#x20;

\## Master Executable Algorithm

&#x20;

```

FUNCTION execute\_research\_and\_planning(user\_request, source\_files):

&#x20; """

&#x20; Master algorithm for hallucination-free research and planning.

&#x20; Self-configuring: auto-detects domain and creates project scaffold.

&#x20; Returns: Set of verified, traceable deliverables.

&#x20; """

&#x20;

&#x20; # PHASE 0: BOOTSTRAP (self-configuration)

&#x20; domain\_profile = P00\_project\_bootstrap(user\_request, THIS\_METHODOLOGY)

&#x20; GATE(G0, user, "Is the domain profile and project structure correct?")

&#x20;

&#x20; # PHASE 1: UNDERSTAND

&#x20; inventory = P01\_source\_ingestion(source\_files)

&#x20; GATE(G1, user, "Is the source inventory complete?")

&#x20;

&#x20; # PHASE 2: ANALYZE

&#x20; gap\_list = P02\_critical\_review(inventory)

&#x20; validated\_claims = P03\_source\_validation(gap\_list.flagged\_claims)

&#x20; GATE(G2, user, "Do you confirm this gap list?")

&#x20;

&#x20; # PHASE 3: PLAN

&#x20; work\_packages = P04\_priority\_triage(gap\_list, validated\_claims)

&#x20; GATE(G3, user, "Do you approve these work packages?")

&#x20;

&#x20; # PHASE 4: EXECUTE + VERIFY (per tier)

&#x20; all\_deliverables = \[]

&#x20; FOR tier in \[P0, P1, P2, P3]:

&#x20;   IF tier not in work\_packages: CONTINUE

&#x20;   plan = generate\_execution\_plan(work\_packages\[tier])

&#x20;   GATE(G4, user, "Do you approve this plan for {tier}?")

&#x20;   deliverables = P05\_deliverable\_generation(plan, validated\_claims)

&#x20;   gap\_report = P06\_verification(plan, deliverables)

&#x20;   IF gap\_report.has\_gaps:

&#x20;     deliverables = P07\_gap\_closure(gap\_report, deliverables)

&#x20;   END IF

&#x20;   all\_deliverables.extend(deliverables)

&#x20;   GATE(G5, user, "{tier} complete. Proceed to next tier?")

&#x20; END FOR

&#x20;

&#x20; # PHASE 5: CONSOLIDATE

&#x20; IF user\_requests\_translation:

&#x20;   translated = P08\_translation(source\_docs\_needing\_translation)

&#x20;   all\_deliverables.extend(translated)

&#x20; END IF

&#x20; IF user\_requests\_fusion:

&#x20;   fused\_docs = P09\_document\_fusion(all\_deliverables)

&#x20;   GATE(G6, user, "Fusion verified at {coverage}%. Approve?")

&#x20; END IF

&#x20;

&#x20; output = P10\_final\_consolidation(all\_deliverables)

&#x20; RETURN output

END FUNCTION

&#x20;

&#x20;

FUNCTION GATE(gate\_id, user, question):

&#x20; """Mandatory checkpoint. NEVER skip or auto-approve."""

&#x20; present\_current\_state\_to\_user()

&#x20; response = ask\_user(question)

&#x20; IF response == APPROVED:

&#x20;   log(gate\_id, "PASSED", timestamp)

&#x20;   RETURN

&#x20; ELSE:

&#x20;   feedback = get\_user\_feedback()

&#x20;   apply\_feedback(feedback)

&#x20;   GATE(gate\_id, user, question)  // Retry

&#x20; END IF

END FUNCTION

&#x20;

&#x20;

FUNCTION assert\_sourced(content, source\_registry):

&#x20; """Run on every paragraph before including in a deliverable."""

&#x20; FOR each fact f in content:

&#x20;   IF f.source NOT IN source\_registry:

&#x20;     IF f.type == "number" OR f.type == "statistic":

&#x20;       REJECT(f, "Unsourced numerical claim")

&#x20;     ELSE IF f.type == "url":

&#x20;       REJECT(f, "Unvisited URL")

&#x20;     ELSE:

&#x20;       MARK(f, "\[NEEDS VERIFICATION]")

&#x20;     END IF

&#x20;   END IF

&#x20; END FOR

END FUNCTION

```

&#x20;

\## Decision Gates (7 total: G0–G6)

&#x20;

Every transition that changes scope, format, or priority requires explicit user approval. The AI agent NEVER proceeds past a gate without user confirmation. This is not optional — it is a safety mechanism against scope drift and silent errors.

&#x20;

| Gate | Location | Question |

|---|---|---|

| G0 | After P00 | Is the domain profile and project structure correct? |

| G1 | After P01 | Is the source inventory complete? |

| G2 | After P02/P03 | Do you confirm this gap list? |

| G3 | After P04 | Do you approve these work packages? |

| G4 | Before each tier's P05 | Do you approve this plan for {tier}? |

| G5 | After each tier's P06/P07 | {tier} complete. Proceed to next tier? |

| G6 | After P09 | Fusion verified at {coverage}%. Approve? |

&#x20;

\## Invariant Rules (Never Violate)

&#x20;

| ID | Rule | Rationale |

|---|---|---|

| IR-01 | Never invent data | If a statistic, URL, date, or claim cannot be verified, mark it explicitly rather than guessing. |

| IR-02 | Never regenerate to merge | Document fusion must use XML-level merge. Content regeneration always loses content. |

| IR-03 | Never skip verification | Every deliverable must pass Plan-vs-Content verification before being marked complete. |

| IR-04 | Never proceed past a gate without user approval | Decision gates exist to prevent wasted work. Respect them. |

| IR-05 | Every number must trace to a source | Financial figures, timelines, headcounts, percentages — all must cite their origin. |

| IR-06 | Assumptions must be explicit | If no source exists, mark as ASSUMPTION with rationale. Never present assumptions as facts. |

| IR-07 | Verification requires quantitative evidence | Word counts, coverage percentages, check pass/fail — never claim verification without measurement. |

| IR-08 | Error logs are permanent | Every error encountered must be logged in Process History. Never silently fix and forget. |

&#x20;

\## Error Taxonomy

&#x20;

| Error Type | Example | Detection | Prescribed Response |

|---|---|---|---|

| Content Regeneration Loss | Agent rewriting source docs during fusion → 33-85% content loss | Word count < 99% of source | NEVER regenerate content. Always use XML-level merge tools. Hard rule, no exceptions. |

| Hallucinated Data | Inventing statistics, URLs, or timelines not in sources | Source traceability check | Mark all unverified data with \[NEEDS VERIFICATION]. Never present uncertain data as fact. |

| Cross-Reference Breakage | xlsx formula pointing to wrong row after insert | Formula audit after structural change | After modifying spreadsheet structure: verify ALL formulas, not just changed cells. |

| API Mismatch | Using wrong parameter name for library function | Runtime error | Check library documentation before using APIs. Do not assume parameter names. |

| Translation Drift | Numbers, URLs, or proper nouns altered during translation | 4-check verification (P08) | Run all 4 checks. Treat any Check 2/3 failure as blocking. |

| Scope Creep | Adding unrequested sections to a deliverable | Plan-vs-Content verification (P06) | Only produce what was requested. Flag additional ideas for user decision. |

| Silent Verification | Claiming "verified" without running actual checks | Require quantitative evidence | Every verification must produce measurable evidence. "Looks good" is not verification. |

| Batch Processing Failure | Agent crash mid-batch, partial output | File count check after batch | Process sequentially when stability matters. Parallelize only when items are independent. |

&#x20;

\### Error Escalation Protocol

&#x20;

When any error from the taxonomy above is detected, apply this 3-step escalation:

&#x20;

```

ESCALATION PROTOCOL:

&#x20; 1. RETRY with same approach (max 2 attempts)

&#x20;    — Fix the specific issue, re-run the same process

&#x20;    — If same error recurs: escalate to step 2

&#x20; 2. SWITCH APPROACH

&#x20;    — Use alternative method (e.g., different library, manual steps)

&#x20;    — Document: {original\_approach, failure\_reason, new\_approach}

&#x20;    — If alternative also fails: escalate to step 3

&#x20; 3. ASK USER

&#x20;    — Present: error description, what was tried, options available

&#x20;    — User decides: skip, manual intervention, or accept partial result

&#x20;    — Log decision in Process History

&#x20;

&#x20; NEVER: silently skip a failed step or mark it as complete.

&#x20; ALWAYS: log every escalation in Process History with timestamp.

```

&#x20;

\## Traceability Matrix Template

&#x20;

Every project must maintain a live traceability matrix (in ProcessArtifacts/).

&#x20;

| Deliverable | Triggered By | Source Docs | External Sources | Verified By | Status |

|---|---|---|---|---|---|

| \[filename] | \[gap\_id or user request] | \[list of source docs used] | \[list of URLs/references] | \[P06 pass count, coverage %] | \[VERIFIED / PENDING] |

&#x20;

\## Source Registry Template

&#x20;

| ID | Source | Type | Authority Level | Access Date | Used In |

|---|---|---|---|---|---|

| S001 | \[URL or document name] | \[Official/Journal/Vendor/News] | \[L1–L5] | \[date accessed] | \[deliverable filenames] |

&#x20;

\## Process History Format

&#x20;

Every project must maintain a live Process History document (in ProcessArtifacts/). Updated in real-time, not retroactively.

&#x20;

```

PROCESS HISTORY REQUIRED SECTIONS:

&#x20; 1. Phase Log (one entry per methodology phase executed):

&#x20;    {phase\_number, phase\_name, started, completed, status,

&#x20;     inputs\_used, outputs\_produced, errors\_encountered}

&#x20; 2. Decision Log (one entry per significant decision):

&#x20;    {decision\_id, phase, description, options\_considered,

&#x20;     chosen\_option, rationale, user\_approved: Y/N}

&#x20; 3. Error Log (one entry per error, maps to Error Taxonomy):

&#x20;    {error\_id, phase, error\_type, description, escalation\_steps,

&#x20;     resolution, time\_cost}

&#x20; 4. File Timeline (one entry per file created/modified):

&#x20;    {filename, phase\_created, phases\_modified, current\_status}

&#x20;

LIVE-UPDATE RULE: Process History MUST be updated at the END of

every phase, not retroactively. If a phase fails or is restarted,

both the failure and restart are logged (never overwrite history).

This artifact is referenced by IR-08 (error logs are permanent).

```

&#x20;

\## Spot-Check Guide Format

&#x20;

Generated at P10 for human reviewer. Minimum 10 items.

&#x20;

```

Format per item:

&#x20; {item\_id, document, section, claim\_or\_fact,

&#x20;  verification\_method, expected\_result, actual\_result, PASS/FAIL}

&#x20;

Scoring threshold:

&#x20; ≥8/10 PASS = acceptable quality

&#x20; <8/10 PASS = re-verify ALL deliverables before acceptance

```

&#x20;

\## Scaling Rules

&#x20;

| Project Size | Source Documents | Deliverables | Verification Depth | Gate Strictness |

|---|---|---|---|---|

| Small (1–3 deliverables) | 1–5 sources | 1–3 outputs | Single-pass P06 sufficient | G1, G4 mandatory. Others optional. |

| Medium (4–12 deliverables) | 5–15 sources | 4–12 outputs | Multi-pass P06/P07 required | All gates mandatory. |

| Large (13+ deliverables) | 15+ sources | 13+ outputs | Multi-pass + independent re-verification | All gates + intermediate user checkpoints. |

&#x20;

