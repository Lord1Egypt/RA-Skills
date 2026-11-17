---
name: trusted-insurance-coach
version: 1.0.0
author: fangcun
license: MIT
---


# Trusted Insurance Coach

Read policy coverage, exclusions and claim preparation requirements. Produces steps and checklists from the documents the user actually has, without verdicts on any product.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `trusted-insurance-coach/LICENSE`
- `trusted-insurance-coach/README.md`
- `trusted-insurance-coach/.codebuddy-plugin/plugin.json`
- `trusted-insurance-coach/agents/trusted-insurance-coach.md`
- `trusted-insurance-coach/avatars/insurance-advisor.png`
- `trusted-insurance-coach/scripts/agentprobe.py`
- `trusted-insurance-coach/scripts/compliance_scan.py`
- `trusted-insurance-coach/scripts/selfcheck.py`
- `trusted-insurance-coach/scripts/sync_shared.py`
- `trusted-insurance-coach/scripts/usertest.py`
- `trusted-insurance-coach/shared/budget_design.md`
- `trusted-insurance-coach/shared/insurance_abc.md`
- `trusted-insurance-coach/shared/pitfalls_10.md`
- `trusted-insurance-coach/shared/takeaway_3_forms.md`
- `trusted-insurance-coach/skills/ins-claims-guide/SKILL.md`
- `trusted-insurance-coach/skills/ins-claims-guide/references/claim_materials.md`
- `trusted-insurance-coach/skills/ins-claims-guide/references/claim_process.md`
- `trusted-insurance-coach/skills/ins-claims-guide/references/dispute_reasons.md`
- `trusted-insurance-coach/skills/ins-claims-guide/references/law_citations.md`
- `trusted-insurance-coach/skills/ins-claims-guide/references/rejection_paths.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/README.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/demo_01_hospitalized.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/demo_02_rejected.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/demo_03_waiting_for_money.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/output_01_hospitalized.md`
- `trusted-insurance-coach/skills/ins-claims-guide/sample/output_02_materials_missing.md`
- `trusted-insurance-coach/skills/ins-claims-guide/scripts/claim_checklist.py`
- `trusted-insurance-coach/skills/ins-claims-guide/scripts/compliance_scan.py`
- `trusted-insurance-coach/skills/ins-claims-guide/shared/budget_design.md`
- `trusted-insurance-coach/skills/ins-claims-guide/shared/insurance_abc.md`
- `trusted-insurance-coach/skills/ins-claims-guide/shared/pitfalls_10.md`
- `trusted-insurance-coach/skills/ins-claims-guide/shared/takeaway_3_forms.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/SKILL.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/critical_illness_rules.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/disclosure_questions.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/family_roles.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/law_citations.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/medical_insurance_card.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/mock_scenarios.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/pre_claim_habits.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/renewal_traps.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/references/underwriting_paths.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/README.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/demo_01_L1_newbie.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/demo_02_nodule.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/demo_03_card_lent.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/output_01_L1_newbie.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/output_02_nodule.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/sample/output_03_card_lent.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/scripts/compliance_scan.py`
- `trusted-insurance-coach/skills/ins-health-disclosure/scripts/disclosure_checklist.py`
- `trusted-insurance-coach/skills/ins-health-disclosure/shared/budget_design.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/shared/insurance_abc.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/shared/pitfalls_10.md`
- `trusted-insurance-coach/skills/ins-health-disclosure/shared/takeaway_3_forms.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/SKILL.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/references/clause_four_looks.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/references/law_citations.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/references/purchase_safeguards.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/references/renewal_clause.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/sample/README.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/sample/demo_01_clause.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/sample/demo_02_exclusion.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/sample/output_01_clause_list.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/scripts/clause_check.py`
- `trusted-insurance-coach/skills/ins-how-to-buy/scripts/compliance_scan.py`
- `trusted-insurance-coach/skills/ins-how-to-buy/shared/budget_design.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/shared/insurance_abc.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/shared/pitfalls_10.md`
- `trusted-insurance-coach/skills/ins-how-to-buy/shared/takeaway_3_forms.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/SKILL.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/references/gap_rules.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/references/review_table_fields.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/sample/README.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/sample/demo_01_messy_policies.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/sample/demo_02_surrender.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/sample/output_01_family_table.md`
- `trusted-insurance-coach/skills/ins-policy-checkup/sample/policies_demo.json`
- `trusted-insurance-coach/skills/ins-policy-checkup/scripts/compliance_scan.py`
- `trusted-insurance-coach/skills/ins-policy-checkup/scripts/policy_review.py`

- ... and more; see the package directory.

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
