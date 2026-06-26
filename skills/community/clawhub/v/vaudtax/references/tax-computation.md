# Tax Computation Guide — Canton Vaud

How to estimate ICC (Impôt Cantonal et Communal) and IFD (Impôt Fédéral Direct) from a VaudTax declaration.
Source: [Instructions générales 21001](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf) (2025 edition, pp. 59–68). Barème tables and coefficients are indexed annually.

> **Quick sanity check / authoritative result:** use `calculate_taxes.py` (see [Official calculator script](#official-calculator-script))

## Contents

- [Prerequisites](#prerequisites)
- [Step 1 — Revenu imposable ICC (code 800)](#step-1--revenu-imposable-icc-code-800)
- [Step 2 — Revenu imposable IFD](#step-2--revenu-imposable-ifd)
- [Step 3 — ICC sur le revenu](#step-3--icc-sur-le-revenu)
- [Step 4 — ICC sur la fortune](#step-4--icc-sur-la-fortune)
- [Step 5 — IFD](#step-5--ifd)
- [Step 6 — Summary table](#step-6--summary-table)
- [Key differences ICC vs IFD](#key-differences-icc-vs-ifd)
- [Official sources and barème files](#official-sources-and-barème-files)

---

## Prerequisites

You need:

1. The **revenu imposable ICC** (code 800) — computed by VaudTax from the declared deductions. If not available, estimate from the deductions chain (see Step 1).
2. The **fortune imposable** (code 800 fortune) — total declared assets minus debts, as computed by VaudTax.
3. The **communal coefficient** for the taxpayer's commune — see [Official sources](#official-sources-and-barème-files).
4. The **situation familiale** (célibataire vs marié/partenariat) and number of **parts** (code 810) if applicable.

---

## Step 1 — Revenu imposable ICC (code 800)

Code 800 = all income minus all deductions, in this order:

```
+ Code 100  Salaire net (activité principale)
+ Code 105  Salaire net (activité accessoire)
+ Code 110  Allocations non versées par l'employeur
+ Code 195  Autres revenus
+ Code 410  Revenus de titres (dividendes, intérêts)
+ Code 500  Immeubles privés (valeur locative nette)
...
− Code 140  Frais de transport (forfait table by km)
− Code 150  Repas hors domicile (max CHF 3'200/year)
− Code 160  Autres frais professionnels (3% of salaire net, min 2'000, max 4'000)
− Code 300  Primes assurances (capped by situation familiale)
− Code 310  Pilier 3a (max CHF 7'258 if LPP-insured, 2025)
− Code 480  Intérêts capitaux d'épargne (max CHF 1'600 single, CHF 3'300 married; savings interest only, NOT dividends)
− Code 490  Frais administration titres
− Code 610  Intérêts de dettes
− Code 618  Frais de formation
− Code 660  Déduction logement (ICC only; formula: see DEDUCTIONS.md)
− Code 710  Frais médicaux (if > 5% of code 700)
− Code 720  Dons (max 20% of revenu intermédiaire I)
= Code 700  Revenu net soumis à l'impôt cantonal
− Déductions sociales (ICC)
= Code 800  Revenu imposable ICC
```

**ICC déductions sociales (2025):**

- Célibataire/veuf/séparé/divorcé: CHF 0
- Marié/partenariat enregistré: CHF 0 (ICC has no standard social deduction for couple)
- Per child with part 0.5 (code 810): various (handled via quotient familial)

In practice for a salaried single person: **code 800 ≈ code 700** (no social deductions apply).

---

## Step 2 — Revenu imposable IFD

IFD uses different deduction caps (see [Key differences](#key-differences-icc-vs-ifd)) and its own social deductions:

```
[Same income lines as ICC]
− Code 140  Transport: capped at CHF 3'300 (not distance table)
− Code 300/340/480  Assurances + intérêts épargne (combined IFD cap)
− Code 310  Pilier 3a (same limits as ICC)
[No code 660 logement deduction]
= Revenu intermédiaire I
− Code 720  Dons (max 20% of revenu intermédiaire I)
= Revenu intermédiaire II
+ Franchise frais médicaux (revenu_interm_II × 5/95, capped at code 710)
− Déductions sociales IFD
= Revenu imposable IFD
```

**IFD déductions sociales (2025):**

- Célibataire: CHF 0
- Marié/partenariat: CHF 2'800
- Per child (mineur, apprentissage, études): CHF 6'800
- Per personne nécessiteuse: CHF 6'800

---

## Step 3 — ICC sur le revenu

### Barème ICC revenu (art. 47, al. 1, LI) — 2025 key brackets

Full table: [barème_revenu_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_revenu_2025.pdf)

| Revenu imposable (CHF) | Impôt de base (CHF) | Par CHF 100 en plus |
|---|---|---|
| 100 | 1.00 | 1.00 |
| 1'600 | 16.00 | 2.00 |
| 3'400 | 52.00 | 3.00 |
| 5'100 | 103.00 | 4.00 |
| 8'300 | 231.00 | 5.00 |
| 11'900 | 411.00 | 6.00 |
| 15'100 | 603.00 | 7.00 |
| 23'600 | 1'198.00 | 8.00 |
| 40'500 | 2'550.00 | 9.00 |
| 57'200 | 4'053.00 | 10.00 |
| 74'300 | 5'763.00 | 11.00 |
| 91'100 | 7'611.00 | 12.00 |
| 108'000 | 9'639.00 | 12.50 |
| 134'900 | 13'001.50 | 13.00 |
| 161'900 | 16'511.50 | 13.50 |
| 192'300 | 20'615.50 | 14.00 |
| 222'800 | 24'885.50 | 14.50 |
| 255'800 | 29'670.50 | 15.00 |
| 291'400 | 35'010.50 | 15.50 |

### Formula — single person (parts = 1)

```
impôt_de_base     = look up code_800 in barème above
impôt_réduit      = impôt_de_base × (1 − 0.04)        # réduction 4%
impôt_cantonal    = impôt_réduit × coeff_cantonal / 100   # e.g. 155%
impôt_communal    = impôt_de_base × coeff_communal / 100  # commune-specific
ICC_revenu        = impôt_cantonal + impôt_communal
```

### Formula — married / quotient familial

```
revenu_déterminant (code 820) = code_800 / parts
impôt_de_base_taux            = look up revenu_déterminant in barème
taux                          = impôt_de_base_taux / revenu_déterminant × 100  # in %
impôt_de_base                 = code_800 × taux / 100
# then apply réduction, cantonal, communal as above
```

### Example (from instructions p. 61)

Célibataire, code 800 = CHF 20'700:

```
Impôt de base pour CHF 15'100  = 603.00
CHF 5'600 supplémentaires      = 56 × 7.00 = 392.00
Impôt de base (100%)           = 995.00
Réduction 4%: 995 × 4/100     = −39.80  → 955.20
Impôt cantonal 155%: 955.20 × 155/100  = 1'480.55
Impôt communal (ex. 78.5%): 995 × 78.5/100 = 781.10
Total ICC revenu               = 2'261.65
```

---

## Step 4 — ICC sur la fortune

### Fortune franchise (minimum threshold)

Fortune nette below CHF 60'000 (single/divorced/separated) or CHF 120'000 (married/registered partnership) is **not taxed at all**. Above those thresholds, the **full amount** is used in the barème (no deduction of the threshold). Fractions below CHF 1'000 are dropped before the barème lookup.

### Barème ICC fortune (art. 59, al. 1, LI) — 2025 key brackets

Full table: [barème_fortune_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_fortune_2025.pdf)

| Fortune imposable (CHF) | Impôt de base (CHF) | Par CHF 1'000 en plus |
|---|---|---|
| 60'000 | 32.65 | 0.97 |
| 95'000 | 66.60 | 1.69 |
| 120'000 | 108.85 | 1.69 |
| 177'000 | 205.20 | 2.42 |
| 355'000 | 635.95 | 3.15 |
| 710'000 | 1'754.20 | 3.39 |

### Formula

> **Important:** the 4% reduction does NOT apply to fortune tax. Both cantonal and communal fortune taxes are computed directly from `impôt_de_base_fortune`.

```
impôt_de_base_fortune  = look up fortune_imposable in barème above
impôt_cantonal_fortune = impôt_de_base_fortune × coeff_cantonal / 100
impôt_communal_fortune = impôt_de_base_fortune × coeff_communal / 100
ICC_fortune            = impôt_cantonal_fortune + impôt_communal_fortune
```

> No IFD on fortune.

---

## Step 5 — IFD

### Barème IFD — single person (Alleinstehende) — 2025 key brackets

Full table: [Bareme_IFD_58c-2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/Bareme_IFD_58c-2025.pdf)

| Revenu imposable (CHF) | IFD annuel (CHF) | Par CHF 100 en plus |
|---|---|---|
| 18'500 | 25.41 | — |
| 26'000 | 83.16 | 0.77 |
| 33'200 | 138.60 | 0.88 |
| 50'000 | 400.80 | 2.64 |
| 58'100 | 614.97 | — |
| 82'100 | 1'506.60 | — |
| 95'000 | 2'358.00 | 6.60 |
| 108'600 | 3'255.60 | — |
| 130'500 | 5'178.40 | 8.80 |
| 185'000 | 10'933.60 | — |
| 755'000 | 86'550.40 | — |
| 895'900+ | flat 11.5% | — |

For married / family: separate table in the same PDF (Verheiratete und Einelternfamilien).

### Formula

```
IFD = look up revenu_imposable_IFD in barème (single or married table)
```

No cantonal or communal multiplier. No réduction. No fortune tax.

Notes:

- Fractions < CHF 100 are abandoned
- Annual tax rounded to nearest CHF 5
- Married couples benefit from a dedicated (lower-rate) table

---

## Step 6 — Summary table

| Component | Formula | ICC | IFD |
|---|---|---|---|
| Revenu imposable | from declaration (code 800) | ICC deductions | IFD deductions |
| Tax on income | barème lookup | ✅ | ✅ |
| Réduction | 4% of impôt de base | ✅ cantonal **income** only (not fortune) | ✗ |
| Cantonal multiplier | × coeff_cantonal% | ✅ (155% in 2025) | ✗ |
| Communal multiplier | × coeff_communal% | ✅ | ✗ |
| Fortune tax | barème lookup | ✅ | ✗ |
| **Total** | | **ICC_revenu + ICC_fortune** | **IFD direct** |

---

## Key differences ICC vs IFD

| Deduction | ICC | IFD |
|---|---|---|
| Transport CODE 140 | forfait table by km (max CHF 4'080) | capped CHF 3'300 |
| Assurances CODE 300 | célibataire: CHF 5'000; marié: CHF 9'900 | célibataire: CHF 1'800; marié: CHF 3'700 |
| Logement CODE 660 | ✅ formula: min(loyer, plafond) − 20%×code650 | ✗ does not exist |
| Fortune tax | ✅ | ✗ |
| Réduction impôt de base | 4% (cantonal part only) | ✗ |
| Déductions sociales | none for célibataire without children | CHF 2'800 for married; CHF 6'800/child |

---

## Official sources and barème files

| Resource | URL | Notes |
|---|---|---|
| Instructions générales 2025 | [21001_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/21001_2025.pdf) | pp. 59–68 for computation; URL is year-specific |
| ICC barème revenu 2025 | [barème_revenu_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_revenu_2025.pdf) | Full table at CHF 100 intervals |
| ICC barème fortune 2025 | [barème_fortune_2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/barème_fortune_2025.pdf) | Full table at CHF 1'000 intervals |
| IFD barème 2025 (form 58c) | [Bareme_IFD_58c-2025.pdf](https://www.vd.ch/fileadmin/user_upload/organisation/dfin/aci/fichiers_pdf/Bareme_IFD_58c-2025.pdf) | Single + married tables |
| Communal coefficients | [Arrêtés d'imposition](https://www.vd.ch/etat-droit-finances/communes/finances-communales/arretes-dimposition-et-tableaux-des-impots-communaux) | Download current year XLS for all communes |

---

## Estimating code 800 from a declaration

`scripts/compute_code800.py` reads a `.vaudtax` file (via `parse_vaudtax.summarize()`) and applies the official deduction rules to produce the taxable income figures needed by `calculate_taxes.py`.

```bash
cd "${CLAUDE_SKILL_DIR}/scripts"

python compute_code800.py /path/to/file.vaudtax
```

Output includes a full deduction breakdown and a ready-to-paste `calculate_taxes.py` command line.

```bash
python compute_code800.py /path/to/file.vaudtax --json   # machine-readable
```

**As a module:**

```python
from parse_vaudtax import open_vaudtax, summarize
from compute_code800 import compute

root, _ = open_vaudtax("file.vaudtax")
result = compute(summarize(root))
print(result["revenu_icc"], result["revenu_ifd"], result["fortune_icc"])
```

> These are **estimates** derived from the declared values. The official figures are computed by the VaudTax software and may differ slightly (rounding, edge cases). Use `calculate_taxes.py` with the official figures when available.

---

## Official calculator script

`scripts/calculate_taxes.py` queries the vd.ch server directly via HTTP POST

```bash
cd "${CLAUDE_SKILL_DIR}/scripts"

python calculate_taxes.py \
  --periode 2025 \
  --commune "Yverdon-les-Bains" \
  --etat-civil single \
  --revenu-icc 99212 \
  --fortune-icc 337081 \
  --revenu-ifd 102946

# JSON output for programmatic use
python calculate_taxes.py ... --json
```

**Key parameters:**

- `--periode` — fiscal year (2016-2026)
- `--commune` — Vaud commune name, accent-tolerant (e.g. `"Yverdon-les-Bains"`)
- `--etat-civil` — `single` | `married` | `parent`
- `--revenu-icc`, `--fortune-icc`, `--revenu-ifd` — taxable amounts (code 800, after all deductions)
- `--enfants`, `--enfants-demi`, `--enfants-menage` — child counts (default 0)
- `--no-icc` / `--no-ifd` — skip one of the two simulations

**As a module:**

```python
from calculate_taxes import calculate_taxes
result = calculate_taxes(periode=2025, commune="Yverdon-les-Bains",
                         revenu_icc=99212, fortune_icc=337081, revenu_ifd=102946)
print(result["total_icc_ifd"])  # "23'450.65"
```

Key result dict fields: `total_icc_ifd`, `total_icc`, `total_ifd`, `revenu_cf_cant`, `revenu_cf_comm`, `fortune_cf_cant`, `fortune_cf_comm`, `revenu_impot_base`, `fortune_impot_base`, `revenu_coef_cant`, `revenu_coef_comm`.

---

## Taux marginal d'imposition

The marginal tax rate answers: *"for each additional CHF 100 of income, how much extra tax is owed?"*

**Method:** finite difference — two calls to the official calculator (base, then base + CHF 1000), comparing the resulting taxes:

```
taux_marginal = (tax(revenu + 1000) − tax(revenu)) / 1000
```

This correctly handles the quotient familial (married couples, children) and all coefficient interactions without any manual barème lookup.

### CLI

```bash
python calculate_taxes.py \
  --periode 2025 \
  --commune "Yverdon-les-Bains" \
  --etat-civil single \
  --revenu-icc 99212 \
  --fortune-icc 337081 \
  --revenu-ifd 102946 \
  --marginal-rate
```

Output:
```
====================================================
  Taux marginal d'imposition
====================================================
  ICC (cantonal + communal)       32.50 %
  IFD (fédéral direct)             8.80 %
  ──────────────────────────────────────
  TOTAL                           41.30 %

  (méthode: Δtax / Δrevenu, Δ = CHF 100)
====================================================
```

Add `--json` for machine-readable output.

### As a module

```python
from calculate_taxes import calculate_marginal_rate

mr = calculate_marginal_rate(
    periode=2025, commune="Yverdon-les-Bains",
    etat_civil="single",
    revenu_icc=99212, fortune_icc=337081, revenu_ifd=102946,
)
print(mr["marginal_total"])   # e.g. 41.3
print(mr["marginal_icc"])     # ICC component
print(mr["marginal_ifd"])     # IFD component
```

> **Note:** fortune (wealth) is not included in the marginal rate — wealth tax is flat once above the threshold, so only income matters for the marginal rate computation.
