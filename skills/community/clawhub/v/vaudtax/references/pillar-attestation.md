# Pillar Attestation (Form 21 EDP / Attestation cotisations de prévoyance)

Official federal form 21 EDP (trilingual DE/FR/IT), issued by bank foundations and insurance companies for 2nd pillar and 3a accounts. Read the extracted PDF natively (agent file reading — no external tools needed).

## Extraction

Locate totals by their labels, not by field letter (letters vary between editions):

- **3a contributions:** the line `Total des cotisations au pilier 3a` (DE: `Total Beiträge an die Säule 3a`)
- **3a buy-ins (rachats):** the line `Total des rachats au pilier 3a`

Some institutions (e.g. PostFinance) issue an "Attestation fiscale" instead of Form 21 EDP — take the annual 3a contribution total from it the same way.

## Form editions

| Edition | Total 3a contributions | Total 3a rachats | Birthdate field |
|---|---|---|---|
| 2025 (current) | field **q** | field **x** | field **c** |
| 2011 | field **r** | field **s** | field **d** |

Do not rely on field letters for extraction — locate the totals by their labels (see Extraction above).

## Structure

**Section 1 — 2nd pillar** (`Cotisations à des institutions de prévoyance professionnelle, 2e pilier`): voluntary LPP buy-ins, ordinary contributions, dates.

**Section 2 — Pillar 3a** (`Cotisations pour des formes reconnues de prévoyance individuelle liée`):

| Field (2025) | Label | VaudTax XML field |
|---|---|---|
| **a** | Nom et siège de l'institution | — |
| **b/c** | Numéro d'assuré AVS | should match `navs13` in `taxpayerPersonalData1` |
| **c/d** | Date de naissance | should match `birthdate` in `taxpayerPersonalData1` |
| **l/m** | No de police / No de contrat | — |
| **n** | Conclusion | contract opening year |
| **p/q** | Année | should match `fiscalPeriod` |
| **q/r** | **Total cotisations au pilier 3a** | summed → `formesReconnuesPrevoyanceIndividuelleContribuable1` |

**Section 3 — Rachats** (`Rachats pour des formes reconnues de prévoyance individuelle liée`): contract number, fiscal period, prior contributions, buy-in date, amount, total (field **x** in 2025, **s** in 2011).

## Taxpayer attribution (joint filers)

Match the document to a taxpayer by comparing the AVS number (field b), birthdate (field c), and name block against `taxpayerPersonalData1` / `taxpayerPersonalData2`. If none match, say so rather than guessing.

## Cross-checking against the declaration

1. Extract all attestation PDFs (label contains "cotisations", "21 EDP", or "pilier 3a")
2. Read each natively, detect format, extract totals
3. For joint filers, attribute each document to a taxpayer (see above)
4. Sum per taxpayer and compare:
   - CTB1 sum → `formesReconnuesPrevoyanceIndividuelleContribuable1`
   - CTB2 sum → `formesReconnuesPrevoyanceIndividuelleContribuable2`
5. Discrepancy → likely a missing attestation or data-entry error

A taxpayer may hold several 3a accounts — each produces a separate attestation. Multiple accounts at the same institution usually carry sequential contract numbers (e.g. `….01`, `….02`, `….04`); a gap in the sequence points to the likely missing attestation — name it when flagging a discrepancy.
