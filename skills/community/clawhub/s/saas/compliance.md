# Compliance and Tax — Audits, Data Protection and Where You Owe Money

Scope: the regimes a SaaS business is actually subject to, the audits buyers ask for, and indirect tax on subscription revenue. What a buyer demands in a deal is `enterprise.md`; implementing tax calculation in code is `billing`.

**Before committing to a regime, a certification date or a tax position**, read `config.yaml` for `compliance_regime` and `billing_platform` (a merchant of record changes the entire tax picture), and `## Commitments` in `~/Clawic/data/saas/memory.md` for certification or residency promises already made to customers with dates attached.

## Which Regime Actually Applies

Distinguish what is legally required from what buyers demand. Both are real; confusing them wastes quarters.

| Regime | Applies because | Nature |
|---|---|---|
| GDPR / UK GDPR | You process personal data of people in the EU/UK, regardless of where you are | Law — not optional, no certificate |
| CCPA/CPRA and US state privacy laws | Thresholds on revenue or volume of state residents' data | Law, threshold-triggered |
| SOC 2 | Buyers ask for it | Attestation, not a law; scope is yours to define |
| ISO 27001 | Buyers ask for it, more often outside the US | Certification against a standard |
| HIPAA | You handle protected health information for a covered entity | Law; requires a BAA and changes the architecture |
| PCI DSS | You touch card data | Law-adjacent; almost entirely avoidable by never touching card data |
| Sector rules (financial, education, government) | The customer's regulator reaches you as a supplier | Varies; read before selling into the sector |

The cheapest PCI position by far is to never let card data reach your servers — hosted fields or a provider-hosted checkout reduces the obligation to the simplest self-assessment. Any design that posts a card number to your backend multiplies the scope enormously and permanently.

## SOC 2 Without Wasting a Year

- **Type I is a point in time; Type II covers an observation window** — commonly three to twelve months. Buyers who matter ask for Type II. A first report often uses a shorter window with the following one covering twelve months.
- **The clock is the constraint.** Nothing compresses an observation window, so the start date is the decision (`enterprise.md`).
- **Scope deliberately.** The five trust services criteria are optional except Security; adding availability, confidentiality, processing integrity and privacy each adds controls and evidence. Start with Security, add what buyers actually request.
- **Evidence collection is the real cost**, not the audit. Access reviews, change management, onboarding and offboarding records, vulnerability management, incident records, vendor reviews — collected continuously, quarterly at worst. Reconstructing a year of evidence in the final month is where programmes fail.
- **A compliance automation platform** is worth it once the control count exceeds what a spreadsheet survives; it does not replace the controls, only the evidence gathering.
- **Track the programme as a project** in the shared `~/Clawic/data/projects/<project>.md` with its milestones — it is a multi-month effort with a start and an end, exactly what that box is for.
- Put evidence collection and the annual renewal in `## Due`. A lapsed report is worse than never having had one: buyers read the gap.

## GDPR in Practice for a SaaS Vendor

You are almost always a **processor** for customer data and a **controller** for your own users and marketing data. Both roles carry obligations and they are different.

- **DPA** offered proactively, with standard contractual clauses where data leaves the EEA, and a published **subprocessor list** with an advance-notice period for changes — commonly thirty days, with a customer right to object.
- **Data subject rights** flow through your customer: access, deletion, portability and correction requests arrive from the controller, and you must be able to service them per tenant within the statutory window. Self-serve export and per-tenant deletion are the implementation (`multitenancy.md`).
- **Breach notification**: to the controller without undue delay, with a 72-hour clock on the controller's own notification to the supervisory authority. Your contract will name a shorter window; know it before you need it.
- **Records of processing**, a lawful basis for each purpose, and a retention schedule that the product actually enforces. A retention policy the system does not implement is a finding waiting to happen.
- **Cookie and tracking consent** on the marketing site is a separate obligation from the product, and it is the one most often failed by an otherwise compliant company.
- **Do not store what you do not need.** Every field of personal data collected is a permanent obligation; the cheapest compliance posture is a smaller data footprint.

## Indirect Tax: Where You Owe It

Digital services are taxable in most jurisdictions where the customer is, not where you are. This is the compliance surface that surprises small SaaS companies hardest, because liability accrues silently.

- **EU VAT**: B2C sales are taxed at the customer's rate from the first euro, filed through a single registration scheme for non-established and established sellers alike. B2B sales to a VAT-registered business in another member state reverse-charge — but only against a validated VAT number, and validation must be recorded at the time of sale.
- **US sales tax**: economic nexus is per state, with thresholds on revenue or transaction count, and software-as-a-service is taxable in some states and not others. Nexus creates a registration and filing obligation, not just a collection one.
- **UK, Canada, Australia, Japan, India, Brazil and many others** each have their own registration threshold and rate for digital services. Selling internationally on the internet means accruing obligations in places you have never visited.
- **Evidence of customer location** must be collected and stored — commonly two non-conflicting pieces, such as billing address and IP country. Without it, the default is usually the least favourable assumption.
- **B2B versus B2C changes everything.** Collect and validate tax identifiers at checkout; the difference between reverse charge and charging local VAT is the difference between owing nothing and owing 20%.

## Merchant of Record: The Decision That Removes Most of This

| | Merchant of record | Direct (payment processor only) |
|---|---|---|
| Who sells to the customer | The provider | You |
| Tax registration, collection, filing | Provider's obligation | Yours in every jurisdiction with nexus |
| Fees | Higher, bundled | Lower processing fee, plus your own tax tooling and filings |
| Customer relationship | Provider appears on the statement and handles disputes | Fully yours |
| Enterprise procurement | Harder: buyers contract with the provider, not you | Standard |
| Reversibility | Migrating away later is a project | — |

An MoR is usually the right call for an early self-serve business selling internationally, and usually the wrong call once enterprise contracts and custom terms dominate — those buyers need to contract with you. Plan the transition rather than discovering it during a large deal, and record the decision with its reasoning in `artifacts/`.

## Accessibility and Sector Rules

- **Accessibility** (WCAG-based requirements) is a procurement gate for public-sector, education and large-enterprise buyers, and increasingly a legal requirement in several jurisdictions. It is far cheaper to build than to retrofit, and a stated conformance report is a common questionnaire item.
- **HIPAA** requires a signed BAA before any protected health information arrives, plus encryption, audit controls and minimum-necessary access. Accepting PHI without a BAA in place is the violation, not a step towards compliance.
- **Government and regulated sectors** carry their own frameworks with their own multi-year clocks. Treat entry into such a sector as a company decision with a budget, never as a single deal (`sales-motion.md`).

**After any compliance decision or milestone**, write the certification, its scope and its dates to `## Commitments` where a customer was promised it, add evidence collection, audit renewal, penetration test and tax registration reviews to `## Due`, track the programme in the shared `~/Clawic/data/projects/<project>.md`, and put the reusable answers into `security-answers.md` with their verification date (`memory-template.md`). A regime decision and its reasoning — why SOC 2 and not ISO, why MoR and not direct — belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line: it is revisited every time a large buyer asks for something different.
