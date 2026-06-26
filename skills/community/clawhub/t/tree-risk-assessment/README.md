# Tree Risk Assessment (ISA BMP-TRA / TRAQ — Basic Level 2)

**Platforms:** Claude · Openclaw · Codex
**Domain:** Arboriculture / Urban Forestry / Risk Management

## Purpose

Turns site / target data, tree biometrics, and observed defects into a DRAFT Basic Level 2 tree risk assessment aligned to the ISA *Best Management Practices — Tree Risk Assessment* (BMP-TRA, 2nd ed.), the ISA TRAQ matrix, and ANSI A300 Part 9. Walks the assessor through target characterization, systematic defect inspection, load-factor capture, the BMP-TRA two-step matrix (likelihood-of-failure × likelihood-of-impact = Likelihood; Likelihood × Consequences = Risk), and produces a DRAFT report with a Low / Moderate / High / Extreme risk rating, mitigation options, residual-risk re-rating, a photo-and-evidence index, an assessor-limitations and disclaimer block, and an open-questions list — for an ISA TRAQ-qualified arborist to verify and sign off before any communication to the tree owner / risk manager.

## When to Use

- A consulting arborist needs a structured Basic Level 2 assessment for an individual tree or a small group of trees on private property, in a park, on a campus, or along a right-of-way
- A municipal urban-forestry crew needs a defensible TRAQ-format assessment before a removal-or-keep decision on a public tree
- An HOA / property manager has received a written concern from a neighbour or insurer and needs a documented assessment on file
- A post-storm crew needs a rapid Level 2 walk for storm-damaged trees to triage retention vs removal
- A construction or development project needs pre-construction tree-risk assessments on trees designated for retention inside the limits of disturbance
- An insurance adjuster or claim defence needs an after-the-fact reconstruction of the foreseeability of failure (the skill explicitly flags this as out-of-scope speculation and refers to a separate forensic assessment)

## What It Does

**Phase 1: Scope of Assessment**
1. Confirms assessment level (Level 1 limited visual / **Level 2 basic — default** / Level 3 advanced with instrumentation), assessor identity and TRAQ status, assessment date and time frame, weather at the time of the assessment, and the trigger for the assessment (routine, post-storm, pre-construction, complaint, real-estate transaction, insurance, regulatory)

**Phase 2: Site and Target Characterization**
2. Captures site context (urban / suburban / rural / parkland / road verge / utility corridor), exposure (open / partially exposed / sheltered), recent disturbance (construction, grade change, trenching, paving)
3. Identifies and characterizes each target within the potential failure zone: target type (person, vehicle, structure, utility, road), occupancy frequency (Rare / Occasional / Frequent / Constant), target value, and whether the target can be moved

**Phase 3: Tree Biometrics and Species Traits**
4. Records species (scientific and common name), DBH (cm or in), total height (m or ft), crown spread, crown class (dominant / co-dominant / intermediate / suppressed), lean (degrees + direction + recent vs long-standing), species-specific failure profile flags (brittle wood — *Salix*, *Populus*; included-bark co-dominants — *Acer saccharinum*, *Ulmus*; root-rot susceptibility — *Quercus* spp. with *Armillaria*; etc.)

**Phase 4: Systematic Defect Inspection**
5. Inspects in a fixed order — Root collar / buttress roots → Lower trunk → Upper trunk → Scaffold limbs → Branch unions → Canopy — capturing each observed defect with size / extent / location / load path implication
6. Captures load factors — wind exposure, recent storm history, edge effects (newly exposed after adjacent removal), soil moisture state, soil type, root-zone disturbance

**Phase 5: BMP-TRA Two-Step Matrix**
7. Rates **likelihood of failure** of each significant defect or part — Improbable / Possible / Probable / Imminent — over the user-specified time frame (typically 1 year, may be longer for monitoring assessments)
8. Rates **likelihood of impact** given failure — Very low / Low / Medium / High — based on target occupancy and the geometry of the potential failure
9. Combines failure-and-impact via the BMP-TRA Likelihood matrix → Unlikely / Somewhat likely / Likely / Very likely
10. Rates **consequences** of impact — Negligible / Minor / Significant / Severe — based on target value and damage potential
11. Combines Likelihood-and-Consequences via the BMP-TRA Risk matrix → **Low / Moderate / High / Extreme**

**Phase 6: Mitigation, Residual Risk, and Report**
12. For each Moderate / High / Extreme finding, lists mitigation options (move target, restrict access, remove tree, remove defective part, prune to reduce loading, install cable / brace, install lightning protection, monitor with re-inspection interval, accept risk) and re-rates the residual risk after each option
13. Produces a DRAFT report with site map / target sketch placeholder, photo-and-evidence index (every finding cross-referenced), assessor-limitations and disclaimer block, the assessment time frame, and an Open Questions list — labelled for ISA TRAQ-qualified arborist sign-off

## Output

A risk-assessment packet consisting of a DRAFT report (site / target characterization, tree biometrics, defect inspection log, load factors, the BMP-TRA two-step matrix with the resulting Low / Moderate / High / Extreme rating, mitigation options with residual-risk re-rating), a photo-and-evidence index with every finding cross-referenced, an assessor-limitations and disclaimer block stating the assessment level, the inspection time frame, weather at inspection, what was and was not inspected (e.g. no aerial or above-ground inspection on Level 2), and the date on which the assessment expires (default 1 year unless the assessor states otherwise) — plus an Open Questions list for any input the user marked unknown. The entire packet is marked **DRAFT — FOR ISA TRAQ-QUALIFIED ARBORIST REVIEW AND SIGN-OFF**.

## Notes

This skill **drafts** a tree risk assessment to support — never replace — an ISA TRAQ-qualified arborist's review and sign-off. The skill does not certify the tree as "safe" (no assessment can — risk is reduced, not eliminated), does not sign or seal the report, does not communicate findings to the tree owner / risk manager (the qualified arborist owns the communication), and does not opine on legal duty of care, liability, or insurance coverage. The skill defaults to a Basic Level 2 assessment per BMP-TRA and refuses to upgrade to Level 3 advanced assessment without specifying which instrumented method (resistograph, sonic tomography, root collar excavation, tensiometer, pull test) the user has actually performed and the qualifications of the person who performed it. Storm-damaged trees with imminent-failure conditions or downed live conductors must be escalated to a qualified arborist and the relevant utility / emergency services immediately — the skill does not delay the report, it flags and proceeds, but it states the escalation clearly. Forensic / retrospective assessments after a failure (litigation, claim defence) are out of scope and the skill refuses to retro-fit a foreseeability conclusion to a tree that has already failed.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
