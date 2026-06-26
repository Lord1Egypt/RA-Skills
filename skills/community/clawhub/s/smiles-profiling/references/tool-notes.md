# Tool Notes

## SwissTargetPrediction

- URL: https://www.swisstargetprediction.ch/
- Default species: Homo sapiens
- Input: paste SMILES, submit, wait for predictions
- Extract: top targets, probabilities, and any class labels shown

## ADMETlab 3.0

- URL: https://admetlab3.scbdd.com/server/evaluation
- Input: evaluation page with a single SMILES
- Extract: ADMET summary, warning flags, and any endpoint values relevant to the user's question
- If many endpoints are shown, prioritize absorption, distribution, metabolism, excretion, and toxicity

## PubChem

- URL: https://pubchem.ncbi.nlm.nih.gov/
- Input: exact SMILES lookup via PUG REST
- Extract: CID, IUPAC name, synonyms, MW, XLogP, TPSA, HBD/HBA, rotatable bonds
- Prefer this as the identity anchor before interpreting prediction tools

## ChEMBL

- URL: https://www.ebi.ac.uk/chembl/
- Input: similarity search from the user SMILES
- Extract: top analogs, similarity score, max phase, mechanism of action, and target name
- Use 90% similarity first, then 80%, then 70% if needed

## PK-Smart Single SMILES

- URL: https://pk-predictor.serve.scilifelab.se/PKSmart_Single_SMILES
- Input: one SMILES string
- Extract: PK estimates and any confidence/interpretation text shown by the app

## Reporting

- Keep tool outputs separate until the final synthesis step.
- Never mix values across tools if names or units differ.
- If the app only shows charts, capture the numeric labels or legend text if available.
