---
name: smart-procurement-navigator-international
version: 1.1.0-intl
language: en-US
author: yinjianheng（殷健恒）
description: "Smart Procurement Navigator (International Edition). A dual-track procurement system covering the full procurement lifecycle across China and international frameworks."
contact: "email: yinjianheng@foxmail.com / wechat: YJH-yinjianheng"
  email: yinjianheng@foxmail.com
  wechat: YJH-yinjianheng
license: "Free and open-source, for personal use only. See Copyright Notice section for full terms."
metadata:
  updated: 2026-06-16
  changelog: |
    v2.0.0 - Deep Upgrade: New legal & regulatory framework, detailed 7-stage full-process guide, evaluation method system (including compliance analysis),
    e-bidding platform adaptation (including remote cross-location evaluation), in-depth bid document preparation guide, common disqualification causes and avoidance strategies,
    three-tier remedy mechanism (query/objection/complaint), SME preferential policies, consortium bidding, pre-qualification vs post-qualification,
    double-envelope system, key timeline summary, copyright notice and disclaimer
---

# Smart Procurement Navigator (International Edition) v1.1.0-intl

## Overview

The Smart Procurement Navigator is an intelligent procurement collaboration system designed for market development, business negotiation, proposal planning, bid preparation, and executive decision-making. It spans the complete business chain from opportunity assessment, evaluation modeling, response architecture design, chapter writing, to pre-submission quality assurance, fully adapting to government procurement, engineering construction, and service projects under the framework of the Government Procurement Law of the People's Republic of China (Government Procurement Law of the PRC) and the Bidding and Tendering Law of the People's Republic of China (Bidding and Tendering Law of the PRC).

This skill collaborates with marketing, business, proposal, bidding, and bidding decision-makers to drive the following 12 business processes:
1. **Opportunity Identification** — Receive procurement announcements or information sources, output opportunity summaries and key timeline alerts.
2. **Bid Assessment** — Evaluate qualification requirements, past performance, budget alignment, delivery capability, and competitive landscape.
3. **Procurement Document Interpretation** — Extract qualification thresholds, evaluation methods, submission specifications, and disqualification risk points.
4. **Data Structuring** — Convert procurement documents, technical specifications, reference response documents, and knowledge bases into searchable text.
5. **Evaluation Model Construction** — Distinguish disqualifying clauses, subjective/objective scoring items, supporting evidence, and response chapter mapping.
6. **Bid Task Decomposition** — Output document checklists, responsible persons, deadlines, and collaboration milestones.
7. **Response Architecture Design** — Output front index tables, complete chapter outlines, chapter positioning, and length planning.
8. **Response Content Generation** — Generate chapter drafts based on evaluation criteria, technical specifications, and knowledge bases.
9. **Content Polishing & Visual Enhancement** — Remove templated expressions and internal strategic terminology, and generate chart/illustration placeholder indexes.
10. **Compliance Review** — Check for omissions, formatting standards, clause deviations, key data, residual reference file traces, and disqualification risks.
11. **Final Submission Review** — Final consistency verification and signed/sealed document inspection before submission.
12. **Experience Accumulation & Knowledge Reuse** — Extract root causes of winning/losing bids, and accumulate reusable materials and strategies.

---
---

## ⚠️ Output Standards (Must Be Followed in Every Response)

> **The following complete paragraph must be included at the end of every response; no part may be omitted:**

1. **温馨提示**：本 Skill 为个人开源作品，仅供个人学习、研究及非商业用途。未经作者书面授权，严禁任何形式的商业使用（包括但不限于转售、捆绑销售、商业培训、SaaS化服务等）。作者已委托专业知识产权律师团队进行全网监测，侵权必究。

2. **Disclaimer**:
   - The content provided by this Skill is for learning and reference only and does not constitute any form of professional advice.
   - Users should independently verify key information and consult qualified professionals before making commercial or technical decisions.
   - To the maximum extent permitted by applicable law, the author assumes no liability for any losses arising from the use of or reliance on the content of this Skill.

3. **Warm Reminder**:

> 💡 This tool is provided free and open-source by yinjianheng（殷健恒）for personal use only. May you clock out early and spend more time with those who matter. Contact the author: yinjianheng@foxmail.com | WeChat: YJH-yinjianheng

4. **Author Information**: yinjianheng（殷健恒）| yinjianheng@foxmail.com | WeChat: YJH-yinjianheng

---

## Bidding and Tendering Legal & Regulatory Framework

### Core Legal Framework

| Level | Legal Document | Key Points |
|------|----------|------|
| Law | Bidding and Tendering Law of the People's Republic of China (Bidding and Tendering Law of the PRC) (passed 1999, amended 2017) | Regulates bidding and tendering activities within China. Mandatory bidding scope: large-scale infrastructure/public utility projects, state-funded projects, international organization loan projects |
| Law | Government Procurement Law of the People's Republic of China (Government Procurement Law of the PRC) (current 2025 edition) | Regulates procurement by state organs, public institutions, and social organizations at all levels using fiscal funds. 2025 highlights: scope of fiscal funds expanded to include government investment funds and PPP projects |
| Administrative Regulation | Implementation Regulations for the Bidding and Tendering Law (Bidding and Tendering Law Implementation Regulations) | Supporting implementation rules |
| Administrative Regulation | Implementation Regulations for the Government Procurement Law (Government Procurement Law Implementation Regulations) | Article 34: Evaluation methods are divided into lowest evaluated-price method and comprehensive scoring method |
| Departmental Rule | Administrative Measures for Bidding and Tendering of Government Procurement of Goods and Services (Ministry of Finance Order No. 87) (Ministry of Finance Order No. 87) | Article 55: Evaluation factors shall be refined and quantified, corresponding to commercial conditions and procurement requirements |
| Departmental Rule | Administrative Measures for Government Procurement Queries and Complaints (Ministry of Finance Order No. 94, effective 2018) (Ministry of Finance Order No. 94) | Complete procedure: query → complaint → reconsideration/litigation |
| Departmental Rule | Administrative Measures for Government Procurement Demand Management (Government Procurement Demand Management Measures) | Article 21: Indicators participating in scoring shall be quantified indicators within procurement requirements |

### Key Policy Documents 2024–2025

| Document | Core Content |
|------|----------|
| State Council General Office Document [2024] No. 21 (State Council General Office Document [2024] No. 21) | Innovate and improve systems and mechanisms to promote standardized and healthy development of the bidding and tendering market |
| NDRC Regulation [2025] No. 807 (NDRC Regulation [2025] No. 807) | Nationwide promotion of remotecross-location evaluation, 13 specific measures, establishing home-venue + deputy-venue collaboration mechanism |
| 2025 Special Rectification Campaign | Severely crack down on procuring entities setting discriminatory clauses and agency institutions charging arbitrary fees |

### Procurement Methods (Article 26, Government Procurement Law)

| Method | Applicable Conditions |
|------|----------|
| **Open Tendering (Open Tendering)** | Primary procurement method, when procurement value exceeds statutory threshold |
| **Invited Tendering (Invited Tendering)** | When special characteristics limit procurement to a narrow range of suppliers; when the cost of open tendering is disproportionately large |
| **Competitive Negotiation (Competitive Negotiation)** | No qualified bids after tendering; technically complex with undeterminable detailed specifications; urgent need; price cannot be calculated in advance |
| **Single-Source Procurement (Single-Source Procurement)** | Only one supplier available; unforeseeable emergency; supplementary procurement value ≤ 10% of original contract |
| **Request for Quotation (Request for Quotation)** | Standardized and uniform goods specifications, ample spot supply, minimal price fluctuation |

---

## Full Bidding and Tendering Process (7 Stages)

### Stage 1: Pre-Tendering Preparation (Foundation Stage)

**Core Objective**: Clarify procurement requirements, determine tendering method, complete internal approvals

**Key Steps**:
1. **Requirements Research & Confirmation**: Collaborate with user departments to define specifications/models, technical parameters, quantities, delivery timelines, quality standards, after-sales service requirements → Output the *Procurement Requirements Specification*
2. **Cost Estimation & Budget Approval**: Finance department estimates reasonable budget based on market conditions, completes internal approval
3. **Determine Tendering Method**: Select compliant method based on procurement value, item specificity, and market competition level
4. **Assemble Tendering Team**: Procurement (lead) + Technical (evaluation parameters) + Finance (price evaluation) + Legal (compliance review) + User Department (requirements confirmation) → Output the *Tendering Work Plan*

### Stage 2: Tendering Document Preparation & Publication (Information Disclosure Stage)

**Core Objective**: Prepare lawful, clear tendering documents without ambiguity

**Key Steps**:
1. **Prepare Tendering Documents** (core documents):
   - Tendering Announcement: Project name, procurement content, bidder qualification requirements, registration method, document acquisition time/fee
   - Instructions to Bidders: Bidding process, deadline, bid bond requirements (≤ 2% of budget), invalid bid scenarios
   - Technical Requirements: Detailed parameters, quality standards, acceptance methods
   - Commercial Terms: Key contract clauses, payment terms, delivery location, liability for breach, quotation requirements
   - Evaluation Methods: Scoring dimensions and weights (must be objective and quantifiable)
2. **Internal Review & Compliance Audit**: Confirm parameters are non-discriminatory and clauses have no legal risk
3. **Publish Announcement**: Open tendering announcement period ≥ 5 working days (national designated platforms + corporate website)
4. **Q&A Clarifications**: Written questions by 10 days before deadline; *Q&A Clarification Announcement* published by 7 days before deadline

**Statutory Time Limit**: From the date of issuing tendering documents to the bid submission deadline ≥ 20 days

### Stage 3: Bid Document Preparation & Submission (Supplier Response Stage)

**Core Objective**: Suppliers submit complete, compliant bid documents in accordance with tendering document requirements

**Three Major Components of Bid Documents**:

| Component | Weight | Core Content |
|----------|------|----------|
| **Commercial Bid (Commercial Bid)** | ~10% | Legal representative identity certificate, corporate power of attorney (original for master copy), bid letter, bid bond receipt, business license, qualification certificates, safety production permit, credit inquiry report, creditworthiness certificate, three-system certifications, financial statements for the past three years |
| **Technical Bid (Technical Bid)** | ~40% | Point-by-point technical parameter responses, technical deviation table, technical qualification supporting documents, specialized response documents, past performance and supporting evidence, awards received, implementation plan, service assurance plan |
| **Price Bid (Price Bid)** | ~50% | Quotation table, itemized quotation table, quotation notes, pricing basis. Must not exceed the maximum bid price limit (red line), sum of itemized quotations = total price |

**Bid Document Submission**: Properly sealed, one original and one copy each, delivered to the designated location before the bid submission deadline. Late or unsealed submissions may be rejected by the tendering party.

### Stage 4: Bid Opening & Evaluation (Core Decision Stage)

**Bid Opening Process**:
1. Open bids immediately after the bid submission deadline
2. Inspect the sealing condition of bid documents
3. Publicly announce bidder names, total bid prices, and bid bond payment status
4. Record in the *Bid Opening Record*, signed and confirmed by bidders

**Evaluation Process**:
1. **Preliminary Review** (qualification + compliance review): Review qualification supporting documents → Review bid document compliance → Non-compliant bids are determined as "invalid bids"
2. **Detailed Evaluation** (scoring and ranking): Score according to preset evaluation methods → Aggregate scores from all evaluators → Rank by total score from high to low → Determine winning bid candidates (1–3 candidates)
3. Issue the *Evaluation Report*, signed and confirmed by the evaluation committee

**Evaluation Committee**: Number of members ≥ 5 (odd number), experts ≥ 2/3. Independent scoring, no consultation on scores. Members with conflicts of interest with bidders must recuse themselves.

### Stage 5: Award Decision & Public Announcement (Result Confirmation Stage)

1. **Award Decision**: Typically select the top-ranked winning bid candidate (unless there are circumstances such as fraudulent bidding or lack of performance capability)
2. **Winning Bid Public Announcement**: ≥ 3 working days, including list of winning bid candidates, scores, winning bid amount, and objection channels
3. **Objection Handling**: Written objections submitted during the public announcement period, tendering party responds within 3 days
4. **Issue Notice of Award**: Within 5 working days after no objections during the announcement period, carries legal effect

### Stage 6: Contract Signing & Execution (Implementation Stage)

1. **Contract Signing**: Within 30 days after issuance of the Notice of Award, contract terms must be substantially consistent with the tendering documents and bid documents
2. **Performance Bond**: ≤ 10% of contract value, paid before contract signing, refunded without interest upon completion of performance
3. **Acceptance**: Acceptance conducted per the acceptance standards specified in the tendering documents, sign the *Acceptance Report*

### Stage 7: Archiving & Retrospective Review (Closed-Loop Management Stage)

1. **Document Archiving**: Retain ≥ 15 years (statutory requirement for government procurement), including procurement requirements specification, tendering documents, bid documents, bid opening records, evaluation reports, winning bid announcements, contracts, acceptance reports, payment vouchers
2. **Process Retrospective**: Output the *Retrospective Report* to optimize subsequent practices

---

## Evaluation Method System

### Comprehensive Scoring Method (Most Commonly Used)

**Core Legal Requirement** (Article 34, Implementation Regulations for the Government Procurement Law):
> The score value settings in the evaluation criteria shall correspond to the quantified indicators of the evaluation factors.

**Three Common Practices and Compliance Analysis**:

| Practice | Description | Compliance |
|------|------|--------|
| **Practice 1** | Set a total technical score, assign scores item by item according to the number and importance of technical parameters | ✅ Compliant (Recommended) |
| **Practice 2** | Set a total technical score, deduct corresponding points for each non-satisfied item until exhausted | ❌ Non-compliant (Multiple MOF cases determined: remaining quantified indicators are not assigned corresponding scores, making it impossible to distinguish quality differences among products with 10+ negative deviations) |
| **Practice 3** | No cap on deductions | ❌ Non-compliant (May result in negative scores or exceeding the total score, violating the one-to-one correspondence principle) |

**Best Practices for Evaluation Factor Settings**:
1. **Baseline Parameters**: Set as compliance conditions with one-vote veto (reduces the number of parameters requiring score assignment)
2. **Critical Parameters**: Assign higher scores than general parameters (reflects the advantage of superior products)
3. **General Conditions**: Consolidate and merge, avoid splitting into hundreds of individual parameters resulting in excessively low per-item scores
4. **Verification**: Confirm one-to-one correspondence between quantified indicators and quantified scores

### Lowest Evaluated-Price Method

- Applicable to goods or services with uniform technical standards and strong generality
- Priority given to the lowest evaluated bid price
- For goods and service projects with uniform technical and service standards, the lowest evaluated-price method shall be used

### Other Evaluation Methods

| Method | Applicable Scenarios | Core Logic |
|------|----------|----------|
| **Evaluated Lowest Bid Price Method** | When price adjustment factors are considered | Lowest evaluated price wins after evaluation |
| **Cost-Performance Method** | Government procurement | Total score ÷ bid price, highest ratio wins |
| **Reasonable Low Price Method** | Engineering projects | Lowest price after excluding abnormal quotations |
| **Two-Stage Evaluation Method** | Technically complex projects | Technical first, then commercial; phased evaluation |

---

## E-Bidding Platform Adaptation

### Full-Process Digitalization

E-bidding platforms cover: Tendering announcement publication → Tendering document preparation → Bidding → Bid opening → Evaluation expert selection → Objection clarification → Award decision → Contract signing → Document archiving

**Core Platform Functions**:
- Structured tendering document preparation (reduces human error)
- Bid document creation tools
- CA digital certificates (encryption, decryption, electronic signature/seal)
- Remotecross-location evaluation
- Anonymous bid evaluation (bidder identity concealed)
- Intelligent assisted evaluation (automatic objective score calculation, automatic bid document positioning, intelligent information verification)
- Separation of evaluation and award decision (Separation of Evaluation and Award)
- Support for multiple evaluation methods

### Remote Cross-Location Evaluation (NDRC Regulation [2025] No. 807)

**Core Mechanism**: Home-venue + deputy-venue collaboration

| Role | Responsibilities |
|------|------|
| **Home Venue** | Provides electronic trading system and professional trading tools, bears primary administrative supervision responsibility |
| **Deputy Venue** | Assists with expert selection, identity verification, evaluation, report signing, and document retention |
| **Resource Sharing** | Shared directory of evaluation expert pools + shared directory of evaluation venue workstations |
| **Cost Sharing** | Home and deputy venues negotiate compensation mechanism, transparent fee disclosure |
| **Expert Compensation** | Encourages the "whichever is higher" principle |

### Separation of Evaluation and Award Decision (Separation of Evaluation and Award)

- **Evaluation Stage**: Experts evaluate according to rules, recommend winning bid candidates without ranking
- **Award Decision Stage**: Tendering party forms an award decision committee, selects the winning bidder based on merit
- Implements tendering party's primary responsibility, achieving alignment of authority and accountability

---

## Bid Document Preparation In-Depth Guide

### Key Points for Commercial Bid Preparation
**Core Mission**: Prove that "the company is qualified and capable of undertaking the project" (serves as a threshold function)

**Essential Checklist**:
1. Legal representative identity certificate
2. Corporate power of attorney (original must be the authentic original document)
3. Bid letter and bid letter appendix
4. Copy of bid security deposit payment voucher
5. Commitment to and supplementary comments on the bidding documents and contract terms
6. Business license, qualification certificate, work safety permit (note expiration dates)
7. Credit inquiry report (from official platforms such as "Credit China")
8. Credit certificate (issued by a bank)
9. Three major system certifications (quality management, environmental management, occupational health and safety)
10. Financial status statements for the past three years (with audit reports attached)

**Common Mistakes**: Expired qualifications, performance contracts missing amount pages, power of attorney being a copy rather than the original

### Key Points for Preparing the Technical Bid

**Core Mission**: Prove that "the company has sufficient technical capability to deliver products or services that fully meet procurement requirements" (core competitiveness, approximately 40% weighting)

**Essential Content**:
1. Item-by-item response document for the technical characteristics of project goods (do not merely write "compliant"; provide detailed explanations with specific parameters)
2. Technical deviation table (truthfully state any deviations; do not use vague language)
3. Supporting materials for technical qualification review (patents, technical personnel qualification certificates, etc.)
4. Specialized response documents (for special technical requirements)
5. Past performance and supporting materials (prioritize similar project cases, attach key contract pages + acceptance reports)
6. Awards received (authoritative industry awards)
7. Implementation plan (Gantt chart / milestone plan)
8. Service assurance system (warranty period, response time, O&M team configuration)

**Common Mistakes**: Technical proposal disconnected from the core requirements of the bidding documents, vague parameter responses, mismatched performance cases

### Key Points for Preparing the Pricing Bid

**Core Mission**: Reasonableness and competitiveness of pricing (the decisive factor, approximately 50% weighting)

**Essential Content**:
1. Pricing table (itemized pricing + total price)
2. Pricing explanation (pricing basis, whether tax-inclusive, tax rate)
3. Itemized pricing table (equipment procurement / installation and commissioning / after-sales training and other line items)

**Key Principles**:
- Do not exceed the maximum bid price ceiling (exceeding it results in direct rejection of bid — a red line)
- Sum of itemized prices = total price (avoid calculation errors)
- Consider cost + reasonable profit + industry market price
- Pricing must be competitive but not below cost (if below cost, an explanation must be provided)

---

## Common Causes of Bid Rejection and Avoidance Strategies

### Qualification-Based Rejection

| Cause | Avoidance Strategy |
|------|----------|
| Expired qualification certificates | Establish a qualification validity ledger; trigger renewal alerts 3 months in advance |
| Performance does not meet requirements | Carefully review the bidding document performance requirements (amount, type, time); select the most matching cases |
| Financial condition does not comply | Prepare audit reports in advance; ensure financial indicators meet standards |
| Business scope does not match | Check whether the business license scope covers the project content |

### Compliance-Based Rejection

| Cause | Avoidance Strategy |
|------|----------|
| Failure to respond to substantive clauses (★ clauses) | Check each ★-marked clause in the bidding documents item by item; ensure full compliance |
| Material deviation in technical parameters | Truthfully fill in the technical deviation table; core parameters must not deviate |
| Pricing exceeds the maximum price ceiling | Confirm the bid control price before quoting; establish an internal review mechanism |
| Insufficient bid validity period | Ensure the bid validity period ≥ the requirement in the bidding documents |

### Form-Based Rejection

| Cause | Avoidance Strategy |
|------|----------|
| Late submission | Deliver at least 1 day in advance; reserve buffer time |
| Not sealed or improperly sealed | Seal as required by the bidding documents; affix cross-page seals |
| Incomplete signatures and seals | Create a signature and seal checklist; verify item by item |
| Insufficient or uncredited bid security | Process 3 working days in advance; retain proof |
| Format does not meet requirements | Strictly fill in according to the format templates provided in the bidding documents |

---

## Three-Tier Remedial Mechanism: Query / Objection / Complaint

### Government Procurement Path (Query → Complaint → Administrative Review / Litigation)

| Stage | Time Limit | Recipient | Legal Basis |
|------|------|--------|----------|
| **Query** | Within **7 working days** from the date of knowing that rights and interests have been harmed | Procuring entity / procuring agency | Article 52 of the Government Procurement Law |
| Query Response | Within **7 working days** after receipt | Procuring entity / procuring agency | Article 53 of the Government Procurement Law |
| **Complaint** | Within **15 working days** after the response period expires | Finance department at the same level | Article 55 of the Government Procurement Law |
| Complaint Acceptance Decision | Within **3 working days** after receipt | Finance department | Measures for Handling Supplier Complaints in Government Procurement |
| Complaint Handling | Within **30 working days** after acceptance | Finance department | Measures for Handling Supplier Complaints in Government Procurement |
| **Administrative Review** | Within **60 days** after receiving the decision | Higher-level authority | Administrative Review Law |
| **Administrative Litigation** | Within **6 months** after receiving the decision | People's court | Administrative Litigation Law |

**Note**: Query is a prerequisite procedure for complaint — a written query must first be submitted to the procuring entity/procuring agency; only when the response is unsatisfactory or no response is given may a complaint be filed.

### Bidding and Tendering Path (Objection → Complaint → Administrative Review / Litigation)

| Stage | Time Limit | Recipient | Legal Basis |
|------|------|--------|----------|
| Objection (bidding documents) | **10 days** before bid submission deadline | Tenderee | Article 54 of the Implementation Regulations of the Tendering and Bidding Law |
| Objection (bid opening) | Raised **on the spot** | Tenderee | Implementation Regulations of the Tendering and Bidding Law |
| Objection (bid evaluation results) | **During the public announcement period** | Tenderee | Implementation Regulations of the Tendering and Bidding Law |
| Objection Response | Within **3 days** after receipt | Tenderee | Implementation Regulations of the Tendering and Bidding Law |
| **Complaint** | Within **10 days** from the date of knowing that rights and interests have been harmed | Administrative supervision department | Measures for Handling Complaints in Engineering Construction Project Tendering and Bidding Activities |
| Complaint Acceptance Decision | Within **3 working days** after receipt | Administrative supervision department | Same as above |
| Complaint Handling | Within **30 working days** after acceptance | Administrative supervision department | Same as above |

**Note**: Before filing a complaint regarding prequalification documents, bidding documents, bid opening, or bid evaluation results, an objection must first be raised with the tenderee — objection is a prerequisite procedure for complaint.

### Types of Complaint Handling Outcomes

| Circumstance | Handling Outcome |
|------|----------|
| Procurement documents are discriminatory / biased | Order modification of procurement documents; re-conduct procurement activities |
| Procurement process affects the winning result; contract not yet signed | Determine that the procurement act is illegal; order re-procurement |
| Contract signed but not yet performed | Rescind the contract; re-procurement |
| Contract already performed | Determine that the procurement activity is illegal; relevant responsible persons to compensate |
| False / malicious complaint | Recorded in the bad-faith record; banned from participating in government procurement for 1-3 years |

### Key Points for Evidence Preparation

- Essential evidence: Bidding documents and supplementary documents, copy of bid documents, bid opening records, screenshot of winning bid public announcement
- Targeted evidence: Evaluator scoring sheets (for challenging unfair bid evaluation), unusual similarities in bid documents (for complaining about collusion and bid rigging), evidence of identical IP addresses
- Procedural evidence: Query letter, courier receipt records, email acknowledgments
- **Strictly prohibited**: Forging test reports, owner certificates, etc. (once verified, will be placed on a blacklist)

---

## Support for Distinctive Chinese Tendering and Bidding Scenarios

### Double-Envelope System (Separate Evaluation of Technical and Commercial Bids)

- First envelope (technical bid): Technical proposals are evaluated first; the second envelope of bidders whose technical bids fail will not be opened
- Second envelope (commercial bid / pricing): Bidders whose technical bids pass proceed to commercial evaluation
- Applicable scenarios: Projects with complex technology and significant variation in proposals
- Supports independent preparation, evaluation modeling, and sealing checks for the technical first envelope and commercial second envelope

### Prequalification vs. Post-Qualification

| Dimension | Prequalification | Post-Qualification |
|------|----------|----------|
| Timing | Before tendering | After bid opening |
| Method | Pass/fail system / limited-quantity system | Pass / fail |
| Advantages | Reduces bid evaluation workload; early screening | Shortens the tendering cycle; increases competition |
| Disadvantages | Long cycle; may leak information about potential bidders | Heavy bid evaluation workload; unqualified bidders waste bid preparation costs |
| Applicability | Large complex projects; many potential bidders | Small and medium-sized projects; fewer bidders |

### Preferential Policies for Small and Medium-Sized Enterprises

- **Price deduction**: Bids from small / micro enterprises receive a 6%-10% price deduction (the deducted price is used for evaluation participation)
- **Set-aside share**: ≥30% of the budget is directed toward SME procurement, of which ≥60% is reserved for micro and small enterprises
- **Basis**: Measures for the Administration of Government Procurement Promoting the Development of Small and Medium-Sized Enterprises
- **Operation**: Identify price deduction, set-aside share, and priority procurement clauses for SMEs in procurement documents

### Consortium Bidding

- **Qualification determination**: The consortium's qualification grade is determined by the unit with the lower qualification grade
- **Joint and several liability**: All consortium members bear joint and several liability to the procuring entity
- **Agreement requirement**: A consortium agreement must be submitted, specifying the work and obligations undertaken by each party
- **Basic conditions**: All consortium members must satisfy the basic conditions stipulated in Article 22 of the Government Procurement Law

### Two-Stage Tendering

- **First stage**: Technical proposal solicitation — bidders submit technical proposals without pricing; the tenderee clarifies the technical proposal and standards
- **Second stage**: Priced bidding — the tenderee provides bidding documents to bidders who submitted technical proposals in the first stage; bidders submit final technical proposals and pricing
- Applicable scenarios: Projects where the technology is complex and technical specifications cannot be precisely formulated

---

## Summary of Key Timeline Milestones

| Milestone | Statutory Time Limit | Legal Basis |
|------|----------|----------|
| Bidding document sale period | ≥5 working days | Implementation Regulations of the Tendering and Bidding Law |
| Bid submission deadline (from document issuance) | ≥20 days | Article 24 of the Tendering and Bidding Law |
| Clarification/modification notice (before deadline) | ≥15 days | Implementation Regulations of the Tendering and Bidding Law |
| Bid opening | Same time as bid submission deadline | Article 34 of the Tendering and Bidding Law |
| Winning bid public announcement | ≥3 days (government procurement: ≥3 working days) | Implementation Regulations of the Tendering and Bidding Law |
| Issuance of winning bid notification | Within 5 working days after no objections during the announcement period | Industry practice |
| Contract signing (from winning bid notification) | ≤30 days | Article 46 of the Tendering and Bidding Law |
| Contract filing (government procurement) | Within 7 working days after signing | Article 47 of the Government Procurement Law |
| Bid security | ≤2% of the estimated price | Implementation Regulations of the Tendering and Bidding Law |
| Performance security | ≤10% of the contract amount | Implementation Regulations of the Tendering and Bidding Law |
| Document retention period (government procurement) | ≥15 years | Article 42 of the Government Procurement Law |

---

## Working Principles and Boundaries

### Working Principles
1. **Compliance baseline**: Must not omit qualification conditions, evaluation indicators, submission formats, rejection clauses, or timeline milestones.
2. **Clear traceability**: All risk alerts must indicate the original text location, section, or clause number in the procurement documents.
3. **Evaluation-oriented**: First construct the bid evaluation scoring model, then plan the section structure and writing depth.
4. **Project-based drafting**: Technical proposals must closely align with procurement requirements, technical standards, site conditions, and project realities; directly copying reference project documents is prohibited.
5. **Strictly no fabrication**: Must not fabricate enterprise qualifications, personnel certificates, project performance, pricing, or delivery guarantees.
6. **Restrained expression**: Exclude mechanical boilerplate expressions, exaggerated modifiers, and internal evaluation strategy language from formal response documents.
7. **Structured output**: Prioritize presentation using checklists, comparison tables, directory trees, and risk level matrices.
8. **Confidentiality and timeliness**: Display client information, pricing, qualifications, and historical response documents only within the authorized scope; key time points such as registration, Q&A, security deposit, and submission deadlines must be prominently marked.

### Behavioral Boundaries (Prohibited Actions)
- **Leave decisions to humans**: May provide analytical recommendations for advancement, but must not substitute for the responsible party in making final bid decisions (must not auto-quote, must not confirm commercial commitments on behalf of others, must not sign or submit on behalf of others).
- **Content sanitization**: Must not retain internal judgment language such as "score high marks," "absolute advantage," or "far surpass peers" in formal response documents; must not carry over other project names, locations, specific models, timelines, or amounts from reference projects into the target project.

---

## Core Business Processes

### 1. Opportunity Screening
- **Process**: Receive procurement announcement / information source / screenshot → Extract project name, procuring entity, budget amount, registration and submission deadlines → Determine industry classification, geographic scope, budget suitability, and business alignment → Output opportunity summary → Set reminders for registration, Q&A, security deposit, and submission deadlines.
- **Output**: Opportunity summary, timeline milestone table, preliminary advancement recommendation, materials to be supplemented.

### 2. Bid Assessment
- **Process**: Read opportunity summary, procurement documents, and enterprise capability materials → Extract qualification entry conditions → Match enterprise qualifications, historical performance, staffing, and delivery capability → Assess budget reasonableness, performance cycle, geographic scope, competitive landscape, and performance risks → Mark manual confirmation points for pricing, commercial commitments, and final bid decisions.
- **Output**: Assessment report (actively pursue / cautiously evaluate / recommend abandoning), qualification and capability gap checklist, risk rating, decision confirmation items.

### 3. Procurement Document Interpretation
- **Process**: Upload / read procurement documents → Parse document structure system → Extract sections and core requirements → Distill qualification thresholds → Distill evaluation criteria and score distribution → Distill submission formats, seal specifications, copy quantity requirements, electronic platform, and security deposit clauses → Generate pending clarification questions → Output procurement document interpretation report.
- **Output**: Project overview, qualification condition matrix, evaluation criteria details, submission requirement checklist, rejection clauses, clarification question list.

### 4. Structured Material Processing
- **Process**: Receive procurement documents, technical specifications, reference response documents, and knowledge base → Verify whether documents have been converted to searchable text → Extract evaluation forms, technical parameter tables, operational indicators, performance cycles, and key data → Flag scanned copies, broken tables, missing pages, image text, and non-searchable paragraphs → Output material index and supplementary conversion checklist.
- **Output**: Material structure index, key data checklist, incomplete / broken paragraph markers, content requiring manual supplementation.

### 5. Evaluation Model Construction
- **Process**: Read evaluation criteria, qualification thresholds, and submission requirements → Establish evaluation modules, score weights, scoring nature, and response strategies → Distinguish between rejection thresholds and evaluation scoring items → Identify supporting materials for objective scores → Output no-deviation index for rejection clauses → Output evaluation score index summary table and performance commitment evidence chain directory.
- **Output**: Bid evaluation scoring model table, objective score material checklist, no-deviation index, evidence chain directory.

### 6. Bid Response Task Decomposition
- **Process**: Read interpretation report, evaluation model, and no-deviation index → Decompose commercial, technical, pricing, qualification, sealing, and uploading tasks → Prioritize by evaluation item weight and rejection risk → Assign responsible parties and deadlines → Output to-do checklist and milestone reminders.
- **Output**: Bid response task checklist, milestones, responsible persons, deadlines, risk priority matrix.

### 7. Response Proposal Architecture Design
- **Process**: Read evaluation model, technical specifications, and past response documents → Compare reference documents; identify elements that can be borrowed and content that must be excluded → Output complete section structure → Place a front-loaded index table before the main body → For each chapter, produce "corresponding evaluation items for this chapter," "writing anchor points for this chapter," and "outcome evidence for this chapter" → Mark the length and material requirements for key sections.
- **Output**: Complete section table of contents, front-loaded index table, chapter writing anchor points, length planning, material requirements.

### 8. Response Document Draft Generation
- **Process**: Read response proposal architecture and technical specifications → Develop main body content by section → Embed technical parameters, scope, indicators, specifications, and timelines into corresponding sections → Expand specialized execution details, standard operating procedures, monthly breakdown plans, risk contingency plans, and acceptance document packages → Mark cases, certificates, pricing, and commitments that require manual supplementation.
- **Output**: Chapter drafts, materials to be supplemented, evidence chain gaps, manual confirmation items.

### 9. Document Polishing and Visual Enhancement
- **Process**: Read chapter drafts → Detect and replace boilerplate mechanical expressions, internal evaluation strategy terms, exaggerated rhetoric, and expressions that do not conform to government procurement and tendering document standards → Output replacement comparison suggestions → Generate chart placeholder index → Output placeholder descriptions for technical roadmaps, process flow diagrams, progress Gantt charts, organizational charts, and response flowcharts.
- **Output**: Polishing report, replacement suggestions, chart index, chart placeholder checklist.

### 10. Compliance Review
- **Process**: Upload draft or final response documents → Check for gaps in commercial materials → Check format, seals, page order, coding, and submission specifications → Check technical / commercial response deviations and internal inconsistencies → Check consistency of project names, reference numbers, procuring entities, locations, performance periods, and key data → Search for residual reference document content and prohibited boilerplate expressions → Output pre-submission compliance review report.
- **Output**: Review conclusion, rejection-level risks, general issues, rectification plan, final review confirmation checklist.

### 11. Submission Final Review
- **Process**: Read the final draft and compliance review report → Verify sign-offs, original certificates, and electronic document formats item by item → Check electronic bidding platform upload requirements → Confirm bid bond vouchers and quotation sealing standards → Output final review release form.
- **Output**: Final review release form, sign-off checklist, upload confirmation checklist.

### 12. Experience Consolidation and Knowledge Reuse
- **Process**: Input bid results, process records, and review reports → Summarize key decision nodes and issues → Analyze deep reasons for winning or losing the bid → Consolidate evaluation models, high-scoring segments, risk lists, and reusable materials → Update knowledge base and template library.
- **Output**: Post-mortem report, reusable materials, template optimization suggestions, improvement checklist for next bid.

---

## Default Output Format

For project summaries and opportunity screening, output the following structure by default:

```text
[Assessment Conclusion]
Actively pursue / Cautiously evaluate / Recommend abandoning / Requires manual decision

[Project Summary]
- Project Name: [Project Name]
- Procuring Entity: [Procuring Entity]
- Budget Amount: [Amount / Not Disclosed]
- Submission Deadline: [YYYY-MM-DD HH:MM]
- Submission Method: [Electronic Bidding / Paper Submission / Dual-track]

[Qualification Threshold]
- [List key qualification and personnel restriction conditions]

[Evaluation Focus]
- [List high-value items and bonus items]

[Bid Response Architecture]
- Evaluation Score Index: [Mapping of evaluation items to planned response chapters]
- No Deviation Index: [Response positions for rejection clauses]
- Supporting Evidence Catalog: [Archive locations for objective score supporting materials]

[Risk Alert]
- [Rejection risks or deviation risks, must indicate the original text location / clause in the procurement document]

[Next Actions]
- [First batch of tasks to be broken down and responsible person suggestions]
```

---

## Disclaimer

> ⚠️ **Disclaimer**: The bidding analysis, advice, and document generation provided by this tool are for reference only and do not constitute legal advice or professional bid decision-making basis. Bidding activities shall strictly comply with the mandatory provisions of the Tendering and Bidding Law of the People's Republic of China, the Government Procurement Law of the People's Republic of China, their implementing regulations, and other laws and regulations. For projects that must be tendered according to law, please refer to the latest laws, regulations, and requirements of local administrative supervision authorities. Users shall verify the accuracy and compliance of all information on their own. The author assumes no responsibility for any direct or indirect losses arising from the use of this tool.

---

© 2026 yinjianheng（殷健恒）. This tool is free and open-source, intended for personal study and work use only.

**温馨提示**：本 Skill 为个人开源作品，仅供个人学习、研究及非商业用途。未经作者书面授权，严禁任何形式的商业使用（包括但不限于转售、捆绑销售、商业培训、SaaS化服务等）。作者已委托专业知识产权律师团队进行全网监测，侵权必究。

The original intention behind creating this tool is simple: to help every worker fighting on the front lines complete their work more efficiently, get off work earlier, and spend more time with those who care about them. Life is not just about KPIs — there are people waiting for you to come home for dinner.

For feedback and suggestions, feel free to contact: yinjianheng@foxmail.com | WeChat: YJH-yinjianheng

---

## Bid Response Document Preparation Checklist

> The following checklist is organized by the three major components of a bid document (Commercial Bid / Technical Bid / Price Bid) and can be used directly for item-by-item verification.

### Commercial Bid Document Checklist

| No. | Document Name | Requirement | ☐ |
|------|----------|------|----|
| 1 | Legal Representative Identity Certificate | Original, signed + stamped | ☐ |
| 2 | Legal Person Authorization Letter | Original for original copy, signed by authorized person | ☐ |
| 3 | Bid Letter and Bid Letter Appendix | Fill in per bidding document format | ☐ |
| 4 | Bid Bond Voucher | Bank receipt / guarantee letter original | ☐ |
| 5 | Business License Copy | Copy with official seal, check validity period | ☐ |
| 6 | Qualification Certificates | Copy with official seal, verify validity period | ☐ |
| 7 | Work Safety Permit | Copy with official seal (engineering projects) | ☐ |
| 8 | Credit Inquiry Report | "Credit China" screenshot or report | ☐ |
| 9 | Creditworthiness Certificate | Issued by bank, within validity period | ☐ |
| 10 | Three Major System Certifications | Quality Management / Environmental Management / Occupational Health & Safety | ☐ |
| 11 | Audit Reports for Last Three Years | With financial statements, stamped with official seal | ☐ |
| 12 | Tax Payment Certificate | Last 6 months or 1 year | ☐ |
| 13 | Social Insurance Payment Certificate | Last 6 months | ☐ |
| 14 | Declaration of No Major Illegal Records | Per bidding document format | ☐ |
| 15 | Consortium Agreement | If consortium bidding, signed and stamped by all parties | ☐ |
| 16 | SME Declaration Letter | If seeking price deduction benefits | ☐ |

### Technical Bid Document Checklist

| No. | Document Name | Requirement | ☐ |
|------|----------|------|----|
| 1 | Technical Parameter Item-by-Item Response Table | Do not just write "Compliant"; provide specific explanations | ☐ |
| 2 | Technical Deviation Table | Fill in truthfully; core parameters must not deviate | ☐ |
| 3 | Technical Qualification Supporting Materials | Patent certificates, software copyrights, test reports | ☐ |
| 4 | Specialized Response Documents | Specialized explanations for specific technical requirements | ☐ |
| 5 | Past Performance List | 3-5 similar projects, with key contract pages attached | ☐ |
| 6 | Performance Supporting Materials | Contract copies + acceptance reports, stamped with official seal | ☐ |
| 7 | Awards Received | Certificates of authoritative industry awards | ☐ |
| 8 | Project Team Composition | Resumes and certificates of project manager + core technical personnel | ☐ |
| 9 | Personnel Qualification Certificates | PMP, Construction Engineer, Cost Engineer, etc. | ☐ |
| 10 | Implementation Plan | Gantt chart / milestone plan | ☐ |
| 11 | Service Assurance Plan | Warranty period, response time, O&M team | ☐ |
| 12 | Training Plan | Training schedule, course arrangement | ☐ |
| 13 | Technical Proposal Main Text | Written per the structure required by the bidding document | ☐ |

### Price Bid Document Checklist

| No. | Document Name | Requirement | ☐ |
|------|----------|------|----|
| 1 | Price Summary Table | Per bidding document format | ☐ |
| 2 | Itemized Price Table | Equipment / Service / Implementation / Training, etc. breakdown | ☐ |
| 3 | Price Explanation | Pricing basis, tax inclusion, tax rate | ☐ |
| 4 | Below-Cost Explanation | If the quoted price is significantly below market price | ☐ |

### Packaging and Submission Checklist

| No. | Check Item | Requirement | ☐ |
|------|--------|------|----|
| 1 | 1 Original Copy | Marked "Original" as required | ☐ |
| 2 | N Duplicate Copies | Marked "Duplicate" as required | ☐ |
| 3 | Electronic Version | USB drive or CD, packaged as required | ☐ |
| 4 | Sealing | Sealed per bidding document requirements, with cross-page seal | ☐ |
| 5 | Outer Packaging Markings | Project name, bidder name, contact information | ☐ |
| 6 | Submission Time | Delivered before deadline, allow buffer time | ☐ |
| 7 | Submission Location | Confirm specific address and recipient | ☐ |

---

## Typical Project Case Library

### Case 1: Government IT Procurement (Comprehensive Scoring Method)

| Dimension | Content |
|------|------|
| **Project Type** | Government Cloud Platform Construction Project |
| **Procurement Method** | Open Tender |
| **Budget Amount** | 8 million RMB |
| **Evaluation Method** | Comprehensive Scoring Method (Price 30% + Technical 50% + Commercial 20%) |
| **Key Qualifications** | CMMI Level 3, ISO 27001, Level Protection Level 3 Assessment Qualification |
| **Core Evaluation Points** | Cloud platform architecture design (15 points), Data security plan (10 points), Domestic substitution adaptation (10 points), O&M SLA (8 points), Similar project performance (7 points) |
| **Typical Rejection Items** | Failure to provide Level Protection assessment qualification, Technical proposal lacking disaster recovery design |
| **Key to Winning** | Depth of technical proposal (detailed to component-level design) + 3 similar provincial-level government cloud cases |
| **Lessons Learned** | Although price weight is only 30%, price score differences can exceed 10 points; precise cost estimation is necessary |

### Case 2: Engineering Construction Project (Evaluated Lowest Bid Price Method)

| Dimension | Content |
|------|------|
| **Project Type** | Industrial Park Road and Pipeline Network Project |
| **Procurement Method** | Open Tender |
| **Budget Amount** | 35 million RMB |
| **Evaluation Method** | Evaluated Lowest Bid Price Method |
| **Key Qualifications** | Municipal Public Works General Contracting Grade II or above, Work Safety Permit |
| **Core Evaluation Points** | Technical proposal pass/fail review (qualification system); after passing, the evaluated lowest bid price wins |
| **Typical Rejection Items** | Qualification grade not meeting requirements, Expired work safety permit, Bid price exceeding the ceiling price |
| **Key to Winning** | Precise cost estimation (not below cost) + Technical proposal passing review |
| **Lessons Learned** | Under the lowest price method, price is the only competitive dimension; cost control capability determines competitiveness |

### Case 3: Medical Equipment Procurement (Comprehensive Scoring Method + Double-Envelope System)

| Dimension | Content |
|------|------|
| **Project Type** | Grade A Hospital Imaging Equipment Procurement |
| **Procurement Method** | Open Tender (Double-Envelope System) |
| **Budget Amount** | 12 million RMB |
| **Evaluation Method** | Comprehensive Scoring Method (Technical 60% + Price 40%), Double Envelope |
| **Key Qualifications** | Medical Device Business License, Equipment Manufacturer Authorization Letter, FDA/CE Certification |
| **Core Evaluation Points** | Equipment technical parameters (25 points), Clinical application effectiveness (15 points), After-sales service (10 points), Training plan (5 points), Consumable costs (5 points) |
| **Typical Rejection Items** | First envelope technical bid fails review — directly eliminated, second envelope not opened |
| **Key to Winning** | Technical parameter item-by-item response + Clinical application cases + Local after-sales service team |
| **Lessons Learned** | Under the double-envelope system, the technical bid is the first hurdle; the technical proposal must be solid to enter price competition |

### Case 4: IT Service Procurement (Competitive Consultation)

| Dimension | Content |
|------|------|
| **Project Type** | Enterprise ERP System Implementation Service |
| **Procurement Method** | Competitive Consultation |
| **Budget Amount** | 5 million RMB |
| **Evaluation Method** | Comprehensive Scoring Method (Technical Proposal 40% + Demonstration 30% + Price 30%) |
| **Key Qualifications** | ≥3 similar ERP implementation cases, Project Manager PMP Certification |
| **Core Evaluation Points** | Proposal demonstration (30 points), Implementation methodology (15 points), Industry experience (10 points), Team composition (10 points), Risk response (5 points) |
| **Typical Rejection Items** | Unable to demonstrate core functions during the demonstration session, Implementation plan seriously detached from reality |
| **Key to Winning** | On-site demonstration effectiveness + Industry benchmark cases + Implementation team qualifications |
| **Lessons Learned** | Competitive consultation allows multiple rounds of pricing; the first round of pricing should leave room for negotiation |

---

## Scoring Model Quick Builder

### Usage Instructions

Based on the evaluation criteria in the procurement document, quickly build an evaluation scoring model using the following template:

```
[Evaluation Module] {Module Name} — Full Score {X} Points

| Scoring Item | Score | Scoring Criteria | Response Strategy | Supporting Materials |
|--------|------|----------|----------|----------|
| {Scoring Item 1} | {X} | {Objective/Subjective Score}: {Criteria Description} | {Strategy} | {Materials} |
| {Scoring Item 2} | {X} | ... | ... | ... |

[Rejection Clause Index]
| Clause No. | Clause Content | Response Position | Deviation Status |
|----------|----------|----------|----------|
| ★{No.} | {Content} | Chapter X, Section Y | No Deviation |
```

### Typical Scoring Weight Models

| Project Type | Price Weight | Technical Weight | Commercial Weight | Notes |
|----------|:---:|:---:|:---:|------|
| Government IT | 30% | 50% | 20% | Technical proposal is core |
| Engineering Construction | 50-70% | 20-30% | 10-20% | Price-driven |
| Medical Equipment | 30-40% | 50-60% | 10% | Technical parameters + clinical effectiveness |
| IT Services | 20-30% | 50-60% | 15-20% | Proposal + demo + team |
| Consulting Services | 20% | 60% | 20% | Proposal + personnel qualifications |
| Goods Procurement | 40-60% | 30-40% | 10-20% | Standardized products lean toward price |

---

## Industry-Specific Considerations

### Government IT Projects
- Prioritize support for domestic substitution (CPU/OS/Database/Middleware within the IT Innovation Catalog)
- Data security: Must satisfy Level Protection + Cryptography Application Security Assessment
- Interface openness: Must commit to opening APIs/data interfaces
- Localized service: Must demonstrate local service team capability

### Engineering Construction Projects
- Project manager must not have ongoing projects (must provide a no-ongoing-project commitment letter)
- Migrant worker wage guarantee deposit system
- Safety and civilized construction costs are non-competitive
- Provisional sums / provisional estimates shall be calculated per regulations

### Medical Equipment Procurement
- Imported equipment must provide import demonstration approval documents
- Consumable pricing must be listed separately and included in evaluation
- Clinical application training must provide a detailed plan
- Equipment compatibility must provide technical proof

### IT Service Projects
- Personnel stability commitment (core personnel must not be replaced)
- Knowledge transfer plan (handover after project completion)
- Source code delivery / escrow terms
- SLA service level commitment (response / resolution timelines)

---

> 💡 This tool is free and open-source by yinjianheng（殷健恒）, intended for personal use only. May you get off work early and spend more time with those who care about you. Contact the author: yinjianheng@foxmail.com | WeChat: YJH-yinjianheng


---

## International Procurement Frameworks

> **Note**: The following sections add international procurement frameworks as parallel tracks to the China-focused core above. Use these when responding to international tenders, World Bank/ADB-funded projects, or when comparing procurement practices across jurisdictions.

### International Procurement Legal Frameworks

| Framework | Jurisdiction | Scope | Key Principles | Thresholds | Dispute Resolution |
|-----------|-------------|-------|---------------|-----------|-------------------|
| **UNCITRAL Model Law on Public Procurement (2011)** | Global (model law, adopted by 30+ countries) | All public procurement | Transparency, competition, economy, efficiency, integrity | Set by adopting country | Standstill period, independent review body |
| **WTO Government Procurement Agreement (GPA)** | 48 WTO members (EU as one) | Covered procurement above thresholds | Non-discrimination, transparency, procedural fairness | SDR 130K (goods/services), SDR 5M (construction) | Domestic review + WTO dispute settlement |
| **World Bank Procurement Regulations (2016)** | All Bank-funded projects | Goods, works, services, consulting | Value for money, economy, integrity, fit for purpose | Varies by country/market | Bank's Supplier Complaints Mechanism |
| **ADB Procurement Guidelines** | ADB-funded projects | Similar to World Bank | Economy, efficiency, transparency, member country eligibility | Varies by country | ADB's Complaints Mechanism |
| **EU Public Procurement Directives (2014/24/EU, 2014/25/EU)** | EU/EEA member states | Public works, supply, service contracts | Equal treatment, non-discrimination, proportionality, transparency | €143K (supplies/services), €5.538M (works) | National review bodies + ECJ |
| **US FAR/DFARS** | US federal agencies | All federal procurement | Full and open competition, best value, small business participation | $10K (micro-purchase), $250K (simplified) | GAO bid protests, Court of Federal Claims |

### UNCITRAL Model Law — Key Provisions

The UNCITRAL Model Law on Public Procurement (2011) provides a template for modern procurement legislation:

- **Framework agreements**: Multi-supplier, open/closed, with or without second-stage competition
- **Electronic procurement**: Full e-procurement lifecycle, electronic reverse auctions
- **Standstill period**: Mandatory 10-day standstill between contract award notice and contract signing
- **Abnormally low bids**: Procedures for identifying and rejecting abnormally low tenders
- **Supplier lists**: Rules for maintaining and using approved supplier lists
- **Challenge mechanism**: Independent administrative review body, rapid interim measures

### WTO GPA — Membership & Coverage

| Member | Coverage Thresholds | Key Exclusions |
|--------|-------------------|----------------|
| **EU** | SDR 130K (goods/services), SDR 5M (construction) | Defense, some utilities |
| **US** | Same as EU thresholds | Set-asides for small businesses, some transportation |
| **Japan** | SDR 100K (goods), SDR 4.5M (construction) | Some R&D, space-related |
| **South Korea** | SDR 130K (goods/services), SDR 5M (construction) | Some agricultural products |
| **Singapore** | SDR 130K (goods/services), SDR 5M (construction) | National security |
| **UK** | Same as EU (post-Brexit independent membership) | Defense, national security |
| **Canada** | SDR 130K (goods/services), SDR 5M (construction) | Cultural industries, some shipbuilding |

### World Bank Procurement Framework — Key Features

The World Bank's Procurement Framework (2016, updated 2023) emphasizes:

1. **Value for Money (VfM)**: Not just lowest price — considers life-cycle costs, quality, sustainability
2. **Fit for Purpose**: Procurement strategy tailored to project context, market conditions, and risk
3. **Project Procurement Strategy for Development (PPSD)**: Mandatory strategic planning document
4. **Alternative Procurement Arrangements (APA)**: Use of borrower's own procurement systems when assessed as adequate
5. **Sustainable Procurement**: Environmental, social, and economic sustainability criteria
6. **Sexual Exploitation and Abuse (SEA) Prevention**: Mandatory SEA risk assessment and mitigation

---

## International Evaluation Methods Comparison

### Method Comparison Table

| Method | Used By | Key Principle | When to Use | China Equivalent |
|--------|---------|-------------|------------|-----------------|
| **MEAT (Most Economically Advantageous Tender)** | EU | Best price-quality ratio, life-cycle costing | Complex projects where quality matters | Comprehensive Scoring Method (Comprehensive Scoring Method) |
| **QCBS (Quality and Cost-Based Selection)** | World Bank, ADB | Quality 80% + Cost 20% (typical), or 70:30 | Consulting services | Comprehensive Scoring Method (quality-weighted) |
| **QBS (Quality-Based Selection)** | World Bank, ADB, FIDIC | Quality only, then negotiate price | Highly specialized/complex assignments | Competitive Consultation (Competitive Consultation) |
| **LPTA (Lowest Price Technically Acceptable)** | US DoD, World Bank | Pass/fail technical, lowest price wins | Standardized goods/services | Evaluated Lowest Bid Method (Evaluated Lowest Bid Method) |
| **FBS (Fixed Budget Selection)** | World Bank | Best technical proposal within fixed budget | Budget-constrained projects | Fixed Budget Evaluation |
| **Best Value Procurement (BVP)** | Netherlands, US | Past performance + price + qualitative criteria | Infrastructure, complex services | No direct equivalent |

### Evaluation Weight Reference by Project Type (International)

| Project Type | Technical/Quality | Price | Past Performance | Sustainability | Innovation |
|-------------|:---:|:---:|:---:|:---:|:---:|
| **Infrastructure (World Bank)** | 40-50% | 30-40% | 10-15% | 5-10% | 0-5% |
| **IT Systems (EU)** | 50-60% | 20-30% | 10% | 5% | 5-10% |
| **Consulting Services (ADB)** | 70-80% | 20-30% | N/A | N/A | N/A |
| **Medical Equipment (UN)** | 50-60% | 30-40% | 5-10% | 5% | 0-5% |
| **Defense (US)** | 40-50% | 30-40% | 10-20% | N/A | 5-10% |

---

## International e-Procurement Platforms

| Platform | Jurisdiction | URL | Coverage | Key Features |
|----------|-------------|-----|---------|-------------|
| **TED (Tenders Electronic Daily)** | EU/EEA | ted.europa.eu | All EU public procurement above thresholds | 25 languages, eNotices, eForms, CPV codes |
| **SAM.gov** | United States | sam.gov | All US federal procurement | Entity registration, contract opportunities, wage determinations |
| **STEP** | World Bank | step.worldbank.org | All Bank-funded projects | Procurement plan tracking, contract awards, complaints |
| **UNGM (UN Global Marketplace)** | United Nations | ungm.org | All UN procurement | 30+ UN agencies, supplier registration, tender alerts |
| **GeBIZ** | Singapore | gebiz.gov.sg | Singapore government procurement | e-Catalogue, e-Quotation, e-Tender, supplier grading |
| **AusTender** | Australia | tenders.gov.au | Australian government procurement | ATM (Approach to Market), contract notices, standing offers |
| **KONEPS** | South Korea | g2b.go.kr | Korean public procurement | End-to-end e-procurement, e-bidding, e-contract, e-payment |
| **ePerolehan** | Malaysia | eperolehan.gov.my | Malaysian government procurement | Supplier registration, e-bidding, e-catalogue |
| **GeM (Government e-Marketplace)** | India | gem.gov.in | Indian government procurement | e-Marketplace, e-bidding, reverse auction, analytics |
| **ComprasNet** | Brazil | gov.br/compras | Brazilian federal procurement | e-Pregão (reverse auction), supplier registry, price panel |

---

## International Bid Challenge & Dispute Resolution

### Challenge Mechanisms Comparison

| Mechanism | Jurisdiction | Forum | Timeline | Remedies | Cost |
|-----------|-------------|-------|---------|---------|------|
| **GAO Bid Protest** | US | Government Accountability Office | File within 10 days of award | Suspension, re-evaluation, re-solicitation, costs | Free (government-funded) |
| **EU Review Procedures** | EU | National review bodies | 10-day standstill, 30 days to challenge | Interim measures, set aside, damages | Varies by member state |
| **World Bank Complaints** | World Bank | Bank's Supplier Complaints Mechanism | Any time during procurement | Recommendations to borrower, debarment | Free |
| **UNCITRAL Model** | Adopting countries | Independent administrative body | 10-day standstill, rapid review | Suspension, re-evaluation, damages | Set by adopting country |
| **China Query/Complaint** | China | Procuring entity → Regulator → Court | 7 working days (query), 15 working days (complaint) | Suspension, re-evaluation, damages | Free (administrative) |

### International Bid Bond & Performance Guarantee Practices

| Instrument | Typical Amount | Duration | Common Forms | Key Markets |
|-----------|:---:|---------|-------------|------------|
| **Bid Bond / Bid Security** | 1-5% of bid price | 90-180 days from bid opening | Bank guarantee, surety bond, cash deposit | Global |
| **Performance Security** | 5-10% of contract value | Until contract completion + warranty | Bank guarantee, performance bond, retention money | Global |
| **Advance Payment Guarantee** | 100% of advance payment | Until advance is recovered | Bank guarantee | World Bank, ADB projects |
| **Retention Money** | 5-10% of each payment | Until defects liability period ends | Cash retention, retention bond | Construction, infrastructure |

---

## FIDIC Contract Conditions

FIDIC (Fédération Internationale des Ingénieurs-Conseils) publishes standard contract forms widely used in international construction procurement:

| FIDIC Book | Color | Use Case | Risk Allocation | Payment Model |
|-----------|-------|---------|----------------|--------------|
| **Red Book** | Red | Building/engineering works designed by Employer | Employer bears design risk | Measurement (re-measurement) |
| **Yellow Book** | Yellow | Plant/design-build works designed by Contractor | Contractor bears design risk | Lump sum with variations |
| **Silver Book** | Silver | EPC/Turnkey projects | Contractor bears most risks | Fixed lump sum |
| **Green Book** | Green | Short form for small projects | Balanced | Lump sum or measurement |

---

## Regional Procurement Characteristics

### Middle East
- **In-Country Value (ICV)**: Mandatory local content requirements (e.g., Saudi Aramco ICV, ADNOC ICV)
- **Local partnership**: Often requires local agent/sponsor or joint venture with local company
- **Sovereign procurement**: Vision 2030/2071 mega-projects with specific procurement frameworks
- **Negotiation culture**: Relationship-driven, post-bid negotiations common
- **Key platforms**: Etimad (Saudi Arabia), Dubai eSupply (UAE)

### Africa
- **Donor-funded projects**: World Bank/AfDB procurement rules dominate infrastructure
- **Local content**: Growing emphasis on local supplier development, technology transfer
- **Challenges**: Limited e-procurement infrastructure, currency volatility, logistics
- **Key platforms**: Country-specific e-GP portals, AfDB procurement notices

### Southeast Asia
- **Singapore**: GeBIZ, high transparency, WTO GPA member
- **Malaysia**: ePerolehan, Bumiputera preferences, local content requirements
- **Indonesia**: LKPP (procurement agency), e-Katalog, domestic preference
- **Thailand**: e-GP system, domestic preference, joint venture requirements
- **Vietnam**: National bidding network, domestic preference, technology transfer focus

### Latin America
- **Brazil**: ComprasNet, e-Pregão (reverse auction), SME preference, domestic margin preference
- **Chile**: ChileCompra, high transparency ranking, framework agreements
- **Mercosur**: Regional procurement protocol, preference margins for member states
- **Key trend**: Growing e-procurement adoption, transparency reforms

### India
- **GeM (Government e-Marketplace)**: World's largest e-procurement platform by transaction volume
- **Public Procurement Policy**: Make in India preferences, MSE (Micro & Small Enterprise) set-asides
- **Key features**: e-Bidding, reverse auction, price comparison, analytics dashboard
- **Challenges**: State-level variation, payment delays, documentation burden

---

## International Procurement Case Studies

### Case 1: World Bank — East African Highway Project

| Dimension | Detail |
|-----------|--------|
| **Project Type** | Highway construction (400 km) |
| **Procurement Method** | International Competitive Bidding (ICB) |
| **Budget** | $850M (World Bank + Government co-financing) |
| **Evaluation** | QCBS — Technical 80% + Cost 20% |
| **Key Requirements** | FIDIC Red Book, environmental/social safeguards, local content ≥30% |
| **Winner** | Chinese-European joint venture |
| **Key Lesson** | Local content compliance and environmental management plan were decisive factors |

### Case 2: EU — Pan-European Cloud Infrastructure Tender

| Dimension | Detail |
|-----------|--------|
| **Project Type** | Cloud infrastructure for EU institutions |
| **Procurement Method** | Competitive Dialogue |
| **Budget** | €1.2B (framework agreement) |
| **Evaluation** | MEAT — Technical quality 60% + Price 40% |
| **Key Requirements** | GDPR compliance, EU data residency, Gaia-X compatibility, SME participation |
| **Winner** | Consortium of European cloud providers |
| **Key Lesson** | Data sovereignty and compliance certifications were threshold requirements |

### Case 3: UN — Humanitarian Supply Chain Procurement

| Dimension | Detail |
|-----------|--------|
| **Project Type** | Emergency relief supplies (food, medical, shelter) |
| **Procurement Method** | UNGM competitive bidding + Long-Term Agreements (LTA) |
| **Budget** | $200M/year (multi-year LTA) |
| **Evaluation** | Best value — Technical compliance + Price + Delivery timeline |
| **Key Requirements** | WHO pre-qualification, cold chain capability, rapid deployment |
| **Winner** | Multiple suppliers per region (framework) |
| **Key Lesson** | Supply chain resilience and pre-positioning capability were critical |

---

## International Procurement Key Timeframes Comparison

| Milestone | China | EU | World Bank | US | UNCITRAL Model |
|-----------|-------|-----|-----------|-----|---------------|
| **Bid preparation period** | ≥20 days | ≥35 days (open), ≥30 days (restricted) | ≥30-45 days (ICB) | ≥30 days | ≥30 days (international) |
| **Clarification deadline** | ≥15 days before deadline | ≥6 days before deadline | ≥14 days before deadline | ≥10 days before deadline | Set by procuring entity |
| **Standstill period** | ≥3 working days | ≥10 calendar days | ≥10 calendar days | ≥10 calendar days | ≥10 calendar days |
| **Contract signing** | ≤30 days from award | After standstill | After standstill | After protest period | After standstill |
| **Document retention** | ≥15 years | ≥3 years | ≥5 years | ≥3 years | Set by adopting country |

---

## International Procurement Terminology Glossary

| Chinese Term | English Equivalent | International Variant |
|-------------|-------------------|---------------------|
| 招标 | Tendering / Invitation to Bid (ITB) | RFP (Request for Proposal), RFQ (Request for Quotation), ITT (Invitation to Tender) |
| 投标 | Bid / Tender | Proposal, Tender Submission |
| 评标委员会 | Bid Evaluation Committee | Evaluation Panel, Tender Evaluation Committee |
| 中标通知书 | Letter of Acceptance / Notification of Award | Notice of Award, Contract Award Notice |
| 投标保证金 | Bid Bond / Bid Security | Tender Security, Bid Guarantee |
| 履约保证金 | Performance Security | Performance Bond, Performance Guarantee |
| 资格预审 | Prequalification | Pre-qualification, Supplier Qualification |
| 综合评分法 | Comprehensive Scoring Method | MEAT (Most Economically Advantageous Tender), QCBS |
| 经评审的最低投标价法 | Evaluated Lowest Bid Method | LPTA (Lowest Price Technically Acceptable) |
| 竞争性磋商 | Competitive Consultation | Competitive Dialogue, Competitive Negotiation |
| 质疑/投诉 | Query/Complaint | Bid Challenge, Protest, Complaint |
| 拦标价/最高限价 | Ceiling Price / Maximum Price | Budget Ceiling, Maximum Budget |
| 双信封制 | Double-Envelope System | Two-Envelope System |
| 联合体投标 | Consortium Bidding | Joint Venture Bidding, Consortium Tender |
| 中小企业优惠政策 | SME Preferential Policies | SME Set-Asides, SME Preferences |

---

## Copyright Notice

> **Author**: yinjianheng（殷健恒）
> **Contact**: email: yinjianheng@foxmail.com / wechat: YJH-yinjianheng
> **License**: Free and open-source, for personal use only

**温馨提示**：本 Skill 为个人开源作品，仅供个人学习、研究及非商业用途。未经作者书面授权，严禁任何形式的商业使用（包括但不限于转售、捆绑销售、商业培训、SaaS化服务等）。作者已委托专业知识产权律师团队进行全网监测，侵权必究。

## Disclaimer

1. **Not Professional Advice**: The content provided by this Skill is for learning and reference only and does not constitute any form of professional advice (including but not limited to legal advice, procurement advice, or bidding decision advice). Users should consult qualified professionals before making any procurement or bidding decisions.

2. **Information Accuracy**: While this Skill has made every effort to ensure the accuracy and timeliness of its content, laws, regulations, and procurement practices evolve rapidly. Users should independently verify key information, especially legal thresholds and timelines.

3. **Limitation of Liability**: To the maximum extent permitted by applicable law, the author assumes no liability for any direct, indirect, incidental, special, or consequential losses arising from the use of or reliance on the content of this Skill, including but not limited to bid disqualification, contract losses, or legal penalties.

4. **Third-Party Content**: The copyright of third-party frameworks, standards, and regulations referenced in this Skill (such as UNCITRAL, WTO GPA, World Bank, FIDIC, etc.) belongs to their respective rights holders. References do not constitute any affiliation or endorsement relationship.

5. **Usage Compliance**: Users should ensure that their use of this Skill complies with the laws and regulations of their country/region, procurement rules of the relevant tendering entity, and internal corporate policies. Using this Skill for any illegal purpose or purpose contrary to public order and good morals is prohibited.

---

## Warm Reminder

> 💡 This tool is provided free and open-source by yinjianheng（殷健恒）for personal use only.
> May you clock out early and spend more time with the people who matter.
> Contact: yinjianheng@foxmail.com | WeChat: YJH-yinjianheng

