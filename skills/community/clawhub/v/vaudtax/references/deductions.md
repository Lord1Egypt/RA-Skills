# Deduction Rules and Limits

Official rules for Canton Vaud (ICC) and federal (IFD) deductions. Source: [Instructions générales 21001](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf) (2025 edition — URL is year-specific, update for other fiscal years).
Limits are indexed annually — verify the year matches the declaration's `fiscalPeriod`.

Each section is keyed by its declaration **CODE**. The code is the stable citation: the official instructions are organised by code, and the ICC section and the IFD annex each list it. Page numbers shift between annual editions, so cite the code, not a page.

## Contents

- [Transport — CODE 140](#transport--code-140)
- [Repas — CODE 150](#repas--code-150)
- [Autres frais professionnels — CODE 160](#autres-frais-professionnels--code-160)
- [Double activité des conjoints — CODE 235](#double-activité-des-conjoints--code-235)
- [Assurances — CODE 300](#assurances--code-300)
- [Pilier 3a — CODE 310](#pilier-3a--code-310)
- [Intérêts capitaux d'épargne — CODE 480](#intérêts-capitaux-dépargne--code-480)
- [Intérêts passifs / dettes privées — CODE 610](#intérêts-passifs--dettes-privées--code-610)
- [Frais de formation et perfectionnement — CODE 618](#frais-de-formation-et-perfectionnement--code-618)
- [Déduction logement — CODE 660](#déduction-logement--code-660)
- [Frais de garde — CODE 670](#frais-de-garde--code-670)
- [Frais médicaux — CODE 710](#frais-médicaux--code-710)
- [Dons — CODE 720](#dons--code-720)
- [Verification checklist](#verification-checklist)

---

## Transport — CODE 140

**ICC:** Forfait table based on shortest one-way distance (transport public). NOT the actual subscription cost.

| Distance (km) | ICC annual (CHF) | | Distance (km) | ICC annual (CHF) |
|---|---|---|---|---|
| 20 | 3'001 | | 35 | 3'448 |
| 25 | 3'136 | | 40 | 3'608 |
| 30 | 3'288 | | 45 | 3'768 |
| 31 | 3'320 | | 51+ | 4'080 (max) |

Full table in instructions pp. 19–20. Capped at the most expensive 2nd-class general pass (= 51 km forfait).

**IFD:** Capped at **CHF 3'300** per employed person regardless of distance.

**2025 limits:** ICC max CHF 4'080 / IFD max CHF 3'300

---

## Repas — CODE 150

**ICC and IFD:** Per-day forfait, capped annually.

| Type | Per day | Max/year |
|---|---|---|
| `HORS_DOMICILE_NORMAL` (regular lunch outside) | CHF 15 | CHF 3'200 |
| Cantine or employer subsidy (`contributionFraisRepas` = true on salary cert) | CHF 7.50 | CHF 1'600 |

Deduction = `min(nbJours × per_day, annual_cap)`. Part-time taxpayers with fewer working days do not reach the cap.

---

## Autres frais professionnels — CODE 160

**ICC and IFD:** Forfait = **3% of `salaireNet`**, min CHF 2'000, max CHF 4'000.

Cross-check: `ctb1_forfait_chf` should equal `max(2000, min(4000, round(salaireNet × 0.03)))`.

---

## Double activité des conjoints — CODE 235

Applies only to jointly-taxed couples where **both** spouses have a lucrative activity (or one substantially and regularly assists the other in their profession/business). Granted once.

**ICC (2025):** CHF 1'700 deducted from the **lower** income. If, after acquisition costs (codes 140–165) and prévoyance contributions (codes 310–340), the lower net income is below CHF 1'700, the deduction equals that actual net amount.

**IFD (2025):** 50% of the lower work income (after acquisition costs and prévoyance contributions), **min CHF 8'600, max CHF 14'100**, never exceeding the lower work income.

ICC and IFD deltas differ — model them separately.

---

## Assurances — CODE 300

Deduction = **min(net premiums after subsidies, family-status cap)**. The cap is always applied — declared gross amounts above the cap have no fiscal impact.

**ICC caps (2025):**

| Situation familiale | Max ICC |
|---|---|
| Célibataire / veuf / séparé / divorcé | CHF 5'000 |
| Marié / partenariat enregistré | CHF 9'900 |
| + par enfant (part 0.5 sous code 810) | + CHF 1'300 |

**IFD caps (2025):**

| Situation familiale | Max IFD |
|---|---|
| Célibataire | CHF 1'800 |
| Marié / partenariat enregistré | CHF 3'700 |
| + par enfant / personne à charge | + CHF 700 |

> If net premiums ≥ ICC cap, the actual deduction equals the cap regardless of whether all premiums are individually justified. Missing justifications for amounts above the cap have no fiscal impact.

---

## Intérêts capitaux d'épargne — CODE 480

**ICC:** Savings interest income from private wealth (savings accounts, postal accounts, Swiss/foreign bonds, mortgages, etc.) is deductible up to:

| Situation familiale | Max ICC |
|---|---|
| Célibataire / veuf / séparé / divorcé | CHF 1'600 |
| Marié / partenariat enregistré | CHF 3'300 |
| + par enfant (part 0.5 code 810) | + CHF 300 |

**Excluded:** dividends, equity fund distributions, and any income without the character of savings interest are **not deductible** under code 480.

**IFD:** Codes 300, 340 and 480 are reported as a **single combined deduction line** ("Primes et cotisations d'assurances et intérêts de capitaux d'épargne", codes 300/340/480 grouped in the IFD income-determination table). That combined line is subject to the code 300 IFD caps above (CHF 1'800 single / CHF 3'700 married / + CHF 700 per child). Code 480 is not a separate IFD line item.

**Will-be-zero check:** if the taxpayer has no savings interest declared under code 410, deduction = CHF 0.

---

## Pilier 3a — CODE 310

**ICC and IFD (2025):**

| Situation | Max |
|---|---|
| Assuré au 2e pilier (LPP) | CHF 7'258 |
| Non assuré au 2e pilier | CHF 36'288 (20% of net lucrative income) |

Cross-check: sum of all form 21 EDP attestations per taxpayer must equal `formesReconnuesPrevoyanceIndividuelleContribuable1/2` and must not exceed the applicable maximum. Missing attestations = unjustified declaration.

---

## Intérêts passifs / dettes privées — CODE 610

**ICC and IFD:** Private debt interest (mortgage and other private loans) is deductible up to **the gross yield of taxable wealth (rendement brut de la fortune) plus CHF 50'000**. Same ceiling for both ICC and IFD.

- Debt **amortisation** (capital repayment) is not deductible — only interest.
- Construction-credit interest is an investment cost, not deductible from income.
- Leasing instalments count as rent, not deductible.
- An early-mortgage-termination penalty is deductible as debt interest only if a new loan is taken with the same lender; otherwise it attaches to the real-estate capital gain.

---

## Frais de formation et perfectionnement — CODE 618

Deductible only when it is **not initial training (formation initiale)**, and the person either holds a secondary-II diploma or is at least 20 and pursuing a diploma other than a first secondary-II diploma. Only costs the person bore themselves count (not those covered by an employer or a foundation). Deductible in the year paid.

**ICC (2025):** max **CHF 12'000** per person per fiscal period (so up to CHF 24'000 for a couple).

**IFD (2025):** max **CHF 13'000** per person (up to CHF 26'000 for a couple).

ICC and IFD deltas differ — model them separately.

---

## Déduction logement — CODE 660

**ICC only** — does not exist for IFD.

**Formula:** `max(0, min(min(loyer_sans_charges, plafond_loyer) − 20% × code_650, max_deduction))`

| Situation | Plafond loyer déterminant | Max déduction |
|---|---|---|
| Célibataire / veuf / séparé / divorcé | CHF 11'100 | CHF 6'800 |
| Marié / partenariat enregistré | CHF 13'700 | CHF 6'800 |
| + par enfant (entretien complet) | + CHF 3'700 | — |

The CHF 6'800 absolute cap applies regardless of family situation.

- `loyer_sans_charges` = annual rent **excluding charges** (not the figure in the declaration, which may include charges)
- `code_650` = revenu net after all deductions (estimated from the declaration)

**Will-be-zero check:** if `20% × code_650 ≥ plafond_loyer`, deduction = CHF 0. For a célibataire, this occurs when code 650 ≥ ~CHF 55'500. High earners typically get no rent deduction.

---

## Frais de garde — CODE 670

Care costs (crèche, maman de jour, etc.) for a child **under 14** living in the taxpayer's household, deductible only when incurred because the parent(s) work, are in training, or are unable to work. Only the cost of care counts — not food, lodging, or household tasks. Costs must be documented and incurred during the activity/training/incapacity.

**ICC (2025):** max **CHF 15'200** per child.

**IFD (2025):** max **CHF 25'800** per child.

ICC and IFD deltas differ — model them separately.

---

## Frais médicaux — CODE 710

**ICC:** Deductible only if frais exceed **5% of code 700** (revenu net soumis à l'impôt cantonal — after all professional deductions, not the raw net salary). Only the excess above the threshold is deductible.

**IFD:** Same 5% threshold applied to revenu intermédiaire II (formula: `revenu_intermédiaire_II × 5/95`, capped at declared frais at code 710).

> For a salaried person, code 700 ≈ net salary + investment income − professional deductions. Compute `5% × code_700` before flagging medical costs as a tax saving. With a high income, the threshold is rarely reached.

---

## Dons — CODE 720

Cash or asset gifts (not labour) to Swiss tax-exempt public-interest legal entities, and to the Confederation, cantons, communes and their establishments. Deductible only if total gifts in the year reach at least **CHF 100**.

**ICC (2025):** capped at **20% of code 700** (revenu net après déductions sociales).

**IFD (2025):** capped at **20% of revenu intermédiaire I**.

Not deductible: association membership dues, and gifts to churches/parishes or cultual institutions (those entities are exempt under art. 90 al. 1 let. d/h LI).

---

## Verification checklist

When verifying deductions, cross-check supporting documents **and** apply deduction rules:

1. **Salary certificate** → cross-check fields C/D/E, lines 10.1, 11, 15 against XML
2. **3a attestations** → sum per taxpayer vs declared; check ≤ annual max; flag missing docs
3. **Transport** → look up declared km in forfait table; verify IFD ≤ CHF 3'300
4. **Repas** → confirm ≤ CHF 3'200 (or ≤ CHF 1'600 if cantine)
5. **Autres frais prof.** → verify 3% × salaireNet ∈ [2'000, 4'000]
6. **Assurances** → compute min(net premiums, ICC cap) and min(net premiums, IFD cap); assess impact of any unjustified amounts
7. **Intérêts épargne (code 480)** → ICC deduction = min(savings interest from code 410, cap); verify only savings-type income is included, not dividends
8. **Logement** → compute min(loyer, plafond) − 20% × code_650; flag if zero
9. **Frais médicaux** → compute 5% × code_700; flag if frais < threshold (deduction = 0)
10. **Double activité (235)** → if both spouses have lucrative income, verify ICC CHF 1'700 / IFD 50% of lower income within [8'600, 14'100]
11. **Intérêts passifs (610)** → verify declared interest ≤ gross wealth yield + CHF 50'000; exclude amortisation
12. **Frais de garde (670)** → verify ≤ ICC CHF 15'200 / IFD CHF 25'800 per child < 14; require documented third-party care
13. **Frais de formation (618)** → verify ≤ ICC CHF 12'000 / IFD CHF 13'000 per person; exclude formation initiale and employer-paid costs
14. **Dons (720)** → verify total ≥ CHF 100 and ≤ 20% of code 700; exclude churches and membership dues
15. **Portfolio / titres** → cross-check fiscal value, gross dividends, withholding tax (IES) against broker statement
