# Records Retention Schedule Drafter

**Domain:** Records & Information Management · Information Governance · Compliance
**Platforms:** Claude · Codex

## Purpose

Drives an ARMA Generally Accepted Recordkeeping Principles® (GARP) and Information Governance Implementation Model (IGIM)-aligned workflow that turns an organization's record-series inventory and legal landscape into a DRAFT records retention schedule. The schedule ties each series to a statutory / regulatory / operational / historical citation, names a custodian and a final-action disposition, defines event-driven retention triggers, addresses format-specific disposition (paper, electronic, email, chat, structured data, backup), drafts the legal-hold suspension protocol, and applies privacy-law minimization overlays (GDPR storage limitation, CCPA / CPRA, HIPAA, FERPA, GLBA, PCI-DSS, PIPEDA, LGPD, APPI). The output is always a DRAFT for Records Officer, Privacy Officer, and General Counsel review — never an executed records-control policy, never legal advice, never an opinion on litigation strategy.

## When to Use

- New retention schedule for a recently formed or recently restructured organization
- First adoption of a big-bucket or functional schedule to replace a legacy series-by-series schedule
- Periodic review (typically every 2–3 years) of an existing schedule against new statutes and case law
- Privacy-law minimization overlay (GDPR Art 5(1)(e), CCPA / CPRA, LGPD, APPI) added to an existing schedule
- Cross-border or multi-jurisdictional organization rationalizing conflicting retention requirements
- M&A integration — merging two organizations' schedules
- Higher-education, healthcare, financial-services, energy, life-sciences, or public-sector schedule covering sector-specific records (FERPA, HIPAA, SEC 17a-4, FERC / NERC, FDA / 21 CFR Part 11, NARA general records schedules)
- Defensible-disposition program build-out where audit trail and approval workflow are required

## What It Does

1. Collects role, organization type and sector, jurisdictions and regulators, lines of business, existing schedule and gap inventory, system landscape (ECM / EDRMS / DMS / SharePoint / Google Workspace / M365 / mainframe / SaaS apps), retention-program owner, and inventory granularity through one-question-at-a-time intake
2. Selects schedule structure (big-bucket, functional, hybrid, hierarchical, taxonomy-aligned) with explicit trade-offs for usability, auditability, and exception handling
3. Inventories record series under a controlled vocabulary (function → activity → series → sub-series) with a unique series identifier per row
4. Captures the four-pillar retention basis for every series — statutory, regulatory, operational, historical / cultural — and names the citation (e.g., 26 U.S.C. § 6001, IRC § 6501, SEC Rule 17a-4, ERISA § 107, OSHA 29 CFR 1904, HIPAA 45 CFR 164.530(j), FERPA 34 CFR 99.32, NARA GRS, state UPA, the organization's litigation history)
5. Defines event-driven triggers — active period (event-based or fixed-cycle) + retention period + final action (destroy / transfer / archive / permanent) — and disallows "indefinite", "as long as needed", or unbounded retention without a basis
6. Addresses format-specific disposition (paper destruction method, electronic deletion vs cryptographic-erasure, email / chat / collaboration retention, structured-data row-level vs full-table retention, backup and DR copies, physical media destruction, mobile-device wipe)
7. Drafts the legal-hold and litigation-hold-suspension protocol — hold notice triggers, custodian acknowledgment, system-level preservation, release procedure, audit log
8. Applies privacy-law minimization overlays — GDPR Article 5(1)(e) storage-limitation, CCPA / CPRA storage limitation, HIPAA minimum-necessary, FERPA destroy-when-no-longer-needed, GLBA Safeguards Rule, PCI-DSS PAN-retention rule, PIPEDA, Quebec Law 25, LGPD, APPI, state privacy laws — and flags conflicts between privacy minimization and statutory retention floors
9. Drafts the defensible-disposition workflow (annual review → records-officer approval → custodian execution → audit-trail record → certification of destruction) and a vendor / cloud-data-portability deletion exhibit
10. Runs a GARP / IGIM / ARMA-principles self-check (accountability, transparency, integrity, protection, compliance, availability, retention, disposition) and maintains a basis-of-retention register
11. Outputs a complete DRAFT schedule with an unsigned Records-Officer / Privacy-Officer / General-Counsel sign-off block and a verbatim "draft for governance-committee review" banner

## Notes

This skill produces a **DRAFT retention schedule** for the records-management governance committee (Records Officer, Privacy Officer, General Counsel, IT / Information Security, Internal Audit, line-of-business owners). It is not an executed records-control policy, not litigation strategy, not legal advice, and not an opinion on the legality of a specific retention period. Citations must be re-verified with current statute, regulation, case law, and the organization's records-management counsel before adoption; the agent works from publicly available citations the user names. Privacy-law minimization rules and statutory retention floors can conflict — every conflict is surfaced in the gap log for counsel resolution. The drafting agent is never the Records Officer, never the Privacy Officer, never the General Counsel, and never the data controller of record.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
