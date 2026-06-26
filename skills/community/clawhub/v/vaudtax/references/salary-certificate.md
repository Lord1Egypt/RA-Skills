# Salary Certificate (Certificat de salaire / Lohnausweis)

Standardized federal form 11, issued by all employers. Read the extracted PDF natively (agent file reading — no external tools needed).

## Numbered fields

| Line | Label (FR) | Description | VaudTax XML field |
|---|---|---|---|
| 1 | Salaire / Rente | Base salary (excluding lines 2–7) | — (not stored separately) |
| 2.1 | Verpflegung, logement | Benefits in kind: meals/lodging | checkbox `transportGratuit` / `contributionFraisRepas` |
| 2.2 | Part privée voiture | Private use of company car | — |
| 2.3 | Autres prestations | Other benefits in kind | — |
| 3 | Prestations non périodiques | Irregular payments, bonuses | — (not stored separately) |
| 4 | Prestations en capital | Capital payments | — |
| 5 | Droits de participation | Employee stock/options | — |
| 6 | Indemnités administrateur | Board member fees | — |
| 7 | Autres prestations | Other payments | — |
| **8** | **Salaire brut total** | **Sum of lines 1–7** | **— (not stored)** |
| 9 | Cotisations AVS/AI/APG/AC/AINP | Social security deductions | — (not stored) |
| **10.1** | **Cotisations LPP (ordinaires)** | **2nd pillar pension contributions** | **`cotisationOrdinaire`** |
| 10.2 | Cotisations LPP (rachat) | 2nd pillar buy-in contributions | — |
| **11** | **Salaire net** | **Line 8 − lines 9 − 10** | **`salaireNet`** ← key field |
| 12 | Impôt à la source | Withholding tax deducted | — |
| 13.1 | Frais effectifs | Actual expense reimbursements | — |
| 13.2 | Frais forfaitaires | Flat-rate expense reimbursements | — |
| 13.3 | Contributions au perfectionnement | Training contributions | checkbox `contributionPerfectionnement` |
| 14 | Autres prestations accessoires | Other accessory benefits | — |
| **15** | **Remarques** | **Free text: PC famille, special notes** | **`autreCotiContractuelle`** |

## Letter fields

| Letter | Meaning | VaudTax field |
|---|---|---|
| **C** | **NAVS13 + date of birth** | `navs13` + `dateNaissance` in `taxpayerPersonalData1` |
| **D** | **Tax year** | `fiscalPeriod` |
| **E** | **Employment period (from – to)** | `dateDebut` / `dateFin` in `activiteSalarieeRevenus` |
| F | Transport gratuit domicile–travail | `transportGratuit` (true/false) |
| G | Repas à la cantine / chèques-repas | `contributionFraisRepas` (true/false) |

## What VaudTax stores

Only a subset is retained in the XML: employer name (`employeur`), line 10.1 (`cotisationOrdinaire`), line 11 (`salaireNet`), line 13.3 (`contributionPerfectionnement`), line 15 (`autreCotiContractuelle`), checkboxes F and G. Lines 1, 3, 8, and 9 are not stored.

## Cross-checking against the declaration

1. Extract the PDF with `parse_vaudtax.py --extract`; read it natively
2. Extract: field C (NAVS13 + birthdate), D (year), E (from/to), employer, lines 10.1, 11, 13.3, 15
3. Compare against XML — mismatches to flag:
   - line 11 ≠ `salaireNet` (beyond ±1 CHF rounding)
   - line 10.1 ≠ `cotisationOrdinaire`
   - field C NAVS13 ≠ `navs13`, birthdate ≠ `dateNaissance`
   - field D ≠ `fiscalPeriod`, field E ≠ `dateDebut`/`dateFin`

**Joint filers:** match employer name from PDF against `activiteSalarieeRevenus` entries (`isContribuable1: true/false`) to assign CTB1 vs CTB2.
