# Smart Procurement Navigator Workflows

## 1. Opportunity Screening

Goal: Convert procurement announcements, links, or screenshots into structured opportunity summaries, and flag key timeline milestones.

```text
User sends announcement/information source/screenshot
  -> ZC01 Receive opportunity information
  -> ZC02 Extract project name, procuring entity, budget, registration and submission deadlines
  -> Determine industry classification, geographic scope, budget suitability, and business fit
  -> Output opportunity summary
  -> ZC14 Set reminders for registration, Q&A, bid bond, and submission deadlines
```

Output: Opportunity summary, timeline table, preliminary recommendation, pending supplementary materials.

## 2. Bid Assessment

Goal: Determine whether to proceed with bid preparation, and list the items that decision-makers must confirm.

```text
Read opportunity summary, procurement documents, and enterprise capability materials
  -> ZC04 Extract qualification and eligibility criteria
  -> ZC08 Match enterprise qualifications, past performance, personnel allocation, and delivery capability
  -> ZC07 Assess budget reasonableness, performance period, geography, competition, and performance risks
  -> Flag manual confirmation points for quotation, commercial commitments, and final bid/no-bid decision
```

Output: Active pursuit / Cautious evaluation / Recommended pass, capability gap checklist, risk rating, decision confirmation items.

## 3. Procurement Document Analysis

Goal: Extract qualification thresholds, evaluation criteria, submission specifications, and disqualification risks from procurement documents.

```text
Upload procurement documents
  -> ZC05 Parse document structure system
  -> ZC03 Extract sections and core requirements
  -> ZC04 Extract qualification thresholds
  -> ZC05 Extract evaluation criteria
  -> ZC06 Extract submission format, seal/signature, number of copies, e-platform, and bid bond clauses
  -> ZC15 Generate clarification questions
  -> Output procurement document analysis report
```

Output: Project overview, qualification threshold matrix, evaluation criteria details, submission requirements checklist, disqualification clauses, clarification question list.

## 4. Material Structuring

Goal: Convert procurement documents, technical specifications, reference response documents, and knowledge bases into full-text-searchable structured materials.

```text
Receive procurement documents, technical specifications, reference response documents, and knowledge bases
  -> ZC17 Verify that documents have been converted to searchable text
  -> Extract evaluation tables, technical parameter tables, operational indicators, performance periods, and key data
  -> Flag scanned pages, broken tables, missing pages, image-embedded text, and non-searchable paragraphs
  -> Output material structure index and supplementary conversion checklist
```

Output: Material structure index, key data checklist, damaged/missing paragraph markers, items requiring manual re-entry.

## 5. Evaluation Model Construction

Goal: Build an accurate model of "how this project scores points."

```text
Read evaluation criteria, qualification thresholds, and submission requirements
  -> ZC18 Establish evaluation modules, score weights, scoring nature, and response strategies
  -> Differentiate between disqualifying thresholds and scored evaluation items
  -> Identify supporting evidence for objective score items
  -> ZC19 Output no-deviation index for disqualifying clauses
  -> Output evaluation score index master table and performance commitment evidence chain directory
```

Output: Evaluation model table, objective score material checklist, no-deviation index, evidence chain directory.

## 6. Bid Task Decomposition

Goal: Break down procurement requirements into executable collaborative bid tasks.

```text
Read analysis report, evaluation model, and no-deviation index
  -> ZC09 Decompose commercial, technical, quotation, qualification, seal/signature, and upload tasks
  -> Prioritize by evaluation item weight and disqualification risk
  -> Assign responsible parties and deadlines
  -> ZC14 Generate collaborative to-do items and milestone reminders
```

Output: Bid task checklist, milestones, responsible parties, deadlines, risk-priority matrix.

## 7. Response Proposal Architecture Design

Goal: Complete the response proposal skeleton, section anchors, and length planning before drafting begins.

```text
Read evaluation model, technical specifications, and past response documents
  -> ZC20 Compare reference documents, identify reusable elements and content to exclude
  -> ZC21 Output complete section structure
  -> Place a front-matter index table before the main body
  -> For each chapter, produce: "corresponding evaluation items," "chapter writing anchors," "chapter outcome evidence"
  -> Mark key chapter length and material requirements
```

Output: Complete chapter directory, front-matter index table, chapter writing anchors, length plan, material requirements.

## 8. Response Draft Generation

Goal: Produce project-specific chapter first drafts based on the evaluation model, technical specifications, and knowledge base.

```text
Read response proposal architecture and technical specifications
  -> ZC22 Develop body content by chapter
  -> Embed technical parameters, scope, indicators, specifications, and project timeline into corresponding chapters
  -> Expand specialized execution details, standard operating procedures, monthly breakdown plans, risk contingency plans, and acceptance document packages
  -> Flag cases, certificates, quotations, and commitments requiring manual supplementation
```

Output: Chapter first drafts, materials to be supplemented, evidence chain gaps, manual confirmation items.

## 9. Document Polishing and Visual Enhancement

Goal: Elevate the quality of formal response documents and add verifiable chart/diagram expressions.

```text
Read chapter first drafts
  -> ZC23 Detect templated mechanical phrasing, internal strategy language, exaggerated rhetoric, and wording unsuitable for government procurement documents
  -> Output replacement comparison suggestions and sentences still requiring manual review
  -> ZC24 Output chart/diagram placeholder index
  -> Output placeholder descriptions for technical roadmap, process flow diagrams, Gantt charts, organizational structure charts, and response flow diagrams
```

Output: Polishing report, replacement suggestions, chart/diagram index, chart/diagram placeholder checklist.

## 10. Compliance Review

Goal: Before submission, check for missing items, clause deviations, format compliance, consistency, reference residue, and disqualification risks.

```text
Upload response document draft or final version
  -> ZC12 Verify commercial material omissions
  -> ZC13 Verify format, seals/signatures, page order, numbering, and submission specifications
  -> ZC14 Verify technical/commercial response deviations and internal contradictions
  -> ZC25 Verify consistency of project name, reference number, procuring entity, location, performance period, and key data
  -> Search for reference document residue and templated phrasing prohibited terms
  -> Output pre-submission compliance review report
```

Output: Review conclusions, disqualification-level risks, general issues, corrective action plan, final review confirmation checklist.

## 11. Submission Final Review

Goal: Before final submission, verify seals/signatures, certificates, electronic documents, and bid bond item by item.

```text
Read final version and compliance review report
  -> Verify seals/signatures, original certificates, and electronic document formats item by item
  -> Verify electronic bidding platform upload specifications
  -> Confirm bid bond receipt and quotation sealed envelope specifications
  -> Output final review clearance slip and seal/signature verification table
```

Output: Final review clearance slip, seal/signature verification table, upload confirmation checklist.

## 12. Experience Capture and Knowledge Reuse

Goal: After bid conclusion, capture experience, materials, and reusable methodologies.

```text
Input bid result, process records, and review reports
  -> ZC16 Summarize key decision nodes and issues
  -> Analyze deep-rooted reasons for winning or losing
  -> Capture evaluation models, high-score sections, risk checklists, and reusable materials
  -> Update knowledge base and template library
```

Output: Retrospective report, reusable materials, template optimization suggestions, improvement checklist for next bid.

---
## v2.0.0 New Workflows

### Electronic Bidding Platform Adaptation Process
1. Identify the e-trading platform specified in the tender announcement
2. Confirm CA digital certificate mutual recognition scope
3. Remote cross-location evaluation: identify primary/secondary venue, confirm expert selection mechanism
4. Electronic seal and encrypted bid document preparation

### Remedy Mechanism Operating Process
```
Receive adverse result
  → Within 7 days: File a challenge (to the procuring entity/procurement agent)
  → Unsatisfied with challenge response
    → Within 15 days: File a complaint with the supervisory authority
    → Unsatisfied with complaint handling
      → Within 60 days: Apply for administrative reconsideration
      → Or within 6 months: File an administrative lawsuit
```

### SME Preferential Policy Application Process
1. Confirm enterprise type (MIIT Joint Enterprise Notice [2011] No. 300)
2. Declaration letter preparation ("SME Declaration Letter")
3. Price deduction calculation (6-10%)
4. Reserved share project identification
5. Consortium bid scheme design