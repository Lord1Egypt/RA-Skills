---
name: smiles-profiling
description: Comprehensive SMILES profiling through SwissTargetPrediction, PubChem, ADMETlab 3.0, ChEMBL, and PK-Smart. Use when given a single SMILES to extract predicted targets, exact identity and physicochemical baselines, known analogs and mechanisms, ADMET properties, and pharmacokinetic estimates; handles salts/counterions and degrades gracefully when any source is unavailable.
---

# SMILES Profiling

Turn one SMILES into a compact pharmacology profile.

## Tool stack

| Tool | Use |
|------|-----|
| SwissTargetPrediction | Predicted protein targets with probabilities |
| PubChem | Exact CID, synonyms, MW, XLogP, TPSA, HBD/HBA, rotatable bonds |
| ADMETlab 3.0 | ADMET flags, drug-likeness, toxicity sections |
| ChEMBL | Similarity hits, max phase, known mechanisms, target names |
| PK-Smart | Human and animal PK estimates (VDss, CL, t½, fu, MRT) |

## Workflow

1. Use the user-provided SMILES as-is unless it clearly needs cleanup.
2. Normalize only obvious salts/counterions.
3. Run SwissTargetPrediction for target hypotheses.
4. Run PubChem for identity and physicochemical baseline.
5. Run ADMETlab 3.0 for ADMET flags and drug-likeness.
6. Run ChEMBL for similarity hits and mechanism context.
7. Run PK-Smart last for PK estimates.
8. Merge the outputs into one short report, preferring direct database evidence over predictions.

## Preferred scripts

- `scripts/run_smiles_profile.py <SMILES>` for the full report.
- `scripts/run_smiles_smoke.py --cases <tsv>` for regression/benchmark runs.

## Extraction notes

- **SwissTargetPrediction**: capture the top 5 targets, probabilities, and species.
- **PubChem**: capture CID, IUPAC name, synonyms, MW, XLogP, TPSA, HBD/HBA, and rotatable bonds.
- **ADMETlab 3.0**: capture the section list and any obvious toxicity/drug-likeness flags.
- **ChEMBL**: capture the similarity threshold, top hits, max phase, mechanism_of_action, and target name.
- **PK-Smart**: capture VDss, CL, t½, fu, MRT, and animal PK when available.

## Handling edge cases

- **Salts/mixtures**: strip common counterions first.
- **Invalid SMILES**: fail cleanly, do not crash.
- **Missing tools**: continue with the remaining sources.
- **PubChem miss**: report the miss and continue.
- **ChEMBL miss**: automatically fall back from 90 → 80 → 70 similarity.

## Output shape

```
SMILES: CC(=O)OC1=CC=CC=C1C(=O)O

## SwissTargetPrediction
- Top target: PTGS1 (prob: 0.76)

## PubChem
- CID: 2244 | Name: 2-acetyloxybenzoic acid
- MW: 180.16 Da | XLogP: 1.2 | TPSA: 63.6 Å²

## ADMETlab 3.0
- MW: 180.04 Da | QED: N/A

## ChEMBL
- Top hit: CHEMBL25 ASPIRIN | sim 100 | phase 4
- Mechanism: Cyclooxygenase inhibitor -> Cyclooxygenase

## PK-Smart
- VDss: 0.23 L/kg | CL: 10.41 mL/min/kg
- t½: 0.34 hr | fu: 0.67
```
