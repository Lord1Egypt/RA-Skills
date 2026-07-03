# Bidding & Procurement Case Library / Procurement Case Library

> This directory contains complete cases from real-world bidding and procurement scenarios, showcasing the full chain from opportunity identification to final submission and review. Cases C01 and C02 are reconstructed from real bidding announcements released by the China Government Procurement Network (ccgp.gov.cn) and the Qingdao Public Resources Trading Center (ggzy.qingdao.gov.cn) respectively.

## Case List

| No. | Case Name | Project Type | Core Methodology |
|------|----------|----------|-----------|
| C01 | Qinghai Provincial Government Cloud Platform 2025 Annual Service Procurement | Government Procurement / Service | Single source procurement + Sub-contract packages + Expert evaluation |
| C02 | Qingdao Metro Line 7 Phase II Weak Current Systems Procurement & Integration | Engineering Construction / Goods | Prequalification (Limited quantity system) + Consortium bidding + Open tendering |

---

## Case C01: Qinghai Provincial Government Cloud Platform 2025 Annual Service Procurement

### Opportunity Identification

**Procurement announcement source**: China Government Procurement Network (ccgp.gov.cn, Single source procurement announcement released on February 14, 2026)
**Project No.**: QZCDZ (Service) 2026-171
**Project Name**: 2025 Annual Provincial Government Cloud Platform Resource Service Fee
**Procuring entity**: General Office of Qinghai Provincial People's Government (at its own level)
**Contact**: Mr. Li Ming, 0971-8252135
**Procurement method**: Single source procurement
**Total budget**: RMB 68.20 million (Telecom package: RMB 35.496086 million; Mobile package: RMB 14.076966 million; Unicom package: RMB 18.626948 million)
**Project overview**: Since its establishment, the Qinghai Provincial Government Cloud Platform has been built and operated by the three major telecom operators, each managing their own government cloud resource pools and hosting the business systems of provincial government departments at all levels. This project is the renewal procurement of cloud resource services for the 2025 fiscal year, covering IaaS/PaaS layer resources including computing, storage, network, and security, as well as operational support services.

**Key Timeline**:

| Milestone | Date | Description |
|------|------|------|
| Single source procurement announcement released | 2026-02-13 | 15-day public notice period |
| Announcement deadline | 2026-02-27 | Proceed to procurement procedure if no objections |
| Award result announcement | 2026-06-13 | QZCDZ (Service) 2026-171 |

**Procurement method explanation**: This project adopts single source procurement on the grounds of "only one supplier available" — the Qinghai Provincial Government Cloud Platform was built separately by the three major telecom operators, with heterogeneous architectures and independent data across resource pools. Migration costs are extremely high and pose business interruption risks, satisfying Article 31, Paragraph 1 of the Government Procurement Law.

### Bid Assessment

**Single source procurement vs Open tendering**: Single source procurement does not involve competitive evaluation; the core lies in "price negotiation" and "service confirmation." The supplier must justify the necessity of renewal, the reasonableness of pricing, and service continuity.

**Sub-contract package structure**:

| Package No. | Item Name | Proposed Supplier | Budget amount (RMB) | Award amount (RMB) | Supplier Address |
|:---:|------|------|:---:|:---:|------|
| Package 1 | Telecom Government Cloud Services | China Telecom Corporation Limited Qinghai Branch | 35,496,086 | 35,270,000 | No. 29 Jinhui Road, Xining, Qinghai |
| Package 2 | Mobile Government Cloud Services | China Mobile Communications Group Qinghai Co., Ltd. | 14,076,966 | 14,030,000 | No. 48 Kunlun East Road, Xining, Qinghai |
| Package 3 | Unicom Government Cloud Services | Unicom Digital Technology Co., Ltd. Qinghai Branch | 18,626,948 | 18,500,000 | 9F, No. 6 Pufeng Road, Chengxi District, Xining, Qinghai |

**Total award amount across all packages**: RMB 67.80 million (saving RMB 0.40 million vs. budget of RMB 68.20 million, savings rate 0.59%)

**Evaluation experts**: Zhang Hong, Qi Mingxing, Liu Peng (procuring entity representative)

**Assessment conclusion**: ✅ Single source procurement — each of the three operators secured their respective package. Award amounts are all slightly below budget (each package declined by approximately 0.5%-0.7%), reflecting some room for price negotiation. Renewal certainty is high for such projects, but attention must be paid to the following year's budget approval and fiscal affordability assessment.

### Procurement Document Interpretation

**Procurement method characteristics**: Single source procurement does not use comprehensive scoring. The core document is the "Single Source Procurement Document," which includes:

| Element | Description |
|------|------|
| Procurement requirements | Continuation of the previous year's government cloud services, including cloud computing, cloud storage, cloud networking, cloud security, and other resources plus operations |
| Service term | Fiscal year 2025 (annual service contract) |
| Service standards | See details in the award result announcement annex (including Service Level Agreement metrics, availability commitments, security compliance requirements) |
| Price negotiation | Negotiate the final transaction price within the budget control price |
| Acceptance method | Quarterly/annual service quality assessment tied to fee payment |

**Compliance essentials for single source procurement**:

| Compliance Step | Requirement | Basis |
|------|------|------|
| Public notice | No fewer than 5 working days | Article 38, Administrative Measures for Non-Tender Government Procurement Methods |
| Expert evaluation | Professional evaluation of single source justification | MOF Order No. 74 |
| Approval | If the amount meets open tendering thresholds, submit to the finance department for approval | Article 27, Government Procurement Law |
| Record-keeping | Full procurement process records archived | Article 42, MOF Order No. 74 |

**Disqualification clauses (Bid rejection risks)**:

| Clause | Risk Level | Mitigation Strategy |
|------|:---:|------|
| Valid objection received during the public notice period | 🔴 One-vote veto | Ensure single source justification is sufficient and supporting materials are complete |
| Supplier quotation exceeds budget | 🔴 One-vote veto | Keep quotation within each package's budget |
| Supplier qualifications do not meet requirements | 🔴 One-vote veto | Verify business license, cloud service qualifications, etc. in advance |
| Service plan fails to meet procurement requirements | 🟡 Negotiation failure | Respond to each procurement requirement item by item with supporting evidence |

### Evaluation Model Construction

**Negotiation points for single source procurement**:

| Negotiation Dimension | Weight | Response Focus | Supporting Materials |
|------|:---:|------|------|
| Price reasonableness | Core | Cross-reference unit prices of similar government cloud services in other provinces | Price comparison table, cost breakdown |
| Service continuity | Critical | Seamless migration plan for existing services, data security commitment | Previous year's service report, SLA achievement records |
| Technical capability | Essential | Cloud platform architecture, resource expansion capability, security compliance | Level 3 classified protection certification, Trusted Cloud certification |
| Operational support | Essential | 7×24 operations, emergency response, major event support | Operations team roster, emergency plan |

### Bid Response Task Breakdown

| Task | Responsible Person | Deadline | Dependency |
|------|--------|:---:|------|
| Single source justification materials preparation | Technical Lead | Before public notice | Previous year's service data |
| Price negotiation plan | Commercial Manager | Before public notice | Cost accounting |
| Service plan update | Technical Lead | Before public notice | Procurement requirement analysis |
| Negotiation response materials | Project Manager | 3 days before negotiation | All materials compiled |
| Internal review | Bid Committee | 1 day before negotiation | All tasks completed |
| Negotiation meeting | Commercial Manager + Technical Lead | Per notification | Internal review passed |

### Response Proposal Architecture Design

**Front-loaded index table**:

| Negotiation Point | Chapter | Core Scoring Point | Evidence |
|------|----------|------|:---:|
| Price reasonableness | Chapter 1 Quotation Statement | Unit price not increased YoY, lower than neighboring provinces | Price comparison table |
| Service continuity | Chapter 2 Service Plan | Zero-downtime migration, data integrity assurance | Previous year's SLA report |
| Technical capability | Chapter 3 Technical Proposal | Cloud-native architecture, elastic expansion, security compliance | Classified protection certificate + Trusted Cloud certification |
| Operational support | Chapter 4 Operations Plan | 7×24 operations, 15-minute response, major event support | Operations team + emergency plan |
| Innovative services | Chapter 5 Value-Added Services | Data middle platform, AI capability exposure | Case studies + demonstration |

**Page budget**: Approximately 80 pages total (including charts). Quotation statement: 10%, Service plan: 30%, Technical proposal: 30%, Operations plan: 20%, Value-added services: 10%

### Quotation Strategy

**Price negotiation model** (each package negotiated independently):

| Package No. | Budget (RMB 10k) | Award Price (RMB 10k) | Decline Rate | Strategy Analysis |
|:---:|:---:|:---:|:---:|------|
| Package 1 (Telecom) | 3,549.61 | 3,527.00 | 0.64% | Largest share, limited bargaining room |
| Package 2 (Mobile) | 1,407.70 | 1,403.00 | 0.33% | Smallest share, least decline |
| Package 3 (Unicom) | 1,862.69 | 1,850.00 | 0.68% | Highest decline rate, slightly stronger competition |

**Strategy summary**: In single source procurement, the room for price decline is limited (0.3%-0.7%). The core is to justify price reasonableness rather than pursuing the lowest price. Recommended strategy: ① Provide horizontal price comparison (unit prices of similar government cloud services in neighboring provinces); ② Commit to no service downgrade; ③ Provide detailed cost breakdown to support the quotation.

### Compliance Review Checklist

| Check Item | Status | Remarks |
|--------|:---:|------|
| Single source justification opinion letter | ☐ | Signed by 3 or more professionals |
| Public notice screenshot and no-objection certificate | ☐ | Obtain after the public notice period expires |
| Supplier qualification documents | ☐ | Business license + cloud service qualifications + classified protection certificate |
| Quotation documents | ☐ | Itemized quotation + total price, not exceeding budget |
| Service plan | ☐ | Respond to each procurement requirement item by item |
| Legal representative authorization letter | ☐ | Signed + official seal |
| Previous year's service report | ☐ | SLA achievement rate, work order processing statistics |
| Negotiation meeting minutes | ☐ | Signed and confirmed by both parties |

### Competitive Landscape Analysis

> ⚠️ **The following analysis is based on industry knowledge inference and is not publicly available information from the bidding announcement.**

| Supplier | Package No. | Strengths | Risks |
|------|:---:|------|------|
| China Telecom Qinghai Branch | Package 1 | Largest government cloud market share (52%), hosts the most core business systems | High resource pool expansion pressure |
| Unicom Digital Technology Qinghai Branch | Package 3 | Rich experience in government extranet construction, outstanding data middle platform capabilities | Relatively smaller share |
| China Mobile Qinghai Co., Ltd. | Package 2 | Rapid growth in mobile government cloud, differentiated advantage with 5G + Edge computing | Later start in government cloud |

**Market landscape**: The "three-way split of Qinghai government cloud" among the three major operators has been stable for many years, with each building independent resource pools, forming a de facto "three clouds" architecture. This landscape is unlikely to change in the short term, but attention should be paid to the potential impact of "one cloud, multi-chip" and the trend toward unified management of heterogeneous resource pools on the existing structure.

### Lessons Learned

1. **Single source ≠ no competitive pressure**: Although there is no competitor rivalry, insufficient justification of price reasonableness and service continuity may still result in rejection by the finance department.
2. **The public notice period is a "window period"**: Any supplier may raise objections during the 15-day public notice period; justification materials must be impeccable.
3. **Insights from the "three-way split" landscape**: The government cloud market has formed an "operator builds + government purchases services" model; new entrants are almost impossible to break in.
4. **Price anchoring effect in renewal projects**: The previous year's price becomes this year's "anchor"; price increases require sufficient justification (e.g., resource expansion, security upgrades).
5. **Fiscal affordability assessment cannot be ignored**: The annual expenditure of RMB 68.20 million must be incorporated into the fiscal budget; the procuring entity must pass the fiscal affordability assessment.

---

## Case C02: Qingdao Metro Line 7 Phase II Weak Current Systems Procurement & Integration Project

### Opportunity Identification

**Procurement announcement source**: Qingdao Public Resources Trading Center (ggzy.qingdao.gov.cn, Prequalification announcement released on March 11, 2026)
**Project name**: Qingdao Metro Line 7 Phase II Weak Current Systems (Communication System, Smart Operation System, Automatic Fare Collection System, Platform Screen Door System) Procurement and Integration Project
**Bid section No.**: E3702002313022657001001
**Tendering party**: Qingdao Metro Group Co., Ltd.
**Tendering party address**: No. 99 Shenzhen Road, Laoshan District, Qingdao
**Contact**: Mr. Miao, 0532-58625267
**Tendering agent**: Qingdao Miaoyifeng Information Consulting Co., Ltd. (Contacts: Wang Yan, Li Yingying, 0532-85605926)
**Supervisory authority**: Qingdao Municipal Housing and Urban-Rural Development Bureau (0532-85066759)
**Procurement method**: Open tendering (Prequalification, Limited quantity system — 9 applicants)
**Total project investment**: RMB 17,816,490,000 (approx. RMB 17.816 billion)
**Weak current systems estimated cost**: RMB 430,000,000 (RMB 430 million)
**Project scale**: 16.9 km (southern extension 3.8 km / 3 stations + northern extension 13.1 km / 11 stations, all underground)
**Funding source**: 40% fiscal funds + 60% bank loans, etc.
**Planning document reference**: QFGZTZ [2021] No. 103
**Unified investment project code**: 2104-370200-04-01-498806

**Key Timeline**:

| Milestone | Date | Description |
|------|------|------|
| Prequalification announcement released | 2026-03-11 | Announcement release date |
| Prequalification application deadline | 2026-03-24 09:30 | Submit via electronic bidding system |
| Prequalification venue | — | Qingdao Civic Center (No. 27 Fuzhou South Road, Shinan District), 3F, Bid Opening Room No. 5 (Room 306) |
| Bidding announcement release date | 2026-03-11 | Released simultaneously with Prequalification |
| Bid opening time | 2026-04-24 09:30 | — |
| Award announcement release date | 2026-05-01 | — |

**Project location**: Licang District, Chengyang District, and Jimo District, Qingdao

### Prequalification

**Prequalification vs Post-qualification**: This project adopts Prequalification (Limited quantity system), screening qualifications before bidding. If there are ≤9 qualified applicants, all advance; if >9, the qualification review committee scores them and selects the top 9 by score (if the 9th place has tied scores, all tied applicants shall be selected).

**Prequalification conditions**:

| Condition | Requirement | Description |
|------|------|------|
| Independent legal entity status | Must have independent legal entity status | All consortium members must satisfy |
| Similar project experience | Completed at least one similar project in the past five fiscal years | Any one consortium member satisfying is sufficient |
| Conflict of interest exclusion | No interested relationship with the tendering party | All consortium members must satisfy |
| Consortium | Consortium accepted (must sign consortium agreement, designate lead party) | Members may not bid separately or join other consortia |
| Bid section division | This project is not divided into bid sections | — |

**Similar project definition** (key threshold):
- Includes at least 2 different systems among **Communication System, Smart Operation System, Automatic Fare Collection System, and Platform Screen Door System** in domestic urban rail transit projects
- Communication system similar projects: must include at least one subsystem among dedicated wireless system (wireless communication system), video monitoring system, and passenger information system, plus dedicated transmission system
- Smart operation system similar projects: refers to integrated monitoring system equipment procurement and integration experience
- System experience may be demonstrated in a single contract or across two or more contracts

### Bidding Content Details

**Four major weak current systems**:

| System | Core Content | Key Parameters |
|------|------|------|
| Communication System | Dedicated communication system (15 subsystems) + Public security communication system (5 subsystems) | Includes transmission, wireless, video monitoring, passenger information, etc. |
| Smart Operation System | Smart operation system + Environmental & equipment monitoring + Substation integrated automation + Access control + Security inspection + Smart park | Integrated monitoring integration |
| Automatic Fare Collection (AFC) | Station ticketing equipment + Tickets + Station computer system + Line network testing center connection + Clearing and multi-line central management system connection | Includes 12-year maintenance service + Line 7 Phase I AFC upgrade |
| Platform Screen Door System | Platform screen door system equipment (including 672 sliding door units) + Spare parts + Maintenance tools | Excludes platform insulation layer + Line 7 Phase I platform screen door upgrade |

**Coverage scope**: 14 stations (including 5 interchange stations) + Bei'an Depot + Line 7 Phase I stations and Dongguozhuang Depot system upgrades

### Consortium Bidding Strategy

**Award result** (actual award situation):

| Role | Company | Award Amount |
|------|------|:---:|
| Lead Party | Qingdao Boning Futian Intelligent Transportation Technology Development Co., Ltd. | — |
| Member | Qingdao Urban Rail Transit Technology Co., Ltd. | — |
| **Total** | **Consortium** | **RMB 409,890,000.00** |
| Project Manager | Cui Rujia | — |

**Award amount analysis**: The award price of RMB 409.89 million represents a decline of approximately 4.7% from the weak current systems estimated cost of RMB 430 million.

**Consortium agreement key points** (based on Prequalification announcement requirements):
- All consortium members shall jointly sign a consortium agreement, clearly defining each member's scope of work, rights, and obligations
- The agreement must designate a lead party
- All consortium members must satisfy "independent legal entity status" and "conflict of interest exclusion"
- Any one consortium member satisfying "similar project experience" is sufficient
- Consortium members (including affiliates) may not separately or through a new consortium submit a Prequalification application for this project

### Evaluation Method Analysis

**Prequalification method**: Limited quantity system (9 applicants)

| Stage | Method | Description |
|------|------|------|
| Preliminary review | Compliance review | Check whether applicants meet qualification requirements |
| Detailed review | Scoring system | Score and rank qualified applicants according to scoring criteria |
| Quantity control | Select top 9 | ≤9: all advance; >9: select top 9 |

**Prequalification scoring dimensions** (inferred based on common industry standards):

| Scoring Item | Estimated Weight | Key Assessment Points |
|------|:---:|------|
| Similar project experience | 35% | Quantity, scale, and system coverage of urban rail transit weak current system integration experience in the past 5 years |
| Financial status | 15% | Audit reports from the past 3 years, bank credit rating |
| Technical capability | 25% | Preliminary technical proposal approach, key equipment selection, system integration capability |
| Project team | 15% | Resumes of project manager and core technical personnel |
| Corporate reputation | 10% | Awards, credit evaluations, litigation records |

### Common Bid Rejection Reasons and Mitigation

| Bid Rejection Reason | Risk Level | Mitigation Strategy |
|----------|:---:|------|
| Prequalification application documents not submitted on time | 🔴 | Upload via electronic bidding system 1 day in advance, allowing buffer for technical issues |
| Similar project experience does not meet "at least 2 different systems" | 🔴 | Carefully verify system types in experience records, ensure coverage of ≥2 among Communication / Smart Operation / AFC / Platform Screen Door |
| Consortium agreement not signed/stamped or lead party not designated | 🔴 | Both parties' legal representatives sign + both official seals, clearly designate lead party in the agreement |
| Duplicate consortium member application | 🔴 | All consortium members confirm uniqueness, avoid affiliate conflicts |
| Incomplete performance evidence materials | 🟡 | Provide full set: letter of acceptance + contract + acceptance report |
| Use of unofficial bid document preparation tools | 🟡 | Must generate via "Qingdao Public Resources Bid Document Preparation Tool" |
| Paper document submission | 🔴 | This project does not accept paper Prequalification application documents |

### Three-Tier Remedy Mechanism: Challenge / Objection / Complaint

**If unfair evaluation occurs, the remedy mechanism may be initiated**:

| Remedy Method | Time Limit | Accepting Authority | Applicable Scenario |
|----------|:---:|------|------|
| Objection | As prescribed | Qingdao Metro Group Co., Ltd. (Mr. Miao, 0532-58625267, mq012345@126.com) | Prequalification documents, bidding documents, bid evaluation results |
| Complaint | As prescribed | Qingdao Municipal Housing and Urban-Rural Development Bureau (0532-85066759, jgjgcc@qd.shandong.cn) | Unsatisfactory / no response to objection |
| Administrative review / litigation | 60 days / 6 months | Superior authority / Court | Disagreement with complaint handling decision |

**Key points for drafting an objection letter**:
1. Objector's name, address, and contact information
2. Respondent's name
3. Objection matter (specific clauses + factual basis)
4. Legal basis (citing the Bidding and Tendering Law and its implementing regulations)
5. Objection request (re-evaluation / bid rejection / compensation)
6. Signed, stamped + date

### Competitive Landscape Analysis

> ⚠️ **The following analysis is based on industry knowledge inference and is not publicly available information from the bidding announcement. The list of qualified Prequalification applicants was not disclosed in the announcement.**

**Potential competitive landscape** (inferred based on industry knowledge):

| Tier | Typical Enterprises | Competitive Advantage | Remarks |
|:---:|------|------|------|
| Tier 1 | CRSC, CREC Electrification Bureau, Casco | National rail transit weak current integration leaders, rich experience | Central SOE background, strong comprehensive capabilities |
| Tier 2 | Qingdao Boning Futian (awardee), Qingdao Urban Rail Transit Technology | Localization advantage, familiar with Qingdao Metro technical systems | Consortium awarded |
| Tier 3 | Other rail transit system integrators | Expertise in specific subsystems | Need consortium to fill gaps |

**Awardee analysis**: Qingdao Boning Futian Intelligent Transportation Technology Development Co., Ltd. is a Qingdao local enterprise (High-tech Zone), forming a consortium with Qingdao Urban Rail Transit Technology Co., Ltd., reflecting the "local enterprise + technical complementarity" consortium strategy. Local enterprises have natural advantages in customer relationships, on-site service, and post-award maintenance.

### Lessons Learned

1. **Prequalification is the "first hurdle"**: The Limited quantity system (9 applicants) means that even if qualification requirements are met, one may be eliminated due to low ranking. Prequalification application documents must be polished item by item against the scoring criteria.
2. **Similar project experience is "hard currency"**: This project requires similar experience in "at least 2 different systems," with clear definitions for each subsystem. Experience selection must be precisely matched.
3. **Consortium strategy must be "complementary"**: The awardee adopted a "local intelligent transportation enterprise + rail transit technology company" combination, achieving the optimal configuration of technology + localization.
4. **Electronic bidding is irreversible**: Must use the Qingdao Public Resources Bid Document Preparation Tool; paper documents are not accepted. Technical operational errors = bid rejection.
5. **12-year maintenance is "long-tail value"**: The AFC system includes 12 years of maintenance service. When bidding, one must consider not only construction costs but also long-term O&M costs and profits.
6. **System upgrades are an "invisible threshold"**: This project includes upgrades to Line 7 Phase I stations and Dongguozhuang Depot systems, requiring bidders to have deep understanding of existing systems, creating a natural advantage for the original system contractor.

---

## Source Attribution

**Case C01 data sources**:
- Single source procurement announcement: China Government Procurement Network, https://www.ccgp.gov.cn/cggg/dfgg/dylygg/202602/t20260214_26184958.htm (released 2026-02-14)
- Award result announcement: China Government Procurement Network, http://www.ccgp.gov.cn/cggg/dfgg/zbgg/202606/t20260613_26745922.htm (released 2026-06-13)

**Case C02 data sources**:
- Prequalification announcement: Qingdao Public Resources Trading Center, https://ggzy.qingdao.gov.cn/c/TradeDetals-ZtbShow/178367-5021-0-0-0/6e49fa80-d501-47cc-9f30-7218624b76d8-B03CE5B6FC1D2D3C2D5FCEBC39AA2406.html (released 2026-03-11)
- Award announcement: China Tendering & Bidding Public Service Platform, https://www.chinabidding.com/bidDetail/262891960-BidResult.html (released 2026-05-01)

> ⚠️ **Disclaimer**: The competitive landscape analysis sections are based on industry knowledge inference and are not publicly available information from the bidding announcements. The detailed scoring criteria in the cases are reasonable reconstructions based on common industry practices; actual scoring details are subject to the bidding documents. This document is for learning and reference only and does not constitute any bidding advice.